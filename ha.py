import heapq
from collections import defaultdict, namedtuple

# Определяем узел дерева Хаффмана
class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

# Функция для построения дерева Хаффмана
def build_huffman_tree(data):
    frequency = defaultdict(int)

    # Подсчет частоты каждого символа
    for byte in data:
        frequency[byte] += 1

    # Создание приоритетной очереди (кучи)
    priority_queue = [Node(char, freq) for char, freq in frequency.items()]
    heapq.heapify(priority_queue)

    # Построение дерева
    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(priority_queue, merged)

    return priority_queue[0]  # Корень дерева

# Функция для генерации кодов Хаффмана
def generate_huffman_codes(node, prefix='', codebook={}):
    if node is not None:
        if node.char is not None:  # Листовой узел
            codebook[node.char] = prefix
        generate_huffman_codes(node.left, prefix + '0', codebook)
        generate_huffman_codes(node.right, prefix + '1', codebook)
    return codebook

# Функция для кодирования данных
def huffman_encode(data):
    root = build_huffman_tree(data)
    huffman_codes = generate_huffman_codes(root)

    # Кодируем данные
    encoded_data = ''.join(huffman_codes[byte] for byte in data)
    return encoded_data, huffman_codes

# Функция для декодирования данных
def huffman_decode(encoded_data, huffman_codes):
    # Создаем обратный словарь для декодирования
    reverse_codes = {v: k for k, v in huffman_codes.items()}
    current_code = ''
    decoded_data = bytearray()

    for bit in encoded_data:
        current_code += bit
        if current_code in reverse_codes:
            decoded_data.append(reverse_codes[current_code])
            current_code = ''

    return bytes(decoded_data)


s = b"abracadabra"
encoded_data, huffman_codes = huffman_encode(s)
print("Encoded data:", encoded_data)
print("Huffman Codes:", huffman_codes)

decoded_data = huffman_decode(encoded_data, huffman_codes)
print("Decoded data:", decoded_data)