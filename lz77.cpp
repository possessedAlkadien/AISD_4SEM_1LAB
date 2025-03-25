#include <iostream>
#include <fstream>
#include <string>
#include <string_view>
#include <forward_list>
#include <algorithm>
#include <windows.h>
#include <cstdint> // Для uint16_t и uint32_t

using namespace std;

struct CodeNode {
    uint16_t beg; // Начало ссылки в окне
    uint8_t len;  // Длина ссылки
    uint8_t ch;   // Символ
};

bool push_shift(string& s, char c, size_t len) {
    if (s.size() < len) {
        s.push_back(c);
        return false;
    }
    move(next(s.begin()), s.end(), s.begin());
    s.back() = c;
    return true;
}

forward_list<CodeNode> LZ77(string_view s, size_t win_len = 1000) {
    forward_list<CodeNode> res;
    auto it = res.before_begin();
    string win;
    win.reserve(win_len);

    for (size_t i = 0; i < s.size(); ++i) {
        char c = s[i];
        size_t pos = win.rfind(s.substr(i)); // Ищем буфер в окне
        CodeNode next = { 0, 0, static_cast<uint8_t>(c) }; // Инициализация текущего узла

        if (pos != string::npos) {
            next.beg = static_cast<uint16_t>(win.size() - pos); // Начало ссылки
            next.len = static_cast<uint8_t>(s.substr(i).find_first_not_of(c)); // Длина совпадения
            if (next.len > 0) {
                next.len = min(next.len, static_cast<size_t>(win.size() - pos)); // Ограничиваем длину
            }
            i += next.len - 1; // Пропускаем совпадение
        }

        if (next.len > 0 || next.ch != 0) {
            res.insert_after(it, next); // Добавляем код
        }
        push_shift(win, c, win_len); // Сдвигаем окно
    }

    return res;
}

size_t LZ77length(const forward_list<CodeNode>& code) {
    size_t len = 0;
    for (const CodeNode& cn : code) len += cn.len + 1; // Длина символа + 1 для ссылки
    return len;
}
string LZ77decode(const forward_list<CodeNode>& code) {
    string res;
    res.reserve(LZ77length(code));

    for (const CodeNode& cn : code) {
        size_t start = res.size();
        if (start >= cn.beg) {
            size_t refStart = start - cn.beg; // Начало ссылки
            size_t end = refStart + cn.len; // Конец ссылки

            // Проверка на границы
            if (refStart < res.size() && end <= res.size()) {
                // Копируем символы по ссылке
                for (size_t i = refStart; i < end; ++i) {
                    res += res[i]; // Копируем символы
                }
            }
        }
        // Добавляем текущий символ, если он не равен нулю
        if (cn.ch != 0) {
            res += cn.ch; // Добавляем текущий символ
        }
    }
    return res;
}

ostream& operator<<(ostream& os, const CodeNode& cn) {
    return os << '<' << cn.beg << ',' << int(cn.len) << ',' << int(cn.ch) << '>';
}

void compressFile(const string& inputFile, const string& outputFile) {
    ifstream inFile(inputFile, ios::binary);
    ofstream outFile(outputFile, ios::binary);

    if (!inFile.is_open() || !outFile.is_open()) {
        cerr << "Ошибка открытия файлов!" << endl;
        return;
    }

    string content((istreambuf_iterator<char>(inFile)), istreambuf_iterator<char>());
    auto code = LZ77(content);

    // Записываем закодированные данные в файл
    for (const CodeNode& cn : code) {
        outFile.write(reinterpret_cast<const char*>(&cn), sizeof(CodeNode));
    }

    inFile.close();
    outFile.close();
}

void decompressFile(const string& inputFile, const string& outputFile) {
    ifstream inFile(inputFile, ios::binary);
    ofstream outFile(outputFile, ios::binary);

    if (!inFile.is_open() || !outFile.is_open()) {
        cerr << "Ошибка открытия файлов!" << endl;
        return;
    }

    forward_list<CodeNode> code;
    CodeNode cn;
    while (inFile.read(reinterpret_cast<char*>(&cn), sizeof(CodeNode))) {
        code.push_front(cn); // Считываем закодированные данные
    }

    string decompressedData = LZ77decode(code); // Раскодируем данные
    outFile.write(decompressedData.c_str(), decompressedData.size()); // Записываем в выходной файл

    inFile.close();
    outFile.close();
}

int main() {
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);

    string inputFile = "tsvet.jpg";          // Путь к входному файлу
    string compressedFile = "compressed.txt"; // Путь к выходному файлу с закодированными данными
    string decompressedFile = "decompressed.jpg"; // Путь к выходному файлу с раскодированными данными

    compressFile(inputFile, compressedFile); // Сжимаем файл
    decompressFile(compressedFile, decompressedFile); // Распаковываем файл

    cout << "Сжатие и распаковка завершены!" << endl;
    return 0;
}
