import requests
from bs4 import BeautifulSoup



# TODO: General URL ---> Categories URL ---> Product Data


def get_category_url(session,headers): 
    url='https://tiki.vn/'
    response=session.get(url=url,headers=headers)
    bs=BeautifulSoup(response.content,'html.parser')
    categories_url=bs.find('div',class_='sc-cffe1c5-0 bKBPyH')
    specifi_url=categories_url.find_all('a',attrs={'href':True})
    try:
        file_location='C:/MY_PROJECT/Lazlytics---Lazada Product Analytics/ETL/TIKI/categories_url.txt'
        with open(file_location,'r',encoding='utf-8') as f:
                items = set(line.strip() for line in f)
    except FileNotFoundError:
        items = set()
    for x in specifi_url:
        href=x['href']
        if href not in items:
            with open(file_location, "a", encoding="utf-8") as f:
                f.write(href + "\n")
        else:
            pass
    return


if __name__=='__main__':
    session=requests.session()
    url='https://tiki.vn/'
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0'}
    get_category_url(session=session,headers=headers)