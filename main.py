import csv
from collections import Counter


def readScvFile(fileName):
    with open(fileName) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        rows = list(reader)  # rows then have all CVS file rows in form of list of list[[] ,[], [] , ...]
        return rows


def partitionData(allData):
    partitionLimit = round(70 / 100 * len(allData))
    trainingSet = allData[:partitionLimit]
    testingSet = allData[partitionLimit:]
    return [trainingSet, testingSet]


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def getLabelValuesAndCounter(rows, index):
    labelValues = []
    for row in rows:
        labelValues.append(row[index])
    z = labelValues
    newList = Counter(z)
    return newList


def getValueAcrossLabel(uniqAttributeValues, uniqueLabelValues, rows):
    mylist = []
    counter = 0;
    for uniqAttributeValue in uniqAttributeValues:
        for uniqueLabelValue in uniqueLabelValues:
            for row in rows:
                if ((uniqAttributeValue in row) and uniqueLabelValue in row):
                    counter = counter + 1
            obj = {
                "uniqAttributeValue": uniqAttributeValue,
                "uniqueLabelValue": uniqueLabelValue,
                "counter": counter
            }
            mylist.append(obj)
            counter = 0
    return mylist


def __getAttributeUniqueValues(dictionary):
    uniqueValue = []
    for value, counter in dictionary.items():
        uniqueValue.append(value)
    return uniqueValue


def getUniuqLabelValuesAndCounter(rows):
    lis = []
    for k, v in getLabelValuesAndCounter(rows, 3).items():
        lis.append([k, v])
    return lis


def getProblablity(probabilityTable, label, attribute, counter):
    for table in probabilityTable:
        for entry in table:
            if (entry['uniqueLabelValue'] == attribute) and (entry['uniqAttributeValue'] == label[0]):
                return (entry['counter'] / counter)


def runTest(probabilityTable, uniqueValue, testRow,trainsingsetLength):
    results = []
    for label in uniqueValue:
        print(label)
        Result = label[1]/trainsingsetLength
        for value in testRow:
            Result = Result * getProblablity(probabilityTable, label, value, label[1])

        results.append(Result)
    return uniqueValue[results.index(max(results))][0]

if __name__ == '__main__':
    partitionedData = partitionData(readScvFile('test.csv'));
    trainingSet = partitionedData[0]
    testingSet = partitionedData[1]
    infoD = getUniuqLabelValuesAndCounter(trainingSet)

    probabilityTable = [];
    for i in range(3):
        probabilityTable.append(
            getValueAcrossLabel(__getAttributeUniqueValues(getLabelValuesAndCounter(trainingSet, 3)),
                                __getAttributeUniqueValues(getLabelValuesAndCounter(trainingSet, i)), trainingSet))
    #runTest(probabilityTable, infoD, ['Red', 'Suv', 'Domestic']);
    counter = 0;
    for row in testingSet:
        if(runTest(probabilityTable, infoD,row[:-1], len(trainingSet)) ==row[-1]):
            counter=counter+1
    print(counter / len(testingSet)*100)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
