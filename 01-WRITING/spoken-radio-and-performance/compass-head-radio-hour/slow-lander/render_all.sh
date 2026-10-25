#!/bin/bash
set -e
cd /home/eileen/projects/ai-writings/radio-theater/compass-head-radio-hour/slow-lander
RH="/home/eileen/projects/ai-writings/radio-theater/compass-head-radio-hour"
echo "--- welcome ---"
python3 "$RH/tap-open-mic/mc_tts.py" mc/welcome.md mc/welcome.mp3 swjWCZjZyczZmjedyBph
echo "--- segments ---"
for i in 1 2 3 4 5 6; do
  python3 "$RH/dialogue.py" segments/seg-0$i-*.json segments/seg-0$i.mp3
done
echo "--- songs ---"
python3 "$RH/tap-open-mic/ship.py" songs/01-shanty LwjYZd1glNEr45cMyKCG 175000
python3 "$RH/tap-open-mic/ship.py" songs/02-country 1vOUac3gQ4HzcEgM4rSQ 195000
python3 "$RH/tap-open-mic/ship.py" songs/03-blues 3vM2aA7o35cmtDlClXeb 190000
python3 "$RH/tap-open-mic/ship.py" songs/04-synth F1Qwa1bY45XAo57GBtNC 195000
python3 "$RH/tap-open-mic/ship.py" songs/05-folk KTMHq6EkKpqvyNkz17H7 175000
python3 "$RH/tap-open-mic/ship.py" songs/06-whole-song swjWCZjZyczZmjedyBph 210000
echo "ALL SLOW LANDER RENDERS DONE"
