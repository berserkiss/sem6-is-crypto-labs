class Program
{
    static void Main()
    {

        var myNameKazakh = Entropy.ReadFromFile("./my_name_kazakh.txt");
        var myNameEnglish = Entropy.ReadFromFile("./my_name_english.txt");
        var myNameASCII = Entropy.ReadFromFile("./my_name_ASCII.txt");

        string kazakhText = Entropy.ReadFromFile("./text_on_kazakh.txt");
        string englishText = Entropy.ReadFromFile("./text_on_english.txt");
        string binaryText = Entropy.ReadFromFile("./text_on_binary.txt");

        // Вывод частоты символов
        Entropy.PrintSymbolFrequencies(kazakhText);
        Console.WriteLine("\n");
        Entropy.PrintSymbolFrequencies(englishText);
        Console.WriteLine("\n");

        // Вычисление энтропии для текстов
        Console.WriteLine("Энтропия казахского текста: " + Entropy.GetShannonEntropy(kazakhText));
        Console.WriteLine("Энтропия английского текста: " + Entropy.GetShannonEntropy(englishText));
        Console.WriteLine("Энтропия бинарного текста: " + Entropy.GetShannonEntropy(binaryText));

        // Вычисление количества информации
        Console.WriteLine("\nЕсли P = 0:");
        Console.WriteLine("Количество информации (казахский): " + Entropy.GetInformationAmount(myNameKazakh));
        Console.WriteLine("Количество информации (английский): " + Entropy.GetInformationAmount(myNameEnglish));
        Console.WriteLine("Количество информации (ASCII): " + Entropy.GetInformationAmount(myNameASCII));

        // Вычисление количества информации с учетом ошибок
        double[] errorRates = { 0.1, 0.5, 1.0 };
        foreach (double p in errorRates)
        {
            Console.WriteLine($"Если P = {p}:");
            Console.WriteLine("Количество информации (ASCII): " + Entropy.GetInformationAmountWithErrors(myNameASCII, p));
            Console.WriteLine();
        }
    }
}