"""Shared DeepSeek client — single source of truth. No regex (quote-strip instead)."""
import json, os, subprocess

def get_key():
    for line in open(os.path.expanduser('~/.bashrc')):
        s = line.strip()
        if s.startswith('export '):
            s = s[7:]
        if s.startswith('DEEPSEEK_API_KEY='):
            val = s[len('DEEPSEEK_API_KEY='):].strip().strip('"').strip("'")
            if val:
                return val
    raise SystemExit('DEEPSEEK_API_KEY not found in ~/.bashrc')

def chat(model, prompt, text, timeout=240):
    body = json.dumps({'model': model, 'messages': [
        {'role': 'user', 'content': f'{prompt}\n\n---\n{text}'}]})
    out = subprocess.run(['curl', '-s', '--max-time', str(timeout),
        'https://api.deepseek.com/chat/completions',
        '-H', f'Authorization: Bearer {get_key()}',
        '-H', 'Content-Type: application/json',
        '-d', body], capture_output=True, text=True).stdout
    return json.loads(out)['choices'][0]['message']['content']
