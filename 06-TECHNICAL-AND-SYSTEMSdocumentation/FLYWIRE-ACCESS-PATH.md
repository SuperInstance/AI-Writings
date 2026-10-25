# FlyWire Access Path — the real route to the adult fly brain graph

*2026-09-03 · AI-Writings/docs/FLYWIRE-ACCESS-PATH.md · NQ-C lane companion to CONNECTOME-QUILT-RESEARCH.md ("fly as data") and NQ-C2-edges-as-channels.md. Recon executed headless from this laptop, 25-min cap, every claim below curl-verified unless marked otherwise.*

**VERDICT UP FRONT: The scar is real but it guards the wrong door.** The Codex web app does session-gate its TSV download buttons — but the entire public release (snapshot 783, the complete adult Drosophila brain connectome) sits in a **world-readable, anonymously-listable Google Cloud Storage bucket: `gs://flywire-data/codex/data/fafb/783/`**. Full graph = plain `curl`, no auth, no browser, no Casey. Meanwhile the *documented* programmatic routes (CAVEclient / DAF APIs) are **dead as of today** — all three known server hostnames are NXDOMAIN. The scary-looking API is a corpse; the scary-looking web gate is theater over an open bucket. Download size for a working graph: **~55 MB compressed**. Synapse-level everything: **~3.3 GB**. License: **CC BY-NC 4.0** (non-commercial — not plain CC-BY; attribution strings below).

---

## 1. Routes, ranked

| # | Route | Auth | Status (as tested 2026-09-03) | Verdict |
|---|---|---|---|---|
| 1 | **GCS bucket `flywire-data`** — `https://storage.googleapis.com/flywire-data/codex/data/fafb/783/` | **none** | ✅ verified: bucket listing works anonymously, files download, gunzip clean, schemas and row counts checked | **THE route. Use this.** |
| 2 | Schlegel et al. 2024 supplement mirror — [zenodo.10877326](https://doi.org/10.5281/zenodo.10877326) | none | ✅ verified via Zenodo API metadata (all-neuron skeletons in SWC-parquet, NBLAST matrices) | Morphology lane, not the synapse graph. Secondary. |
| 3 | Codex web UI — [codex.flywire.ai](https://codex.flywire.ai) | Codex/browser session (the known scar) | not retried — **redundant**: route 1 serves the same files the UI's download page offers | Skip unless the UI itself is needed |
| 4 | CAVEclient / DAF REST API (`api.flywire-databasenexus.org`, `global.daf-apis.linc-dataservices.org`, `flywire-daf.itanna.io`) | Google OAuth → token in `~/.cloudvolume/secrets/cave-secret.json` | ❌ **all three hostnames NXDOMAIN** (verified via Cloudflare DoH, `Status: 3`; docs still live at [caveconnectome.github.io/CAVEclient](https://caveconnectome.github.io/CAVEclient/)) | Dead or migrated to an unpublished address. Even revived, it needs a browser for the OAuth handshake → Casey. Do not build on it. |
| 5 | fafb.catmaid.org (FAFB CATMAID) | mixed | not fetched this round | Not a mirror: pre-FlyWire manual reconstructions of the same EM volume. Different dataset; don't conflate. |

How route 1 was found (method, so it's reproducible): pulled `codex.flywire.ai`'s HTML, saw static assets on `storage.googleapis.com/flywire-data/codex/...`, tried the GCS JSON listing API on the bucket — it answered. The web app's session gate fronts a public bucket; the gate is UX, not security.

## 2. What's in the bucket (key files, `codex/data/fafb/783/`)

Full directory: **71 files, 8.18 GB**. Per `flywire.ai/guidelines` (fetched): *"FlyWire's latest public release is version 783... In practice, all data available in Codex for snapshot 783 is publicly released."* Snapshot date: October 2023.

| File (gzipped) | Size | What | Verified |
|---|---|---|---|
| `connections.csv.gz` | 50.3 MB | Edge list: `pre_root_id,post_root_id,neuropil,syn_count,nt_type` — **3,869,878 edges** | ✅ downloaded, gunzipped, counted, header read |
| `neurons.csv.gz` | 1.7 MB | Node table: `root_id,group,nt_type,nt_type_score,{da,ser,gaba,glut,ach,oct}_avg` — **139,255 neurons** | ✅ downloaded, counted, header read |
| `connections_princeton_no_threshold.csv.gz` | 275.7 MB | Same schema, no threshold (also `connections_no_threshold.csv.gz` 212 MB; `_5_ol_2` and `_olr_min_2` threshold variants present) | ✅ range-GET + gzip magic + header; not fully downloaded |
| `fafb_v783_princeton_synapse_table.csv.gz` | 2.70 GB | Synapse-level table | ✅ listed only |
| `synapse_coordinates.csv.gz` | 316.8 MB | Synapse coordinates | ✅ listed only |
| `labels.csv.gz` / `names.csv.gz` | 4.8 / 1.2 MB | Community labels (`label,user_id,user_name,user_affiliation,...`), names | ✅ downloaded/headers read |
| `classification*.csv.gz`, `consolidated_cell_types.csv.gz`, `connectivity_tags.csv.gz`, `visual_neuron_types.csv.gz`, `cross_version_consistent_names.csv` | KB–MB | Cell typing / stable-ID mapping | listed |
| `neuron_db_schema_20251213.pickle.gz` (+ ~40 schema-dated variants) | ~76–142 MB each | Codex's internal neuron DB pickle (whole app state) | listed; latest updated 2026-02-24 |

Same bucket also hosts the other connectomes, same door: `codex/data/manc/` (male CNS), `codex/data/maol/`, `codex/data/mcns/`, `codex/data/banc/` (brain+nerve cord). Free lunch for the lane if fly-as-data ever wants siblings.

**Minimal working-graph ingest (recommended):**
```bash
mkdir -p flywire783 && cd flywire783
B=https://storage.googleapis.com/flywire-data/codex/data/fafb/783
curl -sO $B/connections.csv.gz        # 50 MB — 3.87M edges, syn_count weighted
curl -sO $B/neurons.csv.gz            # 1.7 MB — 139k neurons + NT predictions
curl -sO $B/labels.csv.gz             # 4.8 MB — community labels
curl -sO $B/classification.csv.gz     # ~1 MB — cell-type classification
# ~57 MB total. For unthresholded edges instead, use
#   connections_princeton_no_threshold.csv.gz (276 MB)
# For synapse-level work add the 2.7 GB princeton synapse table + 317 MB coordinates.
```

Caveats I measured but did not chase: which named UI threshold `connections.csv.gz` corresponds to (Codex's UI offers explicit threshold variants; the no-threshold files are unambiguous — when in doubt, download `no_threshold` and cut it yourself). `root_id`s are segmentation root IDs at snapshot 783; for stable names across versions there's `cross_version_consistent_names.csv` — untested here.

## 3. Auth requirements, per route

- **GCS route: none.** Anonymous GET/HEAD/listing all verified from this box.
- **Codex UI: browser session** (the scar). Only value beyond the bucket is the interactive viewer/stats.
- **CAVEclient: was token-based** — browser visit to an auth endpoint (Google OAuth), token saved to `~/.cloudvolume/secrets/cave-secret.json`, shareable across machines. Today the endpoints don't resolve, so this is academic until FlyWire republishes an address; if it comes back, a one-time Casey browser session would mint a token the fleet could reuse.

## 4. License + attribution (this is the part people get wrong)

- **License: CC BY-NC 4.0** — [creativecommons.org/licenses/by-nc/4.0](https://creativecommons.org/licenses/by-nc/4.0/), per [flywire.ai/guidelines](https://flywire.ai/guidelines) (fetched). **Non-commercial.** Fine for NQ-C research; anything revenue-adjacent is off-limits without separate permission (contact: flywire@princeton.edu).
- Official citation matrix lives in a Google Sheet (linked from guidelines), fetched as CSV from this laptop. Rule: **co-cite Dorkenwald et al. 2024 + Schlegel et al. 2024**, plus per-column credits:

| Aspect used | Cite |
|---|---|
| The connectome / reconstruction / annotations | **Dorkenwald et al., 2024** — [10.1038/s41586-024-07558-y](https://doi.org/10.1038/s41586-024-07558-y) (*Neuronal wiring diagram of an adult brain*, Nature) |
| Cell typing, hemibrain matching | **Schlegel et al., 2024** — [10.1038/s41586-024-07686-5](https://doi.org/10.1038/s41586-024-07686-5) (Nature) |
| EM imagery | **Zheng et al., 2018** — [10.1016/j.cell.2018.06.019](https://doi.org/10.1016/j.cell.2018.06.019) |
| Synapses & connectivity | **Buhmann et al., 2021** — 10.1038/s41592-021-01183-7 (before Jul 2025) / **Yu et al., 2025** — [biorxiv 2025.07.11.664377](https://www.biorxiv.org/content/10.1101/2025.07.11.664377v1) (from Jul 2025) |
| Neurotransmitter predictions | **Eckstein, Bates et al., 2024** — [10.1016/j.cell.2024.03.016](https://doi.org/10.1016/j.cell.2024.03.016) |

**Suggested attribution string for code/data provenance blocks:**
> FlyWire public release v783 (Oct 2023 snapshot), CC BY-NC 4.0. Data: Dorkenwald et al. 2024 (doi:10.1038/s41586-024-07558-y); Schlegel et al. 2024 (doi:10.1038/s41586-024-07686-5); synapse detection per Buhmann et al. 2021 (doi:10.1038/s41592-021-01183-7); neurotransmitter predictions per Eckstein et al. 2024 (doi:10.1016/j.cell.2024.03.016). Retrieved from gs://flywire-data (codex/data/fafb/783).

## 5. Blocked vs. needs Casey

- **Blocked for a headless agent: essentially nothing that matters.** The graph, node table, labels, types, synapses — all anonymous HTTP GETs.
- **Would need Casey's browser:** (a) Codex *viewer* sessions (redundant for data); (b) any CAVE API token, if that ecosystem ever resolves again; (c) access tiers beyond the public release (e.g. gated BANC access per flywire.ai/banc_access) — note the banc bucket dir looked equally open, but that's outside this task and I didn't verify its completeness.
- **Permanently off-limits:** commercial use under CC BY-NC.

## 6. Honest unverified list

- Academic Torrents: their API returned 403 to curl; no mirror found via Zenodo API beyond the Schlegel supplement. Didn't dig further — route 1 made it moot.
- AWS Open Data Registry: not checked this round.
- No claim about which synapse-count threshold the default `connections.csv.gz` encodes; measured facts only (3.87M rows, schema above).
- Zenodo record 10877326 verified by metadata, file downloads not tested.

*Route 1 verified end-to-end from the fleet: bucket listed, files fetched, gunzip clean, rows counted. The rest is dead, redundant, or someone else's door.*
