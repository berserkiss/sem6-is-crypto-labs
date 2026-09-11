import matplotlib.pyplot as plt
from collections import Counter


class FrequencyAnalyzer:
    def __init__(self):
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def analyze(self, text):
        """Анализирует частоту символов в тексте"""
        filtered = [c.upper() for c in text if c.upper() in self.alphabet]
        counter = Counter(filtered)
        total = len(filtered)
        return {char: count / total for char, count in counter.items()}

    def plot_frequencies(self, original_freq, encrypted_freq, title=""):
        """Строит сравнительные графики частот"""
        plt.figure(figsize=(12, 6))

        # Упорядочиваем буквы по алфавиту для красивого графика
        letters = sorted(self.alphabet)
        orig_values = [original_freq.get(l, 0) for l in letters]
        encr_values = [encrypted_freq.get(l, 0) for l in letters]

        bar_width = 0.35
        index = range(len(letters))

        plt.bar(index, orig_values, bar_width, label='Исходный текст')
        plt.bar([i + bar_width for i in index], encr_values, bar_width, label='Шифртекст')

        plt.xlabel('Буквы')
        plt.ylabel('Частота')
        plt.title(title)
        plt.xticks([i + bar_width / 2 for i in index], letters)
        plt.legend()
        plt.tight_layout()
        plt.show()


class EnigmaMachine:
    def __init__(self):
        self.rotors = [
            {
                'wiring': "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
                'notch': "V",
                'position': 0
            },
            {
                'wiring': "FKQHTLXOCBJSPDZRAMEWNIUYGV",
                'notch': "E",
                'position': 0
            },
            {
                'wiring': "LEYJVCNIXWPBQMDRTAKZGFUHOS",
                'notch': "Q",
                'position': 0
            }
        ]
        self.reflector = {
            'A': 'E', 'E': 'A',
            'B': 'N', 'N': 'B',
            'C': 'K', 'K': 'C',
            'D': 'Q', 'Q': 'D',
            'F': 'U', 'U': 'F',
            'G': 'Y', 'Y': 'G',
            'H': 'W', 'W': 'H',
            'I': 'J', 'J': 'I',
            'L': 'O', 'O': 'L',
            'M': 'P', 'P': 'M',
            'R': 'X', 'X': 'R',
            'S': 'Z', 'Z': 'S',
            'T': 'V', 'V': 'T'
        }
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def set_positions(self, l, m, r):
        self.rotors[0]['position'] = self.alphabet.index(l.upper())
        self.rotors[1]['position'] = self.alphabet.index(m.upper())
        self.rotors[2]['position'] = self.alphabet.index(r.upper())

    def rotate_rotors(self):
        # Всегда поворачиваем правый ротор
        self.rotors[2]['position'] = (self.rotors[2]['position'] + 1) % 26

        # Проверяем выемки для каскадного поворота
        if self.rotors[2]['position'] == self.alphabet.index(self.rotors[2]['notch']):
            self.rotors[1]['position'] = (self.rotors[1]['position'] + 1) % 26

            if self.rotors[1]['position'] == self.alphabet.index(self.rotors[1]['notch']):
                self.rotors[0]['position'] = (self.rotors[0]['position'] + 1) % 26

    def encrypt_char(self, c):
        c = c.upper()
        if c not in self.alphabet:
            return c

        self.rotate_rotors()

        signal = self.alphabet.index(c)

        # Прямой проход L → M → R
        signal = self.rotors[0]['wiring'][signal]
        signal = self.rotors[1]['wiring'][self.alphabet.index(signal)]
        signal = self.rotors[2]['wiring'][self.alphabet.index(signal)]

        # Отражатель
        signal = self.reflector.get(signal, signal)

        # Обратный проход R → M → L
        signal = self.alphabet[self.rotors[2]['wiring'].index(signal)]
        signal = self.alphabet[self.rotors[1]['wiring'].index(signal)]
        signal = self.alphabet[self.rotors[0]['wiring'].index(signal)]

        return signal

    def encrypt_text(self, text):
        return ''.join([self.encrypt_char(c) for c in text.upper()])


# Пример использования
if __name__ == "__main__":
    # Создаем машину Enigma
    enigma = EnigmaMachine()
    enigma.set_positions('A', 'A', 'A')

    print("Original text:\n")

    original_text = "P"
    print(original_text)
    encrypted_text = enigma.encrypt_text(original_text)
    print("Encrypted text:\n")
    print(encrypted_text)

    print("Decrypted text:\n")
    encrypted_text = enigma.encrypt_text(encrypted_text)
    print(encrypted_text)
    analyzer = FrequencyAnalyzer()
    orig_freq = analyzer.analyze(original_text)
    encr_freq = analyzer.analyze(encrypted_text)

    # Вывод результатов
    print("Частоты в исходном тексте:")
    print(orig_freq)
    print("\nЧастоты в шифртексте:")
    print(encr_freq)

    # Построение графиков
    analyzer.plot_frequencies(orig_freq, encr_freq,
                              "Сравнение частот символов")


