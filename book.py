from bs4 import BeautifulSoup
import requests
import re

def createSoup(url1, url2, url3):
    URL = url1 + '/' + url2 + '/' + url3
    page = requests.get(URL)
    return BeautifulSoup(page.content, 'html.parser') #soup

def dataCleaning(data):
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    data['About the Book'] = re.sub(cleanr, '', data['About the Book']).replace('\xa0','').replace('\n','')
    data['Content'] = re.sub(cleanr, '', data['Content']).replace('\xa0','').replace('\n','')
    data['About the Author'] = re.sub(cleanr, '', data['About the Author']).replace('\xa0','').replace('\n','')
    return data

    
def dataScraper(soup):
    # dict of elements: extract element based on ID's from tree(soup)
    elementId = {
        'id1':'book-deatil-area'            
        }
    # dict of Class: extract element based on Class's from tree(soup)
    elementClass = {
        'class1': 'book-spec',
        'class2': 'old-price',
        'class3': 'text-uppercase'
        }

    # return variable
    dataExtract = {
        'Category': '',
        'ISBN':'',
        'Title Name':'',
        'Author/Writer':'',
        'Language':'english',
        'Binding':'',
        'Publication Year': '',
        'Pages': '',
        'Sale Territory': '',
        'MRP':'',
        'About the Book': '',
        'Content': '',
        'About the Author': '',
        'Booklink': ''
        }
    
    # extracting useful nodes from soup(tree)
    detailArea = soup.find("div", {"id": elementId['id1']})
    spec = detailArea.find("div", {"class": elementClass['class1']})
    about = detailArea("h3")
    mrp = detailArea.find("small", {"class": elementClass['class2']})


    # title, author and MRP
    dataExtract['Title Name'] = detailArea.h3.text.replace('\t','')
    dataExtract['Author/Writer'] = detailArea.h5.text
    dataExtract['MRP'] = mrp.text
    

    # ISBN, Publication Year, Pages, Sales Territory, Binding
    for div in spec('div'):
        divSpan =  div('span')
        dataExtract[divSpan[0].text] = divSpan[1].text


    # about the book
    for abt in about:
        if abt.text == "About the Book":
            while( abt.next_sibling.name != 'hr'):
                dataExtract['About the Book'] += str(abt.next_sibling)
                abt = abt.next_sibling


    # contents
    content = detailArea.find_all("h3", {"class": elementClass['class3']})
    for cont in content:
        if cont.text == 'Contents':
            while( cont.next_sibling.name != 'hr'):
                dataExtract['Content'] += str(cont.next_sibling)
                cont = cont.next_sibling


    # About the Author
    atr = detailArea.find_all("h3", {"class": elementClass['class3']})
    for at in atr:
        if at.text == 'About the Author / Editor':
            while( at.next_sibling.name != 'hr'):
                dataExtract['About the Author'] += str(at.next_sibling)
                at = at.next_sibling
    

    return dataExtract





def forEach(site=None, subject=None, book=None):
    soup = createSoup(site, subject, book)
    data = dataScraper(soup)
    
    # Edit data absent in HTML code
    data['Category'] = subject
    data['Booklink'] = site + '/' + subject + '/' + book

    return dataCleaning(data)




