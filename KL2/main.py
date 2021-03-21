import collections
import csv
from collections import defaultdict
import re
import math
import matplotlib.pyplot as plt

#гістограма к-тей десяти слів, що найбільше зустрічаються у категорії
def showHistogramFor10Words(res: dict):
    plt.bar(res.keys(), res.values(), color='gold', label="Real distribution")
    plt.show()

#обрахунок даних для гістограми
def showHistogram(file, isMinLength):
    print(file)

    category1 = 'евреи'
    category2 = 'штирлиц'
    arr = readFileText(file)
    arr1 = arrayOfCategory(arr, category1)
    arr2 = arrayOfCategory(arr, category2)

    without3Length1 = removeWords(arr1, isMinLength)
    without3Length2 = removeWords(arr2, isMinLength)
    dictionary1 = fillDictionary(without3Length1)
    dictionary2 = fillDictionary(without3Length2)

    ordered = collections.OrderedDict(sorted(dictionary1.items(), key=lambda x: x[1], reverse=True)[:10])
    showHistogramFor10Words(ordered)
    ordered = collections.OrderedDict(sorted(dictionary2.items(), key=lambda x: x[1], reverse=True)[:10])
    showHistogramFor10Words(ordered)

#початок роботи в режимі дебаг/без дебагу
def DebagAndNotDebagMode(debug):
    fileNameTest = 'test.csv'
    passageThroughDataset('test_10.csv', debug, fileNameTest)
    passageThroughDataset('test_20.csv', debug, fileNameTest)
    passageThroughDataset('test_30.csv', debug, fileNameTest)

#прохід по датасету та аналіз його елементів
def passageThroughDataset(filename, isDebugMode, file):
    isMinLength = False
    print('--------------------------------------')
    print('Назва файлу: ' + filename)
    category1 = 'евреи'
    category2 = 'штирлиц'
    arr = readFileText(filename)

    frequency1 = countFrequency(arr, category1)
    frequency2 = countFrequency(arr, category2)
    arr1 = arrayOfCategory(arr, category1)
    arr2 = arrayOfCategory(arr, category2)

    without3Length1 = removeWords(arr1, isMinLength)
    without3Length2 = removeWords(arr2, isMinLength)
    k = sumOfWordsOfArrays(without3Length1, without3Length2)

    sum1 = sumOfWords(without3Length1)
    sum2 = sumOfWords(without3Length2)
    dictionary1 = fillDictionary(without3Length1)
    dictionary2 = fillDictionary(without3Length2)

    log1 = math.log(frequency1 / (frequency1 + frequency2))
    log2 = math.log(frequency2 / (frequency1 + frequency2))
    arrForTest = readFileText(file)
    arrForTestWithout3Length = removeWords(arrForTest, isMinLength)

    detectedTrue = 0
    allResult = len(arrForTestWithout3Length)
    for row in arrForTestWithout3Length:
        printInDebugMode(isDebugMode, row)
        equation1 = solveEquation(log1, row, dictionary1, k, sum1)
        equation2 = solveEquation(log2, row, dictionary2, k, sum2)
        textForPrint = category1 + ': ' + str(equation1) + '  ' + category2 + ': ' + str(equation2)
        printInDebugMode(isDebugMode, textForPrint)
        if (equation1 > equation2):
            if row[2] == 'класс = евреи':
                detectedTrue += 1
                printInDebugMode(isDebugMode, 'Анекдот розпізнаний правильно: ' + category1)
            else:
                printInDebugMode(isDebugMode, 'Анекдот розпізнаний правильно: ' + category1)
        else:
            if row[2] == 'класс = штирлиц':
                detectedTrue += 1
                printInDebugMode(isDebugMode, 'Анекдот розпізнаний правильно: ' + category2)
            else:
                printInDebugMode(isDebugMode, 'Анекдот розпізнаний неправильно: ' + category1)
    print('Всього тестових анекдотів: ' + str(allResult))
    print('К-ть розпізнаних правильно: ' + str(detectedTrue))
    print('К-ть розпізнаних неправильно: ' + str(allResult - detectedTrue))

#читання елементів з файлу у форматі csv
def readFileText(file):
    resultArray = []
    rows = []
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            rows.append(row)
    for row in rows:
        result = ''.join(row)
        x = result.split(";")
        resultArray.append(x)
    return resultArray

#видалення слів довжиною менших/рівних 3 з елементу
def removeWordsLess3(str, isLessThan3):
    row = re.sub(r'[^\w\s]', '', str).lower();
    if isLessThan3:
        row = re.sub(r'\b\w{1,3}\b', '', row)
    return row

#видалення слів
def removeWords(arr, isLessThan3):
    result = []
    for row in arr:
        str = removeWordsLess3(row[1], isLessThan3)
        row = [row[0], str, row[2]]
        result.append(row)
    return result

#обрахунок частоти
def countFrequency(arr, anekdotClass):
    amount = 0
    for words in arr:
        i = words[2].find(anekdotClass)
        if i >= 0:
            amount = amount + 1
    return amount

#виокремлення масиву для категорії
def arrayOfCategory(arr, anekdotClass):
    result = []
    for words in arr:
        i = words[2].find(anekdotClass)
        if i >= 0:
            result.append(words)
    return result

#підрахунок суми слів
def sumOfWords(arr):
    sum = 0
    for words in arr:
        sum = sum + len(words[1].split())
    return sum

#підрахунок суми слів у масиві
def sumOfWordsOfArrays(arr1, arr2):
    dictionary = {}

    for words in arr1:
        for key in words[1].split():
            if key in dictionary:
                dictionary[key] = dictionary[key] + 1
            else:
                dictionary[key] = 1
    for words in arr2:
        for key in words[1].split():
            if key in dictionary:
                dictionary[key] = dictionary[key] + 1
            else:
                dictionary[key] = 1

    return len(dictionary)

#заповнення словнику словами
def fillDictionary(arr):
    dictionary = {}
    for words in arr:
        for key in words[1].split():
            if key in dictionary:
                dictionary[key] = dictionary[key] + 1
            else:
                dictionary[key] = 1
    return dictionary

#розв'язання рівняння для пошуку значення Dc
def solveEquation(Dc, row, dictionary, k, sum):
    separated = row[1].split()
    value = 0
    for word in separated:
        if word in dictionary:
            value = value + math.log((dictionary[word] + 1) / (k + sum))
        else:
            value = value + math.log((0 + 1) / (k + sum))
    return Dc + value

#виведення інформації по кожному елементу вибірки у режимі дебаг
def printInDebugMode(isDebugMode, text):
    if isDebugMode:
        print(text)

def main():
    debug = False
    DebagAndNotDebagMode(debug)

    showHistogram('test.csv', False)
    showHistogram('test.csv', True)


main()