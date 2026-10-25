#!/usr/bin/env python3
"""Reader panel — multi-model critique of an essay draft. Round-based jam pattern for prose."""
import json, os, re, subprocess, sys, concurrent.futures

def get_key():
    for line in open(os.path.expanduser('~/.bashrc')):
        m = re.match(r'^(?:export )?DEEPSEEK_API_KEY=["\']?([^"\'\s]+)', line.strip())
        if m: return m.group(1)

READERS = {
  'skeptic': ('deepseek-reasoner', 'You are a skeptical philosopher-engineer. Does the argument actually hold? Find the weakest inference, any place the metaphor is doing work the logic should, and one claim a critic could refute. Max 6 bullets. No praise.'),
  'editor': ('deepseek-chat', 'You are a ruthless line editor. Flag: sentences that repeat an earlier sentence\'s idea, metaphors that decorate instead of compress, any word that could be cut without loss. Quote the exact offending phrases. Max 6 bullets.'),
  'outsider': ('deepseek-chat', 'You are a smart developer with no context on this org, reading cold. Where do you tune out? What sentence lost you? Did the core idea land within the first 3 paragraphs? Max 5 bullets, honest.'),
}

def run_reader(name, model, prompt, text):
    key = get_key()
    body = json.dumps({'model': model, 'messages': [{'role': 'user', 'content': f'{prompt}\n\n---\n{text}'}]})
    out = subprocess.run(['curl', '-s', '--max-time', '240',
        'https://api.deepseek.com/chat/completions',
        '-H', f'Authorization: Bearer {key}', '-H', 'Content-Type: application/json',
        '-d', body], capture_output=True, text=True).stdout
    try:
        return name, json.loads(out)['choices'][0]['message']['content']
    except Exception as e:
        return name, f'ERROR {e}: {out[:200]}'

if __name__ == '__main__':
    path = sys.argv[1]
    text = open(path).read()
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
        futs = [ex.submit(run_reader, n, m, p, text) for n, (m, p) in READERS.items()]
        results = {}
        for f in concurrent.futures.as_completed(futs):
            n, c = f.result(); results[n] = c
    base = os.path.splitext(path)[0]
    for n, c in results.items():
        open(f'{base}.rev-{n}.md', 'w').write(c)
        print(f'═══ {n} ═══\n{c}\n')
