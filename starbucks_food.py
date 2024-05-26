from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"


options = Options()

options.add_experimental_option("detach", True)

options.add_argument(f"user-agent={user_agent}")

url = "https://www.starbucks.co.kr/menu/food_list.do"

driver = webdriver.Chrome(options=options)

driver.get(url)
time.sleep(1)


html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

bf_items = soup.select(".product_list ul")
items = []
for item in bf_items:
    if item.has_attr("class"):
        print(item)
        items.append(item)

data = []

count1 = 0
count = 0
for item in items:
    product_lists = item.find_all(class_="menuDataSet")
    items_name = item.get("class")[0]

    print(f"-------{items_name}-------")
    for rank, product in enumerate(product_lists, 1):
        ko_name = product.find("dd").text
        a = product.find("a")
        number = a.get("prod")

        product_url = "https://www.starbucks.co.kr/menu/drink_view.do?product_cd=" + number
        driver.get(product_url)
        time.sleep(1)

        html2 = driver.page_source
        soup2 = BeautifulSoup(html2, "html.parser")

        item = soup2.select(".product_view_detail")[0]
        detail = item.find(class_="myAssignZone")

        eng_name = detail.find("h4").find("span").text
        explanation = detail.find(class_="t1").text

        img_url = item.find_all(class_="m_view_img")[0]["src"]

        print(f"{rank}번째 빵")
        print(ko_name)
        print(eng_name)
        print(explanation)
        print(img_url)

        info_all = item.find(class_="product_info_content").find_all("li")
        dict_info = {}
        for info in info_all:
            info_key = info.get("class")[0]
            info_value = info.find("dd").text
            print(f"{info_key}: {info_value}")
            dict_info[info_key] = info_value

        product_factor = item.find_all(class_="product_factor")
        if product_factor:
            allergy_factor = product_factor[0].text.replace("\n", "")
        else:
            allergy_factor = None

        data.append({
            "Korean Name": ko_name,
            "English Name": eng_name,
            "Image Url": img_url,
            "Explanation": explanation,
            "Category": items_name,
            "Factors": allergy_factor,
            **dict_info
        })

df = pd.DataFrame(data)
df.to_csv("starbucks_food.csv")
print(df.columns)
print(df)

