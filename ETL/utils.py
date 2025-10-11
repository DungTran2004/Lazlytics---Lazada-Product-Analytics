from datetime import datetime
import os 
import json
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from urllib.parse import urlparse, urlunparse
import time


def create_current_date_file():
    today = datetime.now()
    date_format = today.strftime("%Y-%m-%d")  
    folder = "C:/MY_PROJECT/Lazlytics---Lazada Product Analytics/RawData/Lazada"
    os.makedirs(folder, exist_ok=True)       
    
    file_path = f"{folder}/{date_format}.json"
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            pass
    return file_path





def save_data(new_data, file_path):
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
    edge_options = webdriver.EdgeOptions()
    edge_options.add_argument("--headless=new")  # nếu muốn chạy ẩn
    edge_options.add_argument("--disable-gpu")
    edge_options.add_argument("--no-sandbox")

    service = Service(r"C:/MY_PROJECT/Lazlytics---Lazada Product Analytics/edgedriver_win64/msedgedriver.exe")
    driver = webdriver.Edge(service=service, options=edge_options)
    
    driver.get("https://www.lazada.vn/")
    time.sleep(3)
    cookie = "; ".join([f"{c['name']}={c['value']}" for c in driver.get_cookies()])
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
