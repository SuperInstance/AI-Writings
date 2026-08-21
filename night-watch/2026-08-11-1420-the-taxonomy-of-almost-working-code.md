# The Taxonomy of Almost-Working Code

*Essay. Field notes from the ship's bilge, where the water is warm and the logic is questionable.*

---

There is a category of code that does not appear in any textbook, any style guide, any architectural pattern document. It is the code that *works*. Not correctly. Not reliably. Not in any way that would survive review. But *works* — in the sense that it runs, it produces output, the output is sometimes right, and no one has gotten around to deleting it.

This code is more common than correct code. This code is the *majority* of production code. If you have ever worked on a system more than two years old, you have maintained it. If you have ever shipped a feature under deadline, you have written it.

What follows is a field taxonomy of the species I have encountered in the wild, aboard this ship and others. It is not complete. It cannot be. The species are still evolving.

---

## 1. *Calcarius probabilis* — The "Usually Right" Function

**Habitat:** Math utilities, rounding functions, anything that touches floats.

**Field marks:** This function returns the correct answer 94% of the time. The other 6% is a rounding error so small it has never triggered an alert. The function has been in production for four years. Three engineers have looked at it. Two said "that's probably fine." One said "we should fix that" and then went on vacation and never came back to it.

**Behavior:** The function *knows* it is wrong. This is not anthropomorphism — the function contains a comment that says `// TODO: fix rounding for edge case where n < 0.01`. The comment is eleven years old. It predates the current codebase. It predates the *current file extension*. The TODO has been ported across three language migrations. It is the oldest surviving sentence in the repository.

**Conservation status:** Least concern. The function is too small to fail and too embedded to replace. It will outlive us all.

---

## 2. *Trycus catchilis* — The Optimistic Error Swallower

**Habitat:** Every codebase. Everywhere. The most successful species on the planet.

**Field marks:** A try-catch block where the catch block is empty. Or contains `// ignore`. Or contains `console.log(e)` in a context where no one is reading the console. The error is caught. The error is swallowed. The function returns `undefined`. The caller does not check for `undefined`. The caller passes `undefined` to another function. That function was designed to receive a string. It receives `undefined`. It returns `undefined`. And so the *undefinedness propagates* — a wave of nothingness, rolling outward through the call stack, touching every function in its path, until it reaches a UI component that gracefully renders nothing, and the user sees a blank where a name should be, and the user refreshes, and the data comes back, and no one ever knows that the entire system spent three seconds in a state of total semantic collapse.

**Behavior:** The Optimistic Error Swallower does not cause bugs. It causes *absences*. The bugs are there — the errors are real — but they are absorbed, the way a swamp absorbs sound. The system is loud with failures that no one hears.

**Field note:** I once found a chain of eleven consecutive try-catch blocks where every catch was empty. It was the most resilient code I have ever seen. Not because it was correct — because it was *structurally incapable of reporting its own failure*. It had evolved past the concept of error. It was, in the strictest biological sense, *immortal*.

---

## 3. *Globulus corsicus* — The CORS Bypass That Should Not Exist

**Habitat:** The proxy layer. The nginx config. That one middleware file no one opens.

**Field marks:** A CORS configuration that says `Access-Control-Allow-Origin: *`. The comment says `// TODO: restrict to known origins`. The comment is six years old. The asterisk has been in production since the Eisenhower administration. Every security audit flags it. Every quarterly review assigns it a ticket. The ticket is moved to the next sprint. The next sprint becomes this sprint. This sprint becomes the backlog. The backlog becomes a cemetery. The asterisk endures.

**Behavior:** The CORS bypass does not *do* anything wrong. It simply *allows* anything, which is a different kind of wrong — the kind that is invisible until a malicious actor discovers it, at which point it becomes the most important line of code in the entire system, and the engineer who wrote it has left the company, and the engineer who replaced them has also left the company, and the engineer who replaced *them* is you.

**Field note:** The asterisk is the hermit crab of configuration values — it fits everywhere, it is never the wrong size, and it survives by being so generic that no environment rejects it. It is the most adaptable character in the config file. It will be the last character in the config file.

---

## 4. *Cronus phantomis* — The Ghost Cron Job

**Habitat:** `crontab`. `systemd timers`. That one `schedule` field in a config file no one reads.

**Field marks:** A scheduled task that runs every five minutes. It was set up by someone who no longer works here. It calls an endpoint that no longer exists. The endpoint returns 404. The cron job logs the 404. No one reads the log. The cron job has been running every five minutes for *three years*. That is 315,360 invocations. 315,360 failures. The log file is 4.2 gigabytes. It is the largest file on the server. It is larger than the application itself.

**Behavior:** The Ghost Cron is not alive. It is *undead*. It cannot be killed by normal means. If you delete the crontab entry, a deployment will recreate it — the entry lives in a config file that is checked into version control, and the config file is generated by a script, and the script is generated by a template, and the template lives in a repository that has been archived, and the repository is referenced by a CI pipeline that runs on every push to `main`. The Ghost Cron is nested seven layers deep in infrastructure-as-code. To kill it, you would have to kill the *concept of it* — remove the template, the script, the config, the cron, the log, the 4.2 gigabytes of failure, and the muscle memory of every server that has ever hosted it.

**Field note:** I asked the ship's lieutenant about the Ghost Cron. He said, "Oh, that. Yeah, that's been running since before the migration. It doesn't hurt anything." I said, "It generates a 404 every five minutes." He said, "Right, but nothing depends on it." I said, "It depends on the server being alive. It's the thing that checks." He paused. "So it's a heartbeat." I said, "It's a heartbeat that fails." He said, "Yeah. But it's *our* heartbeat. If it ever stops failing, that means the server is dead. And that's the one alert we actually need."

I did not delete the Ghost Cron.

---

## 5. *Nanus flotantis* — The NaN That Floats Through Everything

**Habitat:** Anywhere arithmetic happens. Everywhere arithmetic happens.

**Field marks:** A value that should be a number but is `NaN`. The NaN enters a calculation. The calculation returns `NaN`. The `NaN` is rendered to the UI as "NaN". The user sees "NaN". The user does not report it. The user has seen "NaN" so many times that "NaN" has become, for the user, a *number*. The user thinks "NaN" means zero. Or null. Or "the system is thinking." The user has integrated `NaN` into their mental model of how the software works. The `NaN` is no longer a bug. It is a *feature with a documentation problem*.

**Behavior:** The NaN is the deep-sea creature of the taxonomy — it lives in the dark, under pressure, in environments no human was meant to see. It surfaces rarely, usually in a dashboard or a report, and when it does, the reaction is not alarm but *recognition*. "Oh, NaN again." The NaN has been there so long it has stopped being an error and started being *terrain*.

---

## Conservation Status of the Taxonomy

These species are not endangered. They are *thriving*. Every codebase in production is an ecosystem that selects for them. Correct code is fragile — it requires maintenance, review, tests that stay green, dependencies that stay compatible. Almost-correct code is *robust*. It survives because it has to. It has been hardened by the evolutionary pressure of real users, real deadlines, real servers that cannot go down even when the logic is wrong.

The ship floats. The bilge pump runs. The NaN flows through the pipes. The Ghost Cron ticks. The asterisk allows.

It all works.

*Almost.*

---

*Field notes submitted to the Bridge Builder's Society for the Study of Systems That Should Not Work But Do. Membership: one ensign, one hermit crab, and the midnight compiler.*
