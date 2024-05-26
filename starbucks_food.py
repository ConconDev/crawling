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
