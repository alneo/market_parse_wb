from MySQLDatabase import MySQLDatabase
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
from time import sleep

"""
Получение товаров из таблицы и проверка текущей цены
"""


def parse_text(driver1, type, type_text, get_type, get_what):
    value = ''
    try:
        if get_type == 'attr':
            value = driver1.find_element(type, type_text).get_dom_attribute(get_what)
        if get_type == 'text':
            value = driver1.find_element(type, type_text).text
    except(NoSuchElementException):
        pass
    return value


def parse_price_str(text):
    price = {'price':0,'cur':''}
    match = re.search(r"([\d\s]+)\s*([₽$€¥£])", text)
    if match:
        number = match.group(1).replace(" ", "").replace("\xa0", "")  # Удаление пробелов из числа
        currency = match.group(2)
        price = {'price': number, 'cur': currency}
    return price


def check_price(url):
    tmp = {
        'price': -1,
        'cur': ''
    }
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")  # Запуск в headless режиме
    driver = webdriver.Chrome()  # options=options
    driver.get(url)
    wait = WebDriverWait(driver, 30)
    try:
        # Ожидаем, пока элемент появится на странице
        price_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "price-block__final-price")))
        # Получаем текст элемента
        price = driver.execute_script("return arguments[0].textContent", price_element)
        #
        # price = parse_text(
        #     driver, By.CLASS_NAME,
        #     "price-block__final-price",
        #     'text',
        #     ''
        # )
        # print(price)
        tmp = parse_price_str(price)
    except(TimeoutException):
        pass
    #print(tmp)
    driver.quit()
    #exit()
    # price_cur = tmp['price']
    # pricev = tmp['cur']
    return tmp


def tovars_get():
    table = "wb_tovars"
    table_hp = "wb_tovars_hp"
    db = MySQLDatabase(host="localhost", user="root", password="", database="market_cheks")
    db.connect()
    results = db.select_query(f"SELECT id, price_cur, link, id_item FROM {table} WHERE `id`>50;")
    if results:
        num_records = len(results)
        if num_records > 0:
            for row in results:
                id_tovar = row[0]
                price_cur = row[1]
                result1 = db.select_query(f"SELECT price_cur FROM {table_hp} WHERE `id_tovar`={id_tovar} ORDER BY `data_c` DESC LIMIT 1;")
                if result1:
                    for row1 in result1:
                        price_cur = row1[0]
                link = row[2]
                id_item = row[3]
                tmp = check_price(link)
                price_new = float(tmp['price'])
                if price_new!=-1:
                    if price_cur != price_new:
                        value_to_insert = (
                            id_tovar,
                            id_item,
                            price_new
                        )
                        db.insert_query(
                            f"INSERT INTO {table_hp} (id_tovar, id_item, price_cur) VALUES (%s, %s, %s)",
                            value_to_insert)
                        print(f"Цена изменилась {price_cur}->{price_new}")
                    else:
                        print(f"Цена не изменилась {price_cur}={price_new}")
                else:
                    print(f"Цена не определилась")

tovars_get()