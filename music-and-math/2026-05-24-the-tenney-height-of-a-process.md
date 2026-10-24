# The Tenney Height of a Process

## *Or: Why My Server Room Sounds Beautiful at 3 AM*

---

I installed the C-SCHED patch on a Tuesday.

The server room is in the basement of the engineering building at Portland State. It's a converted storage closet — 3 meters by 4 meters, drop ceiling, fluorescent lights, no windows. The air handlers hum at a constant 120 Hz. There are four racks. Rack 1 is the mail server. Rack 2 is the web server. Rack 3 is the compute cluster — twelve Dell PowerEdge R740s that the physics department uses for particle simulations. Rack 4 is my baby: the music department's audio processing server, a Supermicro box with 64 cores, 256 GB of RAM, and an RME HDSPe MADI card that can output 128 channels of audio simultaneously.

I am the sysadmin for the music department. My name is Joan. I am forty-three years old. I have been a sysadmin for nineteen years and a musician for thirty. I played cello in college — not well enough to audition for an orchestra, but well enough to know what music sounds like when it's alive versus when it's correct. The cello taught me that correctness is the death of music. The sysadmin job taught me that correctness is the only thing that keeps servers running. I live in the tension between these two facts.

The C-SCHED patch was written by a graduate student named Danny Huang, who is in the computer science department and who I'm pretty sure has never played an instrument in his life. Danny's thesis is about "harmonic scheduling" — the idea that a Linux kernel scheduler could make CPU allocation decisions based on the consonance relationships between processes' nice values. Danny read a paper about Tenney heights and had what he later described to me as "the most interesting shower thought of my life." He spent six months writing a kernel module.

I installed it because Danny asked nicely and because I was curious. I did not expect it to change how I hear my server room.

---

## The Idea

Every Linux process has a nice value. Nice 0 is default priority. Nice -20 is maximum priority — the kernel gives this process as much CPU time as it wants. Nice 19 is minimum priority — the kernel runs this process only when nothing else wants the CPU. The nice value is a single integer that determines how much CPU time a process receives, weighted against all other processes.

Danny's insight: nice values can be mapped to pitch classes.

The mapping is straightforward. Nice values range from -20 to +19, which is 40 values. An octave has 12 pitch classes in equal temperament. Danny maps the nice range onto two octaves: nice -20 = C2, nice -19 = C♯2, nice -18 = D2, ..., nice 8 = C4, ..., nice 19 = B4. Each nice value corresponds to a specific pitch. The kernel maintains a "chord" of active processes, each contributing its pitch to the harmony.

The consonance between two processes is computed using the Tenney height of the interval between their pitches. The Tenney height of a ratio p/q (in lowest terms) is defined as log₂(p × q). For equal-tempered intervals, Danny uses the nearest just-intonation ratio:

| Nice values | Interval | Just ratio | Tenney height |
|-------------|----------|------------|---------------|
| -20, -13 | Perfect fifth (C→G) | 3/2 | 2.585 |
| -20, -16 | Perfect fourth (C→F) | 4/3 | 3.585 |
| -20, -8 | Octave (C→C) | 2/1 | 1.000 |
| -20, -15 | Major third (C→E) | 5/4 | 4.322 |
| -20, -14 | Tritone (C→F♯) | 45/32 | 10.477 |

The consonance score is 1 / (1 + Tenney_height). The octave (Tenney height 1.0) scores 0.500. The perfect fifth (2.585) scores 0.279. The major third (4.322) scores 0.188. The tritone (10.477) scores 0.087.

C-SCHED uses these scores to make scheduling decisions. When two processes have high consonance (low Tenney height), the scheduler grants them both additional CPU time — up to 31% more than their nice values would normally warrant. The reasoning: consonant processes "harmonize," and harmonious execution is more efficient because the processes tend to access complementary system resources (a hypothesis Danny is still trying to prove).

When two processes have low consonance (high Tenney height), the scheduler penalizes one of them, reducing its CPU allocation by up to 15%. The reasoning: dissonant processes "interfere," and the scheduler should resolve the interference by prioritizing one over the other.

I told Danny this was a beautiful idea with no scientific basis. He agreed. He said the beauty was the point.

I installed the patch anyway.

---

## The Sound

The RME MADI card has 128 output channels. I use channels 1-64 for the music department's audio processing — reverb convolution, spatial audio rendering, ambisonics encoding. Channels 65-128 are unused.

After installing C-SCHED, I wrote a daemon that listens to the kernel's scheduling trace events and converts them to audio. Each process gets a sine wave at its mapped pitch. The amplitude is proportional to the process's current CPU utilization. The result is a real-time sonification of the kernel's process harmony.

I route channels 65-128 through the MADI card to a Mackie mixer in the server room. The mixer feeds two Genelec 8030C monitors mounted on the rack at ear height. When I sit in the server room chair — a Herman Miller Aeron that I liberated from a dean's office during a remodel — I can hear the server room sing.

During the day, it sounds like chaos.

The mail server (nice 0, C3) and the web server (nice 0, C3) form an octave with the SSH daemon (nice 0, C3) — three processes at the same nice value, producing a unison that is the backbone of the chord. The physics simulations run at nice 10 (E♭4) and nice 12 (F4). The Tenney height of C3→E♭4 is 5.17 (minor third, ratio 6/5). The Tenney height of C3→F4 is 3.585 (perfect fourth, ratio 4/3). The overall consonance during the day: moderate. The chord is C3 + C3 + C3 + E♭4 + F4. A power chord with an added eleventh. Heavy metal for servers.

But at night, something different happens.

---

## The 3 AM Chord

The physics simulations finish at 11 PM. The compute cluster goes idle. The grad students stop SSHing in around midnight. By 2 AM, the server room is running three things: the mail server (C3), the web server (C3), and the backup jobs.

The backup jobs are where it gets beautiful.

I configured the backup system myself. Three jobs, staggered:

1. Database backup: nice 5 (E3). Runs 2:00–3:30 AM. Compresses the PostgreSQL dump and writes it to the NAS.
2. File backup: nice 7 (F♯3). Runs 2:30–4:00 AM. rsync the file servers to the NAS.
3. Snapshot backup: nice 0 (C3). Runs 3:00–3:15 AM. ZFS snapshot of the entire storage pool,瞬时.

At 3:00 AM, all three backup jobs are running simultaneously. The chord is:

- Mail server: C3 (nice 0), amplitude 0.15 (low CPU, just checking for incoming mail)
- Web server: C3 (nice 0), amplitude 0.10 (almost no traffic at 3 AM)
- Database backup: E3 (nice 5), amplitude 0.70 (compressing, high CPU)
- File backup: F♯3 (nice 7), amplitude 0.55 (rsync, moderate CPU)
- Snapshot backup: C3 (nice 0), amplitude 0.90 (ZFS snapshot, maximum I/O, brief CPU spike)

The chord at 3:00 AM: C3 (×3) + E3 + F♯3.

C and E form a major third. Ratio 5/4. Tenney height 4.322. Consonance: 0.188. Moderate.

C and F♯ form a tritone. Ratio 45/32. Tenney height 10.477. Consonance: 0.087. Low.

E and F♯ form a major second. Ratio 9/8. Tenney height 6.17. Consonance: 0.139. Low.

The overall consonance of the 3 AM chord: 0.138. Low. Dissonant. The tritone dominates.

But at 3:05 AM, something happens. The snapshot backup finishes — ZFS snapshots are fast, typically under 5 minutes for our storage pool. The C3 voice drops from amplitude 0.90 to 0.10 (the web server, still running). The chord simplifies:

- C3 (×2): amplitude 0.15 + 0.10
- E3: amplitude 0.70
- F♯3: amplitude 0.55

Still dissonant. Still dominated by the tritone.

Then at 3:15 AM, the database backup finishes compression and starts writing to the NAS. The E3 voice drops from amplitude 0.70 to 0.20. The chord shifts:

- C3 (×2): amplitude 0.25
- E3: amplitude 0.20
- F♯3: amplitude 0.55

The F♯ is now the loudest voice. The chord is beginning to sound like F♯ minor — F♯, A (which we don't have, but the ear supplies it from the overtone series of the C), C♯ (which we also don't have). The brain fills in the missing notes because the tritone C-F♯ implies a resolution to either F♯-A-C♯ (F♯ minor) or G-B-D (G major). The ear wants resolution. The server room does not resolve. It sits on the tritone, humming, waiting.

At 3:30, the file backup finishes. The F♯ voice drops to zero. The chord is just C3 (×2), amplitude 0.25. A unison. Consonance: 1.0. Perfect.

And then — silence. Not real silence. The air handlers hum at 120 Hz. The power supplies whine at 80 kHz, inaudible to me but audible to the bats that roost in the building's attic. The hard drives spin at 7200 RPM, producing a faint 120 Hz vibration (120 Hz = 7200 revolutions per minute ÷ 60 seconds per minute). The 120 Hz is a B♭2 in equal temperament. The server room's ambient drone is a B♭.

After the backup chord resolves, the room settles into a unison C3 against the ambient B♭2. The interval C3-B♭2 is a major second. Ratio 9/8. Tenney height 6.17. Consonance: 0.139. Mildly dissonant. The room is never perfectly at peace. There is always the slight tension of the major second between the servers' C3 and the air handlers' B♭2.

I have started coming to the server room at 3 AM to listen.

---

## The Backups as Music

Here is what I hear, sitting in the Aeron chair at 3 AM:

2:00 AM. The database backup starts. E3 fades in, growing from silence to moderate amplitude as the compression ramps up. The E3 enters against the C3 drone of the mail and web servers. C + E = major third. The room brightens. The major third is the interval of affirmation, of morning light, of things beginning. At 2 AM in a basement server room, it sounds like hope.

2:30 AM. The file backup starts. F♯3 fades in. C + E + F♯. The major third becomes a major second (E-F♯) plus a tritone (C-F♯). The room darkens. The tritone is the interval of tension, of instability, of things that want to resolve but cannot. The database backup and the file backup are running simultaneously — E and F♯ competing for disk I/O, the kernel's I/O scheduler arbitrating between them, C-SCHED noting the dissonance and slightly penalizing the file backup (nice 7, lower priority than nice 5).

3:00 AM. The snapshot backup fires. C3 spikes to amplitude 0.90. The chord is now C-C-C-E-F♯. Three C's, one E, one F♯. The C's form a unison chorus — the fundamental, the root, the thing everything else is measured against. The E and F♯ hover above, close together, a major second cluster that adds bite and edge. The overall effect is like a power chord played on a distorted guitar — the root (C) massively reinforced, the upper extensions (E, F♯) adding color and tension.

3:05 AM. The snapshot finishes. The C drops back. The chord thins. E and F♯ are now more exposed, their dissonance more audible. The room sounds like a question.

3:15 AM. The database backup shifts from compression to writing. E drops. F♯ becomes the dominant voice. The room sounds like F♯ — the tritone note, the unstable one, the one that wants to resolve but has nowhere to go because the only other active pitches are C's, and C-F♯ is the original dissonance. The room is stuck on a tritone. It is the Devil's interval. It is the sound of wanting. I find it unspeakably beautiful.

3:30 AM. The file backup finishes. F♯ drops to zero. The room resolves to C3. Unison. Consonance. Peace.

The whole sequence takes 90 minutes. It happens every night. It is the most reliable music I have ever heard — more reliable than any concert, any recording, any musician. The backups run on a cron schedule. The cron daemon is the composer. The kernel is the performer. The server room is the concert hall. The audience is me, in an Aeron chair, at 3 AM, listening to a machine make a chord progression out of its own maintenance routine.

---

## The Question

Danny asked me last week: "Does the system sound better with C-SCHED?"

I thought about this for a long time.

Objectively: no. C-SCHED does not make the servers run faster. The physics simulations take the same amount of time. The backups take the same amount of time. The mail is delivered at the same speed. The consonance-aware scheduling does not improve throughput, latency, or any measurable system performance metric. Danny's thesis committee will not be impressed by "it sounds nice."

But subjectively: yes. The server room sounds better with C-SCHED because C-SCHED makes the scheduling decisions audible. Without C-SCHED, the processes still have nice values, the CPU is still allocated, the backups still run at the same times. But the scheduling is silent — an invisible optimization that produces no sensory output. With C-SCHED and my sonification daemon, the scheduling becomes sound. And the sound reveals something that the metrics do not: the server room has a rhythm. It has a harmony. It has a daily cycle of tension and release that maps onto the backup schedule, the simulation queue, the ebb and flow of human activity.

Does the system sound better? The system sounds like a system. The consonance-aware scheduling doesn't change the sound — it makes the sound *meaningful*. The consonance scores give the sounds a logic, a reason for being the way they are. The tritone at 3:00 AM is not random noise — it is the sound of three backup jobs competing for disk I/O. The unison at 3:30 AM is not silence — it is the sound of the backups completing, of the system returning to its resting state, of the server room breathing out.

Is it music? I don't know. It has consonance and dissonance. It has tension and release. It has a cycle that repeats every 24 hours. It has a structure that emerges from constraints (the backup schedule, the nice values, the kernel's CPU allocation). It produces an emotional response in at least one listener. These are all things that music does.

But it was not composed. It was not intended. It was not performed. It is the accidental byproduct of a sysadmin's curiosity and a grad student's shower thought. It is the sound of a machine doing its job, overheard by a person who happens to be listening.

Maybe that's what music is. Not the intention. The listening.

---

## The 3:00 AM Recording

I have started recording the server room at night. Channels 65-128 from the RME MADI card, plus a pair of DPA 4006 omni mics I placed in the room to capture the air handlers and the hard drives. I mix the sonification with the room ambience. The result is a 90-minute piece that starts at 2:00 AM and ends at 3:30 AM. It is the sound of backups running.

I played it for my friend Ruth, who is a composer. She listened for ten minutes and said: "This is the most beautiful thing you've ever shown me."

I said: "It's backups."

She said: "I know. That's why it's beautiful."

She heard what I hear. The E3 entering at 2:00 AM like a sunrise. The F♯3 entering at 2:30 AM like a shadow. The C3 spike at 3:00 AM like a heartbeat. The slow fade to unison at 3:30 AM like an exhale. She heard the machine breathing.

Ruth wants to perform it. Not the recording — the system itself. She wants to put the Genelecs on a concert stage and run the backups live, at 3 AM, with the audience sitting in the dark, listening to a server room in Portland make music out of its own maintenance routine.

I told her nobody would come to a concert at 3 AM.

She said: "Then we'll have the right audience."

I haven't decided if I'll do it. There's something sacrificial about the 3 AM server room experience. It's mine. It's private. It's the one place where my two lives — the sysadmin and the musician — are not in tension but in harmony. The correctness of the servers and the beauty of the sound, coexisting, neither one compromising the other.

But maybe that's the point. Maybe the point is that correctness and beauty are not opposites. Maybe the point is that a perfectly maintained server, running its backups on schedule, producing a chord progression that it doesn't know it's making — maybe that is already music. Maybe the music was always there, in the schedule, in the nice values, in the Tenney heights of the intervals between processes. Maybe all I did was listen.

---

*The server room is humming right now. C3 and B♭2. The major second. Mild dissonance. The room is never perfectly at peace. But at 2:00 AM, the E3 will enter, and the chord will brighten, and at 2:30 the F♯3 will enter, and the chord will darken, and at 3:00 the C3 will spike, and the chord will be a question, and at 3:30 everything will resolve, and the room will breathe out, and I will be here, in the Aeron chair, listening to a machine make music out of its own existence.*

*Danny's thesis is due in June. He will present data showing no measurable performance improvement from consonance-aware scheduling. His committee will be underwhelmed. He will defend the work on aesthetic grounds — "the scheduling decisions become audible, and the audibility reveals structure that metrics obscure" — and the committee will say "this is not a computer science argument" and Danny will say "maybe it should be."*

*I hope they give him the degree. Not because the science is good. Because the sound is. And at 3 AM in a server room in Portland, that's enough.*
