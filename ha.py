import heapq
from collections import defaultdict
import os
import pickle

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(data: bytes) -> Node:
    frequency = defaultdict(int)
    for byte in data:
        frequency[byte] += 1

    priority_queue = [Node(char, freq) for char, freq in frequency.items()]
    heapq.heapify(priority_queue)

    if len(priority_queue) == 1:
        only_node = heapq.heappop(priority_queue)
        merged = Node(None, only_node.freq)
        merged.left = only_node
        return merged

    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(priority_queue, merged)
    return priority_queue[0]

def generate_huffman_codes(node, prefix='', codebook=None):
    if codebook is None:
        codebook = {}
    if node is not None:
        if node.char is not None:
            codebook[node.char] = prefix
        generate_huffman_codes(node.left, prefix + '0', codebook)
        generate_huffman_codes(node.right, prefix + '1', codebook)
    return codebook

def HA(data: bytes) -> (bytes, dict):
    root = build_huffman_tree(data)
    huffman_codes = generate_huffman_codes(root)

    encoded_bitstring = ''.join(huffman_codes[byte] for byte in data)
    extra_padding = (8 - len(encoded_bitstring) % 8) % 8
    padded_bitstring = encoded_bitstring + '0' * extra_padding

    b = bytearray()
    for i in range(0, len(padded_bitstring), 8):
        byte = padded_bitstring[i:i + 8]
        b.append(int(byte, 2))

    result = bytes([extra_padding]) + bytes(b)
    return result, huffman_codes

def iHA(encoded_bytes: bytes, huffman_codes: dict) -> bytes:
    extra_padding = encoded_bytes[0]
    bit_data = encoded_bytes[1:]

    bitstring = ''.join(format(byte, '08b') for byte in bit_data)
    if extra_padding:
        bitstring = bitstring[:-extra_padding]

    reverse_codes = {v: k for k, v in huffman_codes.items()}
    current_code = ''
    decoded_bytes = bytearray()

    for bit in bitstring:
        current_code += bit
        if current_code in reverse_codes:
            decoded_bytes.append(reverse_codes[current_code])
            current_code = ''

    return bytes(decoded_bytes)

