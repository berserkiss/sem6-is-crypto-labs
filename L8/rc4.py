import time
import matplotlib.pyplot as plt


class RC4:
    def __init__(self, key):
        """
        Инициализация генератора RC4 с заданным ключом
        :param key: список чисел от 0 до 255 (ключ)
        """
        self.S = list(range(256))
        self.i = self.j = 0
        self.key = key
        self.initial_S = self.S.copy()  # Сохраняем начальное состояние S-блока
        self.key_scheduling()
        self.initialized_S = self.S.copy()  # Сохраняем состояние после инициализации

    def print_key_info(self):
        """Вывод информации о ключе"""
        print("\n" + "=" * 50)
        print("Информация о ключе RC4:")
        print(f"Исходный ключ (десятичный): {self.key}")
        print(f"Длина ключа: {len(self.key)} байт")
        print("Повторенный ключ (для KSA):",
              [self.key[i % len(self.key)] for i in range(256)][:32], "...")

    def print_sbox_init(self):
        """Вывод процесса инициализации S-блока"""
        print("\n" + "=" * 50)
        print("Инициализация таблицы замен (S-блока):")

        print("\n1. Начальное состояние S-блока:")
        self.print_sbox(self.initial_S)

        print("\n2. После перемешивания (первые 32 байта):")
        self.print_sbox(self.initialized_S, limit=32)

        print("\n3. Изменения в S-блоке (первые 32 байта):")
        changes = [(i, self.initial_S[i], self.initialized_S[i])
                   for i in range(32) if self.initial_S[i] != self.initialized_S[i]]
        for i, old, new in changes:
            print(f"  S[{i}]: {old} → {new}")

    @staticmethod
    def print_sbox(sbox, limit=256):
        """Печать S-блока"""
        for i in range(0, limit, 16):
            print(f"{i:3d}-{i + 15:3d}:", " ".join(f"{x:3d}" for x in sbox[i:i + 16]))

    def key_scheduling(self):
        """Алгоритм планирования ключа (KSA)"""
        j = 0
        for i in range(256):
            j = (j + self.S[i] + self.key[i % len(self.key)]) % 256
            self.S[i], self.S[j] = self.S[j], self.S[i]

    def generate_byte(self):
        """Генерация одного псевдослучайного байта (PRGA)"""
        self.i = (self.i + 1) % 256
        self.j = (self.j + self.S[self.i]) % 256
        self.S[self.i], self.S[self.j] = self.S[self.j], self.S[self.i]
        return self.S[(self.S[self.i] + self.S[self.j]) % 256]

    def crypt(self, data):
        """Шифрование/расшифрование данных"""
        if isinstance(data, str):
            data = data.encode('utf-8')

        result = bytearray()
        for byte in data:
            result.append(byte ^ self.generate_byte())
        return bytes(result)


def main():

    key = [13, 19, 90, 92, 240]
    rc4 = RC4(key)

    rc4.print_key_info()
    rc4.print_sbox_init()

    print("\n" + "=" * 50)
    message = input("Введите сообщение для шифрования: ")

    encrypted = rc4.crypt(message)
    print(f"\nЗашифрованное сообщение (hex): {encrypted.hex()}")

    rc4_decrypt = RC4(key)
    decrypted = rc4_decrypt.crypt(encrypted)
    print(f"Расшифрованное сообщение: {decrypted.decode('utf-8')}")

    print("\n" + "=" * 50)
    print("Оценка производительности генерации ПСП...")

    test_sizes = [1024 * (2 ** i) for i in range(0, 11)]  # 1KB до 10MB
    speeds = []

    for size in test_sizes:
        rc4_test = RC4(key)
        start_time = time.time()

        for _ in range(size):
            rc4_test.generate_byte()

        elapsed = time.time() - start_time
        speed = size / elapsed if elapsed > 0 else float('inf')
        speeds.append(speed)

    # Вывод результатов
    print("\nРезультаты производительности:")
    for size, speed in zip(test_sizes, speeds):
        print(f"  {size // 1024} KB: {speed / 1024:.2f} KB/сек")

    # Построение графика
    plt.figure(figsize=(10, 6))
    plt.plot(test_sizes, speeds, 'b-o')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Размер данных (байт)')
    plt.ylabel('Скорость генерации (байт/сек)')
    plt.title('Производительность RC4')
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()