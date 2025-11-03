import requests
from bs4 import BeautifulSoup
from utils import *


# TODO: General URL ---> Categories URL ---> API Url ---> Product Data


def get_category_url(session,headers): # RUN TO GET MORE GENERAL CATEGORY URL (IN THIS URL WILL HAVE DETAIL PRODUCT DATA)
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




def crawling(category_url:str,session,headers,page:int,batch=None):
    api_url=get_api_url(category_url=category_url,page=page)
    try:
        print('-------START CRAWLING-------')
        response=session.get(api_url,headers=headers,timeout=15)
        if response.status_code != 200:
            print(f"----FAILED {api_url} - STATUS: {response.status_code}")
            return

        if "application/json" in response.headers.get("Content-Type", ""):
            print("----SUCCESS GET DATA FROM: ", api_url)
        else:
            pass
        
    except Exception as e:
        print('ERROR WHEN CRAWLING URL: ',api_url, e)
    data=response.json().get('data')
    if data:
        return data
    else:
        print('NO DATA IN URL: ',api_url)
        return
    
    


if __name__=='__main__':
    session=requests.session()
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0'}
    file_path=create_current_date_file('Tiki',1)
    data=crawling('/nha-sach-tiki/c8322',session=session,headers=headers,page=1)
    save_data(data,file_path)
    