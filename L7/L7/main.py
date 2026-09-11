import os
import time
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import binascii
from itertools import zip_longest


WEAK_KEYS = [
    b'\x01\x01\x01\x01\x01\x01\x01\x01',  # 0101010101010101
    b'\xFE\xFE\xFE\xFE\xFE\xFE\xFE\xFE',  # FEFEFEFEFEFEFEFE
    b'\xE0\xE0\xE0\xE0\xF1\xF1\xF1\xF1',  # E0E0E0E0F1F1F1F1
    b'\x1F\x1F\x1F\x1F\x0E\x0E\x0E\x0E'   # 1F1F1F1F0E0E0E0E
]


def format_hex(data):
    """Форматирование данных в HEX с разделением по 4 символа"""
    hex_str = binascii.hexlify(data).decode('utf-8').upper()
    return ' '.join([hex_str[i:i + 4] for i in range(0, len(hex_str), 4)])


def format_binary(data):
    """Форматирование данных в бинарный вид"""
    return ' '.join(f'{byte:08b}' for byte in data)


def split_into_blocks(data, block_size):
    """Разделение данных на блоки с дополнением последнего блока"""
    blocks = [data[i:i + block_size] for i in range(0, len(data), block_size)]
    if len(blocks[-1]) < block_size:
        blocks[-1] = pad(blocks[-1], block_size)
    return blocks


def generate_key_from_name(name):
    """Генерация ключа из имени"""
    name_bytes = name.encode('utf-8')[:8]
    if len(name_bytes) < 8:
        name_bytes += b'\x00' * (8 - len(name_bytes))
    return name_bytes


def flip_bit(data, bit_pos):
    """Инвертирование указанного бита в данных"""
    byte_pos = bit_pos // 8
    bit_in_byte = 7 - (bit_pos % 8)
    modified = bytearray(data)
    modified[byte_pos] ^= (1 << bit_in_byte)
    return bytes(modified)


def measure_performance(text, key, iterations=1000):
    """Измерение скорости шифрования/дешифрования"""
    # Шифрование
    start = time.time()
    for _ in range(iterations):
        des_encrypt(text, key)
    enc_time = (time.time() - start) / iterations * 1000  # мс

    # Дешифрование
    ciphertext = des_encrypt(text, key)
    start = time.time()
    for _ in range(iterations):
        des_decrypt(ciphertext, key)
    dec_time = (time.time() - start) / iterations * 1000  # мс

    return enc_time, dec_time



def des_encrypt(plaintext, key, mode=DES.MODE_ECB, use_padding=True):
    key = adjust_key_parity(key)
    cipher = DES.new(key, mode)
    if use_padding:
        plaintext = pad(plaintext, DES.block_size)
    return cipher.encrypt(plaintext)

def des_decrypt(ciphertext, key, mode=DES.MODE_ECB, use_padding=True):
    key = adjust_key_parity(key)
    cipher = DES.new(key, mode)
    decrypted = cipher.decrypt(ciphertext)
    if use_padding:
        try:
            return unpad(decrypted, DES.block_size)
        except ValueError:
            return decrypted
    return decrypted


def des_encrypt2(plaintext, key, mode=DES.MODE_CBC, use_padding=True):
    key = adjust_key_parity(key)
    if mode == DES.MODE_CBC:
        iv = os.urandom(DES.block_size)  # Генерируем IV
        cipher = DES.new(key, mode, iv)
    else:
        iv = None
        cipher = DES.new(key, mode)

    if use_padding:
        plaintext = pad(plaintext, DES.block_size)

    ciphertext = cipher.encrypt(plaintext)
    return iv + ciphertext if mode == DES.MODE_CBC else ciphertext  # Возвращаем IV + шифротекст


def des_decrypt2(ciphertext, key, mode=DES.MODE_CBC, use_padding=True):
    key = adjust_key_parity(key)
    if mode == DES.MODE_CBC:
        iv = ciphertext[:DES.block_size]  # Извлекаем IV из начала
        ciphertext = ciphertext[DES.block_size:]  # Остальное — зашифрованные данные
        cipher = DES.new(key, mode, iv)
    else:
        cipher = DES.new(key, mode)

    decrypted = cipher.decrypt(ciphertext)
    if use_padding:
        try:
            return unpad(decrypted, DES.block_size)
        except ValueError:
            return decrypted
    return decrypted


def adjust_key_parity(key_bytes: bytes) -> bytes:
    """
    Приводит 8-байтовый ключ к корректному формату DES с чётным числом единиц в каждом байте.
    DES требует, чтобы каждый байт содержал нечётное количество единиц (odd parity).
    """
    result = bytearray()
    for byte in key_bytes:
        ones = bin(byte & 0xFE).count('1')
        parity_bit = 0 if ones % 2 else 1
        result.append((byte & 0xFE) | parity_bit)
    return bytes(result)


def test_semiweak_keys(message):
    """Comprehensive test of semi-weak key pairs with decryption and avalanche analysis"""
    print("\n" + "=" * 80)
    print("SEMI-WEAK KEY PAIRS TEST WITH DECRYPTION AND AVALANCHE ANALYSIS".center(80))
    print("=" * 80)

    if isinstance(message, str):
        message = message.encode('utf-8')

    # Semi-weak key pairs (K1, K2)
    semiweak_pairs = [
        (b'\x01\x1F\x01\x1F\x01\x0E\x01\x0E', b'\x1F\x01\x1F\x01\x0E\x01\x0E\x01'),
        (b'\x01\xE0\x01\xE0\x01\xF1\x01\xF1', b'\xE0\x01\xE0\x01\xF1\x01\xF1\x01'),
        (b'\x1F\xE0\x1F\xE0\x0E\xF1\x0E\xF1', b'\xE0\x1F\xE0\x1F\xF1\x0E\xF1\x0E'),
        (b'\x01\xFE\x01\xFE\x01\xFE\x01\xFE', b'\xFE\x01\xFE\x01\xFE\x01\xFE\x01')
    ]

    for i, (k1, k2) in enumerate(semiweak_pairs, 1):
        print(f"\n{' PAIR ' + str(i) + ' ':-^80}")
        print(f"K1: {format_hex(k1)}")
        print(f"K2: {format_hex(k2)}")

        # Pad the original message once
        padded_msg = pad(message, DES.block_size)

        # ===== Encryption Tests =====
        print("\n" + " Encryption Chain ".center(80, '~'))

        # First encryption (K2)
        cipher_k2 = des_encrypt(padded_msg, k2, use_padding=False)
        print(f"E_K2(x):     {format_hex(cipher_k2)}")

        # Second encryption (K1)
        cipher_k1_k2 = des_encrypt(cipher_k2, k1, use_padding=False)
        print(f"E_K1(E_K2):  {format_hex(cipher_k1_k2)}")

        # Compare with original (consider padding)
        match = cipher_k1_k2[:len(message)] == message
        print(f"\nVerification E_K1(E_K2(x)) = x:")
        print(f"Original:    {format_hex(message)}")
        print(f"Result:      {format_hex(cipher_k1_k2[:len(message)])}")
        print(f"Match:       {'YES' if match else 'NO'}")

        # ===== Decryption Tests =====
        print("\n" + " Decryption Tests ".center(80, '~'))

        # Decrypt with K2 should equal encrypt with K1
        cipher_k1 = des_encrypt(padded_msg, k1, use_padding=False)
        decrypt_k2 = des_decrypt(pad(message, DES.block_size), k2, use_padding=False)

        print(f"E_K1(x):     {format_hex(cipher_k1)}")
        print(f"D_K2(x):     {format_hex(decrypt_k2)}")
        print(f"Match:       {'YES' if cipher_k1 == decrypt_k2 else 'NO'}")

        # Full decryption cycle
        decrypted = des_decrypt(cipher_k2, k2, use_padding=True)
        print("\nFull decryption E_K2(x) with K2:")
        try:
            print(f"Decrypted:   {decrypted.decode('utf-8')}")
        except UnicodeDecodeError:
            print(f"Decrypted:   {format_hex(decrypted)} (binary)")

        # ===== Avalanche Effect Analysis =====
        print("\n" + " Avalanche Effect Analysis ".center(80, '~'))

        # Test positions: first bit of each byte
        bit_positions = [i * 8 for i in range(len(message))]
        if not bit_positions:  # Handle empty message
            bit_positions = [0]

        # Original encryption
        original_cipher = des_encrypt(padded_msg, k1, use_padding=False)

        for bit_pos in bit_positions[:5]:  # Limit to first 5 bits for readability
            modified_msg = flip_bit(padded_msg, bit_pos)
            modified_cipher = des_encrypt(modified_msg, k1, use_padding=False)

            diff_bits = sum(bin(o ^ m).count('1')
                            for o, m in zip(original_cipher, modified_cipher))
            total_bits = len(original_cipher) * 8

            print(f"Bit {bit_pos:2d}: {diff_bits:2d}/{total_bits} bits changed "
                  f"({diff_bits / total_bits:.1%}) | "
                  f"Changed bytes: {format_hex(bytes(o ^ m for o, m in zip(original_cipher, modified_cipher)))}")


def test_weak_keys(message):
    """Тестирование слабых ключей с шифрованием, дешифрованием и лавинным эффектом"""
    print("\n" + "=" * 80)
    print("КОРРЕКТНЫЙ ТЕСТ СЛАБЫХ КЛЮЧЕЙ (E(E(x)) = x) С АНАЛИЗОМ".center(80))
    print("=" * 80)

    original = message.encode('utf-8')
    padded_msg = pad(original, DES.block_size)

    for i, key in enumerate(WEAK_KEYS, 1):
        key = adjust_key_parity(key)
        print(f"\nСлабый ключ {i}: {format_hex(key)}")

        # Шифрование
        cipher = des_encrypt(original, key)
        print(f"Зашифровано: {format_hex(cipher)}")

        # Дешифрование
        decrypted = des_decrypt(cipher, key)
        print(f"Дешифровано: {decrypted.decode('utf-8', errors='replace')}")

        # Двойное шифрование
        cipher2 = des_encrypt(cipher, key)
        is_ok = cipher2.startswith(original)
        print(f"После двойного шифрования: {format_hex(cipher2)}")
        print(f"Соответствие оригиналу: {'ДА' if is_ok else 'НЕТ'}")

        print("\n" + " Анализ лавинного эффекта ".center(80, '~'))

        # Оригинальное шифрование
        original_cipher = des_encrypt(padded_msg, key, use_padding=False)

        # Тестируем изменение каждого бита в сообщении
        bit_positions = [i * 8 for i in range(len(padded_msg))]  # первый бит каждого байта
        if not bit_positions:  # на случай пустого сообщения
            bit_positions = [0]

        for bit_pos in bit_positions[:5]:  # ограничимся первыми 5 битами для читаемости
            modified_msg = flip_bit(padded_msg, bit_pos)
            modified_cipher = des_encrypt(modified_msg, key, use_padding=False)

            # Считаем количество измененных битов
            diff_bits = sum(bin(o ^ m).count('1')
                            for o, m in zip(original_cipher, modified_cipher))
            total_bits = len(original_cipher) * 8

            print(f"Бит {bit_pos:2d}: {diff_bits:2d}/{total_bits} бит изменено "
                  f"({diff_bits / total_bits:.1%}) | "
                  f"Измененные байты: {format_hex(bytes(o ^ m for o, m in zip(original_cipher, modified_cipher)))}")



def main():
    """Главное меню программы"""
    print("=" * 80)
    print("ПОЛНЫЙ АНАЛИЗ DES: ШИФРОВАНИЕ, ЛАВИННЫЙ ЭФФЕКТ И СЛАБЫЕ КЛЮЧИ".center(80))
    print("=" * 80)

    # Ввод данных
    name = input("Введите ваше имя и фамилию (для генерации ключа): ")
    message = input("Введите сообщение для анализа (или Enter для тестового): ") or "Тестовое сообщение для анализа DES"

    # Генерация ключа
    key = generate_key_from_name(name)
    print(f"\nСгенерированный ключ: {format_hex(key)}")
    print(f"Бинарное представление: {format_binary(key)}")

    # Разделение на блоки
    blocks = split_into_blocks(message.encode('utf-8'), DES.block_size)
    print("\nРазделение на блоки:")
    for i, block in enumerate(blocks, 1):
        print(f"Блок {i}: {format_hex(block)}")

    # Шифрование/дешифрование
    ciphertext = des_encrypt2(message.encode('utf-8'), key)
    decrypted = des_decrypt2(ciphertext, key)
    print("\nРезультаты шифрования:")
    print(f"Исходный текст: {message}")
    print(f"Шифротекст: {format_hex(ciphertext)}")
    print(f"Дешифрованный текст: {decrypted.decode('utf-8', errors='replace')}")

    # Оценка производительности
    enc_time, dec_time = measure_performance(message.encode('utf-8'), key)
    print(f"\nСреднее время шифрования: {enc_time:.4f} мс")
    print(f"Среднее время дешифрования: {dec_time:.4f} мс")

    print("\n" + " Анализ лавинного эффекта для сгенерированного ключа ".center(80, '='))

    original = message.encode('utf-8')
    padded_msg = pad(original, DES.block_size)
    original_cipher = des_encrypt2(padded_msg, key, use_padding=False)

    # Тестируем изменение каждого бита в сообщении
    bit_positions = [i * 8 for i in range(len(padded_msg))]  # первый бит каждого байта
    if not bit_positions:
        bit_positions = [0]

    print(f"Оригинальный шифротекст: {format_hex(original_cipher)}")
    print("\nИзменение одного бита в открытом тексте:")

    for bit_pos in bit_positions[:5]:  # первые 5 битов для наглядности
        modified_msg = flip_bit(padded_msg, bit_pos)
        modified_cipher = des_encrypt2(modified_msg, key, use_padding=False)

        diff_bits = sum(bin(o ^ m).count('1')
                        for o, m in zip(original_cipher, modified_cipher))
        total_bits = len(original_cipher) * 8

        print(f"Бит {bit_pos:2d}: {diff_bits:2d}/{total_bits} бит изменено "
              f"({diff_bits / total_bits:.1%}) | "
              f"Измененные байты: {format_hex(bytes(o ^ m for o, m in zip(original_cipher, modified_cipher)))}")


    # Анализ слабых и полуслабых ключей
    test_weak_keys(message)
    test_semiweak_keys(message)



if __name__ == "__main__":
    main()