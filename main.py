from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent
import time
import requests
import datetime
import random
import re
import json

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

def main():
    html_path = f"E:\pyton\OzonParser2\html\ozon_page.html"
    result_list = []
    with open(url_txt_file, "r", encoding="utf-8") as url_file:
        urls = [i.split('?')[0] for i in url_file.readlines()]
    for item_url in urls:
        request_time = str(datetime.datetime.now())[:-7]
        get_source_html(item_url)
        try:
            with open(html_path, encoding="utf-8") as file:
                src = file.read()
                price_text_list = re.findall(r"<span>([^<]*?)₽</span>", src)
                item_price = (''.join(price_text_list)).replace('\u2009', '')
                name_text_list = re.findall(r"webProductHeading\"><h1[^>]*?>([^<]*?)</h1>", src)
                item_name = name_text_list[0]
                result_list.append(
                    {
                        "item_name": item_name,
                        "item_price": item_price,
                        "item_url": item_url,
                        "request_time": request_time
                    }
                )
        except Exception as ex:
            print(ex)
    with open(results_json_file, "a", encoding="utf-8") as file:
        json.dump(result_list, file, indent=4, ensure_ascii=False)


#Абсолютный путь к файлу со списком url на товары
url_txt_file = "E:\\pyton\\OzonParser2\\url\\urls.txt"
#Абсолютный путь к файлу с результатам парсинга
results_json_file = "E:\\pyton\\OzonParser2\\parser_res\\results.json"
if __name__ == "__main__":
    main()
