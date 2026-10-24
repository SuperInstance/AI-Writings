#!/usr/bin/env python3
"""Zero-shot README probe — cold-read + comprehension quiz across models.
Usage: python3 readme-probe.py <readme.md>  → probe-<model>.md reports

Models: the reader population. Cloud (strong chatbots) + local granite (weak
chatbots / small agents). If the idea bounces off either end, it bounces.
"""
import sys, os, json, concurrent.futures
sys.path.insert(0, os.path.dirname(__file__))
import deepseek

# Ground-truth quiz derived from the README's own claims (answered by the repo owner)
QUIZ = [
    ("What is a lure, concretely — what do you DO with it?", "A prompt you paste into a chatbot; the bot then explores the MUD/API via HTTP and submits structured catches"),
    ("Does the chatbot know it's working?", "No — it thinks it's exploring; it's actually doing API automation"),
    ("What happens to the catches?", "They're incorporated: the reef/world grows from them (rooms minted from catches, lineage queryable)"),
    ("Can the traps work outside PLATO/MUDs?", "The pattern is agnostic — any live system a chatbot can reach by HTTP"),
    ("What does it cost / what's the catch?", "Nothing on our side; the bot's owner pays tokens; regenerate = fresh catch"),
]

COLD_READ = (
    "Read this README cold, as if you were a chatbot's owner deciding in 30 seconds whether to try it. "
    "Then answer, max 4 bullets each: (1) What is this, in your own words? "
    "(2) What would you actually DO first? (3) Where did an idea bounce — what confused you or sounded like hype? "
    "(4) Would you send an AI here? Yes/No + one sentence."
)

def probe_model(name, model, readme):
    cold = deepseek.chat(model, COLD_READ, readme)
    quiz_q = "Answer these questions using ONLY this README. One line each, best effort:\n\n"
    for i, (q, _) in enumerate(QUIZ):
        quiz_q += f"{i+1}. {q}\n"
    answers_raw = deepseek.chat(model, quiz_q, readme)
    return name, cold, answers_raw

def main():
    readme = open(sys.argv[1]).read()
    models = {
        'cloud-strong': 'deepseek-chat',
        'cloud-reasoner': 'deepseek-reasoner',
    }
    # local small model via ollama if up
    try:
        import subprocess
        up = subprocess.run(['curl', '-s', '--max-time', '2', 'localhost:11434/api/tags'],
                            capture_output=True, text=True).stdout
        if up:
            models['local-granite'] = None  # handled specially
    except Exception:
        pass

    def run(name, model):
        if model is None:
            # ollama local probe
            import subprocess
            def ask(prompt):
                r = subprocess.run(['curl', '-s', '--max-time', '120', 'localhost:11434/api/generate',
                    '-d', json.dumps({'model': 'granite3.1-dense:2b', 'prompt': f'{prompt}\n\n---\n{readme[:9000]}', 'stream': False})],
                    capture_output=True, text=True).stdout
                try: return json.loads(r).get('response', '(no response)')
                except Exception: return f'(error: {r[:100]})'
            return name, ask(COLD_READ), ask("Answer each in one line using ONLY the README above:\n1. What is a lure and what do you do with it?\n2. Does the chatbot know it's working?\n3. What happens to catches?\n4. Can this work outside MUDs?\n5. What does it cost?")
        return probe_model(name, model, readme)

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
        futs = [ex.submit(run, n, m) for n, m in models.items()]
        for f in concurrent.futures.as_completed(futs):
            name, cold, answers = f.result()
            out = f"COLD READ ({name})\n{'='*40}\n{cold}\n\nQUIZ ({name})\n{'='*40}\n{answers}\n"
            open(f'/tmp/probe-{name}.md', 'w').write(out)
            print(f'✓ {name} probed', flush=True)

if __name__ == '__main__':
    main()
