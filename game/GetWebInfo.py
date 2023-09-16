import urllib
import re

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

class AppURLopener(urllib.request.FancyURLopener):  #Disguise as Firefox version 5.0 to bipass some security
    version = "Mozilla/5.0"


def getUR():

    opener = AppURLopener()
    htmlCode = opener.open('https://tradingeconomics.com/malta/unemployment-rate')

    soup = BeautifulSoup(htmlCode, "html.parser")

    rows = soup.findAll(id="actual")

    unemploymentRate = re.search(r'\n(.*?)\n', str(rows[3])).group(1)
    unemploymentRate = unemploymentRate.replace(" ", "").replace("%","")

    return "emplyomentRate: " + unemploymentRate

def getTax():

    opener = AppURLopener()
    htmlCode = opener.open('https://taxsummaries.pwc.com/malta/individual/taxes-on-personal-income')

    soup = BeautifulSoup(htmlCode, "html.parser")
    rows = str(soup.findAll("table"))

    all = re.findall(r"%\">(.*?)</td>", rows)

    fromSal = []
    toSal = []
    rate = []
    deduct = []

    rowCount = 0
    asString = ""

    for x in range(int(len(all)/4)):
        fromSal.append(all[rowCount])
        toSal.append(all[rowCount + 1])
        rate.append(all[rowCount + 2])
        deduct.append(all[rowCount + 3])

        asString = asString + "From " + all[rowCount] + " to " + all[rowCount+1] + " rate: " + all[rowCount+2] + " deduct " + all[rowCount+3] + "\n"
        rowCount = rowCount + 4

    return asString

def WrightData():
    Data = ""
    Data = Data + getUR() + "\n\n"
    Data = Data + getTax()

    f = open("Information.txt","w")
    f.write(Data)
    f.close()

def GetData():
    Data = ""
    Data = Data + getUR() + "\n\n"
    Data = Data + getTax()

    return Data
