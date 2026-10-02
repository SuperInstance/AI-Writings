    # P2: order-not-time — two streams, same ops different order -> first divergence
    from lab.chain import ReceiptChain, fnv1a64
    a = ReceiptChain(); b = ReceiptChain()
    ops_a = ["alpha", "beta", "gamma"]; ops_b = ["alpha", "gamma", "beta"]
    div = None
    for i, (oa, ob) in enumerate(zip(ops_a, ops_b)):
        ra = a.append(oa); rb = b.append(ob)
        if ra != rb and div is None:
            div = i
    pin("P2 order-not-time", div == 1, f"first-divergence-position={div}")

