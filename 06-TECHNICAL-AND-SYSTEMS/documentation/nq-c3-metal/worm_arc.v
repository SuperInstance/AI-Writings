// NQ-C3 — C. elegans touch-arc, 7 cells, verbatim synapse weights from
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
    // chemical + gap weights (verbatim; gap = 1 each direction)
    localparam [31:0] W_AVBL_AVBR = 1; // chem
    localparam [31:0] W_AVBR_AVBL = 1; // chem
    localparam [31:0] W_AVM_AVBL = 6; // chem
    localparam [31:0] W_AVM_AVBR = 6; // chem
    localparam [31:0] W_AVM_PVCL = 4; // chem
    localparam [31:0] W_AVM_PVCR = 5; // chem
    localparam [31:0] W_EJ_AVBL_AVBR = 1; // EJ gap
    localparam [31:0] W_EJ_AVBL_DB03 = 1; // EJ gap
    localparam [31:0] W_EJ_AVBR_AVBL = 1; // EJ gap
    localparam [31:0] W_EJ_AVBR_DB02 = 1; // EJ gap
    localparam [31:0] W_EJ_AVBR_DB03 = 1; // EJ gap
    localparam [31:0] W_EJ_DB02_AVBR = 1; // EJ gap
    localparam [31:0] W_EJ_DB02_DB03 = 1; // EJ gap
    localparam [31:0] W_EJ_DB03_AVBL = 1; // EJ gap
    localparam [31:0] W_EJ_DB03_AVBR = 1; // EJ gap
    localparam [31:0] W_EJ_DB03_DB02 = 1; // EJ gap
    localparam [31:0] W_EJ_PVCL_PVCR = 1; // EJ gap
    localparam [31:0] W_EJ_PVCR_PVCL = 1; // EJ gap
    localparam [31:0] W_PVCL_AVBL = 5; // chem
    localparam [31:0] W_PVCL_AVBR = 12; // chem
    localparam [31:0] W_PVCL_DB02 = 3; // chem
    localparam [31:0] W_PVCL_DB03 = 4; // chem
    localparam [31:0] W_PVCL_PVCR = 2; // chem
    localparam [31:0] W_PVCR_AVBL = 8; // chem
    localparam [31:0] W_PVCR_AVBR = 6; // chem
    localparam [31:0] W_PVCR_DB02 = 1; // chem
    localparam [31:0] W_PVCR_DB03 = 3; // chem
    localparam [31:0] W_PVCR_PVCL = 3; // chem
    localparam AVM = 0, AVBL = 1, AVBR = 2, PVCL = 3, PVCR = 4, DB02 = 5, DB03 = 6;
    // TH per cell packed MSB-first: [16*i +: 16] = TH of cell i
    localparam [111:0] THV = {16'd4, 16'd3, 16'd5, 16'd4, 16'd12, 16'd8, 16'd6};
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
        // cell 0 (AVM) fires -> fanout (chem + EJ)
        if (f[0]) d[1] = d[1] + W_AVM_AVBL;
        if (f[0]) d[2] = d[2] + W_AVM_AVBR;
        if (f[0]) d[3] = d[3] + W_AVM_PVCL;
        if (f[0]) d[4] = d[4] + W_AVM_PVCR;
        // cell 1 (AVBL) fires -> fanout (chem + EJ)
        if (f[1]) d[2] = d[2] + W_AVBL_AVBR;
        if (f[1]) d[2] = d[2] + W_EJ_AVBL_AVBR;
        if (f[1]) d[6] = d[6] + W_EJ_AVBL_DB03;
        // cell 2 (AVBR) fires -> fanout (chem + EJ)
        if (f[2]) d[1] = d[1] + W_AVBR_AVBL;
        if (f[2]) d[1] = d[1] + W_EJ_AVBR_AVBL;
        if (f[2]) d[5] = d[5] + W_EJ_AVBR_DB02;
        if (f[2]) d[6] = d[6] + W_EJ_AVBR_DB03;
        // cell 3 (PVCL) fires -> fanout (chem + EJ)
        if (f[3]) d[1] = d[1] + W_PVCL_AVBL;
        if (f[3]) d[2] = d[2] + W_PVCL_AVBR;
        if (f[3]) d[5] = d[5] + W_PVCL_DB02;
        if (f[3]) d[6] = d[6] + W_PVCL_DB03;
        if (f[3]) d[4] = d[4] + W_EJ_PVCL_PVCR;
        if (f[3]) d[4] = d[4] + W_PVCL_PVCR;
        // cell 4 (PVCR) fires -> fanout (chem + EJ)
        if (f[4]) d[1] = d[1] + W_PVCR_AVBL;
        if (f[4]) d[2] = d[2] + W_PVCR_AVBR;
        if (f[4]) d[5] = d[5] + W_PVCR_DB02;
        if (f[4]) d[6] = d[6] + W_PVCR_DB03;
        if (f[4]) d[3] = d[3] + W_EJ_PVCR_PVCL;
        if (f[4]) d[3] = d[3] + W_PVCR_PVCL;
        // cell 5 (DB02) fires -> fanout (chem + EJ)
        if (f[5]) d[2] = d[2] + W_EJ_DB02_AVBR;
        if (f[5]) d[6] = d[6] + W_EJ_DB02_DB03;
        // cell 6 (DB03) fires -> fanout (chem + EJ)
        if (f[6]) d[1] = d[1] + W_EJ_DB03_AVBL;
        if (f[6]) d[2] = d[2] + W_EJ_DB03_AVBR;
        if (f[6]) d[5] = d[5] + W_EJ_DB03_DB02;
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
