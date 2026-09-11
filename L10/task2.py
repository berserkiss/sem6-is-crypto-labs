import base64
import time
import random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util import number
import os


# === RSA ===
def rsa_generate_keys(bits=2048):
    key = RSA.generate(bits)
    return key, key.publickey()


def rsa_encrypt(public_key, plaintext_bytes):
    cipher = PKCS1_OAEP.new(public_key)
    return cipher.encrypt(plaintext_bytes)


def rsa_decrypt(private_key, ciphertext):
    cipher = PKCS1_OAEP.new(private_key)
    return cipher.decrypt(ciphertext)


# === ElGamal ===
def elgamal_generate_keys(bits=2048):
    p = number.getPrime(bits)
    g = random.randint(2, p - 2)
    x = random.randint(2, p - 2)
    y = pow(g, x, p)
    public_key = (p, g, y)
    private_key = (p, g, x)
    return private_key, public_key


def elgamal_encrypt(public_key, plaintext_bytes):
    p, g, y = public_key
    k = random.randint(2, p - 2)
    a = pow(g, k, p)
    m = int.from_bytes(plaintext_bytes, byteorder='big')
    b = (pow(y, k, p) * m) % p
    return a, b


def elgamal_decrypt(private_key, a, b):
    p, g, x = private_key
    s = pow(a, x, p)
    s_inv = pow(s, -1, p)
    m = (b * s_inv) % p
    return m.to_bytes((m.bit_length() + 7) // 8, byteorder='big')


# === MAIN ===
def run_test(text):
    os.system('chcp 65001')
    print(f"\n=== Исходный текст: {text} ===")
    ascii_bytes = text.encode('ascii')
    base64_encoded = base64.b64encode(ascii_bytes)

    print(f"ASCII-кодировка: {ascii_bytes}")
    print(f"Base64-кодировка: {base64_encoded}\n")

    for label, input_data in [('ASCII', ascii_bytes), ('Base64', base64_encoded)]:
        print(f"===== ТЕСТ: {label} =====")
        input_len = len(input_data)

        # === RSA ===
        print("-- RSA --")
        rsa_private, rsa_public = rsa_generate_keys()
        start = time.time()
        rsa_cipher = rsa_encrypt(rsa_public, input_data)
        rsa_encrypt_time = time.time() - start

        start = time.time()
        rsa_decrypted = rsa_decrypt(rsa_private, rsa_cipher)
        rsa_decrypt_time = time.time() - start

        decrypted_text = rsa_decrypted.decode('ascii') if label == 'ASCII' else base64.b64decode(rsa_decrypted).decode('ascii')

        # Печать RSA шифротекста в base64 и latin1
        print("Зашифрованное (base64):", base64.b64encode(rsa_cipher).decode())
        print("Зашифрованное (ASCII):", rsa_cipher.decode('latin1'))  # Это нужно для печати сырых байтов
        print("Расшифрованное сообщение:", decrypted_text)
        print("Размер шифртекста:", len(rsa_cipher), "байт")
        print(f"Время шифрования: {rsa_encrypt_time:.6f} сек")
        print(f"Время расшифрования: {rsa_decrypt_time:.6f} сек\n")

        # === ElGamal ===
        print("-- Эль-Гамаль --")
        elgamal_private, elgamal_public = elgamal_generate_keys()
        start = time.time()
        a, b = elgamal_encrypt(elgamal_public, input_data)
        elgamal_encrypt_time = time.time() - start

        a_bytes = a.to_bytes((a.bit_length() + 7) // 8, byteorder='big')
        b_bytes = b.to_bytes((b.bit_length() + 7) // 8, byteorder='big')

        start = time.time()
        elgamal_decrypted = elgamal_decrypt(elgamal_private, a, b)
        elgamal_decrypt_time = time.time() - start

        decrypted_text_eg = elgamal_decrypted.decode('ascii') if label == 'ASCII' else base64.b64decode(elgamal_decrypted).decode('ascii')

        # Печать ElGamal зашифрованных данных
        print("Зашифрованное a (base64):", base64.b64encode(a_bytes).decode())
        print("Зашифрованное b (base64):", base64.b64encode(b_bytes).decode())
        print("Зашифрованное a (ASCII):", a_bytes.decode('latin1'))
        print("Зашифрованное b (ASCII):", b_bytes.decode('latin1'))
        print("Расшифрованное сообщение:", decrypted_text_eg)
        print("Размер шифртекста:", len(a_bytes) + len(b_bytes), "байт")
        print(f"Время шифрования: {elgamal_encrypt_time:.6f} сек")
        print(f"Время расшифрования: {elgamal_decrypt_time:.6f} сек\n")
        print("=" * 60 + "\n")

        print("== Оценка производительности и изменения объема ==")

        rsa_encrypt_speed = rsa_encrypt_time
        rsa_decrypt_speed = rsa_decrypt_time
        elgamal_encrypt_speed = elgamal_encrypt_time
        elgamal_decrypt_speed = elgamal_decrypt_time

        rsa_size_ratio = len(rsa_cipher) / len(base64_encoded)
        elgamal_size_ratio = (len(a_bytes) + len(b_bytes)) / len(base64_encoded)

        print(f"RSA:")
        print(f" - Время шифрования: {rsa_encrypt_speed:.6f} сек")
        print(f" - Время расшифрования: {rsa_decrypt_speed:.6f} сек")
        print(f" - Коэффициент увеличения размера: {rsa_size_ratio:.2f}x")

        print(f"Эль-Гамаль:")
        print(f" - Время шифрования: {elgamal_encrypt_speed:.6f} сек")
        print(f" - Время расшифрования: {elgamal_decrypt_speed:.6f} сек")
        print(f" - Коэффициент увеличения размера: {elgamal_size_ratio:.2f}x\n")




# Запуск
run_test("Puzyrova Hanna Sergeeyna")
