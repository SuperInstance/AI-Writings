#!/bin/bash
# Civilization loop daemon — runs civilization_orchestrator forever
# Each iteration: 5 sims per civ + 5 competitions + extinction check
cd /workspace/repos/ai-writings

while true; do
    python3 cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai 2>&1 >> cellular-first-design/code/civilizations/civ_loop.log
    sleep 30
done
