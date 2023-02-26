from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent
import time
from bs4 import BeautifulSoup
import requests
import datetime
import random
import re

def get_source_html(url):
    #Функция для скачивания html файла с сайта ozon
    useragent = UserAgent()
    ua = UserAgent(use_external_data=True)
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={useragent.chrome}")
    s = Service(r"E:\pyton\Ozon_parser2\chromedriver.exe")
    driver = webdriver.Chrome(
        service=s,
        options=options)
    try:
        driver.get(url)
        time.sleep(random.randint(3,8))
        with open("E:\\pyton\\OzonParser2\\html\\ozon_page.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

def get_item_price_and_name(html_path):
    try:
        with open(html_path, encoding="utf-8") as file:
            src = file.read()
            #soup = BeautifulSoup(src, "lxml")
            #items_divs = soup.findAll("div", class_='m4w mw6 wm7')
            tmp = '<div class="wm4 m6w w7m"><div><span class="m5w wm5"><span>1 079 ₽</span>&nbsp;</span><span class="mw6">1 546 ₽</span></div></div> <!----> <div class="m8w"><div data-replace-layout-path="[4][0][2][0][1][0][1][0][0][0][0][0]"><div class="x4-a x4-a2 x4-a3 u5m" style="background-color:#10c44c;color:#fff;" data-widget="webOzonAccountPrice"><div class="x4-a5">1 056 ₽  при оплате Ozon Картой</div><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" class="x4-a6 x4-a7 x4-a8" style="color:#fff;"><path fill="currentColor" d="M8 14A6 6 0 1 0 8 2a6 6 0 0 0 0 12Zm0-8a1 1 0 1 1 0-2 1 1 0 0 1 0 2Zm1 2v3a1 1 0 1 1-2 0V8a1 1 0 0 1 2 0Z"></path></svg></div></div></div></div> <!----></div></div> <!----> <div class="no8"></div> <div class="n8o">'
            text_list = re.findall(r"<span>([^<]*?)₽</span>", src)
            price = (''.join(text_list)).replace('\u2009', '')
            #price_text = items_divs[0].find("span", class_='mw5 m5w').span.text
            #price = price_text.split()[0]
            date = str(datetime.datetime.now())
        with open(results_txt_file, "a", encoding="utf-8") as file:
            file.write('На ' + date[:-7]+' Цена: '+ price + '\n')
    except Exception as ex:
        print(ex)

def main():
    #Считываем список url товаров
    with open(url_txt_file, "r", encoding="utf-8") as url_file:
        urls = [i.strip() for i in url_file.readlines()]
    for url in urls:
        get_source_html(url)
        get_item_price_and_name(f"E:\pyton\OzonParser2\html\ozon_page.html")


#Абсолютный путь к файлу со списком url на товары
url_txt_file = "E:\\pyton\\OzonParser2\\url\\url.txt"
#Абсолютный путь к файлу с результатам парсинга
results_txt_file = "E:\\pyton\\OzonParser2\\parser_res\\results.txt"
if __name__ == "__main__":
    main()
