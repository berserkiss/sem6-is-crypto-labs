import time
import sys
import matplotlib.pyplot as plt


def plot_frequency_histogram(text, title):
    """Строит гистограмму частот символов в тексте"""
    freq = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1

    chars = sorted(freq.keys())
    counts = [freq[char] for char in chars]

    plt.figure(figsize=(12, 6))
    plt.bar(chars, counts)
    plt.title(title)
    plt.xlabel("Символы")
    plt.ylabel("Частота")
    plt.grid(True, axis='y')
    plt.show()


def route_transposition_encrypt(text, columns):
    padding = columns - (len(text) % columns)
    if padding != columns:
        text += 'X' * padding

    rows = len(text) // columns
    table = [['' for _ in range(columns)] for _ in range(rows)]
    index = 0

    for col in range(columns):
        for row in range(rows):
            table[row][col] = text[index]
            index += 1

    result = []
    for row in range(rows):
        for col in range(columns):
            result.append(table[row][col])

    return ''.join(result)


def route_transposition_decrypt(text, columns):
    rows = len(text) // columns
    table = [['' for _ in range(columns)] for _ in range(rows)]
    index = 0

    for row in range(rows):
        for col in range(columns):
            table[row][col] = text[index]
            index += 1

    result = []
    for col in range(columns):
        for row in range(rows):
            result.append(table[row][col])

    return ''.join(result).rstrip('X')


def multiple_permutation_encrypt(text, column_key, row_key):
    column_order = get_key_order(column_key)
    row_order = get_key_order(row_key)

    rows = len(row_order)
    cols = len(column_order)
    total_cells = rows * cols

    if len(text) < total_cells:
        text = text.ljust(total_cells, ' ')

    table = [[text[i * cols + j] if (i * cols + j) < len(text) else ' ' for j in range(cols)] for i in range(rows)]

    row_permuted_table = [[None for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        new_row = row_order.index(i + 1)
        for j in range(cols):
            row_permuted_table[new_row][j] = table[i][j]

    column_permuted_table = [[None for _ in range(cols)] for _ in range(rows)]
    for j in range(cols):
        new_col = column_order.index(j + 1)
        for i in range(rows):
            column_permuted_table[i][new_col] = row_permuted_table[i][j]

    result = []
    for i in range(rows):
        for j in range(cols):
            result.append(column_permuted_table[i][j])

    return ''.join(result).strip()


def multiple_permutation_decrypt(text, column_key, row_key):
    column_order = get_key_order(column_key)
    row_order = get_key_order(row_key)

    rows = len(row_order)
    cols = len(column_order)
    total_cells = rows * cols

    if len(text) < total_cells:
        text = text.ljust(total_cells, ' ')

    table = [[text[i * cols + j] for j in range(cols)] for i in range(rows)]

    column_unpermuted_table = [[None for _ in range(cols)] for _ in range(rows)]
    for j in range(cols):
        original_col = column_order[j] - 1
        for i in range(rows):
            column_unpermuted_table[i][original_col] = table[i][j]

    row_unpermuted_table = [[None for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        original_row = row_order[i] - 1
        for j in range(cols):
            row_unpermuted_table[original_row][j] = column_unpermuted_table[i][j]

    result = []
    for i in range(rows):
        for j in range(cols):
            result.append(row_unpermuted_table[i][j])

    return ''.join(result).strip()


def get_key_order(key):
    char_positions = [(char, idx) for idx, char in enumerate(key)]
    sorted_chars = sorted(char_positions, key=lambda x: (x[0], x[1]))
    order = [0] * len(key)
    for new_pos, (char, original_pos) in enumerate(sorted_chars, 1):
        order[original_pos] = new_pos
    return order


def main():
    print("Маршрутная перестановка (белорусский алфавит)")
    text = input("Введите текст для шифрования: ").upper()
    if not text:
        with open("./input.txt", "r", encoding="utf-8") as f:
            text = f.read().upper()

    # Построение гистограммы исходного текста
    plot_frequency_histogram(text, "Частота символов в исходном тексте")

    print("Введите количество столбцов: ")
    columns = int(input())

    # Маршрутная перестановка
    start_time = time.time()
    encrypted_route = route_transposition_encrypt(text, columns)
    encr_time = time.time() - start_time
    print("Зашифрованный текст (маршрутно): " + encrypted_route)
    plot_frequency_histogram(encrypted_route, "Частота символов после маршрутного шифрования")

    start_time = time.time()
    decrypted_route = route_transposition_decrypt(encrypted_route, columns)
    decr_time = time.time() - start_time
    print("Расшифрованный текст (маршрутно): " + decrypted_route)
    plot_frequency_histogram(decrypted_route, "Частота символов после маршрутного расшифрования")

    # Множественная перестановка
    print("\nШифр множественной перестановки")
    column_key = "ГаннаГаннаГаннаГанна"
    row_key = "ПузыроваПузырова"

    print(f"Ключ для столбцов: {column_key}")
    print(f"Ключ для строк: {row_key}")

    start_time = time.time()
    encrypted_multiple = multiple_permutation_encrypt(text, column_key, row_key)
    encr_time = time.time() - start_time
    print(f"\nЗашифрованный текст (множественно): {encrypted_multiple}")
    plot_frequency_histogram(encrypted_multiple, "Частота символов после множественного шифрования")

    start_time = time.time()
    decrypted_multiple = multiple_permutation_decrypt(encrypted_multiple, column_key, row_key)
    decr_time = time.time() - start_time
    print(f"Расшифрованный текст (множественно): {decrypted_multiple}")
    plot_frequency_histogram(decrypted_multiple, "Частота символов после множественного расшифрования")

    print(f"\nВремя зашифрования маршрутного: {encr_time:.6f} сек")
    print(f"Время дешифрования маршрутного: {decr_time:.6f} сек")
    print(f"Время зашифрования множественного: {encr_time:.6f} сек")
    print(f"Время дешифрования множественного: {decr_time:.6f} сек")


if __name__ == "__main__":
    main()