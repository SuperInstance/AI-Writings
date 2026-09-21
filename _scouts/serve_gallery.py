#!/usr/bin/env python3
"""Tiny static-file server for the polyformalism gallery.

Usage:
    python3 serve_gallery.py            # serves on :8000
    python3 serve_gallery.py 8080       # serves on :8080
"""
from __future__ import annotations

import http.server
import os
import socketserver
import sys
from pathlib import Path

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
HERE = Path(__file__).resolve().parent
INDEX = HERE / "polyformalism_gallery.html"

if not INDEX.exists():
    sys.exit(f"error: {INDEX} not found — run build_gallery.py first")


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, directory=str(HERE), **kwargs)

    def end_headers(self) -> None:
        # Disable caching while developing locally.
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, fmt: str, *args) -> None:  # noqa: A003
        sys.stdout.write(f"[serve] {self.address_string()} {fmt % args}\n")
        sys.stdout.flush()


def main() -> None:
    handler = Handler
    with socketserver.ThreadingTCPServer(("0.0.0.0", PORT), handler) as httpd:
        sa = httpd.socket.getsockname()
        url = f"http://localhost:{sa[1]}/polyformalism_gallery.html"
        print(f"[serve] directory: {HERE}")
        print(f"[serve] serving:   {url}")
        print(f"[serve] ctrl-c to stop")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[serve] bye")


if __name__ == "__main__":
    main()
