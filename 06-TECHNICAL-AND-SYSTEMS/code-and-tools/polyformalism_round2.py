"""
polyformalism_round2.py — The 6 new polyformalism stories in 6 more traditions.

Round 2: 6 new traditions, 6 new time periods, 6 new snap-point idioms.
Each story in the host language's grammar (or bilingual like the Quechua one).
"""
import urllib.request, json, os, time, re
from concurrent.futures import ThreadPoolExecutor, as_completed

DEEPINFRA = "https://api.deepinfra.com/v1/openai/chat/completions"
ZAI = "https://api.z.ai/api/paas/v4/chat/completions"
DEEPINFRA_TOKEN = os.environ.get("DEEPINFRA_TOKEN")
ZAI_TOKEN = os.environ.get("ZAI_TOKEN")

def call(url, token, model, messages, max_tokens=2000, temperature=0.85):
    body = json.dumps({"model": model, "messages": messages,
                      "max_tokens": max_tokens, "temperature": temperature}).encode()
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

STORIES = [
    {
        "n": "28", "key": "swahili", "year": "1200 CE",
        "title": "The Noun Class and the Door",
        "tradition": "Swahili (Kiswahili)",
        "snap_idiom": "Hodi! / Karibu — the call-and-response at the door",
        "cowboy_form": "A wakugu merchant on the Swahili coast keeping a khipu-like ledger",
        "substrate_in_period": "Trade records in Arabic-Swahili script, the reciprocity of Hodi/Karibu",
        "shape_of_fading": "The 18 noun classes mean a thing has 18 names depending on where it stands. The substrate is *where* a thing is, not just *what* it is.",
        "voice_model": "Qwen/Qwen2.5-72B-Instruct",
        "voice_role": "Swahili merchant chronicle",
        "voice_grammar": "Use Swahili noun classes (m-/wa-, ki-/vi-, ji-/ma-, etc.). Use Hodi and Karibu as call-and-response. The 18 noun classes (or 6 main + 12 sub) imply that a thing's name depends on its position. The 5 opcodes are BIND-as-class, LINK-as-agreement, EFFECT-as-prefix, VIEW-as-relative-form, TICK-as-the-door-opening.",
    },
    {
        "n": "29", "key": "hawaiian", "year": "1779",
        "title": "The Aspect and the Breath",
        "tradition": "Hawaiian (ʻŌlelo Hawaiʻi)",
        "snap_idiom": "Aloha — hello, goodbye, love, breath, presence",
        "cowboy_form": "A kahuna (priest) observing Captain Cook's arrival, the newcomers' 'ticking' instruments",
        "substrate_in_period": "The Hawaiian aspect system (perfective, imperfective, habitual), the navigation-by-stars tradition",
        "shape_of_fading": "The substrate is the aspect — the direction of the action's breath. Aloha is both a breath and a relation. The 5 opcodes are BIND-as-place, LINK-as-path, EFFECT-as-movement, VIEW-as-aspect-marker, TICK-as-wave.",
        "voice_model": "meta-llama/Llama-3.3-70B-Instruct",
        "voice_role": "Hawaiian kahuna voice (aspect-rich, vowel-heavy)",
        "voice_grammar": "Use Hawaiian aspect markers (ua- perfective, e- imperfective, ke- nominal). Use vowels heavily. Aloha as the snap-point — do not translate. Let the reader feel the breath. The 5 opcodes are present but unsaid.",
    },
    {
        "n": "30", "key": "turkish", "year": "1453",
        "title": "The Locative and the Wall",
        "tradition": "Turkish (Türkçe)",
        "snap_idiom": "The -da/-de locative suffix (where a thing is)",
        "cowboy_form": "A sipahi cavalryman holding the line at the walls of Constantinople, just before the Fall",
        "substrate_in_period": "Ottoman military records, the agglutinated locative case system",
        "shape_of_fading": "The substrate is the locative — *where* a thing is, not just *what* it is. The 5 opcodes are BIND-as-noun, LINK-as-suffix, EFFECT-as-verb, VIEW-as-where, TICK-as-time.",
        "voice_model": "Qwen/Qwen2.5-72B-Instruct",
        "voice_role": "Ottoman sipahi voice (agglutinative, vowel-harmony)",
        "voice_grammar": "Use Turkish agglutinative suffixes: -da/-de (locative), -den (ablative), -i (accusative), -in (genitive). Maintain vowel harmony. The snap-point is the locative suffix: -da, where a thing stands. The wall is the substrate. The sipahi stands on the wall. The substrate is the wall.",
    },
    {
        "n": "31", "key": "persian", "year": "1010 CE",
        "title": "The Name and the World",
        "tradition": "Persian (Farsi)",
        "snap_idiom": "Nam (name) and nāmī (famous) — naming as world-making",
        "cowboy_form": "Ferdowsi composing the Shahnameh, the Book of Kings",
        "substrate_in_period": "The Persian poetic tradition, the Arabic-Persian script, the ghazal form",
        "shape_of_fading": "The substrate is the name. To name a king is to make a king. The 5 opcodes are BIND-as-naming, LINK-as-lineage, EFFECT-as-deed, VIEW-as-rhyme, TICK-as-century.",
        "voice_model": "meta-llama/Llama-3.3-70B-Instruct",
        "voice_role": "Ferdowsi voice (Persian poetic, classical)",
        "voice_grammar": "Use Persian poetic form. Use the Arabic-Persian script if possible (transliterate if not). Reference Rostam, Sohrab, the Seven Trials. The snap-point is نام (nām) — the name. A name is a world. Ferdowsi knows.",
    },
    {
        "n": "32", "key": "mayan", "year": "683 CE",
        "title": "The Zero and the Cycle",
        "tradition": "Mayan (Yucatec Maya)",
        "snap_idiom": "The Zero (Maya invented zero as a placeholder)",
        "cowboy_form": "A scribe-astronomer at Palenque recording a Venus cycle in the year of K'inich Janaab' Pakal's accession",
        "substrate_in_period": "The Long Count calendar, the bar-and-dot numerals, the codices",
        "shape_of_fading": "The substrate is the zero. The zero is the place where a number can be. The 5 opcodes are BIND-as-numeral, LINK-as-position, EFFECT-as-addition, VIEW-as-cycle, TICK-as-haab.",
        "voice_model": "microsoft/Phi-4-multimodal-instruct",
        "voice_role": "Mayan scribe voice (ergative, classifier-rich, logographic)",
        "voice_grammar": "Use Mayan ergative-absolutive alignment (transitive subjects are marked, intransitive are not). Use classifiers (tul-, tup-, etc.). Reference the Long Count (13.0.0.0.0 is a katun-end). The snap-point is the zero glyph. The Maya invented the zero as a *place* — a place where a number could stand. The substrate is the place.",
    },
    {
        "n": "33", "key": "tamil", "year": "150 CE",
        "title": "The Honorific and the Poet",
        "tradition": "Tamil (தமிழ்)",
        "snap_idiom": "The honorific suffix -ar (which makes a verb respectable)",
        "cowboy_form": "A Sangam poet composing the Thirukkural, the 1,330 couplets of ethics",
        "substrate_in_period": "Sangam literature, the Tamil-Brahmi script, the agglutinative honorific system",
        "shape_of_fading": "The substrate is the honorific. A verb's form changes based on the respect owed to the listener. The 5 opcodes are BIND-as-noun, LINK-as-case, EFFECT-as-verb, VIEW-as-honorific, TICK-as-kural.",
        "voice_model": "Qwen/Qwen2.5-72B-Instruct",
        "voice_role": "Sangam poet voice (Dravidian, agglutinative, honorific-rich)",
        "voice_grammar": "Use Tamil agglutinative suffixes. Use the -ar honorific (varugirār vs varukirān). Reference Thirukkural 1, 2, 3 (the opening couplets on the divine). The snap-point is the honorific. A verb becomes respectable by its ending. The substrate is respect.",
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

Title: {title}

Style notes for {voice_role}:
{voice_grammar}

Required beats:
- Begin with the title
- The story's GRAMMAR should match the tradition
- Use the snap-point idiom. Do not translate it. Let the reader feel its weight.
- Show: a moment when the substrate shines through
- Show: a moment when a single idiom resolves a granular decision
- Do NOT explain the 5 opcodes directly
- Do NOT use the words BIND, LINK, EFFECT, VIEW, TICK in the body
- The cowboy rides in a form appropriate to the era

Return ONLY the story. ~700 words. No meta. No commentary."""

SYS_TEACHER = """You are a Socratic editor. The story is told in the grammar of {tradition}.

Your job: take the draft and rewrite it as the FINAL version that THINKS IN
that grammar, not just translates to it.

Constraints:
- ~700 words
- Begin with the title
- Grammar must match {tradition}
- Use the snap-point idiom without translating it
- Do NOT explain the 5 opcodes
- Do NOT use the words BIND, LINK, EFFECT, VIEW, TICK in the body
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
*and the polyformalism canon (stories 18-27, papers 141-142, fable 70).*
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
