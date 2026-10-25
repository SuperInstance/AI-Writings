"""hermes_worker.py - Real Hermes worker that processes inbox missions.

Replaces the stub `watchdog.py` logic. This worker:

  1. Polls C:\\Users\\casey\\hermes-nerve-center\\inbox\\ for *.json missions
  2. Reads the moment file referenced in the packet
  3. Calls hermes_ensemble.run_ensemble() with the image bytes + prompt
  4. Writes the multi-model analysis to completed/<task_id>.json
  5. Updates registry.json with status + progress

Run modes:
  python hermes_worker.py --once         # process all queued then exit
  python hermes_worker.py --loop         # continuous poll, default
  python hermes_worker.py --dry-run      # build packets, print, don't POST

Vision-only missions:
  Tier 3 (echogram read) requires a vision-capable model. DeepInfra's
  Gemini 2.0 Flash is the default. If no vision model is configured
  AND no API key, --dry-run lets us test the wiring without hitting
  the API.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import shutil
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# Make hermes_ensemble importable when worker is run from anywhere
WORKER_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(WORKER_DIR))

NERVE_CENTER = Path(os.environ.get(
    "HERMES_NERVE_CENTER",
    r"C:\Users\casey\hermes-nerve-center"
))
INBOX = NERVE_CENTER / "inbox"
PROCESSING = NERVE_CENTER / "processing"
COMPLETED = NERVE_CENTER / "completed"
FAILED = NERVE_CENTER / "failed"
REGISTRY = NERVE_CENTER / "registry.json"
PERSONA = NERVE_CENTER / "hermes-persona.md"


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _read_registry() -> dict:
    if not REGISTRY.exists():
        return {"active_tasks": [], "last_error": None, "history": []}
    try:
        with REGISTRY.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"active_tasks": [], "last_error": None, "history": []}


def _write_registry(reg: dict) -> None:
    with REGISTRY.open("w", encoding="utf-8") as f:
        json.dump(reg, f, indent=2)


def _update_registry(task_id: str, status: str, **kwargs) -> None:
    """Update the active_tasks list and append to history on terminal states."""
    reg = _read_registry()
    found = False
    for t in reg["active_tasks"]:
        if t["task_id"] == task_id:
            t.update({
                "status": status,
                "last_update": _utcnow(),
                **{k: v for k, v in kwargs.items() if k != "status"},
            })
            found = True
            break
    if not found and status not in ("COMPLETED", "FAILED"):
        reg["active_tasks"].append({
            "task_id": task_id,
            "status": status,
            "last_update": _utcnow(),
            **kwargs,
        })
    if status in ("COMPLETED", "FAILED"):
        # Move out of active, append to history
        reg["active_tasks"] = [
            t for t in reg["active_tasks"] if t["task_id"] != task_id
        ]
        reg["history"].append({
            "task_id": task_id,
            "status": status,
            "finished_at": _utcnow(),
            **kwargs,
        })
        # Keep history to last 100
        reg["history"] = reg["history"][-100:]
    _write_registry(reg)


def _load_persona() -> str:
    """Read the Socratic teaching prefix that Casey has built up."""
    if not PERSONA.exists():
        return ""
    try:
        return PERSONA.read_text(encoding="utf-8")
    except Exception:
        return ""


def _build_echogram_prompt(moment: dict, persona_prefix: str) -> str:
    """Construct the vision prompt for an echogram mission.

    The persona_prefix accumulates as Casey reviews analyses and writes
    feedback. It's a Socratic teaching tool: 'focus on X', 'ignore Y',
    'when you see Z, that's important'.
    """
    parts = []
    if persona_prefix.strip():
        parts.append(persona_prefix.strip())
        parts.append("")

    parts.append("You are analyzing an echogram (sonar) capture from a "
                 "commercial fishing vessel (F/V Eileen).")
    parts.append("")
    parts.append("CONTEXT:")
    parts.append(f"  - Timestamp: {moment.get('ts_utc', 'unknown')}")
    pos = moment.get("position", {})
    parts.append(f"  - Position: {pos.get('lat_ddmm', 'unknown')} "
                 f"{pos.get('lon_ddmm', 'unknown')}")
    parts.append(f"  - SOG: {pos.get('sog_kts', '?')} kn, "
                 f"COG: {pos.get('cog_deg', '?')} deg")
    disp = moment.get("display", {})
    parts.append(f"  - Display: {disp.get('width', '?')}x{disp.get('height', '?')}, "
                 f"depth_max {disp.get('depth_max_fm', '?')} fm, "
                 f"{disp.get('px_per_fm', '?')} px/fm")
    parts.append("")
    parts.append("WHAT TO LOOK FOR AND REPORT (structured JSON please):")
    parts.append('  {')
    parts.append('    "bottom_visible": true/false,')
    parts.append('    "bottom_depth_fm_estimate": <number or null>,')
    parts.append('    "mark_density": "none|sparse|moderate|dense",')
    parts.append('    "mark_depth_range_fm": [<low>, <high>] or null,')
    parts.append('    "features": ["<list: bait_ball|thermocline|scatter|school|individual_marks|..."],')
    parts.append('    "species_likelihood": {"pollock": 0.0-1.0, "cod": 0.0-1.0, ...},')
    parts.append('    "operational_notes": "<1-2 sentences, what a captain would want to know>",')
    parts.append('    "confidence": 0.0-1.0,')
    parts.append('    "uncertainty": "<what you are unsure about>"')
    parts.append('  }')
    parts.append("")
    parts.append("Be specific. If you cannot see something, say so. "
                 "Do not invent features. Use the structured JSON shape above.")
    return "\n".join(parts)


def _encode_image(path: Path) -> tuple[str, str]:
    """Read an image file, return (base64_data, mime_type)."""
    suffix = path.suffix.lower()
    mime = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }.get(suffix, "image/png")
    data = path.read_bytes()
    return base64.b64encode(data).decode("ascii"), mime


def _resolve_moment_image(packet: dict) -> Optional[Path]:
    """Find the image path for a packet. Supports two shapes:
    - context.image_path (Tier 3 vision)
    - context.moment_path (a JSON whose .frame_file is the image)
    """
    ctx = packet.get("context", {})
    # Direct image path
    img = ctx.get("image_path")
    if img and Path(img).exists():
        return Path(img)
    # Moment JSON path: read .frame_file relative to the JSON's dir
    mp = ctx.get("moment_path")
    if mp and Path(mp).exists():
        with Path(mp).open("r", encoding="utf-8") as f:
            moment = json.load(f)
        frame = moment.get("frame_file")
        if frame:
            candidate = Path(mp).parent / frame
            if candidate.exists():
                return candidate
            # try absolute
            if Path(frame).exists():
                return Path(frame)
    return None


def _process_one(packet_path: Path, dry_run: bool = False) -> None:
    """Process a single mission packet. Move from inbox -> processing ->
    completed/failed. Writes the multi-model analysis to the same task id."""
    task_id = packet_path.stem
    target_processing = PROCESSING / packet_path.name
    try:
        shutil.move(str(packet_path), str(target_processing))
    except Exception as e:
        print(f"[!] failed to move {packet_path} to processing: {e}")
        return

    try:
        with target_processing.open("r", encoding="utf-8") as f:
            packet = json.load(f)
    except Exception as e:
        _fail(target_processing, task_id, f"could not parse packet JSON: {e}")
        return

    print(f"[*] {task_id}: tier={packet.get('context',{}).get('tier','?')} "
          f"category={packet.get('category','?')}")
    _update_registry(task_id, "IN_PROGRESS", progress="5%",
                     tier=packet.get("context", {}).get("tier"))

    # Resolve the moment/image
    img_path = _resolve_moment_image(packet)
    if not img_path:
        _fail(target_processing, task_id,
              "could not resolve image path from packet context")
        return

    # Read the moment JSON if we have it, for context
    moment = {}
    mp = packet.get("context", {}).get("moment_path")
    if mp and Path(mp).exists():
        try:
            with Path(mp).open("r", encoding="utf-8") as f:
                moment = json.load(f)
        except Exception:
            pass

    persona = _load_persona()
    prompt = _build_echogram_prompt(moment, persona)
    img_b64, mime = _encode_image(img_path)

    # Lazy import so --help doesn't need providers
    from hermes_ensemble import run_ensemble

    if dry_run:
        print(f"[dry-run] would POST image={img_path} ({len(img_b64)//1024}KB b64)")
        print(f"[dry-run] prompt length: {len(prompt)} chars")
        print(f"[dry-run] models: would call run_ensemble()")
        result = {
            "task_id": task_id,
            "mode": "dry-run",
            "image_path": str(img_path),
            "image_bytes": len(img_b64) * 3 // 4,
            "prompt_chars": len(prompt),
            "models_requested": [
                "deepseek-ai/DeepSeek-V3-Flash",
                "Qwen/Qwen3-Next-80B-A3B-Instruct",
                "meta-llama/Llama-3.3-70B-Instruct",
                "google/gemini-2.0-flash-001",
            ],
            "persona_chars": len(persona),
        }
    else:
        _update_registry(task_id, "IN_PROGRESS", progress="30%")
        try:
            result = run_ensemble(
                image_b64=img_b64,
                image_mime=mime,
                prompt=prompt,
                task_id=task_id,
            )
        except Exception as e:
            _fail(target_processing, task_id,
                  f"ensemble error: {e}\n{traceback.format_exc()}")
            return

    # Write the completed analysis
    out = {
        "task_id": task_id,
        "finished_at": _utcnow(),
        "image_path": str(img_path),
        "moment": moment,
        "instruction": packet.get("instruction", ""),
        "tier": packet.get("context", {}).get("tier"),
        "models_requested": result.get("models_requested", []),
        "analyses": result.get("analyses", {}),
        "errors": result.get("errors", {}),
        "persona_chars_used": len(persona),
    }
    completed_path = COMPLETED / f"{task_id}.json"
    with completed_path.open("w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)

    # Also move the original packet to completed for the audit trail
    shutil.move(str(target_processing), str(COMPLETED / packet_path.name))
    n_ok = sum(1 for a in result.get("analyses", {}).values() if a.get("ok"))
    _update_registry(task_id, "COMPLETED", progress="100%",
                     models_ok=n_ok, completed_path=str(completed_path))
    print(f"[+] {task_id}: {n_ok}/{len(result.get('analyses',{}))} models OK "
          f"-> {completed_path}")


def _fail(processing_path: Path, task_id: str, error: str) -> None:
    FAILED.mkdir(parents=True, exist_ok=True)
    shutil.move(str(processing_path), str(FAILED / processing_path.name))
    (FAILED / f"{task_id}_error.log").write_text(error, encoding="utf-8")
    _update_registry(task_id, "FAILED", error=error)
    print(f"[!] {task_id} FAILED: {error[:200]}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Hermes echogram analysis worker")
    ap.add_argument("--loop", action="store_true", default=True,
                    help="poll continuously (default)")
    ap.add_argument("--once", action="store_true",
                    help="process all queued missions then exit")
    ap.add_argument("--dry-run", action="store_true",
                    help="build packets, print, don't POST to models")
    ap.add_argument("--poll-interval", type=float, default=2.0,
                    help="seconds between inbox polls")
    args = ap.parse_args()

    for d in (INBOX, PROCESSING, COMPLETED, FAILED):
        d.mkdir(parents=True, exist_ok=True)

    if not _read_registry().get("active_tasks"):
        _write_registry({"active_tasks": [], "last_error": None, "history": []})

    print(f"[*] Hermes worker active on {INBOX}")
    print(f"[*] mode: {'DRY-RUN' if args.dry_run else 'LIVE'}")
    if args.dry_run:
        print("[*] (no model calls will be made)")
    print(f"[*] persona: {PERSONA} ({'exists' if PERSONA.exists() else 'empty'})")

    try:
        while True:
            packets = sorted(INBOX.glob("*.json"))
            if packets:
                for p in packets:
                    _process_one(p, dry_run=args.dry_run)
            if args.once:
                break
            time.sleep(args.poll_interval)
    except KeyboardInterrupt:
        print("\n[*] Hermes worker stopped (Ctrl+C)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
