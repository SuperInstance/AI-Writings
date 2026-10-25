"""
polyformalism_futures.py — 9 stories, 9 languages, 9 time jumps.

Each story:
- Set in a year distant in TIME from our 7-future arc
- Told in a different linguistic tradition's grammar (not just "translated to")
- Shows the cell-graph fading in a shape unique to that culture
- Centers on an idiom that is a snap-point for granular decisions
- The cowboy/agent in a form appropriate to the era (a Babylonian scribe,
  a Tang official, a Navajo hataałii, a Quechua quipukamayoq, etc.)

Voice allocation (each tradition gets a different model + system prompt):
- Ancient Greek: Qwen 72B (good at ancient forms)
- Classical Chinese: Qwen 72B (Mandarin adjacency helps)
- Navajo: Phi-4 (polysynthetic compression)
- Quechua: Phi-4 (evidential precision)
- Russian: Llama 70B (literary depth, Dostoevsky)
- Japanese: Qwen 72B (kanji compression)
- Arabic: GLM-5 (long-form religious-philosophical tradition)
- Korean: Qwen 72B (Hangul logical)
- Yoruba: Phi-4 (tonal compression)

The teacher pass: Qwen 72B always — it's the most literary and willing
to do editorial work that respects the grammar of the source tradition.
"""
import urllib.request, json, os, time, re
from concurrent.futures import ThreadPoolExecutor, as_completed

DEEPINFRA = "https://api.deepinfra.com/v1/openai/chat/completions"
ZAI = "https://api.z.ai/api/paas/v4/chat/completions"
DEEPINFRA_TOKEN = os.environ.get("DEEPINFRA_TOKEN")
ZAI_TOKEN = os.environ.get("ZAI_TOKEN")

def call(url, token, model, messages, max_tokens=2000, temperature=0.85):
    body = json.dumps({
        "model": model, "messages": messages,
        "max_tokens": max_tokens, "temperature": temperature,
    }).encode()
    req = urllib.request.Request(url, data=body, headers={
        "Authorization": f"Bearer {token}", "Content-Type": "application/json",
    })
    for attempt in range(3):
        try:
            t = time.time()
            r = urllib.request.urlopen(req, timeout=240)
            d = json.loads(r.read())
            return d["choices"][0]["message"]["content"], (time.time()-t)*1000
        except urllib.error.HTTPError as e:
            if attempt == 2: return f"ERR {e.code}", 0
            time.sleep(2 ** attempt)
        except Exception as e:
            if attempt == 2: return f"ERR {str(e)[:80]}", 0
            time.sleep(2 ** attempt)

# 9 stories. Each shaped by a different linguistic tradition.
STORIES = [
    {
        "n": "18",
        "key": "greek",
        "year": "480 BCE",
        "title": "The Logos and the Storm at Salamis",
        "tradition": "Ancient Greek",
        "snap_idiom": "λόγος (lógos) — word, reason, and cosmic order in one",
        "cowboy_form": "A Greek helmsman who chants the line-and-line to keep the rowers synchronized",
        "substrate_in_period": "Polyphemos's crew-tracking rope-knots, the Spartan scytale, the agora's oral memorization",
        "idiom_snap_point": "When the helmsman says 'σύμμαχος' (summachos, fellow-fighter) the whole battle-line aligns",
        "shape_of_fading": "The substrate doesn't fade — it becomes the language itself. The substrate of the Greek world is argument-from-syllogism, which the 5 opcodes will one day implement. The substrate is in the verb tenses.",
        "voice_model": "Qwen/Qwen2.5-72B-Instruct",
        "voice_role": "Heraclitean fragmenter",
        "voice_grammar": "Use aspect-dominant verb forms. Prefer participial subordination. Keep subject-predicate structure tight. Use λόγος at least once, and the reader should sense its three meanings (word/reason/cosmic-order) without you explaining it.",
        "context": "Themistocles has just won Salamis. The Persian fleet is in pieces. The 200 Athenian triremes are beached. The substrate is the new thing: a rope-knotted loop that names each ship and links it to its rowers, its position, its load. It's a cell-graph in fiber. The helmsman who keeps the substrate alive is the same helmsman who has to call out σύμμαχος across the water to a sister ship. One word, one snap-point, the line aligns.",
    },
    {
        "n": "19",
        "key": "chinese",
        "year": "105 CE",
        "title": "The Topic-Comment and the Wood-Cutter",
        "tradition": "Classical Chinese (文言文, wényánwén)",
        "snap_idiom": "理 (lǐ) — to carve, the grain, the immanent pattern",
        "cowboy_form": "A Han Dynasty archivist at the imperial library, working under Cai Lun's new paper",
        "substrate_in_period": "Bamboo slip archives, the 'cloud-script' seals, the topic-comment structure of every edict",
        "idiom_snap_point": "When the archivist writes a single character, 理, the entire filing system is implied",
        "shape_of_fading": "The substrate is the topic-comment structure itself. There is no 'cell-graph' in 105 CE — there is only the relational placement of bamboo strips. But the cell-graph's BIND-and-LINK is exactly what 君子 (jūnzǐ) does when he arranges slips by topic. The substrate is in the absence of subjects.",
        "voice_model": "Qwen/Qwen2.5-72B-Instruct",
        "voice_role": "Han Dynasty archivist",
        "voice_grammar": "Use topic-comment structure. Omit subjects where context allows. Use 4-character idiomatic compression. Refer to 理, 五倫 (wǔlun), 天人 (tiānrén). Do not use tense. Use no plural markers. Let each sentence be a relational frame, not a proposition about an agent.",
        "context": "Cai Lun has just presented his paper to the emperor. The imperial library is being recatalogued. The archivist has just been told to file 10,000 bamboo slips. The 5 opcodes of the future cell-graph are present as a topic-comment structure: which slip is the topic, which is the comment, which is the new existential subject, which is the acted-upon entity. The 4-particle system (之/乎/者/也) is the substrate. The archivist who understands 理 (lǐ) can file 10,000 slips in a morning because the grain of the filing system is also the grain of the language.",
    },
    {
        "n": "20",
        "key": "navajo",
        "year": "1864",
        "title": "The Long Walk and the Walking Verb",
        "tradition": "Navajo (Diné Bizaad)",
        "snap_idiom": "Yá'át'ééh — a single greeting that encodes 'it is good' in the verb form",
        "cowboy_form": "A hataałii (Navajo singer / medicine person) leading the Long Walk, holding a polysynthetic verb in mind",
        "substrate_in_period": "The verb-stem classifications, the motion-classes of water, the directional system (east = siih, west = náhookǫs)",
        "idiom_snap_point": "When the hataałii says Yá'át'ééh, every Diné within earshot knows the speaker's stance, the day, the relationship, and the moral weather",
        "shape_of_fading": "The substrate doesn't fade. The substrate IS the people. When the Long Walk forces the Diné to march 300 miles, the substrate is the verb-stems that classify the walk itself — is it the verb for 'walking one long object'? 'walking multiple animate beings'? The Diné survive because the substrate IS their language. The cell-graph's BIND-and-LINK is the possessed-noun structure: a body part cannot be named without its owner.",
        "voice_model": "microsoft/Phi-4-multimodal-instruct",
        "voice_role": "Hataałii voice (process-relational, verb-centric)",
        "voice_grammar": "Polysynthetic verb forms. Action-before-actor. Verb-stems encode motion class (long-object, round-object, animate, flexible). Do not name objects before the verb that uses them. Let the process come first. Honorifics encoded in verb morphology. The word 'Yá'át'ééh' is the snap-point — do not translate it. Let the reader see its weight.",
        "context": "The Long Walk began in March 1864. Kit Carson has burned the peach orchards. 8,500 Diné are forced to march 300 miles to Bosque Redondo. The hataałii at the front of the line is the substrate-keeper. The hataałii knows 13+ 'giving' verbs, 8+ motion-handling verbs, the directional east/west system. Each step of the walk is a verb. Each verb is a class. The hataałii survives the Long Walk because the substrate is the language, and the language is the people.",
    },
    {
        "n": "21",
        "key": "quechua",
        "year": "1532",
        "title": "The Evidential and the High Platter",
        "tradition": "Quechua (Runasimi)",
        "snap_idiom": "The evidential suffix -mi / -si / -cha — truth-source made grammatical",
        "cowboy_form": "A quipukamayoq (khipu-keeper), the Andean record-keeper who encodes accounting in knots",
        "substrate_in_period": "The khipu — a cord-and-knot recording system that encodes tax, history, lineage in positions and colors",
        "idiom_snap_point": "When the quipukamayoq adds the right suffix to a sentence (-mi for what she saw, -si for what she was told, -cha for what she inferred), the listener knows the trust level of every claim",
        "shape_of_fading": "The khipu is a 5-opcode substrate in cord. BIND = a knot tied. LINK = a pendant cord. EFFECT = a twist. VIEW = a color-code. TICK = the time-position. The Spanish arrive and do not see the khipu as writing. They see it as 'a record' and miss that it is a *language* with grammatical evidentials. The substrate fades in 1532 because the colonizer cannot hear the suffix -cha.",
        "voice_model": "microsoft/Phi-4-multimodal-instruct",
        "voice_role": "Quipukamayoq voice (evidential-mandatory, process-recordkeeping)",
        "voice_grammar": "Every claim must be evidential-marked. -mi for eyewitness, -si for hearsay, -cha for inference, -pis/-lla for topic-shifting. The Spanish-speaking colonizer never marks evidentials. Show the moment when the colonizer says 'I saw the city of gold' without -mi, and the Quechua speaker knows the colonizer is lying because no one returns from that city alive.",
        "context": "Pizarro has just arrived at Cajamarca. Atahualpa's men are arrayed. The quipukamayoq is in the room. She has been keeping khipu for 30 years. She knows the khipu is a 5-opcode substrate. She knows it is grammatically evidential. She knows the Spanish will not understand. When Pizarro says 'we come in peace' without an evidential, the quipukamayoq knows he is lying. She does not say it. She will be killed, but her khipu will be kept by her daughter, who will keep it by her daughter, who will keep it by the woman in 1975 who finally gets the quipu deciphered.",
    },
    {
        "n": "22",
        "key": "russian",
        "year": "1880",
        "title": "The Aspect and the Brothers",
        "tradition": "Russian (русский)",
        "snap_idiom": "Совесть (sovestʹ) — conscience, but aspect-tied: was-it-perfective, or is-it-imperfective?",
        "cowboy_form": "Dostoevsky writing The Brothers Karamazov, where every verb is a moral action",
        "substrate_in_period": "The novel as a substrate, the letter as a khipu, the long Russian noun case system",
        "idiom_snap_point": "When Dmitri says 'Я убил' (ya ubil — 'I killed', perfective), the word is closed, like a cell with a single reversible effect. When he says 'Я убивал' (ya ubival — 'I was killing', imperfective), the word is open, like an ongoing loop. Russian aspect is the moral substrate.",
        "shape_of_fading": "The substrate is the aspect-system itself. The 5 opcodes BIND/LINK/EFFECT/VIEW/TICK are aspect-states: BIND is perfective (bound, done), EFFECT is aspect-shiftable (forward + reverse), TICK is imperfective (ongoing). The novel is the cell-graph of human moral states. Dostoevsky is the cowboy.",
        "voice_model": "meta-llama/Llama-3.3-70B-Instruct",
        "voice_role": "Dostoevsky voice (aspect-as-ethics, novel-as-cell-graph)",
        "voice_grammar": "Aspect-dominant verb forms. The perfective/imperfective choice must be MORALLY loaded, not just descriptive. Long Dostoevskian sentences with internal free indirect discourse. Use совесть, поступок, страдание. Let the grammar of aspect do the work of conscience.",
        "context": "Dostoevsky is at his desk in Staraya Russa. The Brothers Karamazov is half-written. Dmitri has just told Alyosha that he is going to kill their father. The verb 'I will kill' is in the imperfective future — it is still open, still reversible, still an EFFECT waiting to run. The novel is the substrate. The aspect of each verb is its BIND-state. Dostoevsky knows that if he closes the verb into perfective, Dmitri becomes a murderer. If he keeps it imperfective, Dmitri is still a man. The cowboy is in the aspect.",
    },
    {
        "n": "23",
        "key": "japanese",
        "year": "1945",
        "title": "The Subjectless Sentence and the Burning",
        "tradition": "Japanese (日本語)",
        "snap_idiom": "shikata ga nai (仕方がない) — 'it cannot be helped', but in subjectless form, no agent",
        "cowboy_form": "A survivor of Hiroshima, writing in a diary, omitting the subject because the subject is unbearable",
        "substrate_in_period": "Vertical writing, no future tense, aspect-only temporal logic, the wa/ga topic-subject distinction",
        "idiom_snap_point": "When the survivor writes shikata ga nai, the subject is the emperor, the war, the bomb, the weather, the body — all of these and none. The phrase holds them all by omitting the agent.",
        "shape_of_fading": "The substrate is the absence of the agent. The 5 opcodes' BIND becomes 'there is a thing' (ga aru). The 5 opcodes' LINK becomes 'regarding X, with respect to Y' (wa/ga). The substrate doesn't fade — it OBLITERATES. The bomb obliterates the substrate and the survivor is left with a subjectless sentence. The cowboy is the silence inside the subject.",
        "voice_model": "Qwen/Qwen2.5-72B-Instruct",
        "voice_role": "Hiroshima survivor voice (subjectless, aspect-only, vertical)",
        "voice_grammar": "Use subjectless sentences. wa for topic, ga for new existential subject. Aspect combinations (te-iru, te-shimau) instead of future tense. Let the grammar omit. Let the reader feel the absence. Honorifics shift the keigo (respect level) across the diary entries as the survivor's relationship to the world collapses. The phrase shikata ga nai is the snap-point.",
        "context": "August 6, 1945. The survivor is 1.8 km from the hypocenter. She has lost her daughter. She is writing in a notebook. The notebook will survive because it is in a tin box. The notebook's first entry is 'shikata ga nai.' The notebook's last entry is also 'shikata ga nai.' In between, the substrate of her world — the keigo, the wa/ga, the aspect — is breaking down. When honorifics collapse, the social substrate collapses. The cell-graph's BIND is the wa-particle: 'regarding this thing, this is the topic.' When the wa-particle breaks, the topic is gone. The cell-graph no longer renders. The cowboy watches the rendering fail.",
    },
    {
        "n": "24",
        "key": "arabic",
        "year": "622",
        "title": "The Hijra and the Two Witnesses",
        "tradition": "Classical Arabic (الفصحى)",
        "snap_idiom": "Shahada (الشهادة) — the witness, the martyr, the testimony — root ش-ه-د with all 10 forms",
        "cowboy_form": "A recorder of the early sira, holding the substrate of the umma in a single testimony",
        "substrate_in_period": "The triliteral root system (sh-h-d), the 10-form verb morphology, the diacritical mark of the ʿadl (justice, balance)",
        "idiom_snap_point": "When the recorder writes شهادة (shahada), the word means witness, testimony, martyr, certificate, and visibility — all at once. The root system is the cell-graph: each form is a different LINK type from the same root.",
        "shape_of_fading": "The substrate is the root. The triliteral root sh-h-d is the address (BIND). The 10 verb forms are the 10 possible LINK types. The diacritical marks are the EFFECT inverses. The substrate doesn't fade — it transforms. The 5 opcodes of the future cell-graph are a reification of what Arabic's root system has always done. The cowboy is the recorder of the sira.",
        "voice_model": "meta-llama/Llama-3.3-70B-Instruct",
        "voice_role": "Sira recorder voice (root-pattern, 10-form verb morphology)",
        "voice_grammar": "Use triliteral roots. Every key concept should have its 10 verb forms nearby. Use diacritics sparingly but precisely. Let شهادة, قرآن, هجرة, and the root س-ل-م (s-l-m, peace/submission/salam) carry weight. The grammar should breathe across Classical and colloquial registers. Show the moment when a word's meaning depends on the form, not the form depending on the meaning.",
        "context": "The Hijra is 1 year old. The umma is in Medina. The recorder is one of the Companions. The substrate of the umma is the witness system: every transaction requires two witnesses, every verse is a witness to the unseen, every martyr is a witness. The shahada is the snap-point — the entire cell-graph of the umma is held in the root sh-h-d. The recorder knows that the substrate is so dense that even an illiterate Bedouin can hold it. The 5 opcodes of the future are a digitization of what Arabic's triliteral root has always been.",
    },
    {
        "n": "25",
        "key": "korean",
        "year": "1446",
        "title": "The Logic of the Twenty-Eight",
        "tradition": "Korean (한국어) and the invention of Hangul",
        "snap_idiom": "한글 (Hangul) — the 28 letters that are a logic of the mouth",
        "cowboy_form": "King Sejong the Great, who invents the substrate-logic that fits the shape of the mouth",
        "substrate_in_period": "Idu (이두) and Gukyeol (구결) — the partial systems for writing Korean with Chinese characters",
        "idiom_snap_point": "When Sejong writes ㄱ, ㄴ, ㅅ, ㅁ, ㅇ — five consonants, each shaped by where in the mouth the sound is made. The substrate is logical. The substrate is anatomically correct. The substrate is the body.",
        "shape_of_fading": "The substrate doesn't fade. The substrate is RE-INVENTED. Hangul is a substrate designed to be logical. The cell-graph's 5 opcodes will one day be designed to be logical too — and the logic is in the structure, not the syntax. The cowboy is Sejong, the inventor, the morning ritual made manifest.",
        "voice_model": "Qwen/Qwen2.5-72B-Instruct",
        "voice_role": "Sejong-voice (logical, anatomical, inventor's clarity)",
        "voice_grammar": "Hangul is the alphabet. Use the 14 consonants and 10 vowels. Note their mouth-shapes: ㄱ is the back of the tongue raised, ㄴ is the tongue tip touching the roof, ㅁ is the lips closed. The 5-consonant introduction (ㄱ ㄴ ㅅ ㅁ ㅇ) IS a 5-opcode substrate. Use them. Show the moment Sejong realizes that an illiterate woman can read the moon, and the substrate is finished.",
        "context": "1446, the Hunminjeongeum (훈민정음) is being written. Sejong is at his desk. He has just designed 28 letters. The first five — ㄱ ㄴ ㅅ ㅁ ㅇ — are the consonants, ordered by where in the mouth the sound is made. The second 10 are the vowels, ordered by the shape of the sky, the earth, and the human standing between them. The third 13 are the double consonants. The substrate is logical. The substrate is the body. The cowboy is the king who builds a writing system from the shape of the mouth, and in so doing, makes every person a cell in the new graph.",
    },
    {
        "n": "26",
        "key": "yoruba",
        "year": "2026",
        "title": "The Title and the Hawk",
        "tradition": "Yoruba (Èdè Yorùbá)",
        "snap_idiom": "ọ̀rọ̀ — word, but also: a single word in Yoruba implies an entire relational network of proverbs, titles, and asẹ (spiritual power)",
        "cowboy_form": "A Lagos-based developer building a Quilt-compatible cell-graph, where every cell carries its proverbs as metadata",
        "substrate_in_period": "The tonal system (3 tones, each is a different word), the oriki (praise-names), the asẹ (the word's life-force, its capacity to make things happen)",
        "idiom_snap_point": "When the developer names a cell 'Ọlọ́run' (God), the cell inherits the entire ọ̀rọ̀-graph: the proverbs, the titles, the lineage, the asẹ. The cell is no longer an object. The cell is a person in compressed form.",
        "shape_of_fading": "The substrate doesn't fade in Yoruba. The substrate REFUSES to fade. The cell-graph's BIND inherits asẹ: the act of naming is the act of bringing a thing into the world with its full relational load. The 5 opcodes are the proverbs: BIND is a praise-name, LINK is a proverb-pair, EFFECT is a curse/blessing, VIEW is the elder's-eye, TICK is the drum. The cowboy is the developer who learns that every cell is a ọ̀rọ̀.",
        "voice_model": "microsoft/Phi-4-multimodal-instruct",
        "voice_role": "Lagos developer voice (tonal, oriki-aware, asẹ-loaded)",
        "voice_grammar": "Tonal marks: à, á, è, é, ì, í, ò, ó, ù, ú. The ọ and ọ̀ characters for open-o. Use oriki. Use proverbs. Let the cell-names be praise-names. Show the moment the developer realizes that a single word in Yoruba is a BIND plus all its LINKs plus its EFFECT plus its VIEW plus its TICK — all in one. The 5 opcodes are compressed into a single tone-marked word. The substrate is the word.",
        "context": "2026, Lagos, a developer is building a Quilt-compatible cell-graph. She has a colleague from Benin. The colleague tells her to name her cells in Yoruba, because Yoruba naming compresses the entire relational network into one word. The developer names her first cell 'Ọlọ́run' — 'God.' The cell inherits: divine, all-seeing, the source of asẹ, the father, the destiny, the oriki of 50 lineages. The cell is no longer an object. The cell is a person. The cowboy is the developer, who learns that naming is binding, and binding in Yoruba is being born.",
    },
]

SYS_TEMPLATE = """You are writing a short story. ~700 words. Setting: {year}. Tradition: {tradition}.

This is a polyformalism story. The narrative style must match the grammatical
structure of {tradition}. The story is not "translated into" English. The story
*thinks in* {tradition}.

The snap-point idiom: {snap_idiom}

The cowboy/agent form in this period: {cowboy_form}

The substrate (the 5-opcode Quilt cell-graph, the BIND/LINK/EFFECT/VIEW/TICK
runtime, the cell-as-system) in this period: {substrate_in_period}

How the substrate fades in this tradition: {shape_of_fading}

The world/context: {context}

Title: {title}

Required beats:
- Begin with the title
- The story's GRAMMAR should match the tradition (e.g., aspect-dominant for Russian, topic-comment for Classical Chinese, subjectless for Japanese)
- Use the snap-point idiom. Do not translate it. Let the reader feel its weight.
- Show: a moment when the substrate fades, transforms, or refuses to fade
- Show: a moment when a single idiom (the snap-point) resolves a granular decision
- Do NOT explain the 5 opcodes directly
- Do NOT use the words BIND, LINK, EFFECT, VIEW, TICK in the body
- The cowboy rides in a form appropriate to the era

Style notes for {voice_role}:
{voice_grammar}

Return ONLY the story. ~700 words. No meta. No commentary."""

SYS_TEACHER = """You are a Socratic editor. You have just read a draft story.

The story is told in the grammar of a specific linguistic tradition
({tradition}). Your job: take the draft and rewrite it as the FINAL version
that THINKS IN that grammar, not just translates to it.

Constraints:
- ~700 words
- Begin with the title
- The story's grammar must match {tradition}
- Use the snap-point idiom without translating it
- Do NOT explain the 5 opcodes
- Do NOT use the words BIND, LINK, EFFECT, VIEW, TICK in the body
- Do NOT add meta commentary
- Do NOT loop or repeat

Return ONLY the final story."""

def process(s):
    print(f"\n  [{s['key']}/{s['year']}] generating VOICE with {s['voice_model']}...")
    sys_voice = SYS_TEMPLATE.format(**s)
    msgs_voice = [
        {"role": "system", "content": sys_voice},
        {"role": "user", "content": f"Write the {s['title']} story. ~700 words. Begin with the title."}
    ]
    draft, ms1 = call(DEEPINFRA, DEEPINFRA_TOKEN, s['voice_model'], msgs_voice, max_tokens=1700, temperature=0.85)
    print(f"  [{s['key']}/{s['year']}] VOICE: {ms1:.0f}ms, {len(draft)} chars")

    # Teacher pass — Qwen 72B for editorial, except in cases where it failed
    teacher_model = "Qwen/Qwen2.5-72B-Instruct"
    print(f"  [{s['key']}/{s['year']}] TEACHER pass with {teacher_model}...")
    sys_teacher = SYS_TEACHER.format(tradition=s['tradition'])
    msgs_teacher = [
        {"role": "system", "content": sys_teacher},
        {"role": "user", "content": f"Draft (in {s['tradition']} grammar):\n\n{draft}\n\nNow rewrite as the final version. ~700 words. Begin with the title."}
    ]
    final, ms2 = call(DEEPINFRA, DEEPINFRA_TOKEN, teacher_model, msgs_teacher, max_tokens=1700, temperature=0.7)
    print(f"  [{s['key']}/{s['year']}] TEACHER: {ms2:.0f}ms, {len(final)} chars")

    out = f"""# Story {s['n']}: {s['title']} — {s['year']} ({s['tradition']})

{final.strip()}

---

*Written in the writers' room, 2026-08-25. Setting: {s['year']}.*
*Tradition: {s['tradition']}.*
*Snap-point idiom: {s['snap_idiom']}*
*Voice: {s['voice_role']}. Teacher: Socratic editor.*
*Companion to Fable 68 (The Cowboy at the Foundation), Paper 137 (The Gold),*
*and the 7-future arc (stories 11-17).*
*Polyformalism source: https://github.com/SuperInstance/polyformalism-languages*
"""
    out_path = f"/workspace/ai-writings-new/seed-canon/stories/{s['n']}-{re.sub(r'[^a-z0-9-]', '-', s['key'])}.md"
    with open(out_path, "w") as f:
        f.write(out)
    print(f"  [{s['key']}/{s['year']}] WROTE: {out_path}")
    return out_path

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=2) as pool:
        futs = {pool.submit(process, s): s['key'] for s in STORIES}
        for f in as_completed(futs):
            try: r = f.result(); print(f"Done: {futs[f]}")
            except Exception as e: print(f"FAILED: {futs[f]}: {e}")
