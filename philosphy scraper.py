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
def getFirstLink(pList): # takes a lost of p tags
    allow = True
    for p in pList:           # iterate through p tags
        print("P: " + p.name)
        children = p.contents # iterate through each p tags contents
        for child in children:
            if "(" in child:  #
                allow = False #
                print(allow)  # disallow links in brackets
            if ")" in child:  #
                allow = True  #
                print(allow)  #
            print(child)
            if child.name == "i" or child.name == "b" and allow: # allow for bold and italic links
                print("ok")
                if(len(child.contents)) == 0:
                    continue
                print(child.contents[0])
                if child.contents[0].name == "a":
                    if 'title' in child.attrs:
                        if child.contents[0]['title'][:4] == 'wikt': # prevent links to wiktionary
                            continue
                        link = child.contents[0].get("href") # get hyperlink
                        if link != None:
                            return "https://en.wikipedia.org"+link

            if child.name == "a" and allow:          # non bold or italic links
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
        connect(string)   # if cant connect then don't throw an error just try again
        
G = nx.Graph() # create networkx graph object
num = input("how many repetitions? ")
print()
visitedtitles = []
for x in range(int(num)):
    src = connect("https://en.wikipedia.org/wiki/Special:Random")
    #visitedtitles = []
    firstpage = BeautifulSoup(src,'lxml').title.string
    philosophy = False
    search = True
    write = True
    previousnode = None
    while(search):
        print("----------* " + "LINK " + str(len(visitedtitles)) + " run: "+ str(x+1) +" / "+num+ " *----------" )
        print()
        soup = BeautifulSoup(src, "lxml")
        for title in visitedtitles: # if page has been visited exit while lop
            if title.string == soup.title.string:
                search = False
        if soup.title.string == "Philosophy - Wikipedia": # set philosophy visited flag to true if philosophy visited
            philosophy = True
            
        visitedtitles.append(soup.title.string) 

        print("TITLE: " + soup.title.string[:-12]) # get a sub string to remove the "- Wikipedia" bit from the page titles
        if G.has_node(soup.title.string[:-12]) == False:
            G.add_node(soup.title.string[:-12])
        if previousnode != None:
            if G.has_edge(previousnode, soup.title.string[:-12]) == False:
                G.add_edge(previousnode, soup.title.string[:-12])
        previousnode = soup.title.string[:-12]

        mwparseroutput = soup.find('div', class_='mw-parser-output') # this div tag contains the article

        #soup2 = BeautifulSoup(t, "lxml")
        pList = mwparseroutput.find_all('p') # find all paragraphs in article
        firstlink = getFirstLink(pList)      # get the first link on the page
        if firstlink != None:
            print("FIRST LINK: "+firstlink)
            src = connect(firstlink)
            print()
        #else:
         #   write = False
          #  break
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
 
