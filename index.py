from bs4 import BeautifulSoup
import requests

def createSoup(url1, url2, url3 = ''):
    URL = url1 + '/' + url2 + '/' + url3
    print(URL)
    page = requests.get(URL)
    return BeautifulSoup(page.content, 'html.parser') #soup

def all_books_page(soup):
    
    elementId = {
        'id1': 'book-listing',
        }

    elementClass = {
        'class1': 'book-row row'
        }

    
    booksUrlList = []
    
    
    bookList = soup.find("div", {"id": elementId['id1']})

    
    # Extarct all links from sub column
    for book in bookList('div', {"class": elementClass['class1']}):
        booksUrlList.append(book.a.get('href'))
    return booksUrlList


def changePage(site, subject):
    GlobalbooksUrlList = []
    i = 1
    while(1):
        soup = createSoup(site, subject, str(i))
        books = all_books_page(soup)
        if books == []:
            return GlobalbooksUrlList
        GlobalbooksUrlList.extend(books)
        i+=1        
    return GlobalbooksUrlList


def bookUrl(site="https://www.rawatbooks.com", subject = None):
    return changePage(site, subject)
    

