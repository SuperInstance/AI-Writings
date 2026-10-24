# nvidia/NVIDIA-Nemotron-3-Super-120B-A12B



**Witness‑Stream Viewer – a minimal Quilt + Makepad ingestion tool**  
*(≈ 820 words, ready to `cargo run`)*  

---

## 1. What we are building

A tiny desktop app that **continuously reads a “witness log”** (a line‑delimited JSON file produced by any instrumentation pipeline) and visualises the incoming values as a scrolling line chart.  
The UI is written entirely with **Makepad** – the immediate‑mode, GPU‑accelerated Rust UI framework – so the rendering lives on the GPU and updates at 60 fps without any extra work.  
Because Makepad apps are ordinary Cargo crates, the whole thing can be built and run with a single `cargo run` command, satisfying the “Quilt + Makepad integration” ask: the app is a Quilt‑compatible plugin (just a normal binary that can be dropped into a Quilt host) and it consumes the witness stream instead of screenshots.

---

## 2. File layout

```
witness-stream/
├─ Cargo.toml
├─ src/
│  ├─ main.rs          # application entry point & UI logic
│  └─ log_reader.rs    # background thread that tails the witness log
└─ sample/
   └─ witness.log      # a tiny demo log (optional)
```

Only two source files are needed; Makepad’s shader DSL lives inside `main.rs`, so no separate GLSL file is required.

---

## 3. Cargo.toml

```toml
[package]
name = "witness-stream"
version = "0.1.0"
edition = "2021"
license = "MIT"
description = "Ingests a witness log and renders a live line chart with Makepad"
repository = "https://github.com/yourorg/witness-stream"

[dependencies]
makepad = { version = "0.12.0", features = ["glow"] }   # GPU backend via glow
crossbeam = "0.8"
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
notify = { version = "5", features = ["fsnotify"] }    # for file watching (optional)
```

*Why these deps?*  
- **makepad** gives us the UI, the Live shader system, and the event loop.  
- **crossbeam** provides a simple bounded channel for passing log lines from the reader thread to the UI thread.  
- **serde**/`serde_json` decode the JSON lines.  
- **notify** (used only in `log_reader.rs`) lets us tail the file efficiently on all platforms.

---

## 4. src/log_reader.rs – the witness‑stream ingestor

```rust
use crossbeam::channel::{self, Sender};
use notify::{RecommendedWatcher, RecursiveMode, Watcher};
use serde::Deserialize;
use std::fs::File;
use std::io::{BufRead, BufReader, Seek, SeekFrom};
use std::path::Path;
use std::sync::{Arc, Mutex};
use std::thread;
use std::time::Duration;

/// One record from the witness log.
#[derive(Debug, Deserialize)]
pub struct WitnessRecord {
    #[serde(rename = "ts")]
    pub timestamp: f64,   // seconds since epoch (float for sub‑second)
    pub value: f64,       // the metric we want to plot
}

/// Spawns a background thread that watches `path` and sends new records
/// over `tx`. Returns a handle that can be dropped to stop the thread.
pub fn start_watcher<P: AsRef<Path>>(path: P, tx: Sender<WitnessRecord>) -> thread::JoinHandle<()> {
    let path = path.as_ref().to_path_buf();
    thread::spawn(move || {
        // Initialise the file at its current end (ignore historic data).
        let mut file = File::open(&path).expect("failed to open witness log");
        file.seek(SeekFrom::End(0)).expect("seek to end failed");
        let mut reader = BufReader::new(file);

        // Set up a file‑watcher so we notice when the file is rotated/truncated.
        let (notify_tx, notify_rx) = std::sync::mpsc::channel();
        let mut watcher = RecommendedWatcher::new(
            move |res| {
                if let Ok(event) = res {
                    if event.kind.is_modify() {
                        let _ = notify_tx.send(());
                    }
                }
            },
            notify::Config::default(),
        )
        .expect("watcher creation failed");
        watcher
            .watch(&path, RecursiveMode::NonRecursive)
            .expect("failed to watch file");

        loop {
            // Drain any pending notify events (rotation/truncation).
            while let Ok(_) = notify_rx.try_recv() {
                // Re‑open the file at the beginning – a new file may have been created.
                let _ = file.seek(SeekFrom::Start(0));
                let mut new_file = File::open(&path).expect("re‑open failed");
                std::mem::swap(&mut
