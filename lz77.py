import os
import struct


def LZ77(input_file, output_file, window_size=1024, lookahead_buffer=10000):
    with open(input_file, 'rb') as f_in:
        data = f_in.read()

    compressed = []
    i = 0
    data_len = len(data)

    while i < data_len:
        best_offset = 0
        best_length = 0
        best_char = data[i] if i < data_len else 0

        search_start = max(0, i - window_size)
        search_window = data[search_start:i]
        current_buffer = data[i:i + lookahead_buffer]

        for length in range(1, len(current_buffer) + 1):
            pattern = current_buffer[:length]
            offset = search_window.rfind(pattern)

            if offset != -1:
                best_length = length
                best_offset = i - (search_start + offset)
                best_char = data[i + length] if (i + length) < data_len else 0

        compressed.append((best_offset, best_length, best_char))
        i += best_length + 1 if best_length > 0 else 1

    with open(output_file, 'wb') as f_out:
        for triplet in compressed:
            f_out.write(struct.pack("!HHB", *triplet))


def iLZ77(input_file, output_file):
    with open(input_file, 'rb') as f_in:
        compressed_data = f_in.read()

    if len(compressed_data) % 5 != 0:
        raise ValueError("Invalid compressed file format")

    compressed = []
    for i in range(0, len(compressed_data), 5):
        triplet = struct.unpack("!HHB", compressed_data[i:i + 5])
        compressed.append(triplet)

    decompressed = bytearray()
    for offset, length, char in compressed:
        if length == 0:
            decompressed.append(char)
            continue

        start = len(decompressed) - offset
        if start < 0:
            raise ValueError("Invalid offset in compressed data")

        for i in range(length):
            decompressed.append(decompressed[start + i])

        decompressed.append(char)

    with open(output_file, 'wb') as f_out:
        f_out.write(decompressed)


if __name__ == "__main__":
    # Настройки путей
    original_file = "enwik7.txt"
    compressed_file = "compressed.txt"
    decompressed_file = "decompressed.txt"
    try:
        # Шаг 1: Сжатие файла
        LZ77(original_file, compressed_file)
        print(f"[Сжатие] Размер оригинального файла: {os.path.getsize(original_file)} байт")
        print(f"[Сжатие] Размер сжатого файла: {os.path.getsize(compressed_file)} байт")

        # Шаг 2: Распаковка файла
        LZ77_decompress(compressed_file, decompressed_file)
        print(f"[Распаковка] Размер распакованного файла: {os.path.getsize(decompressed_file)} байт")

        # Проверка целостности данных
        with open(original_file, 'rb') as f1, open(decompressed_file, 'rb') as f2:
            if f1.read() == f2.read():
                print("Проверка: Данные совпадают!")
            else:
                print("Ошибка: Данные не совпадают!")

    except FileNotFoundError as e:
        print(f"Ошибка: Файл не найден - {e.filename}")
    except Exception as e:
        print(f"Критическая ошибка: {str(e)}")

        for f in [compressed_file, decompressed_file]:
            if os.path.exists(f):
                os.remove(f)