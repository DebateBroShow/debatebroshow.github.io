import fileinput
import os
import shutil
import time
from sitemap import *


def GenerateFiles(epsiodefilename, cardfilename, pagefilename, maincardfilename, folderName):
    episodeInfo = parseEpisode(episodefilename)

    newCardFilename = episodeInfo[0]+"_Card.html"
    newMainCardFilename = episodeInfo[0]+"_MainCard.html"
    newPageFilename = episodeInfo[0]+".html"

    src_dir = os.getcwd()
    # clean up, in case files had been generated previously, to avoid errors
    # creates a backup of the edited files the first time only
    print("cleaning up previous automation attempts")
    cleanAutomation(episodeInfo[0], newPageFilename)
    # time.sleep(15) #to see if automated deleting is working

    # start generating pages
    print("creating copies of the files to edit")
    os.makedirs("./GeneratedPages/"+episodeInfo[0])
    shutil.copyfile(cardfilename, newCardFilename)
    shutil.copyfile(pagefilename, newPageFilename)
    shutil.copyfile(maincardfilename, newMainCardFilename)

    # generates html code
    print("generating new html files")
    generateCard(episodeInfo, newCardFilename)
    generateMainCard(episodeInfo, newMainCardFilename)
    generatePage(episodeInfo, newPageFilename)

    print("automatically updating the html of the website")
    # updating and moving files automatically
    # copies the generated episode file to the main site
    shutil.copyfile(newPageFilename, "../pages/episodeList/"+newPageFilename)

    # copies the card into episodeIndex.html
    updateIndex(newMainCardFilename)
    updateEpisodeIndex(newCardFilename)

    print("cleaing up remaining files")
    # file organization
    shutil.move(newCardFilename, "./GeneratedPages/"+episodeInfo[0])
    shutil.move(newPageFilename, "./GeneratedPages/"+episodeInfo[0])
    shutil.move(newMainCardFilename, "./GeneratedPages/"+episodeInfo[0])

    mainRoutine()
    if os.path.exists("../sitemap.xml"):
        os.remove("../sitemap.xml")
    shutil.move("sitemap.xml", "..")


def cleanAutomation(filename1, filename2):
    #print(not os.listdir("./GeneratedPages/"+filename1))
    if (os.path.exists("./GeneratedPages/"+filename1) and os.listdir("./GeneratedPages/"+filename1)) or os.path.exists("../pages/episodeList/"+filename2):
        if os.path.exists("./GeneratedPages/"+filename1):
            shutil.rmtree("./GeneratedPages/"+filename1)
        if os.path.exists("../pages/episodeList/"+filename2):
            os.remove("../pages/episodeList/"+filename2)
        # todo: restore the other 2 files from backup perhaps?
    else:
        if os.path.exists("./GeneratedPages/"+filename1):
            shutil.rmtree("./GeneratedPages/"+filename1)
        shutil.copyfile("../pages/episodeIndex.html", "episodeIndex.backup")
        shutil.copyfile("../index.html", "index.backup")

# updates the homepage automatically, works really great


def updateIndex(filename):
    indexFilename = "../index.html"
    i = -1
    j = 0
    newIndex = []
    maincard = open(filename, "r").readlines()
    with open(indexFilename, 'r') as file:
        for line in file.readlines():
            i += 1
            if "<!--Autogenerated-->" in line or (j > 0 and j < 14):
                newIndex.append(maincard[j])
                j += 1
                continue
            newIndex.append(line)
    open(indexFilename, 'w').close()
    with open(indexFilename, "w") as file:
        for line in newIndex:
            file.write(line)

# updates the index, some indentation gets messed up, but appears to work overall


def updateEpisodeIndex(filename):
    indexFilename = "../pages/episodeIndex.html"
    i = -1
    j = 0
    k = 0
    newIndex = []
    oldEpisode = []
    card = open(filename, "r").readlines()
    with open(indexFilename, 'r') as file:
        print(len(card))
        for line in file.readlines():
            i += 1
            if "id=\"marker\"" in line or (j > 0 and j < 13):
                if k == 0:
                    k = i
                print(j)
                newIndex.append(card[j])
                oldEpisode.append((line))
                j += 1
                continue
            newIndex.append(line)
    newIndex = newIndex[:k+15] + oldEpisode + newIndex[k+14:]
    open(indexFilename, 'w').close()
    with open(indexFilename, "w") as file:
        for line in newIndex:
            file.write(line)

#reigon Gets the data from the
def generateCard(info, filename):
    EPISODEFILENAME, IMAGENAME, EPISODETITLE, EPISODESUBTITLE, PAGETITLE, BUZZSPROUTURL, SPOTIFYURL, YOUTUBEURL = GetPageData(
        info)

    with open(filename, 'r') as file:
        filedata = file.read()

    filedata = getBasicData(filedata, EPISODEFILENAME, IMAGENAME, EPISODETITLE, EPISODESUBTITLE)

    with open(filename, 'w') as file:
        file.write(filedata)


def generateMainCard(info, filename):
    EPISODEFILENAME, IMAGENAME, EPISODETITLE, EPISODESUBTITLE, PAGETITLE, BUZZSPROUTURL, SPOTIFYURL, YOUTUBEURL = GetPageData(
        info)

    with open(filename, 'r') as file:
        filedata = file.read()

    filedata = getBasicData(filedata, EPISODEFILENAME, IMAGENAME, EPISODETITLE, EPISODESUBTITLE)

    with open(filename, 'w') as file:
        file.write(filedata)


def generatePage(info, filename):
    EPISODEFILENAME, IMAGENAME, EPISODETITLE, EPISODESUBTITLE, PAGETITLE, BUZZSPROUTURL, SPOTIFYURL, YOUTUBEURL = GetPageData(
        info)

    with open(filename, 'r') as file:
        filedata = file.read()

    filedata = editData(filedata, EPISODEFILENAME, IMAGENAME, EPISODETITLE,
                            EPISODESUBTITLE, PAGETITLE, BUZZSPROUTURL, SPOTIFYURL, YOUTUBEURL)

    with open(filename, 'w') as file:
        file.write(filedata)
#endreigon

#reigon Parses and Edits the Page Data
def GetPageData(info):
    EPISODEFILENAME = info[0]
    IMAGENAME = info[1]
    EPISODETITLE = info[2]
    EPISODESUBTITLE = info[3]
    PAGETITLE = info[4]
    BUZZSPROUTURL = info[5]
    SPOTIFYURL = info[6][info[6].rindex('/')+1:]
    YOUTUBEURL = info[7][info[7].rindex('=')+1:]
    return EPISODEFILENAME, IMAGENAME, EPISODETITLE, EPISODESUBTITLE, PAGETITLE, BUZZSPROUTURL, SPOTIFYURL, YOUTUBEURL

def editData(filedata, EPISODEFILENAME, IMAGENAME, EPISODETITLE, EPISODESUBTITLE, PAGETITLE, BUZZSPROUTURL, SPOTIFYURL, YOUTUBEURL):
    filedata = getBasicData(filedata, EPISODEFILENAME, IMAGENAME, EPISODETITLE, EPISODESUBTITLE)
    filedata = filedata.replace('PAGETITLE', PAGETITLE)
    filedata = filedata.replace('BUZZSPROUTURL', BUZZSPROUTURL)
    filedata = filedata.replace('SPOTIFYURL', SPOTIFYURL)
    filedata = filedata.replace('YOUTUBEURL', YOUTUBEURL)
    return filedata

def getBasicData(filedata, EPISODEFILENAME, IMAGENAME, EPISODETITLE, EPISODESUBTITLE):
    filedata = filedata.replace('EPISODEFILENAME', EPISODEFILENAME)
    filedata = filedata.replace('IMAGENAME', IMAGENAME)
    filedata = filedata.replace('EPISODETITLE', EPISODETITLE)
    filedata = filedata.replace('EPISODESUBTITLE', EPISODESUBTITLE)
    return filedata
#endreigon

#Hopefully works with linux and windows
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
    print("Type y to confirm you actually read and understood all the steps in the how to use this text file, anything else with exit safely :)")
    text = input()  # is this python 2 only?
    if(text != "y" and text != "Y"):
        exit()
    print("TODO: fix the cleanup with episodeIndex, it appends episodes more than once")
    episodefilename = "episode.txt"
    cardfilename = "card.html"
    maincardfilename = "mainCard.html"
    pagefilename = "page.html"
    folderName = "GeneratedPages"
    GenerateFiles(episodefilename, cardfilename,
                  pagefilename, maincardfilename, folderName)
