import sys
import re
import os
from bs4 import BeautifulSoup
def parseXML(file):
    f = open(file, encoding="utf8")     
    soup = BeautifulSoup(f, "html.parser")

    #parse sumary
    sumaryContent = soup.find_all("div", {"class":"infoBox"})
    if len(sumaryContent)>0:
        print("-----------------------------------------------------------------------------------------------------------")
        print("Test Summary")
        for subSum in sumaryContent:
            if len(subSum.get_text(strip=True)) != 0:
                keyValue = subSum.text.replace('\n',' ').split()
                print(printFormatter(keyValue[0], keyValue[1]))
    else:
        print("No data for Test sumary")

    #parse detail
    regex = re.compile('tab *')
    contentDiv = soup.find_all("div", {"class":regex})
    for tIndex in range(len(contentDiv), 1 if len(contentDiv) > 2 else 0, -1):
        print("-----------------------------------------------------------------------------------------------------------")
        titles = []
        contents = []
        titleTags = contentDiv[tIndex-1].find_all("th")
        allAClass = contentDiv[tIndex-1].find_all("a")
        for titleTag in titleTags:
            titles.append(titleTag.text)
        contentTags = contentDiv[tIndex-1].find_all("td")
        i=0
        for contentTag in contentTags:
            if i % len(titles) == 0 :
                contents.append(allAClass[int(i / len(titles))].text)
            elif i > 0 and i % len(titles) == (len(titles) - 1):
                contents.append(contentTag.text)
            else:
                contents.append(contentTag.text)
            i+=1
        max = getMaxLenForClass(contents)
        if titles[0] == "Class":
            print("Detail of classes:")
        else:
            print("Defail of packages:")
        print(getTitleFormat(titles, max))
        print(getContentFormat(titles, contents, max))
    print("-----------------------------------------------------------------------------------------------------------")
    #print detail message
    if len(contentDiv) > 2:
        print("Failed tests:\n")
        failLink = contentDiv[0].find_all("a")
        for i in range(1,len(failLink),2):
            print("----------------------------------------------")
            print(printFormatter("Name:", failLink[i].text))
            fileName = failLink[i-1]['href']
            if failLink[i-1]['href'].startswith("classes/"):
                fileName = failLink[i-1]['href'][failLink[i-1]['href'].rindex("/")+1:]
            print(printFormatter("File:", fileName))
            detailFile = findFileByNameInFolder(file[:file.rindex("/")], fileName)
            extractDetailFailed(detailFile, failLink[i].text)
            
def extractDetailFailed(file, testName):
    f = open(file, encoding="utf8")     
    soup = BeautifulSoup(f, "html.parser")
    faileTables = soup.find_all("table")
    faildTds = faileTables[2].find_all("td")
    failedNameTags = soup.find_all("h3",{"class":"failures"})
    messages = soup.find_all("span",{"class":"code"})
    for i in range(len(faildTds)):
        if(faildTds[i].text == testName):
            print(printFormatter("Duration:", faildTds[i+1].text))
            messageIndex = findMessageIndex(testName, failedNameTags)
            print(printFormatter("Message:", messages[messageIndex].text.replace("\n","",1)))

def findMessageIndex(testName, failedNameTags):
    for i in range(len(failedNameTags)):
        if failedNameTags[i].text == testName:
            return i
    return -1

def findFileByNameInFolder(sFold, sName):
    for root, dirs, files in os.walk(sFold):
        for name in files:
            if name == sName:
                return os.path.join(root, name)
    return null

def getContentFormat(title, content, max):
    t = ""
    nCol = len(title)
    for i in range(0, len(content)):
        if i % nCol == 0:
            t += content[i] + " "*(max- len(content[i]))
        else:
            t += content[i] + " " * (len(title[i%nCol]) * 2 - (len(content[i])))
            if i % nCol == (len(title) -1):
                t+="\n"
    return t

def getTitleFormat(title, max):
    t = "" 
    for i in range(0, len(title)):
        if i == 0:
            t += title[0] + " "*(max-len(title[0]))
        else:
            t += title[i] + " " * len(title[i])
    return t

def getMaxLenForClass(classes):
    max = 0
    for c in classes:
        if len(c) > max:
            max = len(c)
    return max +20

def printFormatter(key, msg):
    keyLen = len(key)
    space = 15-keyLen
    return(key.capitalize() + " "*space + msg)

def main():
    path = sys.argv[1]
    print(path + "\n")
    parseXML(path)

if __name__ == "__main__":
    main()