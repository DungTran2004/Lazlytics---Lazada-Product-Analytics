from datetime import datetime
import os 
import json
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from urllib.parse import urlparse, urlunparse
import time
import pandas as pd

def create_current_date_file(platform:str,batch:int):
    if platform not in ['Lazada', 'Tiki', 'Shopee']:
        raise ValueError("Platform must be one of ['Lazada', 'Tiki', 'Shopee']")
    
    
    root_path = 'C:/MY_PROJECT/Lazlytics---Lazada Product Analytics/RawData'
    today = datetime.now()
    date_format = today.strftime("%Y-%m-%d")

    folder_path = os.path.join(root_path, platform)
    os.makedirs(folder_path, exist_ok=True) 
    
    file_path = os.path.join(folder_path, f"{date_format}_{batch}.json")
    
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            pass
    
    return file_path




def save_data(new_data, file_path): # Have to update, hien tai phai doc toan bo du lieu cua file, nen sua thanh append truc tiep
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    if isinstance(new_data, list):
        data.extend(new_data)
    else:
        data.append(new_data)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
        
        
        
        
        
def get_cookie():
    try:
        edge_options = webdriver.EdgeOptions()
        edge_options.add_argument("--headless=new")  # nếu muốn chạy ẩn
        edge_options.add_argument("--disable-gpu")
        edge_options.add_argument("--log-level=3")  # 0=all, 3=error only
        edge_options.add_argument("--silent")
        edge_options.add_argument("--no-sandbox")

        service = Service(r"C:/MY_PROJECT/Lazlytics---Lazada Product Analytics/edgedriver_win64/msedgedriver.exe")
        driver = webdriver.Edge(service=service, options=edge_options)
        
        driver.get("https://www.lazada.vn/")
        time.sleep(3)
        cookie = "; ".join([f"{c['name']}={c['value']}" for c in driver.get_cookies()])
        print("SUCCESS GET COOKIE")
    except Exception as e:
        print("ERROR WHEN GET COOKIE: ",e)
        
    driver.quit()
    return cookie





def format_url(url: str) -> str:
    url = url.strip()
    if url.startswith('//'):
        url = 'https:' + url
    
    parsed = urlparse(url)
    path = parsed.path
    if not path.endswith('/'):
        path += '/'
    
    formatted = urlunparse((
        parsed.scheme,
        parsed.netloc,
        path,
        parsed.params,
        parsed.query,
        parsed.fragment
    ))
    
    return formatted



def to_parquet(json_file_path, platform):
    return
