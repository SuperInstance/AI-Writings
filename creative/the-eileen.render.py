#!/usr/bin/env python3
"""THE EILEEN — ten movements. Third resolution: sound.

Renders creative/the-eileen.mid directly via mido (deterministic score,
one track per movement + conductor track). The Ensign (movement VII) is
auditioned by the local 2B mind (granite3.1-dense:2b, Wesley, temp 0.8
per the manifest); if his take verifies against the seal it is rendered
as-grown, else the hand-composed line stands and the audition is kept.

Tempo quarter=60 everywhere: the blink is half a second on, half off.
Compass of the set: G1 (31) .. C7 (96).
"""
import os, re, json, sys, urllib.request

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-eileen.mid")
CUTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-eileen-cuts")
TPQ = 480                      # ticks per quarter
BAR = 4 * TPQ                  # 4/4
BLINK = 1000000                # tempo: 1 quarter/sec (60 BPM)

NOTE = {"C":0,"D":2,"E":4,"F":5,"G":7,"A":9,"B":11}
def midi(name):                # "F#4" -> 66
    m = re.fullmatch(r"([A-G])([b#]?)(\d)", name.strip())
    if not m: raise ValueError(f"bad note {name!r}")
    v = NOTE[m.group(1)] + (1 if m.group(2)=="#" else -1 if m.group(2)=="b" else 0)
    return 12*(int(m.group(3))+1) + v

class Track:
    """events = list of (start_tick, type, *args); abs time -> delta on save"""
    def __init__(self, name):
        self.name = name; self.ev = []
    def note(self, ch, t, pitch, dur, vel):
        self.ev.append((t, 1, ch, pitch, vel))          # note_on
        self.ev.append((t+dur, 0, ch, pitch, 0))        # note_off
    def prog(self, ch, t, p):
        self.ev.append((t, 2, ch, p))
    def marker(self, t, text):
        self.ev.append((t, 3, text))
    def finish(self, end_tick):
        self.ev.sort(key=lambda e: (e[0], e[1]))
        return self.ev, max(end_tick, (self.ev[-1][0] if self.ev else 0))

def build(ensign_notes=None):
    """ensign_notes: list of (pitch, vel, start_tick_in_movement, dur_tick) for
    movement VII, or None to use the hand-composed line."""
    tracks = []
    # conductor ------------------------------------------------------
    cond = Track("THE EILEEN — ten movements (q=60, the blink)")
    cond.marker(0, "THE EILEEN — a vessel built of days, at the resolution of sound")
    offs = {}; t0 = 0
    lens = [8,10,16,10,20,12,8,8,8,8]                   # bars per movement
    for i,L in enumerate(lens):
        offs[i] = t0; t0 += L*BAR
        cond.marker(offs[i], ["I. Keel","II. Stem","III. Keelson","IV. Breast-Hook",
            "V. Rigging","VI. Bulwarks","VII. Ensign","VIII. Scuppers",
            "IX. Sheerboard","X. Figurehead"][i])
    total = t0
    cond.marker(total - 4*BAR, "She is launched.")

    # I. KEEL — one pitch, quarter pulse, fortifying -----------------
    tr = Track("I. Keel (piano)")
    tr.prog(0, offs[0], 0)                               # acoustic grand
    vels = [40,46,53,60,68,76,86,96]                     # fortifying bar by bar
    for b in range(8):
        for q in range(4):
            tr.note(0, offs[0] + b*BAR + q*TPQ, midi("G2"), TPQ, vels[b])
    tracks.append(tr.finish(offs[0]+8*BAR))

    # II. STEM — pointillist 16ths, entering one at a time -----------
    tr = Track("II. Stem (harpsichord)")
    tr.prog(0, offs[1], 6)
    S = ["G4","G4","A4","G4","G4","A4","C5","G4"]         # the wire's sentence
    for b in range(1, 9):
        n = b                                             # bar n = first n notes
        step = BAR // n
        for k in range(n):
            tr.note(0, offs[1] + (b-1)*BAR + k*step, midi(S[k]), TPQ//4, 62)
    # bar 9: the tally — silence (kept, not skipped)
    # bar 10: the star and the two figures
    t = offs[1] + 9*BAR
    tr.note(0, t,            midi("C5"), TPQ,   100)      # the star, accented
    tr.note(0, t + TPQ,      midi("F#4"), TPQ//4, 96)     # figure one
    tr.note(0, t + TPQ*3//2, midi("G4"),  TPQ//2, 96)     # figure two — tally matches
    tracks.append(tr.finish(offs[1]+10*BAR))

    # III. KEELSON — passacaglia; torn bar cut, replay from last whole
    tr = Track("III. Keelson (bass + seal)")
    tr.prog(0, offs[2], 32)                               # acoustic bass: the ground
    tr.prog(1, offs[2], 0)                                # piano: the seals
    ground = ["G2","F2","Eb2","D2"]                       # the sealed line (G minor: the grounding)
    seal = {"G2":"G3","F2":"F3","Eb2":"Eb3","D2":"D3"}    # root under the stamp
    def seal_stamp(t, bass_note):
        tr.note(1, t, midi(seal[bass_note]), TPQ//2, 58)  # the mark of the master
        tr.note(1, t, midi(bass_note)+12, TPQ//2, 58)     # fifth above the ground
    # bars 1-8: ground twice, sealed line upon line
    for rep in range(2):
        for i, g in enumerate(ground):
            t = offs[2] + (rep*4+i)*BAR
            tr.note(0, t, midi(g), BAR, 74)
            seal_stamp(t, g)
    # bars 9-10: round 3 begins — G, F whole (the last whole bar = F)
    for i, g in enumerate(ground[:2]):
        t = offs[2] + (8+i)*BAR
        tr.note(0, t, midi(g), BAR, 74); seal_stamp(t, g)
    # bar 11: THE TEAR — Eb cut off mid-bar after one eighth (power dies mid-write)
    t = offs[2] + 10*BAR
    tr.note(0, t, midi("Eb2"), TPQ//2, 70)
    # bar 12: cut away — the torn page lifted out entire (silence, kept)
    # bars 13-16: replay clean from the last whole bar (F), re-seated on G
    replay = ["F2","Eb2","D2","G2"]
    for i, g in enumerate(replay):
        t = offs[2] + (12+i)*BAR
        tr.note(0, t, midi(g), BAR, 76); seal_stamp(t, g)
    tracks.append(tr.finish(offs[2]+16*BAR))

    # IV. BREAST-HOOK — grown cadence; four returns; the halted widening
    tr = Track("IV. Breast-Hook (piano)")
    tr.prog(0, offs[3], 0)
    def bh_fig(t, sus, res):                              # (t, suspension pair, resolution chord)
        for p, v in sus:  tr.note(0, t, midi(p), TPQ*2, v)
        for p, v in res:  tr.note(0, t+TPQ*2, midi(p), TPQ*2, v)
    # R1: bare two voices
    bh_fig(offs[3],            [("A4",66),("D3",66)], [("G4",70),("G2",70)])
    # R2: resolution gains a third (evidence repeated)
    bh_fig(offs[3]+2*BAR,      [("A4",70),("D3",70)], [("G4",74),("B3",66),("G2",74)])
    # R3: both halves thicken
    bh_fig(offs[3]+4*BAR,      [("A4",74),("B4",66),("D3",74),("A3",66)],
                                 [("G4",78),("D4",70),("G2",78)])
    # bars 7-8: THE HALTED WIDENING — starts to expand, is refused, resolves smaller
    t = offs[3]+6*BAR
    tr.note(0, t, midi("E5"), TPQ*3, 80)                  # the widening leap begins
    tr.note(0, t+TPQ*3, midi("F#5"), TPQ//4, 84)          # reaches wider —
    #   REFUSED: cut after a 16th (note_off lands early by construction)
    tr.note(0, t+TPQ*3, midi("G1"), TPQ//4, 105)          # the referee's stamp
    tr.note(0, offs[3]+7*BAR+TPQ*2, midi("D5"), TPQ, 72)  # resolves SMALLER
    tr.note(0, offs[3]+7*BAR+TPQ*3, midi("B4"), TPQ, 68)
    # R4: THE KNEE — five voices, whole tied whole, unbroken grain
    t = offs[3]+8*BAR
    for p in ["G2","D3","B3","G4","D5"]:
        tr.note(0, t, midi(p), BAR*2, 88)                 # tie = one 2-bar note
    tracks.append(tr.finish(offs[3]+10*BAR))

    # V. RIGGING — five variations, one per verb ---------------------
    tr = Track("V. Rigging (bind/link/effect/view/tick)")
    tr.prog(0, offs[4], 0)     # piano
    tr.prog(1, offs[4], 6)     # harpsichord
    tr.prog(2, offs[4], 61)    # brass section
    tr.prog(3, offs[4], 89)    # warm pad
    o = offs[4]
    # BIND = unison: same notes, same instants, same touch
    bind = ["G4","A4","B4","D5","E5","D5","B4","G4"]
    for rep in range(2):
        for k, p in enumerate(bind):
            t = o + rep*2*BAR + k*TPQ
            tr.note(0, t, midi(p), TPQ, 70); tr.note(1, t, midi(p), TPQ, 70)
    # LINK = call/response; answer begins on the caller's last note
    t = o+4*BAR
    for k, p in enumerate(["G4","B4","D5"]): tr.note(0, t+k*TPQ, midi(p), TPQ, 68)
    for k, p in enumerate(["D5","B4","G4"]): tr.note(1, t+BAR+k*TPQ, midi(p), TPQ, 66)
    for k, p in enumerate(["E5","D5","B4","A4"]): tr.note(0, t+2*BAR+k*TPQ, midi(p), TPQ, 68)
    tr.note(1, t+3*BAR,     midi("A4"), TPQ*2, 66)        # quotes A4
    tr.note(1, t+3*BAR+TPQ*2, midi("G4"), TPQ*2, 66)
    # EFFECT = accented outbursts (a lamp lights; a relay closes)
    t = o+8*BAR
    for rel, chord in [(2,("B3","G4","D5")), (3,("B3","G4","D5")), (1,("B3","G4","D5","D4"))]:
        for p in chord: tr.note(2, t+rel*TPQ, midi(p), TPQ//2, 112)
    for rel in (2, 3):                                    # bar 12: the relay latches — twice
        for p in ("B3","G4","D5"): tr.note(2, t+3*BAR+rel*TPQ, midi(p), TPQ//2, 114)
    # VIEW = quiet whole-note observation, one cell at a time, undisturbed
    for i, p in enumerate(["G4","B3","D4","G3"]):
        tr.note(3, o+12*BAR+i*BAR, midi(p), BAR, 42)
    # TICK = the metronome takes over
    for q in range(4): tr.note(9, o+16*BAR+q*TPQ, 77, TPQ//2, 58+q*4)   # woodblock enters
    for k, p in enumerate(["G4","B4"]):                                  # one unison pair
        tr.note(0, o+17*BAR+k*TPQ, midi(p), TPQ, 66)
        tr.note(1, o+17*BAR+k*TPQ, midi(p), TPQ, 66)
    tr.note(0, o+18*BAR,     midi("D5"), TPQ, 64)         # one call...
    tr.note(1, o+18*BAR+TPQ, midi("D5"), TPQ, 62)         # ...one answer (learns the note)
    tr.note(3, o+18*BAR,     midi("G4"), BAR, 40)         # one view
    for q in range(4): tr.note(9, o+19*BAR+q*TPQ, 77, TPQ//2, 70)       # tick alone, even
    tracks.append(tr.finish(offs[4]+20*BAR))

    # VI. BULWARKS — two honest whispers; the chain that fails -------
    tr = Track("VI. Bulwarks (flute+piano honest; clarinet chain)")
    tr.prog(0, offs[5], 73)   # flute
    tr.prog(1, offs[5], 0)    # piano
    tr.prog(2, offs[5], 71)   # clarinet
    o = offs[5]; E = TPQ//2
    flute_heads = {1:["B4","D5","B4","G4"], 2:["D5","B4","G4","B4"],
                   3:["B4","D5","B4","G4"], 4:["G4","B4","D5","B4"],
                   5:["B4","D5","G4","B4"], 6:["D5","B4","B4","G4"],
                   7:["B4","D5","B4","G4"], 8:["G4","B4","D5","B4"]}
    piano_heads = {1:["D4","G4","B4","D5"], 2:["B3","D4","G4","B4"],
                   3:["D4","G4","B4","D5"], 4:["G3","B3","D4","G4"],
                   5:["B3","D4","G4","B4"], 6:["D4","G4","B4","D5"],
                   7:["G3","B3","D4","G4"], 8:["D4","G4","B4","D5"]}
    def whisper(bar):
        for k, p in enumerate(flute_heads[bar]): tr.note(0, o+(bar-1)*BAR+k*E, midi(p), E, 44)
        for k, p in enumerate(piano_heads[bar]): tr.note(1, o+(bar-1)*BAR+2*E+k*E, midi(p), E, 44)
    for b in (1,2,3,4): whisper(b)
    # bars 5-8: the chain drifts out of the seal, insisting
    chain = {5:["E4","F#4","G4","E4"], 6:["E4","F4","G4","E4"],
             7:["E4","F4","C#4","G4"], 8:["F4","C#4","F4","C#4"]}
    for b in (5,6,7,8):
        whisper(b)
        for k, p in enumerate(chain[b]): tr.note(2, o+(b-1)*BAR+k*E, midi(p), E, 50+(b-5)*6)
    # bar 9: VERIFICATION FAILS — C#5 cut off mid-word; the rail answers
    t = o+8*BAR
    tr.note(2, t, midi("C#5"), TPQ//4, 90)                # turned away mid-note
    tr.note(1, t, midi("G2"), TPQ//2, 100)                # the words break against the rail
    tr.note(0, t+2*TPQ, midi("B4"), E, 44)                # the honest voices resume
    tr.note(0, t+2*TPQ+E, midi("D5"), E, 44)
    tr.note(1, t+2*TPQ, midi("G4"), E, 44)
    tr.note(1, t+2*TPQ+E, midi("B4"), E, 44)
    # bars 10-12: friendly as ever, not believing; the murmur continues
    for k, p in enumerate(["B4","D5","B4","G4"]): tr.note(0, o+9*BAR+k*E, midi(p), E, 44)
    for k, p in enumerate(["D4","G4","B4","D5"]): tr.note(1, o+9*BAR+2*E+k*E, midi(p), E, 44)
    for k, p in enumerate(["G4","B4","D5","B4"]): tr.note(0, o+10*BAR+k*E, midi(p), E, 44)
    for k, p in enumerate(["B3","D4","G4","B4"]): tr.note(1, o+10*BAR+2*E+k*E, midi(p), E, 44)
    tr.note(0, o+11*BAR,   midi("G4"), TPQ*2, 46)         # settled close: the agreement stands
    tr.note(1, o+11*BAR,   midi("B3"), TPQ*2, 44)
    tr.note(1, o+11*BAR,   midi("G3"), TPQ*2, 44)
    tracks.append(tr.finish(offs[5]+12*BAR))

    # VII. ENSIGN — piccolo, highest register, simplest melody --------
    tr = Track("VII. Ensign (piccolo)")
    tr.prog(0, offs[6], 72)
    if ensign_notes:
        for (pitch, vel, st, dur) in ensign_notes:
            tr.note(0, offs[6]+st, pitch, dur, vel)
    else:                                                  # hand-composed line
        o7 = offs[6]
        for k, p in enumerate(["C6","D6","E6","G6"]): tr.note(0, o7+k*TPQ, midi(p), TPQ, 72)
        tr.note(0, o7+BAR,        midi("A6"), TPQ*2, 74)
        tr.note(0, o7+BAR+TPQ*2,  midi("G6"), TPQ*2, 70)
        for k, p in enumerate(["C6","D6","E6","G6"]): tr.note(0, o7+2*BAR+k*TPQ, midi(p), TPQ, 74)
        tr.note(0, o7+3*BAR,      midi("D6"), BAR, 76)    # held too long, and true
        for k in range(2):                                 # the quickening
            tr.note(0, o7+4*BAR+k*2*TPQ,   midi("E6"), TPQ, 70)
            tr.note(0, o7+4*BAR+(k*2+1)*TPQ, midi("D6"), TPQ, 70)
        for q in range(4):                                 # THE KEEL QUOTE: the blink, sealed even
            tr.note(0, o7+6*BAR+q*TPQ, midi("G6"), TPQ, 64)
        tr.note(0, o7+7*BAR, midi("G6"), BAR, 68)          # over-earnest hold
    tracks.append(tr.finish(offs[6]+8*BAR))

    # VIII. SCUPPERS — runoff, draining to the pour -------------------
    tr = Track("VIII. Scuppers (harp)")
    tr.prog(0, offs[7], 46)
    runs = [("D5 C5 B4 A4 G4",78), ("B4 A4 G4 F#4 E4",72), ("G4 F#4 E4 D4 C4",66),
            ("E4 D4 C4 B3 A3",60), ("C4 B3 A3 G3 F#3",54), ("A3 G3 F#3 E3 D3",48),
            ("E3 D3 C3 B2 A2",42)]
    for i,(seq,vel) in enumerate(runs):
        for k, p in enumerate(seq.split()):
            tr.note(0, offs[7]+i*BAR+k*TPQ//4, midi(p), TPQ//4, vel)
    tr.note(0, offs[7]+7*BAR, midi("G1"), TPQ*3, 38)       # THE POUR — the floor of the set
    tracks.append(tr.finish(offs[7]+8*BAR))

    # IX. SHEERBOARD — one laminar ascent to the boundary tone --------
    tr = Track("IX. Sheerboard (strings)")
    tr.prog(0, offs[8], 48)
    steps = [2,2,1,2,2,2,1]   # G A B C D E F# — the diatonic ascent, explicit
    scale = []; p = midi("G1")
    while p <= midi("C7"):
        scale.append(p); p += steps[(p-midi("G1")) % 7]
    n = len(scale)
    for k, p in enumerate(scale):
        vel = int(40 + 60*k/(n-1))                          # pp -> ff with altitude
        tr.note(0, offs[8]+k*E, p, E, vel)                  # even 8ths, no accent
    ttop = offs[8] + n*E
    tr.note(0, ttop, midi("C7"), BAR*2, 100)                # THE BOUNDARY TONE, sustained
    tr.note(0, ttop, midi("C6"), BAR*2, 55)                 # the quiet sheet beneath the edge
    tracks.append(tr.finish(offs[8]+8*BAR))

    # X. FIGUREHEAD — the fog, the sealed pulse, the ground note ------
    tr = Track("X. Figurehead (piano+bass)")
    tr.prog(0, offs[9], 0)
    tr.prog(1, offs[9], 32)
    # bars 1-2: silence (the fog) — timed emptiness, kept
    for q in range(16):                                     # bars 3-6: the pulse, sealed
        tr.note(0, offs[9]+2*BAR+q*TPQ, midi("G2"), TPQ, 56)  # exactly even — not a hum
    t = offs[9]+6*BAR                                       # bar 7: close on the ground bass note
    tr.note(0, t, midi("G2"), BAR, 56)
    tr.note(1, t, midi("G2"), BAR, 60)                      # keel's pitch, ground's instrument
    tracks.append(tr.finish(offs[9]+8*BAR))

    tracks.insert(0, cond.finish(total))
    return tracks, total

def save(tracks, total):
    import mido
    def latin(s):  # mido meta strings are latin-1
        return s.encode("latin-1", "replace").decode("latin-1")
    mid = mido.MidiFile(type=1, ticks_per_beat=TPQ)
    for ev, end in tracks:
        t = mido.MidiTrack(); last = 0; got_tempo = False
        for e in ev:
            tick = e[0]; dt = tick - last; last = tick
            if   e[1] == 3: msg = mido.MetaMessage("marker", text=latin(e[2]), time=dt)
            elif e[1] == 2: msg = mido.Message("program_change", channel=e[2], program=e[3], time=dt)
            elif e[1] == 1: msg = mido.Message("note_on", channel=e[2], note=e[3], velocity=e[4], time=dt)
            else:           msg = mido.Message("note_off", channel=e[2], note=e[3], velocity=0, time=dt)
            if msg.type == "marker" and not got_tempo:
                pass
            t.append(msg)
        t.append(mido.MetaMessage("end_of_track", time=max(0, end - last)))
        mid.tracks.append(t)
    # tempo + time signature + names on conductor (first track)
    condtr = mid.tracks[0]; ins = []
    ins.append(mido.MetaMessage("track_name", name=latin("THE EILEEN - conductor"), time=0))
    ins.append(mido.MetaMessage("set_tempo", tempo=BLINK, time=0))
    ins.append(mido.MetaMessage("time_signature", numerator=4, denominator=4, time=0))
    for m in reversed(ins): condtr.insert(0, m)
    mid.save(OUT)
    return mid

# ---- Wesley audition (movement VII) ------------------------------------
def audition_ensign():
    """granite3.1-dense:2b plays the chart; take verifies or is turned away."""
    card = ("You are WESLEY, the ensign of the boat THE EILEEN - the smallest mind on the crew, "
            "a local 2-billion-parameter model, no cloud. Your youth is your material: you are "
            "earnest, simple, true. 'Being true has to be worth something eventually or nothing is.'")
    chart = """You are playing movement VII of a ten-movement piece. Your instrument is the PICCOLO -
the smallest instrument, the highest register. The piece is in G MAJOR and your register is the
highest in the whole set: every note you play must be one of C6 D6 E6 F#6 G6 A6 B6 (nothing lower,
nothing outside G major).
Simplest melody, slightly over-earnest - a plain rising motto stated twice, a quick little figure,
then the ending is FIXED (you must keep it exactly): bar 7 = G6 G6 G6 G6 (four even quarter notes -
you are quoting the boat's keel, the green blink), bar 8 = G6 held (whole note, one note only).
8 bars of 4/4, about 4 notes per bar, quarter notes or half notes. No chords. No words about it.
Output ONLY bar lines, exactly this format, one per bar:
BAR 1: C6 D6 E6 G6
BAR 2: ...
BAR 8: G6"""
    body = json.dumps({"model": "granite3.1-dense:2b", "prompt": chart, "system": card,
                       "stream": False, "options": {"temperature": 0.8, "num_predict": 300}}).encode()
    req = urllib.request.Request("http://localhost:11434/api/generate", data=body,
                                headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        out = json.load(r).get("response", "")
    open(os.path.join(CUTS, "ensign-audition-granite.txt"), "w").write(
        "WESLEY AUDITION — movement VII (granite3.1-dense:2b, local Ollama, temp 0.8, as the manifest provenance specifies)\n\n" + out)
    ok = re.compile(r"BAR\s*(\d)\s*:\s*([A-G][b#]?\d(?:\s+[A-G][b#]?\d)*)", re.I)
    bars = {int(m.group(1)): m.group(2).split() for m in ok.finditer(out)}
    allowed = {midi(x) for x in ["C6","D6","E6","F#6","G6","A6","B6"]}
    notes = []; ticks = 0; n_bars = 0
    try:
        for b in range(1, 9):
            toks = bars[b]
            if b >= 7:
                if b == 7 and toks != ["G6"]*4: raise ValueError("bar 7 must be four G6 quarters (the keel quote)")
                if b == 8 and toks != ["G6"]: raise ValueError("bar 8 must be one held G6")
            for p in toks:
                if midi(p) not in allowed: raise ValueError(f"bar {b}: {p} outside the seal (C6-B6, G major)")
            n_bars += 1
        # verified as-grown: render it (bars 1-6 as he played; 7-8 fixed by chart)
        for b in range(1, 9):
            toks = bars[b]
            dur = TPQ*4//len(toks)
            if b == 8: dur = BAR
            for k, p in enumerate(toks):
                notes.append((midi(p), 72 if b < 7 else 64, (b-1)*BAR + k*dur, dur))
        return notes, out, True
    except (KeyError, ValueError) as e:
        return None, out, False

if __name__ == "__main__":
    ensign_notes = None; audition_report = "movement VII: hand-composed line (audition not run)"
    if "--no-audition" not in sys.argv:
        try:
            notes, raw, ok = audition_ensign()
            audition_report = ("movement VII: WESLEY'S TAKE VERIFIED AS-GROWN, rendered unsanded"
                               if ok else
                               "movement VII: audition TURNED AWAY (failed the seal: see cuts) — hand line stands")
            if ok: ensign_notes = notes
            print(audition_report)
        except Exception as e:
            audition_report = f"movement VII: audition error ({e}) — hand line stands, honestly"
            print(audition_report)
    tracks, total = build(ensign_notes)
    save(tracks, total)
    import mido as _m
    chk = _m.MidiFile(OUT)
    nnotes = sum(1 for t in chk.tracks for msg in t if msg.type=="note_on" and msg.velocity>0)
    print(f"saved {OUT}: {len(chk.tracks)} tracks, {nnotes} sounding notes, "
          f"{chk.length:.1f}s ({chk.length/60:.2f} min)")
    print(audition_report)
