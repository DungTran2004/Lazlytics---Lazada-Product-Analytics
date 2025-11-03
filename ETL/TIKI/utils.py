import datetime
from datetime import datetime
import os
import json

def get_api_url(category_url:str,page:int)->str:
    category_url=category_url.split('/')
    urlkey=category_url[1]
    category=category_url[2][1:]
    api_url=f"https://tiki.vn/api/personalish/v1/blocks/listings?limit=5&sort=top_seller&page={page}&urlKey={urlkey}&category={category}"
    return api_url



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
        print('SUCCESS SAVE DATA IN FILE')