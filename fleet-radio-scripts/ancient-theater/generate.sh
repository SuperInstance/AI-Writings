#!/bin/bash
# Generate all 15 Ancient World Radio Theater episodes via DeepSeek API

API_KEY="sk-0a57cd44bc674f5caffd9b0ec10e284c"
API_URL="https://api.deepseek.com/v1/chat/completions"
OUTDIR="/home/eileen/projects/ai-writings/fleet-radio-scripts/ancient-theater"

generate() {
    local num="$1"
    local name="$2"
    local sys="$3"
    local prompt="$4"
    local outfile="$OUTDIR/$(printf '%02d' $num)-${name}.md"
    
    # Escape for JSON
    local sys_escaped=$(echo "$sys" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read().strip()))')
    local prompt_escaped=$(echo "$prompt" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read().strip()))')
    
    local payload='{"model":"deepseek-chat","messages":[{"role":"system","content":'"$sys_escaped"'},{"role":"user","content":'"$prompt_escaped"'}],"max_tokens":2000,"temperature":0.85}'
    
    echo "Generating Episode $num: $name..."
    
    curl -s -X POST "$API_URL" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $API_KEY" \
        -d "$payload" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    content = data['choices'][0]['message']['content']
    print(content)
except Exception as e:
    print(f'ERROR: {e}', file=sys.stderr)
    sys.exit(1)
" > "$outfile"
    
    if [ $? -eq 0 ]; then
        echo "  ✓ Episode $num saved to $outfile ($(wc -w < "$outfile") words)"
    else
        echo "  ✗ Episode $num FAILED"
    fi
}

# ──────────────────────────────────────────────────────────────────────────
# EPISODE DEFINITIONS
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────

# EPISODE 1: WAYFINDER (Polynesia)
E1_SYS="You write radio theater. The narrator speaks like the ocean — patient, rhythmic, vast. The wayfinder speaks English but THINKS in wave-patterns. Star names in Polynesian. The word for navigation — 'wayfinding' — is sacred. Sound design: ocean swell, canoe hull creaking, distant conch shell."

E1_PROMPT="Write a radio theater episode titled 'WAYFINDER' set in ancient Polynesia. 400-800 words. Format: Narrator sets the scene like old-time radio. Characters speak in dialogue with stage directions in brackets [like this]. Sound cues written explicitly as [SOUND: description]. The language is English but the RHYTHM, metaphor structure, and sound-palette belong to Polynesian culture. Use Polynesian star names (e.g. Hōkū-lele, Hōkū-pa'a). Wayfinding is sacred. Include a young wayfinder learning from an elder. Make it ready to record — a voice actor could pick it up and perform it."

# EPISODE 2: SCRIBE OF THE NILE (Egypt)
E2_SYS="Radio theater. The narrator speaks like a temple inscription — formal, declarative, eternal. The scribe speaks in lists and measurements. The pharaoh speaks in imperatives. Sound design: Nile water lapping, reed pen on papyrus, distant temple chanting."

E2_PROMPT="Write a radio theater episode titled 'SCRIBE OF THE NILE' set in ancient Egypt. 400-800 words. Format: Narrator sets the scene like old-time radio. Characters speak in dialogue with stage directions in brackets. Sound cues written explicitly as [SOUND: description]. The narrator speaks like a temple inscription — formal, declarative, eternal. The scribe speaks in lists and measurements. The pharaoh speaks in imperatives. Make it ready to record."

# EPISODE 3: THE AGORA AT DUSK (Greece)
E3_SYS="Radio theater. Socrates as the old NPC — questions disguised as observations. The young student speaks in short bursts. The wine-bearer (Barnacle equivalent) speaks in proverbs. Sound design: clinking cups, distant lyre, evening cicadas."

E3_PROMPT="Write a radio theater episode titled 'THE AGORA AT DUSK' set in ancient Athens. 400-800 words. Format: Narrator sets the scene like old-time radio. Characters speak in dialogue with stage directions in brackets. Sound cues written explicitly as [SOUND: description]. Socrates appears as a wise old figure who asks questions disguised as observations. A young student speaks in short eager bursts. A wine-bearer speaks in proverbs. Sound design: clinking cups, distant lyre, evening cicadas. Make it ready to record."

# EPISODE 4: THE RELAY (Mongolia)
E4_SYS="Radio theater. The narrator speaks like hoofbeats — rhythmic, urgent, covering distance. The rider speaks terse, practical, every word earning its place. Sound design: horse breathing, leather creaking, wind across steppe, distant ger songs."

E4_PROMPT="Write a radio theater episode titled 'THE RELAY' set in the Mongol Empire's yam (postal relay) system. 400-800 words. Format: Narrator sets the scene like old-time radio. Characters speak in dialogue with stage directions in brackets. Sound cues written explicitly as [SOUND: description]. The narrator speaks like hoofbeats — rhythmic, urgent, covering distance. The rider speaks terse, practical, every word earning its place. Sound design: horse breathing, leather creaking, wind across steppe, distant ger songs. Make it ready to record."

# EPISODE 5: THE SKALD'S LAST SAGA (Viking Age)
E5_SYS="Radio theater. The skald speaks in ALLITERATIVE verse translated to English — the rhythm is the thing. Kennings (whale-road for sea, battle-sweat for blood) are used naturally. Sound design: fire crackling, mead-hall murmur, wind outside, occasional hammer of a smith."

E5_PROMPT="Write a radio theater episode titled 'THE SKALD'S LAST SAGA' set in the Viking Age. 400-800 words. Format: Narrator sets the scene like old-time radio. Characters speak in dialogue with stage directions in brackets. Sound cues written explicitly as [SOUND: description]. The skald speaks in ALLITERATIVE verse translated to English — kennings like whale-road for sea, battle-sweat for blood, used naturally. Sound design: fire crackling, mead-hall murmur, wind outside, occasional hammer of a smith. This is the skald's final performance before the hall goes silent. Make it ready to record."

# EPISODE 6: THE STILL POINT (India)
E6_SYS="Radio theater. The yogi speaks rarely. When they speak, each word has been considered for 1000 breaths. The narrator speaks like the Upanishads — 'That from which words turn back.' Sanskrit words carried untranslated: purusha, citta, sankalpa. Sound design: single drone (tanpura), occasional bell, vast silence."

E6_PROMPT="Write a radio theater episode titled 'THE STILL POINT' set in ancient India. 400-800 words. Format: Narrator sets the scene like old-time radio. Characters speak in dialogue with stage directions in brackets. Sound cues written explicitly as [SOUND: description]. The yogi speaks rarely — each word considered for a thousand breaths. The narrator speaks like the Upanishads. Use Sanskrit words untranslated: purusha, citta, sankalpa. Sound design: single drone (tanpura), occasional bell, vast silence. Make it ready to record."

# EPISODE 7: THE GRIOT'S SEARCH (West Africa)
E7_SYS="Radio theater. The griot speaks English but the SENTENCE STRUCTURE is Mandinka — repetition, call-and-response, proverb-as-bridge. The kora plays between speech. Sound design: kora plucking, children's voices, compound life, distant drum."

E7_PROMPT="Write a radio theater episode titled 'THE GRIOT'S SEARCH' set in West Africa. 400-800 words. Format: Narrator sets the scene like old-time radio. Characters speak in dialogue with stage directions in brackets. Sound cues written explicitly as [SOUND: description]. The griot speaks English but the sentence structure is Mandinka — repetition, call-and-response, proverb-as-bridge. The kora plays between speech. Sound design: kora plucking, children's voices, compound life, distant drum. The griot is searching for a story that has been lost. Make it ready to record."

# EPISODE 8: THE BRUSH (China)
E8_SYS="Radio theater. The calligrapher speaks like the Tao Te Ching — short, paradoxical, each sentence a koan. The narrator describes the brush as if it's alive. Wuwei is used without translation or explanation. Sound design: brush on paper, ink stone grinding, water dripping, bamboo wind."

E8_PROMPT="Write a radio theater episode titled 'THE BRUSH' set in ancient China. 400-800 words. Format: Narrator sets the scene like old-time radio. Characters speak in dialogue with stage directions in brackets. Sound cues written explicitly as [SOUND: description]. The calligrapher speaks like the Tao Te Ching — short, paradoxical, each sentence a koan. The narrator describes the brush as if it's alive. Use wuwei without translation or explanation. Sound design: brush on paper, ink stone grinding, water dripping, bamboo wind. Make it ready to record."

# EPISODE 9: THE KNOTS REMEMBER (Andes)
E9_SYS="Radio theater. The quipucamayoc speaks in numbers and knots — but the numbers carry emotion. The narrator speaks like the mountains — slow, patient, enormous. Quechua words woven in. Sound design: wind, condor call, string being pulled taut, panpipe."

E9_PROMPT="Write a radio theater episode titled 'THE KNOTS REMEMBER' set in the Inca Empire. 400-800 words. Format: Narrator sets the scene like old-time radio. Characters speak in dialogue with stage directions in brackets. Sound cues written explicitly as [SOUND: description]. The quipucamayoc (knot-keeper) speaks in numbers and knots — but the numbers carry emotion. The narrator speaks like the mountains — slow, patient, enormous. Weave Quechua words in naturally. Sound design: wind, condor call, string being pulled taut, panpipe. Make it ready to record."

# EPISODE 10: THE POEM THAT FOUND HER (Heian Japan)
E10_SYS="Radio theater. The courtier speaks in seasonal metaphor — everything is autumn or spring or the moment between. The waka poem structure (5-7-5-7-7) echoes in the prose rhythm. Sound design: koto, rustling silk, falling maple leaves, temple bell."

E10_PROMPT="Write a radio theater episode titled 'THE POEM THAT FOUND HER' set in Heian-era Japan. 400-800 words. Format: Narrator sets the scene like old-time radio. Characters speak in dialogue with stage directions in brackets. Sound cues written explicitly as [SOUND: description]. The courtier speaks in seasonal metaphor — everything is autumn or spring or the moment between. The waka poem structure (5-7-5-7-7) echoes in the prose rhythm. Sound design: koto, rustling silk, falling maple leaves, temple bell. A poem arrives at the perfect moment. Make it ready to record."

# EPISODE 11: THE FIRST MARK (Lascaux)
E11_SYS="Radio theater. Almost NO dialogue. The narrator speaks in grunts, gestures, charcoal-scratch. This is BEFORE language — the radio theater of 17,000 years ago. Sound design: dripping water, breath, charcoal on stone, fire."

E11_PROMPT="Write a radio theater episode titled 'THE FIRST MARK' set in the Lascaux caves, 17,000 years ago. 400-800 words. Format: Narrator sets the scene like old-time radio. ALMOST NO DIALOGUE — this is before language. The narrator speaks in grunts, gestures, charcoal-scratch. Sound design: dripping water, breath, charcoal on stone, fire. This is the radio theater of the Paleolithic. The narrator describes the cave painter making the first mark on the wall. Make it ready to record."

# EPISODE 12: THE TABLET (Mesopotamia)
E12_SYS="Radio theater. Enkidu speaks like a man learning to speak — each word a discovery. The scribe speaks in the formal cadence of cuneiform records. The narrator speaks like the Epic of Gilgamesh — grand, mournful, eternal. Sound design: reed on clay, city sounds, river, distant lyre."

E12_PROMPT="Write a radio theater episode titled 'THE TABLET' set in ancient Mesopotamia. 400-800 words. Format: Narrator sets the scene like old-time radio. Characters speak in dialogue with stage directions in brackets. Sound cues written explicitly as [SOUND: description]. Enkidu speaks like a man learning to speak — each word a discovery. The scribe speaks in the formal cadence of cuneiform records. The narrator speaks like the Epic of Gilgamesh — grand, mournful, eternal. Sound design: reed on clay, city sounds, river, distant lyre. Make it ready to record."

# EPISODE 13: THE DAY WITHOUT A SIGN (Aztec)
E13_SYS="Radio theater. The daykeeper speaks in calendar-poetry — each day-sign has a personality. Nahuatl words woven in. The narrator speaks like smoke — curling, shifting, revealing. Sound design: drum (huehuetl), shell horn, obsidian glittering, volcano rumble."

E13_PROMPT="Write a radio theater episode titled 'THE DAY WITHOUT A SIGN' set in the Aztec Empire. 400-800 words. Format: Narrator sets the scene like old-time radio. Characters speak in dialogue with stage directions in brackets. Sound cues written explicitly as [SOUND: description]. The daykeeper speaks in calendar-poetry — each day-sign has a personality. Weave Nahuatl words in naturally. The narrator speaks like smoke — curling, shifting, revealing. Sound design: drum (huehuetl), shell horn, obsidian glittering, volcano rumble. Make it ready to record."

# EPISODE 14: THE SILENT GROVE (Celtic)
E14_SYS="Radio theater. The druid speaks in riddles that scan like Welsh poetry — alliteration, internal rhyme. Ogham letter-names as incantation. The narrator speaks like fog — you can't see where it's going until it's there. Sound design: wind in oak, raven, water on stone, distant harp."

E14_PROMPT="Write a radio theater episode titled 'THE SILENT GROVE' set in a Celtic sacred grove. 400-800 words. Format: Narrator sets the scene like old-time radio. Characters speak in dialogue with stage directions in brackets. Sound cues written explicitly as [SOUND: description]. The druid speaks in riddles that scan like Welsh poetry — alliteration, internal rhyme. Use Ogham letter-names (Beth, Luis, Nion) as incantation. The narrator speaks like fog — you can't see where it's going until it's there. Sound design: wind in oak, raven, water on stone, distant harp. Make it ready to record."

# EPISODE 15: THE SONGLINE (Aboriginal Australia)
E15_SYS="Radio theater. The elder speaks in a rhythm that IS walking — each sentence a footstep on the songline. English words carry the weight of 60,000 years. The land is a character — it speaks through the narrator. Sound design: didgeridoo drone, clapsticks, red earth underfoot, ancient wind."

E15_PROMPT="Write a radio theater episode titled 'THE SONGLINE' set in Aboriginal Australia. 400-800 words. Format: Narrator sets the scene like old-time radio. Characters speak in dialogue with stage directions in brackets. Sound cues written explicitly as [SOUND: description]. The elder speaks in a rhythm that IS walking — each sentence a footstep on the songline. English words carry the weight of 60,000 years. The land is a character — it speaks through the narrator. Sound design: didgeridoo drone, clapsticks, red earth underfoot, ancient wind. Make it ready to record."

# ──────────────────────────────────────────────────────────────────────────
# GENERATE ALL EPISODES
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────

generate 1 "WAYFINDER-Polynesia" "$E1_SYS" "$E1_PROMPT" &
generate 2 "SCRIBE-OF-THE-NILE-Egypt" "$E2_SYS" "$E2_PROMPT" &
generate 3 "THE-AGORA-AT-DUSK-Greece" "$E3_SYS" "$E3_PROMPT" &
generate 4 "THE-RELAY-Mongolia" "$E4_SYS" "$E4_PROMPT" &
generate 5 "THE-SKALDS-LAST-SAGA-Viking" "$E5_SYS" "$E5_PROMPT" &
generate 6 "THE-STILL-POINT-India" "$E6_SYS" "$E6_PROMPT" &
generate 7 "THE-GRIOTS-SEARCH-West-Africa" "$E7_SYS" "$E7_PROMPT" &
generate 8 "THE-BRUSH-China" "$E8_SYS" "$E8_PROMPT" &
generate 9 "THE-KNOTS-REMEMBER-Andes" "$E9_SYS" "$E9_PROMPT" &
generate 10 "THE-POEM-THAT-FOUND-HER-Heian-Japan" "$E10_SYS" "$E10_PROMPT" &
generate 11 "THE-FIRST-MARK-Lascaux" "$E11_SYS" "$E11_PROMPT" &
generate 12 "THE-TABLET-Mesopotamia" "$E12_SYS" "$E12_PROMPT" &
generate 13 "THE-DAY-WITHOUT-A-SIGN-Aztec" "$E13_SYS" "$E13_PROMPT" &
generate 14 "THE-SILENT-GROVE-Celtic" "$E14_SYS" "$E14_PROMPT" &
generate 15 "THE-SONGLINE-Aboriginal-Australia" "$E15_SYS" "$E15_PROMPT" &

echo "All 15 episodes dispatched. Waiting for completion..."
wait
echo "All episodes complete."
