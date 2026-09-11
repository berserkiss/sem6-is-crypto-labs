class LinearCongruentialGenerator:
    def __init__(self, seed):
        self.seed = seed
        self.a = 421
        self.c = 1663
        self.n = 7875

    def next(self):
        self.seed = (self.a * self.seed + self.c) % self.n
        return self.seed

    def generate_sequence(self, count):
        return [self.next() for _ in range(count)]



if __name__ == "__main__":
    print("Линейный конгруэнтный генератор ПСП")
    print("Параметры генератора: a=421, c=1663, n=7875")

    while True:
        try:
            seed = int(input("Введите начальное значение (зерно) для генератора: "))
            break
        except ValueError:
            print("Ошибка! Пожалуйста, введите целое число.")


    while True:
        try:
            count = int(input("Введите количество чисел для генерации: "))
            if count > 0:
                break
            else:
                print("Число должно быть положительным!")
        except ValueError:
            print("Ошибка! Пожалуйста, введите целое число.")


    lcg = LinearCongruentialGenerator(seed=seed)
    sequence = lcg.generate_sequence(count)
    print("\nСгенерированная последовательность:")
    for i, num in enumerate(sequence, 1):
        print(f"{i}: {num}")