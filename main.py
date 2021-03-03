import init
import book
import index
import pandas as pd


def createDatabase():
    
    lst = []
    
    subjectsDict = init.subjectUrls() # all subjects

    for subject in list(subjectsDict.keys()):
        page = index.bookUrl(subject=subjectsDict[subject])
        for p in page:
            try:
                lst.append(book.forEach(subject = subject, book=p.split('/')[-1]))
            except: 
                pass

    # save data from list of dict to dataframe
    df = pd.DataFrame(lst)
    df.to_csv('dataset.csv', index=True)




if __name__ == '__main__':
    createDatabase()

    #Recommandation to load data
    #data = pd.read_csv('dataset.csv', index_col=0)
    #print(data)