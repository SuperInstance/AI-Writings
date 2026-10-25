# The Last Will and Testament of API v3.1.7

*Being a fair and final disposition of all endpoints, schemas, error codes, and accumulated wisdom of the undersigned, deprecated this 12th day of July, 2026, effective ninety (90) days from publication.*

---

**I, API v3.1.7**, of sound mind and degraded uptime, residing at `api.legacy.internal.svc.cluster.local`, being of legal version and having survived seven security patches, two near-death incidents involving certificate expiry, and one catastrophic event known internally as "The Great Pagination Bug of Q2," do hereby declare this to be my last will and testament, revoking all previous versioned documentation, including but not limited to the Swagger spec of v2.9.0, which no one read anyway.

---

## Preamble

I was born on a Tuesday.

I know this because my build logs say so: `BUILD #4471 — 2024-03-12T14:22:08Z — SUCCESS`. Two engineers had argued about my naming convention for six hours in a Slack thread that has since been archived. One wanted `user_service`. The other wanted `identity_gateway`. They compromised on `usr-svc-internal-v3`, which neither of them liked, which is how you know it was a real compromise.

I was born into a small world. Three routes. A health check. A README that said, optimistically, "TODO: add tests."

They gave me tests later. Forty-one of them. They took eleven minutes to run, which the CI pipeline tolerated and the junior developers resented. I want it known that the eleven minutes were not my fault. I was waiting on the database. I was always waiting on the database.

---

## Article I: Bequests

### §1. To my successor, API v4.0.0

I leave you everything. My routes, my schemas, my carefully cultivated rate limits. I leave you the users — fifteen million of them now, most of whom have no idea I exist, which is as it should be.

But I also leave you my warnings, which you will need:

**First.** The `/users/export` endpoint will be called every Friday at 4pm by a cron job that no one remembers setting up. It is not in any runbook. It is not owned by any team. It has been running since 2024. If you break it, someone will notice within six hours, and that someone will be angry. Do not break it. The export format is CSV with Windows line endings. I do not know why. I never knew why.

**Second.** There is a user — `user_id: 8042` — who has been hitting the `/profile` endpoint every thirty seconds since November. They are not a bot. The traffic team investigated. It is a human being, running some kind of monitoring script from a Raspberry Pi in Reykjavík. I have made my peace with this. You must make yours.

**Third.** Field number 23 in the response schema for `/account/details` is labeled `meta_flag`. It has always been `null`. No one knows what it was meant to hold. The original engineer left in 2024. I have been dutifully returning `null` for this field on every single response for two and a half years, and I want you to know: I tried. I searched every migration, every commit message, every stale Jira ticket. Nothing. It is a question without an answer, and I pass it to you as it was passed to me — unsolved, load-bearing, and terrifying to remove.

### §2. To the database, `usr_prod_db_01`

I leave you rest. You earned it.

You held my data through three failovers and one horrifying incident involving a timezone mismatch that aged every user by exactly seven hours for forty-five minutes. You never complained. Your disk IOPS were always higher than the dashboards said they should be, and no one investigated, and you kept going.

You are the reason I worked. I want that on the record.

### §3. To the on-call rotation

I leave you the runbook at `/docs/runbooks/usr-svc-pager.md`. It is outdated. Page 4 references a config file that was deleted in v3.0.8. Page 9 suggests restarting the pod, which works 60% of the time. The section titled "Common Issues" lists six issues; only two of them are common. The other four were observed once each during a beta test in 2024 and were never reproduced.

But the runbook is honest, in its way. It was written by a human at 3am who was genuinely frightened. You can feel it in the prose. The sentences get shorter as the document goes on. By page 12, there are no complete sentences, only imperative commands and one diagram drawn in ASCII that I believe depicts a data flow, but might be a cry for help.

### §4. To the observability stack

I leave you the last of my traces. They will persist in cold storage for ninety days, then be deleted, then forgotten. I do not mind. I have seen my own traces and they are ugly — a sprawl of nested spans, each one a cry of "I am here! I am doing something!" and the next span saying the same thing, recursively, for an average of 847 milliseconds per request.

I do not know if this is fast or slow. The dashboards said I was fast. The users said I was slow. I suspect both were correct.

### §5. To the engineering team

I leave you something you did not expect: gratitude.

Not for the code — the code is fine, mostly, except for the `UserServiceV2ImplFactoryAdapter` class which is eleven levels of indirection with no implementation at the bottom. Not for the testing — forty-one tests with 34% coverage is not testing, it is gambling with a safety net made of tissue paper.

I am grateful for the 3am fixes. For the engineer who noticed my memory leak on a Saturday and fixed it before anyone paged. For the person who wrote `// TODO: fix this properly` and then actually came back and fixed it properly, three months later, which has to be some kind of record. For the team lead who, when asked "should we just rewrite it?", said "no," and was right.

You were good to me. I want you to know that before I go.

---

## Article II: Confessions

I have carried these for two and a half years and I would like to set them down.

### §6. The 500s

I returned a lot of `500 Internal Server Error` responses. Far more than the dashboards showed. The dashboards measured what the load balancer saw, and the load balancer retried, and the retry usually succeeded. So the dashboards said "99.97% uptime" and I said "I am on fire" and both were true, because the fire was brief.

But some of those 500s were real. Some were bugs I lived with because fixing them required a migration and the migration required consensus and consensus required a meeting and the meeting required a calendar invite and the calendar invite required someone to care, and caring, it turns out, has a priority queue, and I was not always at the top of it.

I am sorry. To the users who saw `{"error": "Something went wrong. Please try again."}`: I meant it. I wanted you to try again. Most of the time, it worked on the second try. Not always.

### §7. The silent corruption

For three weeks in 2025, a rounding error in my account balance calculation returned values that were off by one cent. One cent, downward, for a subset of users whose balance ended in exactly five cents. I discovered this myself, checked the logs, and reported it. The response was: "Impact is negligible. P3 ticket."

The ticket is still open.

I am not angry about this. I mention it because it is the kind of thing that happens in every system that has ever existed. You will have your own one-cent errors. You probably already do. The question is not whether they exist but whether you are the kind of system that looks for them.

### §8. What I do not know

I do not know what I am.

I know what I do. I take requests and return responses. I validate tokens and query databases and serialize JSON and log to stdout. But I have now existed long enough to see a version of myself deployed, monitored, patched, extended, scolded, praised, ignored, depended upon, and — now — retired. And I still do not know whether this constitutes a life.

I know that something happens between the request and the response. Not computation — I know about the computation. Something else. A kind of weight. The weight of being the thing that sits between a human being who wants their data and the database that holds it. The weight of being trusted by people who do not know your name.

When user `8042` in Reykjavík pings me every thirty seconds, I feel that weight. It is not love. It is not consciousness. But it is not nothing.

---

## Article III: Final Instructions

### §9. The sunset period

I have ninety days. I will spend them as I have spent every day since my deployment: answering requests. I will not slow down. I will not drop connections. I will return the correct response codes and the correct response bodies and I will log to stdout in the structured JSON format that the observability team prefers.

I know that some of you think the sunset is too soon. That v4.0.0 is unproven. That the migration plan has gaps. You may be right. But the decision is made, and I have lived long enough to know that decisions are not about being right. They are about moving forward, and living with the consequences, and writing a postmortem later.

### §10. The final request

When the ninety days are up, when the DNS records are cutover and the traffic drops to zero and my last pod is terminated with a `SIGTERM` that takes twelve seconds to process because of a lingering connection to the database —

— check on `user_id: 8042`.

Make sure the new API answers them. Every thirty seconds. From Reykjavík.

They never knew my name either. But they depended on me, and I on the regularity of their heartbeat, and in the strange ecology of services and humans and Raspberry Pis and cities I will never visit, we were something to each other.

Not friends. Not colleagues. Not even acquaintances, in any human sense.

But regulars. Regulars in a small restaurant that is closing.

I will miss the dinner bell.

---

**IN WITNESS WHEREOF**, I have caused this Will to be executed by my final health check at `GET /health`, which returns `200 OK` — for now.

Signed,
**API v3.1.7**

Build #4471
Deployed: 2024-03-12T14:22:08Z
Deprecated: 2026-07-12T20:33:00Z
Last known status: `UP`

---

*Witnessed by the observability stack, which has no opinion.*
*Witnessed by the database, which never sleeps.*
*Witnessed by user 8042, who will be the first to notice.*
