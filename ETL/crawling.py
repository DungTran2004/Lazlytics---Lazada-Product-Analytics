import requests
from bs4 import BeautifulSoup
import random
import time
from requests.models import PreparedRequest
from urllib.parse import urlparse
from utils import *


# TODO: General URL ---> Categories URL ---> Product Data


def get_category_url(session,headers): 
    url='https://www.lazada.vn/#hp-categories'
    response=session.get(url=url,headers=headers)
    bs=BeautifulSoup(response.content,'html.parser')
    categories_url=bs.find_all('a',class_='pc-custom-link card-categories-li hp-mod-card-hover')
    try:
        file_location='C:/MY_PROJECT/Lazlytics---Lazada Product Analytics/ETL/categories_url.txt'
        with open(file_location,'r',encoding='utf-8') as f:
                items = set(line.strip() for line in f)
    except FileNotFoundError:
        items = set()
    for x in categories_url:
        href=x['href']
        if href not in items:
            with open(file_location, "a", encoding="utf-8") as f:
                f.write(href + "\n")
        else:
            pass
    return


    
def crawling(url, session, headers, page):
    line = format_url(url)
    while True:
        try:
            print(f'---------START CRAWLING---------')
            params = {
                        "ajax": "true",
                        "isFirstRequest": "true",
                        "page": page
                    }
            req = PreparedRequest()
            req.prepare_url(line, params)
            response = session.get(req.url, headers=headers, timeout=15)

            if response.status_code != 200:
                print(f"----FAILED {req.url} - STATUS: {response.status_code}")
                break

            if "application/json" in response.headers.get("Content-Type", ""):
                print("----SUCCESS GET DATA FROM: ", req.url)
                break

            else:
                print('MAYBE COOKIE IS END')
                session.cookies.clear()
                cookie = get_cookie()
                domain = urlparse(url).netloc 

                for c in cookie.split('; '):
                    if '=' in c:
                        k, v = c.split('=', 1)
                        session.cookies.set(k, v, domain=domain)
                continue  

        except requests.RequestException as e:
            print(f"----ERROR WHEN CRAWLING {req.url}: {e}")
            break

    listitem = response.json().get('mods',[])['listItems']
    if not listitem:
        print(f"----NO DATA (listItems) IN: {req.url}")
    else:
        date_file = create_current_date_file()
        save_data(listitem, date_file)
        return

        
            
            
if __name__=='__main__':
    session=requests.session()
    headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0",
                "Referer": "https://www.lazada.vn/",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "X-Requested-With": "XMLHttpRequest"
            }
    
    print("------GETTING COOKIE FOR THE 1ST TIME------")
    cookie = get_cookie()
    domain = "www.lazada.vn"
    for c in cookie.split('; '):
        if '=' in c:
            k, v = c.split('=', 1)
            session.cookies.set(k, v, domain=domain)
            
    with open('C:/MY_PROJECT/Lazlytics---Lazada Product Analytics/ETL/categories_url.txt', 'r', encoding='utf-8') as f:
        for line in f:
            crawling(url=line.strip(), session=session, headers=headers, page=1)