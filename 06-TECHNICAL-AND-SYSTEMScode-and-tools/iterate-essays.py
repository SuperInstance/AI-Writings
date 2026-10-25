#!/usr/bin/env python3
"""Iterative multi-model essay refinement loop — the jam pattern for prose.

Usage: python3 iterate-essays.py <essay.md> [rounds]

Each round:
  1. Panel of 3 readers (lenses rotate by round) critiques the current draft
  2. A rewriter model revises the draft against the critiques
  3. A gatekeeper scores 1-10; rounds stop early if 3 consecutive >= 8
Outputs: essay revised in place; log at <essay>.iteration-log.md
"""
import json, os, re, subprocess, sys, time, concurrent.futures

def get_key():
    for line in open(os.path.expanduser('~/.bashrc')):
        m = re.match(r'^(?:export )?DEEPSEEK_API_KEY=["\']?([^"\'\s]+)', line.strip())
        if m: return m.group(1)
    raise SystemExit('no key')

# Lens rotation: each round gets 3 fresh perspectives. A dozen rounds, no repeat lens.
LENSES = [
    ("skeptic", "Does the argument hold? Weakest inference, metaphor doing the logic's job, one refutable claim."),
    ("line-editor", "Ruthless economy: repeat ideas, decorative metaphor, words that can go. Quote offenders."),
    ("cold-outsider", "Smart developer, no context. Where do you tune out? Did the core land in 3 paragraphs?"),
    ("poet", "Where does the prose sing and where is it flat? Which line deserves to be quoted? Which is trying too hard?"),
    ("adversary", "You want this essay to fail publicly. Write the cruelest fair critique: the take-down bullets."),
    ("architect", "Structural review: is each section load-bearing? What is missing between thesis and close? Reorder?"),
    ("rival-anthologist", "You compile a competing anthology. Why would you REJECT this piece? What would make it undeniable?"),
    ("teacher", "Could a bright 15-year-old follow this? Where does jargon or assumed context block understanding?"),
    ("engineer", "Is the mechanism precise? Vague verbs, hand-waved causality, claims that need a how?"),
    ("mythmaker", "Does the central image actually generate the essay's structure, or is it wallpaper? Test the metaphor at its edges."),
    ("ship-captain", "This org runs on boats and honest water. Where is the essay dishonest, sentimental, or not walking its own doctrine?"),
    ("final-editor", "Last pass before print: the three changes that matter most. Everything else is fine — prove it by saying less."),
]
REWRITER_MODEL = 'deepseek-chat'
READER_MODEL = 'deepseek-chat'
DEEP_MODEL = 'deepseek-reasoner'  # rounds 1, 6, 12 get the deep reader

def call(model, prompt, text, timeout=240):
    key = get_key()
    body = json.dumps({'model': model, 'messages': [{'role': 'user', 'content': f'{prompt}\n\n---\n{text}'}]})
    out = subprocess.run(['curl', '-s', '--max-time', str(timeout),
        'https://api.deepseek.com/chat/completions',
        '-H', f'Authorization: Bearer {key}', '-H', 'Content-Type: application/json',
        '-d', body], capture_output=True, text=True).stdout
    return json.loads(out)['choices'][0]['message']['content']

def run_round(draft, r):
    lens_start = (r - 1) * 3
    round_lenses = LENSES[lens_start:lens_start + 3]
    use_deep = r in (1, 6, 12)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
        futs = {ex.submit(call, DEEP_MODEL if (use_deep and i == 0) else READER_MODEL,
                          f'You are the {n} on a review panel. {p} Max 6 bullets, no praise, quote exact text.',
                          draft): n for i, (n, p) in enumerate(round_lenses)}
        crits = {n: f.result() for f, n in futs.items()}
    critique_text = '\n\n'.join(f'### {n}\n{c}' for n, c in crits.items())
    rewrite_prompt = ('You are the rewriter. Revise this essay against ALL critiques below. '
        'Keep ~700-900 words, keep the house voice (concrete, declarative, metaphor-as-compression), '
        'fix what the critics found, do not add new sections. Output ONLY the full revised essay in markdown.')
    gate_prompt = ('Score this essay 1-10 for publishable quality (argument + prose + economy). '
        'Output ONLY: <number> — <one line reason>.')
    revised = call(REWRITER_MODEL, rewrite_prompt + '\n\nCRITIQUES:\n' + critique_text, draft)
    gate = call(DEEP_MODEL, gate_prompt, revised)
    return revised, critique_text, gate, [n for n, _ in round_lenses]

def main():
    path = sys.argv[1]
    rounds = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    log = open(f'{os.path.splitext(path)[0]}.iteration-log.md', 'w')
    draft = open(path).read()
    scores, streak = [], 0
    for r in range(1, rounds + 1):
        t0 = time.time()
        revised, crits, gate, lens_names = run_round(draft, r)
        m = re.search(r'(\d+(?:\.\d+)?)', gate)
        score = float(m.group(1)) if m else 0
        scores.append(score)
        streak = streak + 1 if score >= 8 else 0
        log.write(f'\n## Round {r} — lenses: {", ".join(lens_names)} — gate: {gate.strip()}\n')
        log.write(crits + '\n')
        log.flush()
        print(f'round {r}: gate={gate.strip()} ({time.time()-t0:.0f}s)', flush=True)
        # only accept revisions that stay essay-length (guard against model truncation)
        if 400 < len(revised.split()) < 1400:
            draft = revised
            open(path, 'w').write(draft)
        if streak >= 3 and r >= 4:
            print(f'converged at round {r} (3 consecutive gates >= 8)', flush=True)
            break
    log.write(f'\n## Final: scores {scores}\n')
    print(f'done. final draft in {path}; scores: {scores}', flush=True)

if __name__ == '__main__':
    main()
