using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
public class Entropy
{
    // Чтение текста из файла
    public static string ReadFromFile(string filePath)
    {
        if (!File.Exists(filePath))
        {
            Console.WriteLine($"Файл {filePath} не найден.");
            return "";
        }
        return File.ReadAllText(filePath, Encoding.UTF8).ToLower();
    }

    // Получение частоты символов
    public static Dictionary<char, int> GetSymbolFrequencies(string text)
    {
        Dictionary<char, int> frequencies = new Dictionary<char, int>();
        foreach (char c in text)
        {
            if (char.IsLetterOrDigit(c)) // Учитываем только буквы и цифры
            {
                if (frequencies.ContainsKey(c))
                    frequencies[c]++;
                else
                    frequencies[c] = 1;
            }
        }
        return frequencies;
    }

    // Расчет вероятностей для символов
    public static Dictionary<char, double> GetSymbolProbabilities(string text)
    {
        var frequencies = GetSymbolFrequencies(text);
        double totalCount = text.Length;
        Dictionary<char, double> probabilities = frequencies.ToDictionary(
            pair => pair.Key, 
            pair => pair.Value / totalCount);
        return probabilities;
    }

    // Рассчитываем энтропию текста
    public static double GetShannonEntropy(string text)
    {
        var probabilities = GetSymbolProbabilities(text);
        double entropy = 0;
        foreach (var prob in probabilities.Values)
        {
            if (prob > 0) // Логарифм от нуля не существует
                entropy -= prob * Math.Log2(prob); // Энтропия = -Σ p(x) * log2(p(x))
        }
        return Math.Round(entropy, 3); // Округляем до 3 знаков
    }

    // Рассчитываем количество информации (для текста без ошибок)
    public static double GetInformationAmount(string text)
    {
        double entropy = GetShannonEntropy(text);
        return entropy * text.Length;
    }

    // Функция для расчета количества информации с учетом ошибок
    public static double GetInformationAmountWithErrors(string text, double errorProbability)
    {
        // Получаем энтропию текста
        double entropy = GetShannonEntropy(text);

        // Проверка на крайние случаи P = 0 или P = 1
        if (errorProbability == 0 || errorProbability == 1)
        {
            return entropy * text.Length; // Без ошибок, обычная информация
        }
        // Рассчитываем корректированное количество информации с учетом ошибок
        double effectiveError = -(errorProbability * Math.Log2(errorProbability) + (1 - errorProbability) * Math.Log2(1 - errorProbability));

        // Формула: количество информации = длина текста * (энтропия - эффективная ошибка)
        double informationAmount = text.Length * (entropy - effectiveError);

        return Math.Round(informationAmount, 3); // Округляем до 3 знаков
    }
        

    // Метод для вывода частоты символов
    public static void PrintSymbolFrequencies(string text)
    {
        var frequencies = GetSymbolFrequencies(text);
        Console.WriteLine("Частоты символов:");
        foreach (var pair in frequencies)
        {
            Console.WriteLine($"Символ: {pair.Key}, Частота: {(double)pair.Value / text.Length:F4}");
        }
    }
}