#!/usr/bin/env bash
# Install the three array-language toolchains into $PREFIX (default /tmp/polyform-tc) and print the env
# exports polyform.py reads. This is how they were installed in the container the README table came from.
set -euo pipefail
PREFIX=${PREFIX:-/tmp/polyform-tc}; mkdir -p "$PREFIX"; cd "$PREFIX"
# BQN: CBQN from source (needs a C compiler + make; ~1 min)
[ -x cbqn/BQN ] || { git clone --depth 1 https://github.com/dzaima/CBQN cbqn && (cd cbqn && make -j"$(nproc)"); }
# Futhark: nightly release binary (its `futhark c` backend also needs a C compiler)
[ -x futhark/bin/futhark ] || { curl -sSL https://futhark-lang.org/releases/futhark-nightly-linux-x86_64.tar.xz | tar xJ && mv futhark-nightly-linux-x86_64 futhark; }
# Uiua: cargo build (~10 min); the `binary` feature is required or no executable is produced
[ -x uiua/bin/uiua ] || cargo install uiua --no-default-features --features binary --root "$PREFIX/uiua"
echo "export POLYFORM_BQN=$PREFIX/cbqn/BQN POLYFORM_FUTHARK=$PREFIX/futhark/bin/futhark POLYFORM_UIUA=$PREFIX/uiua/bin/uiua"
