from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
import gzip
import os

def pad(text):
    while len(text) % 8 != 0:
        text += b' '
    return text

def compress_file(filename):
    compressed_name = filename + '.gz'
    with open(filename, 'rb') as f_in, gzip.open(compressed_name, 'wb') as f_out:
        f_out.writelines(f_in)
    return compressed_name

def file_size(path):
    return os.path.getsize(path)

# 1. Считываем открытый текст из файла
with open('input_text.txt', 'rb') as f:
    plaintext = f.read()

# Сохраняем для сравнения
with open('plaintext.txt', 'wb') as f:
    f.write(plaintext)

# 2. Шифрование с использованием CBC
key = get_random_bytes(8)  # DES-ключ = 8 байт
iv = get_random_bytes(8)   # Инициализирующий вектор для CBC
cipher = DES.new(key, DES.MODE_CBC, iv)
padded_text = pad(plaintext)
ciphertext = cipher.encrypt(padded_text)

# Сохраняем вместе с IV, чтобы можно было расшифровать при необходимости
with open('ciphertext.txt', 'wb') as f:
    f.write(iv + ciphertext)

# 3. Сжатие
plain_compressed = compress_file('plaintext.txt')
cipher_compressed = compress_file('ciphertext.txt')

# 4. Вывод результатов
print("=== Результаты сжатия ===")
sizes = {
    "Открытый текст": file_size('plaintext.txt'),
    "Зашифрованный текст": file_size('ciphertext.txt'),
    "Сжатый открытый текст": file_size(plain_compressed),
    "Сжатый зашифрованный текст": file_size(cipher_compressed)
}

for label, size in sizes.items():
    print(f"{label}: {size} байт")

print("\n=== Степень сжатия ===")
plain_ratio = (sizes["Открытый текст"] - sizes["Сжатый открытый текст"]) / sizes["Открытый текст"] * 100
cipher_ratio = (sizes["Зашифрованный текст"] - sizes["Сжатый зашифрованный текст"]) / sizes["Зашифрованный текст"] * 100

print(f"Открытый текст: {plain_ratio:.2f}%")
print(f"Зашифрованный текст: {cipher_ratio:.2f}%")
