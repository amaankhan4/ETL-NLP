# from openpyxl import workbook
from nltk.tokenize import word_tokenize
import pandas as pd
import os

def analyse(fileName):

    pos_score,neg_score,subjectivity,polarity = [0 for i in range(0,100)],[0 for i in range(0,100)],[0 for i in range(0,100)],[0 for i in range(0,100)]
    df = pd.read_excel('./Input.xlsx')
    wordCount = 0

    txt = []

    for file in fileName:
        try:
            f = open(f'./text_results/{file}.txt','r',encoding='utf-8')
        except FileNotFoundError as err:
            print(err)
            return
        txt.append(word_tokenize(f.read()))

    stopWords = []

    files = os.listdir('./StopWords')

    for file in files:
        file_path = os.path.join('./StopWords',file)
        with open(file_path,'r') as f:
            stopWords.append(word_tokenize(f.read()))


    for word in stopWords:
        for q in word:
            txt = [[item for item in sublist if item != q] for sublist in txt]  


    postivewords = []
    negativewords = []

    try:
        with open('./MasterDictionary/positive-words.txt','r') as f:
            postivewords = (word_tokenize(f.read()))

        with open('./MasterDictionary/negative-words.txt','r') as f:
            negativewords = (word_tokenize(f.read()))

    except FileNotFoundError:
        print(FileNotFoundError)


    for pos in postivewords:
        for sublist in txt:
            for word in sublist:
                wordCount += 1
                if pos == word:
                    pos_score[txt.index(sublist)] += 1
        


    for neg in negativewords:
        for sublist in txt:
            for word in sublist:
                if neg == word:
                    neg_score[txt.index(sublist)] += 1
        

    for idx in range(0,100):

        polarity[idx] = (pos_score[idx] - neg_score[idx]) / ((pos_score[idx] + neg_score[idx]) + 0.000001)

        subjectivity[idx] = (pos_score[idx] + neg_score[idx]) / (wordCount+0.000001)

    data = {'URL_ID':fileName,'Positive Score':pos_score,'Negative Score':neg_score,
            'Polarity':polarity,'Subjectivity':subjectivity}
    
    df2 = pd.DataFrame(data)

    df = df.merge(df2,how='left',on='URL_ID')

    df.to_excel('Output.xlsx',index=False)