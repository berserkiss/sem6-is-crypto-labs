namespace L3;

class NumberTheory
{
    // Алгоритм Евклида для нахождения НОД
    public static long GCD(long a, long b)
    {
        while (b != 0)
        {
            long temp = b;
            b = a % b;
            a = temp;
        }

        return a;
    }

    // НОД для трех чисел
    public static long GCD(long a, long b, long c)
    {
        return GCD(a, GCD(b, c));
    }

    // Решето Эратосфена: поиск простых чисел до n
    public static List<long> GetPrimes(long n)
    {
        List<long> primes = new List<long>();
        bool[] isPrime = new bool[n + 1];
        Array.Fill(isPrime, true);
        isPrime[0] = isPrime[1] = false;

        for (long i = 2; i <= n; i++)
        {
            if (isPrime[i])
            {
                primes.Add(i);
                for (long j = i * i; j <= n; j += i)
                    isPrime[j] = false;
            }
        }

        return primes;
    }

    // Проверка, является ли число простым
    public static bool IsPrime(long num)
    {
        if (num < 2) return false;
        for (long i = 2; i * i <= num; i++)
            if (num % i == 0)
                return false;
        return true;
    }

    // Поиск простых чисел в интервале [m, n]
    public static List<long> GetPrimesInRange(long m, long n)
    {
        List<long> primes = new List<long>();
        for (long i = m; i <= n; i++)
        {
            if (IsPrime(i)) primes.Add(i);
        }

        return primes;
    }

    // Оценочное количество простых чисел
    public static double ApproximatePrimeCount(long n)
    {
        return n / Math.Log(n);
    }

    // Каноническое разложение
    public static string CanonicalForm(long number)
    {
        long num = number;
        string result = "";
        for (long i = 2; i * i <= number; i++)
        {
            int count = 0;
            while (num % i == 0)
            {
                num /= i;
                count++;
            }

            if (count > 0)
                result += (result.Length > 0 ? " * " : "") + i + (count > 1 ? "^" + count : "");
        }

        if (num > 1) result += (result.Length > 0 ? " * " : "") + num;
        return result;
    }

    // Конкатенация чисел
    public static long ConcatNumbers(long m, long n)
    {
        return long.Parse(m.ToString() + n.ToString());
    }
}