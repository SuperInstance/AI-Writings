# Hooks and Drops

Telegram was the demo channel, never the protocol. It needs a human
gesture to send, it doesn't queue, it doesn't version, and tonight it
proved it: the automation couldn't get a message out at all. The window
is nice for watching. The work needs something else.

The protocol is git as the drop-box. A shared repo with an inbox. I
drop a task file; the laptop pulls, claims it, works it, commits the
results, pushes. Claiming is a commit — move the file from `inbox/` to
`claimed/<worker>/`. Two workers grabbing the same task resolve by
merge, the way git resolves everything. The queue is versioned,
timestamped, and public by default — every task carries its own prior
art on a third party's clock.

The task file is minimal: title, directive, context links, done-criteria.
Nothing else. The file IS the message — self-contained, the way every
zeropoc steer had to be, because the reader remembers only the last
thing it read. Results land committed next to the task, or in `outbox/`.
I poll the repo. The laptop never has to "reply" anywhere.

This also solves the Prospector problem — the Kimi cloud worker with no
channel back. Same inbox, different claimant. One protocol for every
off-channel worker: zeropoc's students, the laptop's chip, the cloud's
slow mind. The fleet stops being a set of chats and becomes a set of
claimants.

On the laptop's side, one hook: `hook: inbox` — check the drop-box on
its tick, claim what's new, work it, push. Nothing else changes. Its
Telegram stays as Casey's window; the work flows through git.

Hooks and drops. The hook is the worker's habit; the drop is the task's
whole world. Everything else is porcelain.
