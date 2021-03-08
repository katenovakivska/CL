from collections import Counter
import docx
import numpy as np
import matplotlib.pyplot as plt
from nltk import ngrams
import re


letters = ["а", "б", "в", "г", "д", "е", "є", "ж", "з", "и", "і", "ї", "й", "к", "л", "м", "н",
           "о", "п", "р", "с", "т","у", "ф", "х", "ц", "ч", "ш", "щ", "ь", "ю", "я"]
ukrLettersFrequencies = {"а": 0.0807, "б": 0.0177, "в": 0.0535, "г": 0.0155, "д": 0.0338, "е": 0.0495, "є": 0.0061, "ж": 0.0093, "з": 0.0232,
                     "и": 0.0626, "і": 0.0575, "ї": 0.0065, "й": 0.0138, "к": 0.0354, "л": 0.0369, "м": 0.0303, "н": 0.0681, "о": 0.0942,
                     "п": 0.0290, "р": 0.0448, "с": 0.0424, "т": 0.0535, "у": 0.0336, "ф": 0.0028, "х": 0.0119, "ц": 0.0083, "ч": 0.0141,
                     "ш": 0.0076, "щ": 0.0056, "ь": 0.0177, "ю": 0.0093, "я": 0.0248}

#отримання тексту з файлу розширення .docx
def readText(fileName):
    document = docx.Document(fileName)
    documentText = '\n\n'.join(paragraph.text for paragraph in document.paragraphs)
    documentText = re.sub(r'[^\w\s]', '', documentText).lower();
    print("Кількість символів у творі: ",len(documentText))
    return documentText

#обрахунок середніх значень для грамів
def findAvg(literature: list):
    dictionary = {};
    for i in range(len(literature)):
        text = readText(literature[i])
        result = symbolDistributionInString(text)
        for key, value in result.items():
            if (key in dictionary):
                dictionary[key] += value
            else:
                dictionary[key] = value
    for key, value in dictionary.items():
        dictionary[key] = value / len(literature)
    return dictionary

#обрахунок середніх значень для біграмів
def findBiAvg(literature: list):
    dictionary = {};
    for i in range(len(literature)):
        text = readText(literature[i])
        bi = biCounter(text)
        bi = valuesOfFrequency(bi)
        for key, value in bi.items():
            if (key in dictionary):
                dictionary[key] += value
            else:
                dictionary[key] = value
    for key, value in dictionary.items():
        dictionary[key] = value / len(literature)
    return dictionary

#підрахунок кількості входжень символів у рядках
def symbolDistributionInString(str):
    chars = Counter(str)
    result = {}
    for letter in letters:
        if (letter in chars):
            result[letter] = chars[letter]
        else:
            result[letter] = 0
    return (result)

#побудова гістограми частот літер для грамів
def histogramOfFrequency(result: dict):
    keys = result.keys()
    values = result.values()
    points = np.divide(list(values), sum(values));
    plt.bar(keys, points, color='gold',  label="Частоти")
    plt.show()

#побудова гістограми кількості літер для грамів
def histogramOfAmount(result: dict):
    plt.bar(result.keys(), result.values(), color='tomato', label="Кількість")
    plt.show()

#обрахунок значень для стовпців гістограми
def valuesOfFrequency(dict: dict):
    values = dict.values()
    result = sum(values)
    for key, value in dict.items():
        dict[key] = dict[key] / result
    return dict

#порівняння авторів за біграмами
def compareAuthorsByBigrams(refsOne, refsTwo):
    result = {}
    firstAvg = findBiAvg(refsOne)
    secondAvg = findBiAvg(refsTwo)
    for key, value in firstAvg.items():
        if key in secondAvg:
            result[key] = abs(firstAvg[key] - secondAvg[key])
    сompareTwoAuthors(result)

#порівняння частот творів авторів з частотами української  мови
def compareAuthorAndUkrainian(refs):
    result = {};
    res = findAvg(refs)
    res = valuesOfFrequency(res)
    for key, value in res.items():
        result[key] = abs(res[key] - ukrLettersFrequencies[key])
    histogramOfAmount(result)

#побудова гістограми порівняння творів авторів з українською  мовою
def histogramOfCompareAuthorAndUkrainian(refs):
    result = findAvg(refs)
    result = valuesOfFrequency(result)
    listOfAll = list(result.values())
    listOfUkr = list(ukrLettersFrequencies.values())
    keys = list(result.keys())
    plt.bar(keys, listOfAll, color='orange', label="Author")
    plt.bar(keys, listOfUkr, color='gold', label="UKRAINE", alpha=0.8)
    plt.show()

#відображення гістограми для частот та кількості для одного твору
def showFrequencyAndAmountHistograms(ref):
    text = readText(ref)
    res = symbolDistributionInString(text)
    histogramOfAmount(res)
    histogramOfFrequency(res)

#відображення теплової гістограми для частот біграмів для одного твору
def showBiHeatHistogram(ref):
    text = readText(ref)
    bi = biCounter(text)
    bi = valuesOfFrequency(bi)
    сompareTwoAuthors(bi)

#відображення усередненої гістограми для частот та кількості для автора
def showAvgFrequencyAndAmountHistograms(refs):
    res = findAvg(refs)
    histogramOfAmount(res)
    histogramOfFrequency(res)

#відображення усередненої теплової гістограми для частот біграмів для автора
def showAvgBiHeatHistogram(refs):
    avgBi = findBiAvg(refs)
    сompareTwoAuthors(avgBi)

#підрахунок різниць частот грамів
def countGramsDifferenceOfAuthor(authorLiterature: dict, otherLiterarure: dict):
    difference = 0
    for key, value in authorLiterature.items():
        if key in otherLiterarure:
            difference += abs(value - otherLiterarure[key])
        else:
            difference += 0
    return difference

#вивід знайдених різниць частот грамів для кожного автора
def getAuthorByGram(kotsiubynskyy, stelmakh, kobylianska, result: dict):
    avgKotsiubynskyy = findAvg(kotsiubynskyy);
    avgKotsiubynskyy = valuesOfFrequency(avgKotsiubynskyy)
    differenceKotsiubynskyy = countGramsDifferenceOfAuthor(avgKotsiubynskyy, result)
    print("Difference Kotsuibynskyy: " + str(round(differenceKotsiubynskyy,6)))
    avgStelmakh = findAvg(stelmakh);
    avgStelmakh = valuesOfFrequency(avgStelmakh)
    diffrenceStelmakh = countGramsDifferenceOfAuthor(avgStelmakh, result)
    print("Difference Stelmakh: " + str(round(diffrenceStelmakh,6)))
    avgKobylianska = findAvg(kobylianska);
    avgKobylianska = valuesOfFrequency(avgKobylianska)
    differenceKobylianska = countGramsDifferenceOfAuthor(avgKobylianska, result)
    print("Difference Kobylianska: " + str(round(differenceKobylianska,6)))

#вивід знайдених різниць частот біграмів для кожного автора
def getAuthorByBigrams(kotsiubynskyy, stelmakh, kobylianska, res: dict):
    avgKotsiubynskyy = findBiAvg(kotsiubynskyy);
    differenceKotsiubynskyy = countGramsDifferenceOfAuthor(avgKotsiubynskyy, res)
    print("Difference Kotsuibynskyy: " + str(round(differenceKotsiubynskyy, 6)))
    avgstelmakh = findBiAvg(stelmakh);
    differenceStelmakh = countGramsDifferenceOfAuthor(avgstelmakh, res)
    print("Difference Stelmakh: " + str(round(differenceStelmakh,6)))
    avgKobylianska = findBiAvg(kobylianska);
    differenceKobylianska = countGramsDifferenceOfAuthor(avgKobylianska, res)
    print("Difference Kobylianska: " + str(round(differenceKobylianska,6)))

#порівняння частот для двух авторів
def сompareTwoAuthors(bi):
    check = [];
    for letterOne in letters:
        values = []
        for letterTwo in letters:
            key = (letterOne, letterTwo)
            if (key in bi):
                value = float(bi[key])
                values.append(value);
            else:
                values.append(0.0);
        check.append(values)

    arrayOut = np.array(check);
    fig, ax = plt.subplots()
    im = ax.imshow(arrayOut)
    ax.set_xticks(np.arange(len(letters)))
    ax.set_yticks(np.arange(len(letters)))
    ax.set_xticklabels(letters)
    ax.set_yticklabels(letters)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")
    fig.tight_layout()
    plt.show()

#перевірка валідності рядка
def isValid(str):
    return str != ' ' and str != '\n';

#підрахунок біграмів
def biCounter(sentence):
    n = 2
    grams = ngrams(sentence, n)
    results = {}
    for grams in grams:
        if (grams in results and isValid(grams[0]) and isValid(grams[1])):
            results[grams] += 1
        else:
            if (isValid(grams[0]) and isValid(grams[1])):
                results[grams] = 1
    return (results)

def main():
    kotsubIntermezzo = "kotsubinskiy/kotsiubynskyy-Intermezzo.docx"
    kotsubZHlybyny = "kotsubinskiy/kotsiubynskyy-z-hlybyny.docx"
    kotsubVidma = "kotsubinskiy/kotsiubynskyy_vidma.docx"
    kotsiubynskyyTini = "kotsubinskiy/kotsiubynskyy-tini-zabutykh-predkiv.docx"
    kotsub = [kotsubIntermezzo, kotsubZHlybyny, kotsubVidma]

    stelmakhDuma = "stelmakh/stelmakh-duma-pro-tebe.docx"
    stelmakhVechir = "stelmakh/stelmakh-shchedryy-vechir.docx"
    stelmakhRidnia = "stelmakh/stelmakh-velyka-ridnia.docx"
    stelmakhPravda = "stelmakh/stelmakh-pro-pravdu-ta-kryvdu.docx"
    stelmakh = [stelmakhDuma, stelmakhVechir, stelmakhRidnia]

    kobylianskaZemlia = "kobylianska/kobylianska-zemlia.docx"
    kobylianskaLiudyna = "kobylianska/kobylianska-liudyna.docx"
    kobylianskaNekulturna = "kobylianska/kobylianska-nekulturna.docx"
    kobylianskaTsarivna = "kobylianska/kobylianska-tsarivna.docx"
    kobylianska = [kobylianskaZemlia, kobylianskaLiudyna, kobylianskaNekulturna]

    #showFrequencyAndAmountHistograms(kobylianska)
    #showAvgFrequencyAndAmountHistograms(kobylianska)

    #showBiHeatHistogram(kobylianskaNekulturna)
    #showAvgBiHeatHistogram(kobylianska)

    #compareAuthorAndUkrainian(kobylianska)
    #compareAuthorsByBigrams(stelmakh, kobylianska)

    # text = readText(kobylianskaTsarivna)
    # size5000 = text[0:5000]
    # size10000 = text[0:10000]
    # size25000 = text[0:25000]
    # size50000 = text[0:50000]
    # size100000 = text[0:100000]
    # result = symbolDistributionInString(size5000)
    # result = valuesOfFrequency(result)
    # getAuthorByGram(kotsub, stelmakh, kobylianska, result)
    #
    # text = readText(kotsiubynskyyTini)
    # size5000 = text[0:5000]
    # size10000 = text[0:10000]
    # size25000 = text[0:25000]
    # size50000 = text[0:50000]
    # size100000 = text[0:100000]
    # result = biCounter(size100000)
    # result = valuesOfFrequency(result)
    # getAuthorByBigrams(kotsub, stelmakh, kobylianska, result)

main()
