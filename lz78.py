import struct


def LZ78(data):
    dictionary = {b'': 0}
    current = b''
    encoded = []
    code = 1  # Следующий доступный код

    for byte in data:
        current_candidate = current + bytes([byte])
        if current_candidate in dictionary:
            current = current_candidate
        else:
            # Добавляем (код предыдущей строки, новый байт)
            encoded.append((dictionary[current], bytes([byte])))
            dictionary[current_candidate] = code
            code += 1
            current = b''

    # Сериализация в бинарный формат с использованием 4 байт для кода
    result = bytearray()
    for code_num, char in encoded:
        result += struct.pack('>I', code_num)  # 4 байта для кода
        result += char  # Символ всегда присутствует

    return bytes(result)


def iLZ78(compressed_data):
    dictionary = {0: b''}
    decoded = bytearray()
    code = 1

    # Чтение данных по 5 байт (4 байта код + 1 байт символ)
    for i in range(0, len(compressed_data), 5):
        chunk = compressed_data[i:i + 5]
        if len(chunk) < 5:
            break

        # Распаковка кода и символа
        current_code = struct.unpack('>I', chunk[:4])[0]
        current_char = chunk[4:5]

        # Получение фразы из словаря
        if current_code not in dictionary:
            raise ValueError(f"Invalid code {current_code}")

        phrase = dictionary[current_code] + current_char
        decoded += phrase

        # Добавление новой фразы в словарь
        dictionary[code] = phrase
        code += 1

    return bytes(decoded)


