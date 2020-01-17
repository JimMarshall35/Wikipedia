from bs4 import BeautifulSoup
import requests
import csv

def getFirstLink(pList):
    allow = True
    for p in pList:
        children = p.contents
        for child in children:
            if "(" in child:
                allow = False
                #print(allow)
            if ")" in child:
                allow = True
                #print(allow)
            #print(child)
            if child.name == "a" and allow:
                if child['title'][:4] == 'wikt':
                    continue
                link = child.get("href")
                if link != None:
                    return "https://en.wikipedia.org"+link
    return None;
def connect(string):
    try:
        src = requests.get(string).text
        return src
    except:
        connect(string)
        
num = input("how many repetitions? ")
for x in range(int(num)):
    src = connect("https://en.wikipedia.org/wiki/Special:Random")
    visitedtitles = []
    firstpage = BeautifulSoup(src,'lxml').title.string
    philosophy = False
    search = True
    write = True
    while(search):
        print("----------* " + "LINK " + str(len(visitedtitles)) + " *----------" )
        print()
        soup = BeautifulSoup(src, "lxml")
        for title in visitedtitles:
            if title.string == soup.title.string:
                search = False
        if soup.title.string == "Philosophy - Wikipedia":
            philosophy = True
            
        visitedtitles.append(soup.title.string)

        print("TITLE: " + soup.title.string)

        mwparseroutput = soup.find('div', class_='mw-parser-output')

        #soup2 = BeautifulSoup(t, "lxml")
        pList = mwparseroutput.find_all('p')
        firstlink = getFirstLink(pList)
        if firstlink != None:
            print("FIRST LINK: "+firstlink)
            src = connect(firstlink)
            print()
        else:
            write = False
            break
    print(str(len(visitedtitles)) + " PAGES VISITED")
    print("LOOP " + visitedtitles[len(visitedtitles)-1].string)
    if write:
        with open('output.csv', 'a') as file:
            filewriter = csv.writer(file)
            p = "False"
            if philosophy:
                p = "True"
            filewriter.writerow([firstpage, visitedtitles[len(visitedtitles)-1].string, str(len(visitedtitles)), p])
 
