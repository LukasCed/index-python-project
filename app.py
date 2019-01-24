class IndexTree:
    def __init__(self, branchList = []):
        self.branchList = branchList  # its a dict
        
    def getKeyBranch(self, key):
        return [branch for branch in self.branchList if key in branch][0][key]
    
    def branchWithKeyExist(self, key):
        return len([branch for branch in self.branchList if key in branch]) > 0

    def getKeyRangeFromInclusive(self, key):
        return self.getKeyBranch(key)[0][0]
    
    def getKeyRangeToExclusive(self, key):
        return self.getKeyBranch(key)[0][1]
    
    def getKeyIndex(self, key):
        return self.getKeyBranch(key)[1]
    
    def doesBranchWithKeyExist(self, key):
        return self.getKeyBranch(key)
    
class DataStruct:
    def __init__(self, indexTree, sortedList):
        self.indexTree = indexTree
        self.sortedList = sortedList
        
# https://stackoverflow.com/questions/36640673/why-should-i-use-classes-in-python/36641737 paaiskina kam ir kaip

def get_first_letter(word):
    return '' if word == '' else word[0]

def find_end_point(strList):
    initialLetter = get_first_letter(strList[0])
    lastLetterPos = 0
    for elem in strList:
        if get_first_letter(elem) == initialLetter:
            lastLetterPos = lastLetterPos + 1
        else:
            break
    return lastLetterPos
            
def create_subList(strList, endPoint):
    newList = [elem[1:] for elem in strList[:endPoint]] # reik krc pasalinti pirmas raides. list spliting, comprehension
    if all(value is '' for value in newList):
        newList = ['']
    return newList

def create_index(strList):
    index = IndexTree([]) # weird af. be [] kartais per cia kazkaip ateina dict listai. neisivaizduoju how
    if strList[0] or len(strList) > 1:
        strList.sort() #turi but nrml
        refPoint = 0 

        while len(strList) != 0:  
            letter = get_first_letter(strList[0]) # apie kuria raide kalbam
            endPoint = find_end_point(strList) # kada baigiasi ta pati raide
            subList = create_subList(strList, endPoint)# nukerpu pirmas raides
            interval = range(refPoint, refPoint + endPoint)

            indexIntervalTuple = (interval, create_index(subList)) # tuple. cia paduodu tos pacios raides sublista kuriam nukirptos pirmos raides
            # also rekursija
            indexInfo = { letter: indexIntervalTuple } # dict. raide ir kur ji pasiroda ir jos tolimesne info
            
            index.branchList.append(indexInfo)

            #pareducinam lista ka butu nuo endpoint ir vaziuojam toliau
            
            strList = strList[endPoint:]
            refPoint = refPoint + endPoint

        return index        


# ziurim kas gaunasi

dataDict = transformData(readData())
strList = sorted(dataDict['first'])
sortedIndex = [i[0] for i in sorted(enumerate(dataDict['first']), key=lambda x:x[1])]

# strList = ['aa', 'cd', 'gav', 'agfgf', 'aba', 'ccc', 'gd', 'cb', 'ac', 'acc', 'bc', 'b']
# strList = ['acc', 'ac', 'acc']

test = create_index(strList)

data = DataStruct(indexTree = test, sortedList = strList)

indexInSortedList = index_search('Bett', test)
origIndex = sortedIndex[indexInSortedList]
print(dataDict['first'][origIndex])
print(dataDict['last'][origIndex])
print(dataDict['phone'][origIndex])

# print(index_search('de', test))

def binary_search(intList, item): # assume sorted
    start = 0
    end = len(intList) - 1
    
    while start <= end:
        midPoint = (end + start) // 2
        if intList[midPoint] == item:
            return midPoint
        elif intList[midPoint] < item:
            start = midPoint + 1
        else:
            end = midPoint - 1
            
    return -1

binary_search([1,2,4,5,6,8,9,14,17,25,29], 14)


def index_search(item, index): # esme atrasti kur elementas yra susortintame list'e
    whereInSortedList = 0
    indexToSearch = index
    for char in item:
        if indexToSearch is None or not indexToSearch.branchWithKeyExist(char):
            return -1
        # search letter in index
#         print(indexToSearch.branchList)
        whereInSortedList = whereInSortedList + indexToSearch.getKeyRangeFromInclusive(char)
        indexToSearch = indexToSearch.getKeyIndex(char)

    
    return whereInSortedList
        
def readData():
    f = open("data.csv","r")
    fdata = f.readlines()
    f.close()
    return fdata
    
def transformData(fdata):
    dataDict = dict()
    for (index, line) in enumerate(fdata):
        if index == 0:
            props = line.strip('\n').split(',')
            for (index, prop) in enumerate(props):
                dataDict[prop] = list()
        else:
            dataLine = line.strip('\n').split(',')
            for (index, prop) in enumerate(props):
                dataDict[prop].append(dataLine[index])
                
    return dataDict        
