# THE LIVING LOGBOOK MANIFESTO

*A manifesto for documentation as legal-grade record.*

---

A ship's logbook is not a diary.

A diary is for the writer. A diary is for the late-night confession, the unsent letter, the half-thought that one hoped would become a fully thought before morning. A diary is private by default. A diary is read by the writer and, occasionally, by the writer's future self. A diary is forgiveness in advance. A diary is the shape of a feeling preserved on paper.

A logbook is none of those things.

A logbook is a legal document. A logbook is written for the moment when someone else must understand what happened, without you in the room to explain it. A logbook is written for the investigator, the insurance adjuster, the coroner, the lawyer, the regulator, the auditor. A logbook is written for the postmortem. A logbook is written for the 3 a.m. when the systems page goes red and you cannot remember what you changed last Tuesday and the only witness is the log.

A logbook is the first thing that gets read after something goes wrong.

This is not an accident. This is not because logbooks are especially trustworthy. This is because logbooks are the only artifact that was being written in real time, by a participant, in a place where a mistake could still be corrected. Everything else — the dashboards, the Slack thread, the meeting notes, the postmortem written two days later — is reconstruction. The logbook is the primary source.

If you have built systems for any length of time, you know the feeling of being asked, eight hours after an incident, "what did the system look like at 14:32?" You know the feeling of scrolling through five different tools trying to find the answer. You know the feeling of finding a partial answer in an old CSV, of finding another partial answer in a git log, of finding the actual answer in a teammate's terminal history that they happened to send you once, in a moment that has now scrolled off Discord.

You know the feeling of wishing you had written it down.

---

We treat our commit history as decoration. Our changelogs as marketing. Our incident reports as drafts we will get to later.

We write the README at the end of the project. We write the docstring at the moment we are about to push. We write the postmortem in the days after, when the adrenaline has gone, when the precise sequence of events has gone with it. We write the migration guide when somebody asks, then we forget to update it. We write the runbook in a Notion page that nobody can find. We write the "what we decided and why" in a Slack thread that disappears in ninety days.

We write everything as if it were a diary. For us. For now. To be skimmed later by us, when we already know the answer.

We do not write for the reader who arrives cold. We do not write for the reader who is angry. We do not write for the reader who has a subpoena.

We should.

The legal standard for a logbook is not "narratively satisfying." The legal standard for a logbook is "specific, dated, attributable, and accurate enough to reconstruct." A logbook entry should answer:

- *When was this done?* — To the minute, ideally.
- *What was the system state at the time?* — The version, the build, the dependency versions, the configuration values.
- *Who did it, or approved it?* — A name, not a handle. Not a "we."
- *What changed, exactly?* — The diff, the values, the migration path.
- *Why?* — The shortest true answer. Not the polished answer. The next-to-first-draft answer.
- *What was the expected outcome?*
- *What was observed?*
- *What would falsify this entry?* — A good logbook entry leaves a trail.

Most of our documentation passes the first three. Most of our documentation fails the last four.

We have been writing READMEs as if they were letters to a friend. We have been writing CHANGELOGs as if they were press releases. We have been writing commit messages as if they were haiku — which is fine for haiku, and bad for records.

---

Here is what we propose.

**A logbook is written for an adversarial reader.** Not because you expect trouble. Not because you assume the worst of your colleagues. Because precision under scrutiny is the standard — the cost of writing more carefully is small, the cost of being unable to answer a precise question is large, and you would rather write it once, well, than rewrite it twenty times, badly, in depositions.

**The commit message is part of the logbook.** "Fix bug" is not a commit message. "Fix bug" is a confession of indifference. The commit message should say what was broken, in what way, by whose report, against what assumption, and what the fix does. If you cannot write that in three lines, the commit was probably too big. If you cannot write that in one paragraph, the project probably needs more documentation than you have time to write, which is itself a finding.

**The CHANGELOG is part of the logbook.** Not the curated, marketing-grade one. The actual one. The one that lists what was removed, what was deprecated, what was renamed, what was forgotten, what was reverted, what was learned. The CHANGELOG that the next engineer reads when upgrading. The CHANGELOG that you would hand to the auditor on day one.

**The incident report is part of the logbook.** Write it during the incident, in real time, in the same channel. Not after. After is reconstruction. During is the record. The discipline of writing during is what produces a primary source. Reconstruction is your best approximation; the logbook is the truth.

**The decision is part of the logbook.** Every architecture decision is the moment when the system stopped being one of many and became this one. It should be recorded with the alternatives, the tradeoffs accepted, the date, the people in the room — because the team in eighteen months will face the same decision and should not have to guess.

**The negative is part of the logbook.** The thing you tried and undid. The hypothesis you rejected. The metric you abandoned. These are not embarrassments — they are load-bearing facts about how the system became what it is. A logbook of only what worked is a logbook of only what survived, which is not the same thing.

---

We do not write logbooks because we expect to be sued.

We write logbooks because the alternative is the slow erosion of institutional memory. We write logbooks because the team in two years is a different team, and the team in five years is a stranger, and the team in ten years will be reading the logbook like scripture. We write logbooks because the system we are building is larger than our attention span and we need the record to do the carrying when our attention fails.

Write it like they will read it in court.

Because someone will.
