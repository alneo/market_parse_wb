from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from time import sleep
import re
import os
from MySQLDatabase import MySQLDatabase


def add_tovar(tovar):
    # CREATE TABLE `market_cheks`.`wb_tovars` (
    # `id` INT NOT NULL AUTO_INCREMENT ,
    # `data_c` INT NOT NULL ,
    # `label` VARCHAR(255) NOT NULL ,
    # `price_cur` DOUBLE NOT NULL ,
    # `price_old` DOUBLE NOT NULL ,
    # `link` VARCHAR(255) NOT NULL ,
    # `price_val` VARCHAR(5) NOT NULL ,
    # PRIMARY KEY (`id`)) ENGINE = InnoDB;
    # ALTER TABLE `wb_tovars` CHANGE `data_c` `data_c` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP;
    table = "wb_tovars"
    table_hp = "wb_tovars_hp"
    db = MySQLDatabase(host="localhost", user="root", password="", database="market_cheks")
    db.connect()

    results = db.select_query(f"SELECT id FROM {table} WHERE id_item={tovar['id_item']}")
    if results:
        num_records = len(results)
        if num_records > 0:
            # проверить цену
            for row in results:
                id_tovar = row[0]
                value_to_insert = (
                    id_tovar,
                    tovar['id_item'],
                    tovar['price_cur']
                )
                db.insert_query(
                    f"INSERT INTO {table_hp} (id_tovar, id_item, price_cur) VALUES (%s, %s, %s)",
                    value_to_insert)
    else:
        value_to_insert = (
            tovar['label'],
            tovar['price_cur'],
            tovar['price_old'],
            tovar['link'],
            tovar['pricev'],
            tovar['id_item']
        )
        db.insert_query(f"INSERT INTO {table} (label, price_cur, price_old, link, price_val, id_item) VALUES (%s, %s, %s, %s, %s, %s)",value_to_insert)

    db.close_connection()

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
        number = match.group(1).replace(" ", "")  # Удаление пробелов из числа
        currency = match.group(2)
        price = {'price': number, 'cur': currency}
    return price


def url_get_id(url):
    match = re.search(r"/catalog/(\d+)/", url)
    if match:
        product_id = match.group(1)
    else:
        product_id = 0

    return product_id


def tovars_parse(url, razdel):
    driver = webdriver.Chrome()
    driver.get(url)
    # Скролл страницы
    for i in range(1, 10):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(2)
    # <article data-nm-id="275069596" id="c275069596" data-card-index="0" class="product-card j-card-item j-analitics-item   product-card--adv ">
    tovars = driver.find_elements(By.CLASS_NAME, "product-card.j-card-item")
    for tovar in tovars:
        link = parse_text(
            tovar, By.CLASS_NAME,
            "product-card__link.j-card-link.j-open-full-product-card",
            'attr',
            'href'
        )
        label = parse_text(
            tovar, By.CLASS_NAME,
            "product-card__link.j-card-link.j-open-full-product-card",
            'attr',
            'aria-label'
        )
        price_cur = parse_text(
            tovar, By.CLASS_NAME,
            "price__lower-price",
            'text',
            ''
        )
        price_old = parse_text(
            tovar, "xpath",
            ".//div[@class='product-card__price price']//del",
            'text',
            ''
        )

        tmp = parse_price_str(price_cur)
        price_cur = tmp['price']
        pricev = tmp['cur']

        tmp = parse_price_str(price_old)
        price_old = tmp['price']

        id_item = url_get_id(link)

        tovar_cur = {
            'price_cur': price_cur,
            'price_old': price_old,
            'label': label,
            'pricev': pricev,
            'link': link,
            'id_item': id_item
        }
        add_tovar(tovar_cur)

    driver.quit()

# razdel = 'Ноутбуки и ультрабуки'
# url = 'https://www.wildberries.ru/catalog/elektronika/noutbuki-pereferiya/noutbuki-ultrabuki'
razdel = 'Телефоны от 10000'
url = 'https://www.wildberries.ru/catalog/elektronika/telefony-i-gadzhety/mobilnye-telefony?page=1&sort=priceup&priceU=2000000%3B9000000'
tovars_parse(url, razdel)