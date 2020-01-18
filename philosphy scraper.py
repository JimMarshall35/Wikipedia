from bs4 import BeautifulSoup
import requests
import csv
import io
import networkx as nx
import matplotlib.pyplot as plt
print()
print('╔═╗╦ ╦╦╦  ╔═╗╔═╗╔═╗╔═╗╦ ╦╦ ╦  ╔═╗╔═╗╦═╗╔═╗╔═╗╔═╗╦═╗')
print('╠═╝╠═╣║║  ║ ║╚═╗║ ║╠═╝╠═╣╚╦╝  ╚═╗║  ╠╦╝╠═╣╠═╝║╣ ╠╦╝')
print('╩  ╩ ╩╩╩═╝╚═╝╚═╝╚═╝╩  ╩ ╩ ╩   ╚═╝╚═╝╩╚═╩ ╩╩  ╚═╝╩╚═')
print()
def getFirstLink(pList):
    allow = True
    for p in pList:
        children = p.contents
        for child in children:
            if "(" in child:
                allow = False
            if ")" in child:
                allow = True
            #print(child.name)
            if child.name == "i" or child.name == "b" and allow:
                #print("ok")
                if(len(child.contents)) == 0:
                    continue
                #print(child.contents[0])
                if child.contents[0].name == "a":
                    if 'title' in child.attrs:
                        if child.contents[0]['title'][:4] == 'wikt':
                            continue
                        link = child.contents[0].get("href")
                        if link != None:
                            return "https://en.wikipedia.org"+link

            if child.name == "a" and allow:
                if 'title' in child.attrs:
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
G = nx.Graph()
num = input("how many repetitions? ")
print()
for x in range(int(num)):
    src = connect("https://en.wikipedia.org/wiki/Special:Random")
    visitedtitles = []
    firstpage = BeautifulSoup(src,'lxml').title.string
    philosophy = False
    search = True
    write = True
    previousnode = None
    while(search):
        print("----------* " + "LINK " + str(len(visitedtitles)) + " run: "+ str(x+1) +" / "+num+ " *----------" )
        print()
        soup = BeautifulSoup(src, "lxml")
        for title in visitedtitles:
            if title.string == soup.title.string:
                search = False
        if soup.title.string == "Philosophy - Wikipedia":
            philosophy = True
            
        visitedtitles.append(soup.title.string)

        print("TITLE: " + soup.title.string[:-12])
        if G.has_node(soup.title.string[:-12]) == False:
            G.add_node(soup.title.string[:-12])
        if previousnode != None:
            if G.has_edge(previousnode, soup.title.string[:-12]) == False:
                G.add_edge(previousnode, soup.title.string[:-12])
        previousnode = soup.title.string[:-12]

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
    print()
    print(str(len(visitedtitles)) + " PAGES VISITED")
    print("LOOP " + visitedtitles[len(visitedtitles)-1].string)
    for i in range(30):
        print()
    if write:
        with io.open('output.csv', 'a', encoding="utf-8") as file:
            filewriter = csv.writer(file)
            p = "False"
            if philosophy:
                p = "True"
            filewriter.writerow([firstpage, visitedtitles[len(visitedtitles)-1].string, str(len(visitedtitles)), p])
pos = nx.kamada_kawai_layout(G)
nx.draw(G, pos, with_labels = 1)
plt.show()        
 
