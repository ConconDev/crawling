from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

options = Options()
options.add_argument("--start-maximized")
options.add_experimental_option("detach", True)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

baseurl = "https://m.cgv.co.kr/WebApp/GiftV5/storeCategory.aspx?CategoryIdx=4"
driver.get(baseurl)
time.sleep(1)

data = []

def process_items(items, cate):
    for i in range(len(items)):
        items = driver.find_elements(By.CLASS_NAME, "img_wrap")
        titles1 = driver.find_elements(By.CLASS_NAME, "list_type0_title")
        
        product_name = titles1[i].text
        items[i].click()
        time.sleep(1)
        
        price = driver.find_element(By.CLASS_NAME, "store_deatail_sale_price").text
        
        info = driver.find_element(By.CLASS_NAME, "store_deatail_add_info")
        info_dict = {}
        
        detail = driver.find_element(By.CLASS_NAME,"store_detail_product_introduce")
        
        for dt, dd in zip(info.find_elements(By.TAG_NAME, "dt"), info.find_elements(By.TAG_NAME, "dd")):
            info_dict[dt.text] = dd.text
            
        # 필요한 정보만 추출
        item_data = {
            "Product Name": product_name,
            "Price": price,
            "Composition": info_dict.get("상품구성"),
            "Expiration": info_dict.get("유효기간"),
            "Origin": info_dict.get("원산지"),
            "Detail":detail
        }
        data.append(item_data)

        driver.back()
        driver.find_element(By.LINK_TEXT, cate).click()
        time.sleep(1)

# 세트 메뉴
cate1 = "콤보"
items1 = driver.find_elements(By.CLASS_NAME, "img_wrap")
process_items(items1, cate1)

cate2 = "팝콘"
driver.find_element(By.LINK_TEXT, "팝콘").click()
time.sleep(1)
items2 = driver.find_elements(By.CLASS_NAME, "img_wrap")
process_items(items2, cate2)

cate3 = "음료"
driver.find_element(By.LINK_TEXT, "음료").click()
time.sleep(1)
items3 = driver.find_elements(By.CLASS_NAME, "img_wrap")
process_items(items3, cate3)

cate4 = "스낵"
driver.find_element(By.LINK_TEXT, "스낵").click()
time.sleep(1)
items4 = driver.find_elements(By.CLASS_NAME, "img_wrap")
process_items(items4, cate4)

# DataFrame으로 변환하여 CSV로 저장
df = pd.DataFrame(data)
df.to_csv("cgv_food_info.csv", index=False, encoding='utf-8-sig')
print(df)