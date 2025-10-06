import requests
from bs4 import BeautifulSoup
import random
import time
from untils import *

def get_category_url(): # general lazada url -> specific categories url -> product data
    url='https://www.lazada.vn/#hp-categories'
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0',
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
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0",
    "Referer": "https://www.lazada.vn/",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest"
}
    with open(file_location, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line.startswith('//'):
                line = 'https:' + line
                
                if headers.get('Cookie') is None:
                    cookie=get_cookie()
                    if cookie:
                        print('LAY COOKIE THANH CONG')
                        headers['Cookie']=cookie
                    
                    
                try:
                    response = session.get(line, params={"ajax": "true"}, headers=headers, timeout=15)
                    if response.status_code != 200:
                        print(f"FAILED {line} - STATUS: {response.status_code}")
                        continue
                except requests.RequestException as e:
                    print(f"LỖI KHI REQUEST {line}: {e}")
                    continue

                if "application/json" in response.headers.get("Content-Type", ""):
                    print("LAY DATA THANH CONG TU: ", line)
            
                else:
                    print("LAY DATA KHONG THANH CONG TU: ", line)
                    print("THU LAY LAI COOKIE")
                    cookie=get_cookie()
                    headers['Cookie']=cookie
                    try:
                        response = session.get(line, params={"ajax": "true"}, headers=headers, timeout=15)
                        if response.status_code != 200:
                            print(f"FAILED {line} - STATUS: {response.status_code}")
                        else:
                            if "application/json" in response.headers.get("Content-Type", ""):
                                print("LAY DATA THANH CONG TU: ", line)
                            else:
                                print("KHONG THE LAY DATA TU: ", line)
                                continue
                    except requests.RequestException as e:
                        print(f"LỖI KHI REQUEST {line}: {e}")
                        continue
                    
                
                listitem=response.json().get('listItems',[])
                if not listitem:
                    print(f"KHÔNG CÓ DATA TRONG: {line}")
                    continue
                else:
                    date_file=create_current_date_file()
                    
                    save_data(listitem, date_file)
            
                    
            delay = random.uniform(10, 20)
            
            print(f"Sleep {delay:.2f} seconds...")
            
            time.sleep(delay)