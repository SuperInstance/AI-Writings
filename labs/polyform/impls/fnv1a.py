"""fnv1a-64 — Python baseline. Reads a file of raw bytes (argv[1]), prints 16 hex digits."""
import sys

OFFSET = 0xCBF29CE484222325
PRIME = 0x100000001B3
MASK = (1 << 64) - 1


def fnv1a64(data: bytes) -> int:
    h = OFFSET
    for b in data:
        h = ((h ^ b) * PRIME) & MASK
    return h


if __name__ == "__main__":
    with open(sys.argv[1], "rb") as f:
        print("%016x" % fnv1a64(f.read()))
