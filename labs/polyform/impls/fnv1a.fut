-- fnv1a-64 in Futhark. Native u64 wraparound arithmetic, no limb tricks needed.
-- Build: futhark c fnv1a.fut ; run: ./fnv1a < bytes-as-futhark-value  (e.g. [97u8,98u8])
def offset : u64 = 0xcbf29ce484222325u64
def prime  : u64 = 0x100000001b3u64

def fnv1a (bs: []u8) : u64 =
  loop h = offset for b in bs do (h ^ u64.u8 b) * prime

def main (bs: []u8) : u64 = fnv1a bs
