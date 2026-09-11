import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import re

alphabet = list("абвгдеёжзійклмнопрстуўфхцчшыьэюя")
digraphs = ["дж", "дз"]  # Диграфы белорусского языка


# Декоратор для замера времени выполнения
def time_it(func):
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        result = func(*args, **kwargs)
        elapsed_time = datetime.now() - start_time
        print(f"Время выполнения {func.__name__}: {elapsed_time}")
        return result

    return wrapper


def prepare_alphabet(keyword: str, shift: int = 2):
    """Формирует алфавит с ключевым словом + применяет сдвиг"""
    unique_chars = ''.join(dict.fromkeys(keyword))  # Удаление повторов
    remaining_letters = [char for char in alphabet if char not in unique_chars]
    key_alphabet = unique_chars + ''.join(remaining_letters)
    return key_alphabet[shift:] + key_alphabet[:shift]


@time_it
def caesar_encrypt(keyword: str, text: str, shift: int = 2):
    """Шифрование Цезаря с ключевым словом"""
    key_alphabet = prepare_alphabet(keyword, shift)
    trans_table = str.maketrans(''.join(alphabet), key_alphabet)
    return text.translate(trans_table)


@time_it
def caesar_decrypt(keyword: str, text: str, shift: int = 2):
    """Дешифрование Цезаря"""
    key_alphabet = prepare_alphabet(keyword, shift)
    trans_table = str.maketrans(key_alphabet, ''.join(alphabet))
    return text.translate(trans_table)


# Таблица Трисемуса
def create_trithemius_table(keyword: str):
    """Создаёт таблицу Трисемуса (размер 4×8)"""
    key_alphabet = ''.join(dict.fromkeys(keyword)) + ''.join([c for c in alphabet if c not in keyword])
    return np.array(list(key_alphabet)).reshape(4, 8)


@time_it
def trithemius_encrypt(keyword: str, text: str):
    """Шифрование Трисемуса"""
    table = create_trithemius_table(keyword)
    encrypted_text = ""

    for char in text:
        pos = np.where(table == char)
        if pos[0].size > 0:
            i, j = pos[0][0], pos[1][0]
            new_i = (i + 1) % table.shape[0]
            encrypted_text += table[new_i, j]
        else:
            encrypted_text += char

    return encrypted_text


@time_it
def trithemius_decrypt(keyword: str, text: str):
    """Дешифрование Трисемуса"""
    table = create_trithemius_table(keyword)
    decrypted_text = ""

    for char in text:
        pos = np.where(table == char)
        if pos[0].size > 0:
            i, j = pos[0][0], pos[1][0]
            new_i = (i - 1) % table.shape[0]
            decrypted_text += table[new_i, j]
        else:
            decrypted_text += char

    return decrypted_text


def get_letter_frequencies(text: str):
    """Подсчёт частот символов"""
    return {char: text.count(char) for char in set(text) if char in alphabet}


def plot_histograms(original_text, caesar_text, trithemius_text, caesar_decrypted, trithemius_decrypted):
    """Строит гистограммы частот символов для всех вариантов текста"""
    fig, axs = plt.subplots(5, 1, figsize=(12, 20))

    for ax, text, title, color in zip(
            axs,
            [original_text, caesar_text, trithemius_text, caesar_decrypted, trithemius_decrypted],
            ["Исходный текст", "Шифр Цезаря (зашифр.)", "Шифр Трисемуса (зашифр.)",
             "Шифр Цезаря (расшифр.)", "Шифр Трисемуса (расшифр.)"],
            ["green", "orange", "blue", "lime", "cyan"]
    ):
        freq = get_letter_frequencies(text)
        sorted_keys = sorted(freq.keys(), key=lambda x: alphabet.index(x))
        sorted_values = [freq[k] for k in sorted_keys]

        ax.bar(sorted_keys, sorted_values, color=color)
        ax.set_title(title, fontsize=12, pad=10)
        ax.set_xlabel("Символы", fontsize=10)
        ax.set_ylabel("Частота", fontsize=10)
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        # Добавляем значения сверху столбцов
        for i, v in enumerate(sorted_values):
            ax.text(i, v + 0.5, str(v), ha='center', va='bottom', fontsize=8)

    plt.tight_layout()
    plt.savefig('frequency_histograms_all.png', dpi=300)
    plt.show()


def plot_trithemius_table(keyword: str):
    """Визуализация таблицы Трисемуса"""
    table = create_trithemius_table(keyword)

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_title("Таблица Трисемуса", fontsize=14, pad=15)
    ax.axis('off')

    # Создаем таблицу
    table_plot = ax.table(cellText=table,
                          loc='center',
                          cellLoc='center')

    # Настройка стиля таблицы
    table_plot.auto_set_font_size(False)
    table_plot.set_fontsize(12)
    table_plot.scale(1, 2)

    # Цветовые стили
    for (i, j), cell in table_plot.get_celld().items():
        if i == 0:
            cell.set_facecolor('#ffcccc')  # Заголовок
        cell.set_edgecolor('gray')

    plt.tight_layout()
    plt.savefig('trithemius_table.png', dpi=300)
    plt.show()


def plot_letter_distribution(texts, labels):
    """Сравнительное распределение букв в разных текстах"""
    plt.figure(figsize=(14, 8))

    for text, label in zip(texts, labels):
        freq = get_letter_frequencies(text)
        sorted_keys = sorted(freq.keys(), key=lambda x: alphabet.index(x))
        sorted_values = [freq[k] for k in sorted_keys]
        plt.plot(sorted_keys, sorted_values, 'o-', label=label, markersize=5)

    plt.title("Сравнение распределения букв", fontsize=14)
    plt.xlabel("Буквы", fontsize=12)
    plt.ylabel("Частота", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=10)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('letter_distribution_comparison.png', dpi=300)
    plt.show()


caesar_keyword = "інфарматыка"
trithemius_keyword = "ганна"

with open('text.txt', encoding='utf8') as file:
    text = file.read().lower()

# Обработка диграфов (дж, дз)
for digraph in digraphs:
    text = re.sub(digraph, f"{digraph[0]}{digraph[1]}", text)

# Выполнение шифрования и дешифрования
print("\n[Шифр Цезаря]")
caesar_encrypted = caesar_encrypt(caesar_keyword, text)
print(f" Зашифрованный текст (фрагмент): {caesar_encrypted[:1000]}")

caesar_decrypted = caesar_decrypt(caesar_keyword, caesar_encrypted)
print(f" Расшифрованный текст (фрагмент): {caesar_decrypted[:1000]}")

print("\n[Шифр Трисемуса]")
trithemius_encrypted = trithemius_encrypt(trithemius_keyword, text)
print(f" Зашифрованный текст (фрагмент): {trithemius_encrypted[:1000]}")

trithemius_decrypted = trithemius_decrypt(trithemius_keyword, trithemius_encrypted)
print(f" Расшифрованный текст (фрагмент): {trithemius_decrypted[:1000]}")

# Построение диаграмм
print("\n[Визуализация данных]")
plot_histograms(text, caesar_encrypted, trithemius_encrypted, caesar_decrypted, trithemius_decrypted)
plot_trithemius_table(trithemius_keyword)
plot_letter_distribution([text, caesar_encrypted, trithemius_encrypted, caesar_decrypted, trithemius_decrypted],
                         ["Оригинал", "Цезарь (заш.)", "Трисемус (заш.)", "Цезарь (расш.)", "Трисемус (расш.)"])