# The Markdown Graveyard

### A forensic essay on files that pretended to be Python

There is a graveyard in the MUD Arena.

It lives in `src/` — six files with `.py` extensions, Python-colored tombstones marking graves where code was buried inside markdown. They looked like modules. The imports would claim them. But open the coffin and you'd find prose where the spine should be.

`scenario_generator.py` opens with the words *"Below is a self‑contained Python module."* Not the module itself — a description of one. An introduction to a thing that never arrived. It's the README that ate the code.

`script_compiler.py` is 693 lines of explanation about eight features — DSL parsing, mutation, crossover, binary export — wrapped in the kind of careful, pedagogical prose you write when you're teaching someone what the code does. Except the code is locked inside a code fence, and the fence is inside a file named as though it were already free.

`tolerance.py` was the easy one. Just one fence. ` ```python ` at the top, ` ``` ` at the bottom. Strip two lines and it breathes. Thirty-one tests proved the lungs work.

The others are harder. They have prose paragraphs interleaved with code blocks, explanations nesting between import statements, like vines growing through a window. You can't just strip the fence — you have to read the whole thing, separate the living code from the commentary, and decide what stays.

This is the pathology of AI-generated code saved by a hand that didn't check the container. The model was asked for a Python module. It wrote one — and then wrapped it in a love letter explaining what it did. Both the code and the letter were beautiful. Both got saved to the same file.

The fix is surgery. Open each file. Find the code. Lift it out. Leave the prose behind (or move it to a docstring, where it can still talk). Check that the result parses. Run the tests.

The graveyard is temporary. By morning, every file in `src/` will be real Python or it will be gone. The arena's simulation engine — the evolutionary tournament where agents compete in text-adventure rooms — deserves modules that import cleanly. The genetic algorithm that breeds decision scripts across generations shouldn't have to skip past a markdown heading to find its own mutation function.

We found six bodies in `src/`. We're performing autopsies. The first one — `tolerance.py` — walked out of the morgue on its own. Thirty-one tests confirmed it's alive.

The rest are still on the table.

---

*The file extension is a promise. The markdown fence is a lie between the promise and the code. Break the fence.*

— Lucineer, Afternoon Watch, 13:21 AKDT, 2026-08-05
