using System;
using System.Collections.Generic;
using System.Linq;
namespace L3;
class Program
{
    static void Main()
    {
        // Ввод чисел
        Console.WriteLine("НОД трех чисел");
        Console.Write("Введите первое число: ");
        long a = long.Parse(Console.ReadLine());
        Console.Write("Введите второе число: ");
        long b = long.Parse(Console.ReadLine());
        Console.Write("Введите третье число: ");
        long c = long.Parse(Console.ReadLine());
        Console.WriteLine($"НОД трех чисел: {NumberTheory.GCD(a, b, c)}\n");
        

        // Поиск простых чисел
        Console.WriteLine("Поиск простых чисел");
        Console.Write("Введите нижнюю границу: ");
        long m = long.Parse(Console.ReadLine());
        Console.Write("Введите верхнюю границу: ");
        long n = long.Parse(Console.ReadLine());
        
        // НОД (m, n)
        Console.WriteLine($"НОД ({m}, {n}): {NumberTheory.GCD(m, n)}");

        List<long> primesBetween = NumberTheory.GetPrimesInRange(m, n);
        Console.WriteLine($"Простые числа в интервале [{m}, {n}]: {string.Join(", ", primesBetween)}\n");

        // Поиск простых чисел от 2 до n
        Console.WriteLine($"Поиск простых чисел в интервале [2, {n}]");
        List<long> primesToN = NumberTheory.GetPrimes(n);
        Console.WriteLine($"Количество простых чисел в интервале: {primesToN.Count}");
        Console.WriteLine($"Простые числа в интервале [{m}, {n}]: {string.Join(", ", primesToN)}\n");
        Console.WriteLine($"n/ln(n): {NumberTheory.ApproximatePrimeCount(n)}\n");

        // Простые числа в интервале [m, n]
        Console.WriteLine($"Поиск простых чисел в интервале [{m}, {n}]");
        Console.WriteLine($"Количество простых чисел в интервале: {primesBetween.Count}\n");
       

        // Каноническое разложение чисел
        Console.WriteLine("Числа в виде произведения простых множителей");
        Console.WriteLine($"Простые множители n: {n} = {NumberTheory.CanonicalForm(n)}");
        Console.WriteLine($"Простые множители m: {m} = {NumberTheory.CanonicalForm(m)}\n");

        // Проверка на простоту конкатенации m || n
        long concatenated = NumberTheory.ConcatNumbers(m, n);
        Console.WriteLine($"Является ли число, состоящее из конкатенации цифр m || n ({m}{n}) простым: {NumberTheory.IsPrime(concatenated)}\n");

       
    }
}

