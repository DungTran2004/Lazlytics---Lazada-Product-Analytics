import requests
from bs4 import BeautifulSoup
import json
import random
from selenium import webdriver
from selenium.webdriver.edge.service import Service
import time
import boto3
from botocore.client import Config
from keys import *
import os
from datetime import datetime

key_id=datalake_key['keyID']
key_name=datalake_key['keyName']
application_key=datalake_key['applicationKey']
endpoint=datalake_key['Endpoint']


def current_date():
    today=datetime.now()
    return f'{today.year}-{today.month}-{today.day}'


def create_current_date_file():
    today = datetime.now()
    date_format = today.strftime("%Y-%m-%d")  
    folder = "./Lazada"
    os.makedirs(folder, exist_ok=True)       
    
    file_path = f"{folder}/{date_format}.json"
    
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            pass  
    
    return file_path
    


def append_to_json(new_data, file_path):
    """Thêm dữ liệu vào file JSON dạng list"""
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    # Nếu new_data là list thì nối, còn không thì append
    if isinstance(new_data, list):
        data.extend(new_data)
    else:
        data.append(new_data)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
  
  
        
def get_cookie():
    edge_options = webdriver.EdgeOptions()
    edge_options.add_argument("--headless=new")  # nếu muốn chạy ẩn
    edge_options.add_argument("--disable-gpu")
    edge_options.add_argument("--no-sandbox")

    service = Service(r"C:/MY_PROJECT/Lazlytics---Lazada Product Analytics/edgedriver_win64/msedgedriver.exe")
    driver = webdriver.Edge(service=service, options=edge_options)
    
    driver.get("https://www.lazada.vn/")
    cookie = "; ".join([f"{c['name']}={c['value']}" for c in driver.get_cookies()])
    driver.quit()
    return cookie



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
                    
                    append_to_json(listitem, date_file)
            
            break
                    
            delay = random.uniform(10, 20)
            
            print(f"Sleep {delay:.2f} seconds...")
            
            time.sleep(delay)





def load_datalake_layer1(local_dir):
    s3=boto3.client(
    "s3",
    endpoint_url=endpoint,
    aws_access_key_id=key_id,
    aws_secret_access_key=application_key,
    config=Config(signature_version="s3v4")
    )
    bucket_name='Lazlytics-DataLake'
    for filename in os.listdir(local_dir):
        local_path = os.path.join(local_dir, filename)
        object_key = f"RawData/Lazada/2025-09-11/{filename}"
        s3.upload_file(local_path, bucket_name, object_key)
        print(f"✅ Uploaded {filename} → {object_key}")
    return

def load_datalake_layer2():
    return

def load_datalake_layer3():
    return


if __name__=='__main__':
    crawling()