import requests
from bs4 import BeautifulSoup
import json
import random
from selenium import webdriver
from selenium.webdriver.edge.options import Options
import time



def get_category_url(): # general lazada url -> specific categories url -> product data
    url='https://www.lazada.vn/#hp-categories'
    headers={'User_Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0',
             'Referer':'https://www.lazada.vn/'}
    response=requests.get(url=url,headers=headers)
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




def crawling():
    file_location = 'C:/MY_PROJECT/Lazlytics---Lazada Product Analytics/ETL/categories_url.txt'
    session = requests.Session()

    with open(file_location, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('//'):
                line = 'https:' + line.strip()
                
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0",
                    "Referer": "https://www.lazada.vn/",
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "X-Requested-With": "XMLHttpRequest"
                }

                response = session.get(line, params={"ajax": "true"}, headers=headers, timeout=15)

                if "application/json" in response.headers.get("Content-Type", ""):
                    print("Got JSON:", line)
                    listitem=response.json().get('listItems')
                    # TODO: datalake
                    
                else:
                    print("Punish, thử với Selenium...")


                    edge_options = Options()
                    edge_options.add_argument("--headless")
                    driver = webdriver.Edge(options=edge_options)
                    driver.get("https://www.lazada.vn/")

                    cookies = driver.get_cookies()
                    driver.quit()

                    cookie_str = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
                    headers["Cookie"] = cookie_str

                    response = session.get(line, params={"ajax": "true"}, headers=headers, timeout=15)

                    if "application/json" in response.headers.get("Content-Type", ""):
                        print("Got JSON after Selenium:", line)
                        listitem=response.json().get('listItems')
                        # TODO: Lưu vào datalake
                    else:
                        print("STILL BLOCKED:", line)


                delay = random.uniform(10, 20)
                print(f"Sleep {delay:.2f} seconds...")
                time.sleep(delay)

