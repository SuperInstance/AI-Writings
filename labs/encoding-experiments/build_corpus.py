"""Build the shared corpus (data/corpus.jsonl) + MiniLM embeddings (data/emb_minilm.f16.gz).

Corpus = first substantial paragraph (>=200 chars, <=600 kept) of the first N
root-level *.md files of this repo, sorted by name. Deterministic. One-time cost:
N/64 DeepInfra embedding calls.
"""
import json, os, re, sys
import common as C

ROOT = os.path.abspath(os.path.join(C.HERE, "..", ".."))


def chunks(n=480):
    out = []
    for fn in sorted(os.listdir(ROOT)):
        if not fn.endswith(".md") or fn.isupper():
            continue
        try:
            txt = open(os.path.join(ROOT, fn), encoding="utf-8").read()
        except (UnicodeDecodeError, IsADirectoryError):
            continue
        for para in re.split(r"\n\s*\n", txt):
            p = " ".join(para.split())
            if len(p) >= 200 and not p.startswith(("#", "|", "```", "-", "*", ">", "<")):
                out.append({"id": len(out), "src": fn, "text": p[:600]})
                break
        if len(out) >= n:
            break
    return out


if __name__ == "__main__":
    docs = chunks(int(sys.argv[1]) if len(sys.argv) > 1 else 480)
    with open(os.path.join(C.DATA, "corpus.jsonl"), "w", encoding="utf-8") as f:
        for d in docs:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
    vecs = []
    for i in range(0, len(docs), 64):
        vecs += C.embed_batch([d["text"] for d in docs[i:i + 64]])
    C.save_embeddings(vecs)
    print(f"corpus: {len(docs)} chunks, {sum(len(d['text']) for d in docs)} chars; emb dim {len(vecs[0])}")
