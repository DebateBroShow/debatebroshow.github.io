import fileinput
import os
import shutil
import time

def GenerateFiles(epsiodefilename, cardfilename, pagefilename, folderName):
    episodeInfo = parseEpisode(episodefilename)

    i = 0
    for _ in episodeInfo:
        print(str(i) + ": " + _)
        i += 1

    newCardFilename = episodeInfo[0]+"_Card.html"
    newPageFilename = episodeInfo[0]+".html"

    src_dir = os.getcwd() 
    #clean up, in case files had been generated previously, to avoid errors
    cleanAutomation(episodeInfo[0])
    if path.exists("./GeneratedPages/"+episodeInfo[0]): 
        shutil.rmtree("./GeneratedPages/"+episodeInfo[0])
    if path.exists("../pages/episodeList/"+newPageFilename): 
        shutil.rmtree("../pages/episodeList/"+newPageFilename)
    time.sleep(5)
    #start generating pages
    os.makedirs("./GeneratedPages/"+episodeInfo[0])
    shutil.copyfile(cardfilename, newCardFilename)
    shutil.copyfile(pagefilename, newPageFilename)

    generateCard(episodeInfo, newCardFilename)
    generatePage(episodeInfo, newPageFilename)
    #all pages generated, automatically updating the files now

    #copies the generated episode file to the main site
    shutil.copyfile(newPageFilename, "../pages/episodeList/"+newPageFilename)

    shutil.copyfile("../pages/episodeIndex.html", "episodeIndexHtml.html.bak")
    #copies the card into episodeIndex.html
    updateEpisodeIndex()

    #cleanup
    shutil.move(newCardFilename, "./GeneratedPages/"+episodeInfo[0])
    shutil.move(newPageFilename, "./GeneratedPages/"+episodeInfo[0])

def cleanAutomation(filename):
    print('hello')

def updateEpisodeIndex():  
    print("hello")


def generateCard(info, filename):
    EPISODEFILENAME = info[0]
    IMAGENAME = info[1]
    EPISODETITLE = info[2]
    EPISODESUBTITLE = info[3]

    with open(filename, 'r') as file:
        filedata = file.read()
    
    filedata = filedata.replace('EPISODEFILENAME', EPISODEFILENAME)
    filedata = filedata.replace('IMAGENAME', IMAGENAME)
    filedata = filedata.replace('EPISODETITLE', EPISODETITLE)
    filedata = filedata.replace('EPISODESUBTITLE',EPISODESUBTITLE)

    with open(filename, 'w') as file:
        file.write(filedata)

def generatePage(info, filename):
    EPISODEFILENAME = info[0]
    IMAGENAME = info[1]
    EPISODETITLE = info[2]
    EPISODESUBTITLE = info[3]
    PAGETITLE = info[4]
    BUZZSPROUTURL = info[5]
    SPOTIFYURL = info[6][info[6].rindex('/')+1:]
    print(SPOTIFYURL)
    YOUTUBEURL = info[7][info[7].rindex('=')+1:]
    print(YOUTUBEURL)

    with open(filename, 'r') as file:
        filedata = file.read()
    
    filedata = filedata.replace('EPISODEFILENAME', EPISODEFILENAME)
    filedata = filedata.replace('IMAGENAME', IMAGENAME)
    filedata = filedata.replace('EPISODETITLE', EPISODETITLE)
    filedata = filedata.replace('EPISODESUBTITLE',EPISODESUBTITLE)
    filedata = filedata.replace('PAGETITLE', PAGETITLE)
    filedata = filedata.replace('BUZZSPROUTURL', BUZZSPROUTURL)
    filedata = filedata.replace('SPOTIFYURL', SPOTIFYURL)
    filedata = filedata.replace('YOUTUBEURL', YOUTUBEURL)

    with open(filename, 'w') as file:
        file.write(filedata)
    
#hope this works lol, not many edge cases handled
def parseEpisode(episodefilename):
    episode = open(episodefilename, "r+")
    lines = [line for line in episode.readlines()]
    linesParsed = []
    for _ in lines:
        if _[-2:] == "\r\n": 
            linesParsed.append(_[0:-2])
            continue
        elif _[-1:] == "\n": 
            linesParsed.append(_[0:-1])
            continue
        else:
            linesParsed.append(_)
    return linesParsed[linesParsed.index("---")+1:]

if __name__ == "__main__":
    episodefilename="episode.txt"
    cardfilename="card.html"
    pagefilename="page.html"
    folderName="GeneratedPages"
    GenerateFiles(episodefilename,cardfilename,pagefilename,folderName)
