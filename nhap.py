import requests
from ETL.utils  import get_cookie
from urllib.parse import urlparse


session=requests.session()

url='https://www.lazada.vn/ao-hoodie-cua-nam/?up_id=3140240239&clickTrackInfo=ctr--0.0___matchType--20___description--Gi%25E1%25BA%25A3m%2B33%2525___seedItemMatchType--c2i___bucket--0___spm_id--category.hp___seedItemScore--0.0___abId--333258___score--0.09555488___pvid--bbdb38e2-2b1b-4bcf-89ee-4b857dbb18fc___refer--___appId--7253___seedItemId--3140240239___scm--1007.17253.333258.0___categoryId--6424___cvr--0.0___timestamp--1757431133836&from=hp_categories&item_id=3140240239&version=v2&q=%C3%A1o%20hoodies%20%20sweater%20nam&params=%7B%22catIdLv1%22%3A%2262541004%22%2C%22pvid%22%3A%22bbdb38e2-2b1b-4bcf-89ee-4b857dbb18fc%22%2C%22src%22%3A%22ald%22%2C%22categoryName%22%3A%22%25C3%2581o%2Bhoodies%2B%2Bsweater%2Bnam%22%2C%22categoryId%22%3A%226424%22%7D&src=hp_categories&ajax=true&isFirstRequest=true&page=1'

headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0",
                "Referer": "https://www.lazada.vn/",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "X-Requested-With": "XMLHttpRequest"
            }


cookie = get_cookie()
domain = urlparse(url).netloc 

for c in cookie.split('; '):
    if '=' in c:
        k, v = c.split('=', 1)
        session.cookies.set(k, v, domain=domain)

response=session.get(url=url,headers=headers)
print(response.headers)