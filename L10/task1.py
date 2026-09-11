import time
import matplotlib.pyplot as plt
from sympy import isprime, nextprime
from secrets import randbits


# Возвращает случайное простое число длины `bits` бит
def generate_large_prime(bits):
    while True:
        candidate = randbits(bits)
        candidate |= (1 << bits - 1) | 1  # Убедимся, что это число с заданной длиной и нечётное
        if isprime(candidate):
            return candidate


# Выбор значений a
a_values = [7, 19]

# Выбор значений x — простые числа, равномерно распределённые от 10^3 до 10^100
x_values = [10 ** i for i in range(3, 101, 10)]
x_primes = [nextprime(x) for x in x_values[:6]]  # Берем 6 значений

# Генерация модулей n длиной 1024 и 2048 бит
n_1024 = generate_large_prime(1024)
n_2048 = generate_large_prime(2048)

# Измерим время выполнения pow(a, x, n) для разных a, x и n
results = {"1024-bit": {}, "2048-bit": {}}

for a in a_values:
    times_1024 = []
    times_2048 = []
    for x in x_primes:
        # Для модуля 1024 бит
        start = time.time()
        y = pow(a, x, n_1024)
        end = time.time()
        times_1024.append(end - start)

        # Для модуля 2048 бит
        start = time.time()
        y = pow(a, x, n_2048)
        end = time.time()
        times_2048.append(end - start)

    results["1024-bit"][a] = times_1024
    results["2048-bit"][a] = times_2048

# Построение графиков
fig, ax = plt.subplots(1, 2, figsize=(14, 6))

x_labels = [f"10^{i}" for i in range(3, 3 + 10 * len(x_primes), 10)]

for a in a_values:
    ax[0].plot(x_labels, results["1024-bit"][a], label=f"a = {a}")
    ax[1].plot(x_labels, results["2048-bit"][a], label=f"a = {a}")

ax[0].set_title("Время вычисления y = a^x mod n (n = 1024 бита)")
ax[0].set_xlabel("x (порядок 10^i)")
ax[0].set_ylabel("Время (сек)")
ax[0].legend()
ax[0].grid(True)

ax[1].set_title("Время вычисления y = a^x mod n (n = 2048 бит)")
ax[1].set_xlabel("x (порядок 10^i)")
ax[1].set_ylabel("Время (сек)")
ax[1].legend()
ax[1].grid(True)

plt.tight_layout()
plt.show()
