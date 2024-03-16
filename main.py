from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import os
from text_analysis import analyse


def main():

    df = pd.read_excel('./Input.xlsx')

    header = {
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0'
    }
    textFiles = []

    for idx in df.index:
        try:
            fileName = df['URL_ID'][idx]
            textFiles.append(fileName)
            directory = './text_results'
            file_path = os.path.join(directory,f'{fileName}.txt')

            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                if file_size > 0:
                    continue
                    
            url = df['URL'][idx]
            res = requests.get(url,headers=header)
            doc = bs(res.text,'html.parser')

            div = doc.find('div',class_='td-post-content tagdiv-type')
            title = doc.find('h1',class_='entry-title')

            try:
                textRm = doc.find('pre',class_='wp-block-preformatted')
                textRm.replace_with('')
            except AttributeError as err:
                pass
            
            with open(f'./text_results/{fileName}.txt','w',encoding='utf-8') as file:
                file.write(f'{title.text}\n{div.text}')

        except AttributeError as err:

            div = doc.find('div',class_='td_block_wrap tdb_single_content tdi_130 td-pb-border-top td_block_template_1 td-post-content tagdiv-type')

            title = doc.find('h1',class_='tdb-title-text')

            try:
                textRm = doc.find('pre',class_='wp-block-preformatted')
                textRm.replace_with('')
            except AttributeError:
                pass
            
            try:
                with open(f'./text_results/{fileName}.txt','w',encoding='utf-8') as file:
                    file.write(f'{title.text}\n{div.text}')
            except AttributeError:
                pass
    analyse(textFiles)


if __name__ == '__main__':
    main()