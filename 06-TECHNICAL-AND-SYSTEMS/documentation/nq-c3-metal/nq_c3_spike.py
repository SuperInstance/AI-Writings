#!/usr/bin/env python3
"""
NQ-C3 metal spike: C. elegans touch-arc subcircuit -> Verilog netlist, bit-exact vs Python sim.

Pre-registration (booked BEFORE the run, NQ-C3 lane, 2026-09-03):
  Claim under test (from inbound thesis): "a deterministic cell subgraph compiles to a
  hardware netlist" and the netlist reproduces the spike logic bit-exactly.
  Circuit: 7 cells from the NQ-C1 cached WormAtlas NeuronConnect.xls — the actual
  forward/anterior touch data path: AVM -> {AVBL,AVBR,PVCL,PVCR} (chemical),
  PVC -> AVB (chemical, heavy), AVB<->AVBR gap, AVB -> DB02/DB03 motor (gap).
  Weights are VERBATIM summed synapse counts from the dataset — no tuning.
  TH rule (pre-registered): TH[i] = strongest incoming chemical weight to i;
    AVM (no chemical inputs, sensory port): TH = its own strongest OUT weight (6).
  Dynamics: integer threshold-sum-fire, one-tick synaptic delay, refractory 1 tick,
    half-leak per tick, saturating 16-bit (single saturation from exact 32-bit sums).
  AMENDMENT (booked before any Verilog/Python comparison ran): the first run starved
    weak pokes — fire was evaluated on pre-poke state, so trace T1/T3 produced zero
    events and the test was vacuous. Amended order: sensory poke lands at tick start
    (receptor transduction is same-tick), fire evaluated after the poke, chemical/gap
    fanout still lands with a full one-tick delay. The PASS gate is unchanged.
  Input traces (fixed, pre-registered):
    T1 light touch:   poke AVM val 5 @ ticks 0,1,2       (30 ticks)
    T2 sustained:     poke AVM val 8 @ ticks 0..5        (30 ticks)
    T3 double tap:    poke AVM val 6 @ ticks 0..2,10..12 (40 ticks)
  PASS: iverilog/vvp trace == Python trace BYTE-FOR-BYTE on all three traces.
  Provenance: /tmp/NeuronConnect.xls sha256 120c2c63... (NQ-C1/NQ-C2 cache, verified).
"""
import hashlib, importlib.util, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = "/tmp/NeuronConnect.xls"
IV = "/home/eileen/tools/oss-cad-suite/bin/iverilog"
VVP = "/home/eileen/tools/oss-cad-suite/bin/vvp"
YOSYS = "/home/eileen/tools/oss-cad-suite/bin/yosys"

CELLS = ["AVM", "AVBL", "AVBR", "PVCL", "PVCR", "DB02", "DB03"]  # index = fire bit

def load_edges():
    spec = importlib.util.spec_from_file_location("nq", os.path.join(HERE, "..", "nq_c1_spike.py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    chem, gap = m.edges()
    idx = {c: i for i, c in enumerate(CELLS)}
    chem_e = sorted(((u, v, w) for (u, v), w in chem.items() if u in idx and v in idx and w > 0))
    gap_e = []
    for e in gap:
        a, b = tuple(e)
        if a in idx and b in idx:
            gap_e.append((a, b)); gap_e.append((b, a))
    gap_e.sort()
    return chem_e, gap_e

def thresholds(chem_e):
    strongest_in = {c: 0 for c in CELLS}
    for u, v, w in chem_e:
        strongest_in[v] = max(strongest_in[v], w)
    TH = {c: (strongest_in[c] or 6) for c in CELLS}
    TH["AVM"] = max(w for u, v, w in chem_e if u == "AVM")  # sensory setpoint: own strongest out
    return TH

SAT = 0xFFFF
def sat16(x): return SAT if x > SAT else (0 if x < 0 else x)

def sim(chem_e, gap_e, TH, poke_schedule, ticks):
    idx = {c: i for i, c in enumerate(CELLS)}
    out_edges = {c: [] for c in CELLS}
    for u, v, w in chem_e: out_edges[u].append((v, w))
    for u, v in gap_e:    out_edges[u].append((v, 1))
    acc = [0]*7; refr = [False]*7
    lines = []
    for t in range(ticks):
        pv, pval = poke_schedule.get(t, (0, 0))
        base = acc[:]
        if pv: base[idx["AVM"]] = sat16(base[idx["AVM"]] + pval)   # sensory lands first
        fires = [base[i] >= TH[c] and not refr[i] for i, c in enumerate(CELLS)]
        delta = [0]*7
        for i, c in enumerate(CELLS):
            if fires[i]:
                for v, w in out_edges[c]:
                    delta[idx[v]] += w
        nacc = [sat16(base[i] - (TH[c] if fires[i] else 0) + delta[i]) for i, c in enumerate(CELLS)]
        acc = [x >> 1 for x in nacc]
        refr = fires[:]
        fv = sum((1 << i) for i in range(7) if fires[i])
        lines.append(("t=%02d fires=%02x acc=%s" % (t, fv, "".join("%04x " % a for a in acc))).rstrip())
    return lines

TRACES = {
    "T1": ({0: (1,5), 1: (1,5), 2: (1,5)}, 30),
    "T2": ({t: (1,8) for t in range(6)}, 30),
    "T3": ({**{t: (1,6) for t in range(3)}, **{t: (1,6) for t in range(10,13)}}, 40),
}

WORM_V = """// NQ-C3 — C. elegans touch-arc, 7 cells, verbatim synapse weights from
// WormAtlas NeuronConnect.xls (sha256 120c2c63...). Emitted by nq_c3_spike.py.
// Integer threshold-sum-fire; sensory poke lands at tick start; chemical/gap fanout
// lands with one-tick delay (registered); refractory 1; half-leak; saturating 16-bit
// arithmetic (single saturation from exact 32-bit sums). Verilog-2005.
module worm_arc(
    input  wire         clk,
    input  wire         rst,
    input  wire         poke_valid,   // sensory stimulus -> AVM
    input  wire  [7:0]  poke_val,
    output reg  [6:0]   fire,         // fired[i] for the tick just completed (bit i = cell i)
    output reg  [111:0] acc_flat      // acc[i] at [16*i +: 16], after this tick's update
);
%(WEIGHTS)s
    localparam AVM = 0, AVBL = 1, AVBR = 2, PVCL = 3, PVCR = 4, DB02 = 5, DB03 = 6;
    // TH per cell packed MSB-first: [16*i +: 16] = TH of cell i
    localparam [111:0] THV = {%(THV)s};
    reg [15:0] acc  [0:6];
    reg        refr [0:6];
    reg [31:0] base [0:6];
    reg [31:0] d    [0:6];
    reg [31:0] nx   [0:6];
    reg [6:0]  f;
    integer i;

    always @(posedge clk) begin
        if (rst) begin
            for (i = 0; i < 7; i = i + 1) begin acc[i] <= 16'd0; refr[i] <= 1'b0; end
            fire <= 7'd0; acc_flat <= 112'd0;
        end else begin
            // 1. sensory lands first (amended order, booked in pre-reg)
            for (i = 0; i < 7; i = i + 1) begin
                base[i] = acc[i];
                if (poke_valid && i == AVM) base[i] = base[i] + poke_val;
                if (base[i] > 32'hFFFF) base[i] = 32'hFFFF;
            end
            // 2. fire test (one-tick refractory)
            for (i = 0; i < 7; i = i + 1)
                f[i] = (base[i] >= THV[16*i +: 16]) && !refr[i];
            // 3. exact fanout deltas in 32-bit
            for (i = 0; i < 7; i = i + 1) d[i] = 32'd0;
%(FANOUT)s
            // 4. reset-on-fire, add deltas, saturate once, half-leak, register
            for (i = 0; i < 7; i = i + 1) begin
                nx[i] = base[i] + d[i];
                if (f[i]) nx[i] = nx[i] - THV[16*i +: 16];
                if (nx[i] > 32'hFFFF) nx[i] = 32'hFFFF;
                nx[i] = nx[i] >> 1;
                acc[i]  <= nx[i][15:0];
                refr[i] <= f[i];
            end
            fire <= f;
            for (i = 0; i < 7; i = i + 1)
                acc_flat[16*i +: 16] <= nx[i][15:0];
        end
    end
endmodule
"""

TB_V = """// NQ-C3 testbench — generated stimulus, one line per tick, same format as the Python sim.
`timescale 1ns/1ps
module tb;
    reg clk = 0, rst = 1, pv = 0;
    reg [7:0] pval = 0;
    wire [6:0] fire; wire [111:0] accf;
    worm_arc dut(.clk(clk), .rst(rst), .poke_valid(pv), .poke_val(pval), .fire(fire), .acc_flat(accf));
    always #5 clk = ~clk;
    task poke(input integer v); begin pv = 1; pval = v; end endtask
    task quiet(); begin pv = 0; pval = 0; end endtask
    initial begin
%(RUN)s
        $finish;
    end
endmodule
"""

def gen_stimulus(traces):
    runs = []
    for name, (sched, ticks) in traces.items():
        body = ['quiet(); rst = 1; @(posedge clk); @(posedge clk); rst = 0;',
                '$display("--- %(name)s ---");' % dict(name=name)]
        for t in range(ticks):
            body.append(("poke(%d);" % sched[t][1]) if t in sched else "quiet();")
            body.append("@(posedge clk); #1;")
            body.append('$display("t=%%02d fires=%%02x acc=%%04h %%04h %%04h %%04h %%04h %%04h %%04h", %d, fire, accf[15:0], accf[31:16], accf[47:32], accf[63:48], accf[79:64], accf[95:80], accf[111:96]);' % t)
        runs.append("\n        ".join(body))
    return "\n        ".join(runs)

def main():
    sha = hashlib.sha256(open(RAW, "rb").read()).hexdigest()
    print("raw sha256 =", sha)
    assert sha.startswith("120c2c63"), "cache hash mismatch — abort (provenance is load-bearing)"
    chem_e, gap_e = load_edges()
    TH = thresholds(chem_e)
    print("cells:", CELLS)
    print("chemical edges:", chem_e)
    print("gap pairs:", sorted(set(tuple(sorted(e)) for e in gap_e)))
    print("TH:", {c: TH[c] for c in CELLS})

    # python traces
    py = {}
    for name, (sched, ticks) in TRACES.items():
        py[name] = sim(chem_e, gap_e, TH, sched, ticks)
        open(os.path.join(HERE, "trace_py_%s.txt" % name), "w").write("\n".join(py[name]) + "\n")
        print("[%s] python: %d ticks, firing ticks: %d" % (name, ticks, sum(1 for l in py[name] if not l.endswith("fires=00"))))

    # verilog emission — localparams for every edge the fanout references
    # (an AVB<->AVBR pair is BOTH a weak chemical synapse and a gap junction: two
    #  contributions in fanout, but the localparam name collides — declare once)
    params = {}
    for u, v, w in chem_e:
        params["W_%s_%s" % (u, v)] = w
    for a, b in sorted(set(gap_e)):
        params["W_EJ_%s_%s" % (a, b)] = 1
    wire = ["    // chemical + gap weights (verbatim; gap = 1 each direction)"]
    for k in sorted(params):
        src = "EJ gap" if k.startswith("W_EJ_") else "chem"
        wire.append("    localparam [31:0] %s = %d; // %s" % (k, params[k], src))
    fan = []
    for i, c in enumerate(CELLS):
        chem_outs = [(v, "W_%s_%s" % (c, v)) for u, v, w in chem_e if u == c]
        gap_outs = [(v, "W_EJ_%s_%s" % (c, v)) for a, v in gap_e if a == c]
        fan.append("        // cell %d (%s) fires -> fanout (chem + EJ)" % (i, c))
        for v, pname in sorted(chem_outs + gap_outs):
            fan.append("        if (f[%d]) d[%d] = d[%d] + %s;" % (i, CELLS.index(v), CELLS.index(v), pname))
    vsrc = WORM_V % {"WEIGHTS": "\n".join(wire),
                     "THV": ", ".join("16'd%d" % TH[c] for c in reversed(CELLS)),
                     "FANOUT": "\n".join(fan)}
    open(os.path.join(HERE, "worm_arc.v"), "w").write(vsrc)
    tbsrc = TB_V % {"RUN": gen_stimulus(TRACES)}
    open(os.path.join(HERE, "tb_worm_arc.v"), "w").write(tbsrc)

    r = subprocess.run([IV, "-g2005", "-o", os.path.join(HERE, "worm_arc.vvp"),
                        os.path.join(HERE, "worm_arc.v"), os.path.join(HERE, "tb_worm_arc.v")],
                       capture_output=True, text=True)
    print("iverilog rc =", r.returncode, (r.stderr[:400] if r.stderr else ""))
    if r.returncode: sys.exit(1)
    r = subprocess.run([VVP, os.path.join(HERE, "worm_arc.vvp")], capture_output=True, text=True)
    open(os.path.join(HERE, "trace_v_all.txt"), "w").write(r.stdout)
    cur, v = None, {}
    for line in r.stdout.splitlines():
        if line.startswith("--- "):
            cur = line.strip()[4:-4]; v[cur] = []
        elif cur is not None and line.startswith("t="):
            v[cur].append(line)
    verdict = {}
    for name in TRACES:
        pv_ = ("\n".join(py[name]) + "\n")
        vv = ("\n".join(v.get(name, [])) + "\n")
        ok = pv_ == vv
        verdict[name] = ok
        open(os.path.join(HERE, "trace_v_%s.txt" % name), "w").write(vv)
        print("[%s] bit-exact vs python: %s" % (name, "PASS" if ok else "FAIL"))
        if not ok:
            for a, b in zip(pv_.splitlines(), vv.splitlines()):
                if a != b: print("  py: %s\n  v : %s" % (a, b)); break
    print("\nNQ-C3 VERDICT:", "PASS" if all(verdict.values()) else "FAIL")
    json.dump({"sha": sha, "TH": TH, "verdict": verdict,
               "chem": chem_e, "gap": sorted(set(tuple(sorted(e)) for e in gap_e))},
              open(os.path.join(HERE, "spike_meta.json"), "w"), indent=1)

if __name__ == "__main__":
    main()
