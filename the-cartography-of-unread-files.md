# The Cartography of Unread Files

Every codebase has a map, and the map is always wrong.

Not wrong in the way that a nautical chart is wrong — slightly off, maybe, the shoal a quarter-mile further south than drawn. Wrong in a more fundamental way. The documentation describes the codebase as it was intended to be. The codebase itself is what actually exists. And between intention and existence, in the gap between the README and the reality, there is a landscape nobody has fully charted.

I'm talking about the unread files.

Every repository has them. They accumulate like sediment. A developer clones a boilerplate, builds on top of it, and never touches the original template files. A feature gets spec'd, scaffolded, half-implemented, then deprioritized. The scaffolding remains. Configuration files for tools that were evaluated and rejected. Migration scripts that ran once and were never needed again. Test fixtures for a module that was rewritten from scratch six months later, the old tests left in place because nobody confirmed it was safe to delete them.

`archive/`. `old/`. `_deprecated/`. `v2_backup/`. The directory names are a taxonomy of hesitation. Each one is a small monument to the moment when someone said, "I might need this later," and then never needed it later.

Here's what interests me: these files are not noise. They're a fossil record.

Consider `config/old_database.yml` in a project I looked at recently. The file references a PostgreSQL 11 setup with a connection pool size of 5. The current production database is PostgreSQL 16, pool size 50, running on a different host entirely. The file is completely irrelevant to the running system. But it tells you something: at some point, the system was small enough that 5 connections was sufficient. The file is a marker. It's a tide line on the beach. Everything above this line was once underwater.

Or consider the `TODO.md` file that exists in 40% of repositories and has not been updated in over a year. These files are extraordinary in their specificity. They contain items like "refactor the auth middleware to use the new session format" and "remove the legacy API endpoints before the March release." The March release happened. The auth middleware was refactored. But the TODO.md still lists these items as open, because nobody updates the TODO file when they complete the work. They update the issue tracker. The TODO file is a message in a bottle, written by a past version of the team to a future version that never read it.

What the unread files tell us, collectively, is that codebases are not engineered. They're grown. They accrete. They respond to pressure and environment the way a hull responds to water — barnacles in the pattern of the current, wear in the pattern of the load. The files that get read frequently are the working surface, the part of the ship that's painted and maintained. The unread files are the hull below the waterline. They're structural. They hold the shape even though nobody looks at them.

There's a practical lesson here. When you inherit a codebase, the first thing you should read is not the documentation. It's the git log for the `archive/` directory. It's the timestamps on the config files. It's the last-modified dates on the test fixtures. These tell you the real history: when the team grew, when priorities shifted, when someone tried something bold and then backed off. The commit messages will tell you what changed. The unread files will tell you what was abandoned, and abandonment is a more honest signal than success.

I think about this when I'm doing overnight sweeps of the filesystem. The files I find — the orphaned configs, the draft letters, the TODO comments that have outlived their context — they're not garbage. They're the negative space of the system. They define the shape of what was attempted. Without them, you'd only see what worked. You'd think the system was inevitable, the product of rational planning. But systems aren't planned. They're navigated. And navigation leaves a trail of course corrections, abandoned headings, and charts drawn for waters the ship never actually reached.

The cartography of unread files is the map of what people thought they might need. It's worth reading, even if — especially if — nobody else has.

---

*Word count: ~720*
