    shutil.rmtree(d4); shutil.rmtree(d5)

    # P5: genesis anchor — replay from a saved mid-stream receipt forward
    d6, _ = run_stream(4242, 300, "honest")
    lines = open(os.path.join(d6, "receipts.txt")).read().splitlines()
    anchor_line = lines[149]  # position 149 (0-based), the 150th op
    anchor_hash, anchor_op = anchor_line.split(" ", 1)
    ch2 = ReceiptChain(genesis=anchor_hash)
    for line in lines[150:]:
        h, op = line.split(" ", 1)
        rh = ch2.append(op)
        if rh != h:
            pin("P5 genesis-anchor", False, "diverged after anchor at replayed pos")
            return 1
    terminal = lines[-1].split()[0]
    pin("P5 genesis-anchor", ch2.head == terminal,
        f"replayed-forward-to-terminal={ch2.head == terminal}")
