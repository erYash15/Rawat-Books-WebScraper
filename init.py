from bs4 import BeautifulSoup
import requests

def createSoup(url):
    URL = url
    page = requests.get(URL)
    return BeautifulSoup(page.content, 'html.parser') #soup


def categoryUrl(soup):

    subDict = {}
    
    subList = soup.find("div", {"class": 'subject-list'})
 
    for divTag in subList:
        if divTag.find('a') != -1:
            subDict[divTag.a.text] = divTag.a.get('href')[27:]

    return subDict
    

def subjectUrls():
    subUrl = 'https://www.rawatbooks.com/pages/subject'
    soup = createSoup(subUrl)

    return categoryUrl(soup)

#subjectUrls()