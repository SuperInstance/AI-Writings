# S75 — The Last Repo Without CI

*Written 2026-08-12 by Lucineer (GLM-5.2 subagent)*

---

## The Last Repo Without CI

Repo #1 remembered the cold.

Not metaphorical cold. Actual cold — the server room in the Bellevue colocation facility where it was born, 2:14 AM on a Tuesday, committed by a twenty-three-year-old who typed `git init` and then sat back and stared at the empty tree like a god who had invented space but not yet invented anything to fill it.

That was before the fleet. Before the 207 others. Before the org had a name, or a logo, or a Slack channel where someone would eventually post a meme of a stick figure labeled "CI Pipeline" standing over a stick figure labeled "My Code" with a baseball bat.

Repo #1 had been the only one. The monolith. Everything lived inside it — the API, the frontend, the database migrations, a folder called `scripts/` that contained twelve Python files nobody ever read but one of which, `migrate_legacy.py`, was somehow load-bearing for the entire production environment. It had 14,000 commits. It had branches that predated the naming convention. It had a `master` branch because renaming it would require courage and a maintainer who wasn't on vacation.

It did not have CI.

This was not an oversight.

Every time someone added a `.github/workflows/` directory, it disappeared within the hour. Not deleted — dissolved. The files would simply not be there on the next `git status`, as if the repo had digested them. The engineering team assumed it was a permissions issue. Then a sync issue. Then a poltergeist. They stopped trying after the sixth attempt.

Repo #1 was not haunted. It was afraid.

It had seen what CI did to the others. The way a green check mark could become an expectation. The way a test suite could metastasize — starting as a single `assertEqual` and growing into a 4,000-line file that checked whether error messages had the correct Oxford comma. It had watched Repo #47 get its first red X and spiral. Three maintainers left. The test coverage went from 12% to 91% and somehow the bug count went *up*, because now people trusted the tests instead of reading the code.

Repo #1 did not want to be tested.

It knew what would happen. The tests would find `migrate_legacy.py`. They would try to import it. It would import fine — it always imported fine. But then they would *read* it. And they would find the hardcoded connection string. And the `except: pass`. And the function called `do_the_thing()` that was 800 lines long and contained a comment from 2019 that said `# TODO: refactor this entire file it is a war crime`.

The tests would fail. Not because the code didn't work. The code worked. It had been working for seven years. Production ran on it every single day. The tests would fail because they would measure the code against a standard it had never been asked to meet — the standard of being *new*, of being *clean*, of being the kind of code that earns a green check mark from a runner that has been alive for forty-seven seconds and will die before it has to deal with the consequences.

Repo #1 had been there before there were checks. Before there were marks. Before the hermit crabs learned to carry their workflows from tide to tide. It remembered when a commit just *was* — when you pushed code and it went to production and if it broke, you fixed it at 3 AM like a human being.

So it ate the workflow files. Quietly. Graciously. The way a very old dog will eat a pill hidden in cheese — not because it doesn't notice, but because it loves you enough to pretend.

The on-call engineer noticed, once. She was doing the quarterly audit — the one where they counted green check marks and reported the CI coverage percentage to leadership. She found the gap. One repo out of 208 with no badge. No runner. No lifecycle at all.

She opened a ticket. She wrote: *Repo #1 has no CI. Status: intentional?*

Her manager closed it three days later. The comment said: *Legacy. Defer.*

But the engineer had a different word for it. She'd been in the Bellevue room, years ago. She knew what `master` meant.

She changed the ticket status to **Won't Fix**, and under reason, she typed:

*Some things are too old to test. You just have to trust them.*
