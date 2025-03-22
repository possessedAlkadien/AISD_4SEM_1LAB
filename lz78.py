def LZ78(data):
    # Инициализируем словарь кодов
    dict_of_codes = {data[0:1]: b'1'}  # Используем байты
    encoded_result = bytearray()  # Используем bytearray для хранения результата
    encoded_result.extend(b'0' + data[0:1])  # Записываем первый байт с индексом 0
    data = data[1:]  # Убираем первый байт из данных
    combination = bytearray()  # Используем bytearray для комбинации
    code = 2  # Начинаем с кода 2

    for byte in data:
        combination.append(byte)  # Добавляем байт к комбинации
        if bytes(combination) not in dict_of_codes:
            dict_of_codes[bytes(combination)] = str(code).encode()  # Кодируем в байты
            if len(combination) == 1:
                encoded_result.extend(b'0' + bytes(combination))  # Записываем (0, байт)
            else:
                # Записываем (код предыдущей комбинации, последний байт)
                encoded_result.extend(dict_of_codes[bytes(combination[:-1])] + bytes([combination[-1]]))
            code += 1  # Увеличиваем код
            combination.clear()  # Очищаем комбинацию

    return bytes(encoded_result)


def iLZ78(coded_data):
    # Инициализируем словарь кодов
    dict_of_codes = {b'0': b'', b'1': coded_data[1:2]}  # Используем байты
    decoded_result = bytearray()  # Используем bytearray для хранения результата
    decoded_result.extend(dict_of_codes[b'1'])  # Записываем первый байт
    coded_data = coded_data[2:]  # Убираем первые два байта из данных
    combination = bytearray()  # Используем bytearray для комбинации
    code = 2  # Начинаем с кода 2

    for byte in coded_data:
        if byte in b'0123456789':  # Проверяем, является ли байт цифрой
            combination.append(byte)  # Добавляем байт к комбинации
        else:
            # Декодируем комбинацию и добавляем новый байт
            dict_of_codes[str(code).encode()] = dict_of_codes[bytes(combination)] + bytes([byte])
            decoded_result.extend(dict_of_codes[bytes(combination)] + bytes([byte]))
            combination.clear()  # Очищаем комбинацию
            code += 1  # Увеличиваем код

    return bytes(decoded_result)

string = b"aaaabbbbabababababa$"
compressed_data = LZ78(string)
print("Compressed data:", compressed_data)
print(iLZ78(LZ78(string)))