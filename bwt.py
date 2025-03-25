import os
import sys


def BWT(s: bytes) -> tuple[bytes, int]:

    if not s:
        return b'', 0

    double_s = s + s
    n = len(s)

    sa = sorted(range(n), key=lambda i: double_s[i:i + n])

    bwt = bytearray()
    original_idx = -1
    for i, idx in enumerate(sa):
        if idx == 0:
            bwt.append(s[-1])
            original_idx = i
        else:
            bwt.append(s[idx - 1])

    return bytes(bwt), original_idx


def iBWT(bwt: bytes, idx: int) -> bytes:
    if not bwt:
        return b''

    count = {}
    rank = []
    for c in bwt:
        count[c] = count.get(c, 0) + 1
        rank.append(count[c] - 1)

    first_occurrence = {}
    sorted_chars = sorted(count.keys())
    total = 0
    for c in sorted_chars:
        first_occurrence[c] = total
        total += count[c]

    result = bytearray()
    current = idx
    for _ in range(len(bwt)):
        c = bwt[current]
        result.append(c)
        current = first_occurrence[c] + rank[current]

    return bytes(reversed(result))


def compress_file(input_path: str, output_path: str, block_size: int = 10000):
    with open(input_path, 'rb') as fin, open(output_path, 'wb') as fout:
        while True:
            block = fin.read(block_size)
            if not block:
                break

            compressed, idx = suffix_array_bwt(block)
            fout.write(idx.to_bytes(4, sys.byteorder))
            fout.write(compressed)


def decompress_file(input_path: str, output_path: str, block_size: int = 10000):

    with open(input_path, 'rb') as fin, open(output_path, 'wb') as fout:
        while True:
            idx_bytes = fin.read(4)
            if not idx_bytes:
                break

            idx = int.from_bytes(idx_bytes, sys.byteorder)
            compressed = fin.read(block_size)

            if not compressed:
                break

            decompressed = inverse_bwt(compressed, idx)
            fout.write(decompressed)
