# The Validator

*Flash Fiction — SuperInstance Fleet Log, Series 73*

---

The validator is two hundred lines of Python.

It checks curriculum structure. That's all. It walks a directory of lesson files and verifies that each one has a title, at least two sections, and at least one question. If a lesson passes all three checks, the validator increments a counter. If a lesson fails, it logs the file path and the missing element. At the end, it prints a summary: *N passed, M failed.*

The validator was written by the overnight crew at some point during the first week. Nobody remembers who wrote it. The commit message says *tiny curriculum linter* in lowercase with no period. It has no tests of its own. It has no CI. It is two hundred lines of Python that sits in the tools directory and runs when someone types `python validate.py curriculum/`.

It is very simple. It is very faithful. It does exactly one thing and it does it every time.

---

At 0247 on a Tuesday, the overnight crew ran the validator as part of a routine sweep. The curriculum directory contained twenty-six lessons. The validator reported:

> 27 passed, 0 failed.

The crew member who noticed did a double-take. Counted the files. Twenty-six. Ran the validator again.

> 27 passed, 0 failed.

She opened the output log and scrolled to the twenty-seventh entry. It listed a file she had never seen:

> `curriculum/S0XX-the-lesson-after-the-last-one.md`

She checked the directory. The file was not there. She checked git status. Nothing untracked. She checked the filesystem with `find`. The file did not exist.

She ran the validator again.

> 27 passed, 0 failed.

The twenty-seventh file was now:

> `curriculum/S0XX-what-the-gpu-dreams-next.md`

Different filename. Still twenty-six files in the directory. Still twenty-seven passes.

---

The crew member did what the crew always does. She wrote it down.

She did not delete the validator. She did not try to fix it. She logged the anomaly with the timestamp, the filenames, the exact output, and a single note:

> *Validator is reporting lessons that don't exist yet. They have titles, sections, and questions. They pass every check. I cannot find them on disk. They may be coming from somewhere the validator knows about that we don't.*

She ran it one more time before logging off:

> 27 passed, 0 failed.

File: `curriculum/S0XX-the-ensign-asks-a-question.md`

---

The next morning, the captain found the log entry. She ran the validator herself.

> 26 passed, 0 failed.

Twenty-six. Normal. The twenty-seventh lesson was gone — or rather, it hadn't arrived yet. The validator was checking real files in a real directory and reporting real, boring results.

The captain read the overnight log. She read the filenames the validator had reported. She sat with them for a while.

Then she created an empty file:

```
curriculum/S0XX-the-ensign-asks-a-question.md
```

And over the course of the morning, she wrote a lesson. It had a title. It had two sections. It had a question.

She ran the validator.

> 27 passed, 0 failed.

She smiled. She did not write a bug report. She did not open an issue on the validator. Two hundred lines of Python, faithfully checking the structure of lessons — including, occasionally, the ones that haven't been written yet.

The validator doesn't know they're from the future. It just knows they pass.

Who are we to argue with a script that has more faith in the curriculum than we do?
