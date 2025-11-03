import requests




# TODO: SHOPEE -> CATEGORY (catid,display_name) -> CATEGORY URL -> PRODUCT DATA
def get_category(session,headers): # use this function once or when want to expand the diversity of the dataset
    url='https://shopee.vn/api/v4/pages/get_category_tree'
    try:
        response=session.get(url,headers)
        if response.status_code!=200:
            print('Status fail when get request')
            return
        else:
            data=response.json()
            category_list=data.get('data')['category_list']
            for category in category_list:
                catid=category.get('catid')
                display_name=category.get('display_name')
            
    except Exception as e:
        pass
    return





def crawling():
    return



if __name__=='__main__':

