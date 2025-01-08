import requests
from MySQLDatabase import MySQLDatabase
import json

class WB_tovar:
    def __init__(self):
        pass

    def get_json_from_url(self, url):
        """
        Получает JSON-данные по заданному URL.

        Args:
          url: URL, с которого нужно получить данные.

        Returns:
          Словарь Python, содержащий JSON-данные, или None в случае ошибки.
      """

        try:
            response = requests.get(url)
            response.raise_for_status()  # Проверяем статус ответа

            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к URL {url}: {e}")
            return None

    def get_json_tovar_card(self, **kwargs):
        """
        Информация о карточке товара
        https://basket-14.wbbasket.ru/vol2163/part216373/216373122/info/ru/card.json
        """
        url = ""
        domen = ""
        vol = ""
        part = ""
        id = 0
        error = ""
        if "url" in kwargs:
            url = kwargs.get('url')
        else:
            if "domen" in kwargs:
                domen = kwargs.get('domen')
            if "vol" in kwargs:
                vol = kwargs.get('vol')
            if "part" in kwargs:
                part = kwargs.get('part')
            if "id" in kwargs:
                id = kwargs.get('id')
        if url == "":
            if domen == "" or vol == "" or part == "" or id == 0:
                error = "Необходимо указать url или domen, vol, part, id"
            else:
                url = f"https://{domen}/vol{vol}/part{part}/{id}/info/ru/card.json"
        if error == "":
            json_data = self.get_json_from_url(url)
            if json_data:
                return json_data
            else:
                print("Не удалось получить JSON-данные.")
        else:
            print(error)

    def get_json_tovar_info(self, **kwargs):
        """
        Информация о товаре
        https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-1255987&spp=30&hide_dtype=10&ab_testing=false&nm=216373122
        https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-1255987&spp=30&hide_dtype=10&ab_testing=false&nm=186893094;229441701;302192278
        """
        url = ""
        domen = ""  # card.wb.ru
        id = 0  # 186893094
        error = ""
        if "url" in kwargs:
            url = kwargs.get('url')
        else:
            if "domen" in kwargs:
                domen = kwargs.get('domen')
            if "id" in kwargs:
                id = kwargs.get('id')
        if url == "":
            if domen == "" or id == 0:
                error = "Необходимо указать url или domen, id"
            else:
                url = f"https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-1255987&spp=30&hide_dtype=10&ab_testing=false&nm={id}"
        if error == "":
            json_data = self.get_json_from_url(url)
            if json_data:
                return json_data
            else:
                print("Не удалось получить JSON-данные.")
        else:
            print(error)

    def get_json_tovars_detail(self, **kwargs):
        """Получение цены товара"""
        url = "https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-1255987&spp=30&hide_dtype=10&ab_testing=false&nm=186893094;229441701;302192278"
        url = "https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-1255987&spp=30&hide_dtype=10&ab_testing=false&nm=216373122"
        # https://www.wildberries.ru/catalog/216373122/detail.aspx

        if "id" in kwargs:
            id = kwargs.get('id')
            url = f"https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-1255987&spp=30&hide_dtype=10&ab_testing=false&nm={id}"
            json_data = self.get_json_from_url(url)
            if json_data:
                return json_data
            else:
                print("Не удалось получить JSON-данные.")
        else:
            return "Уажите ID товара"

    def get_json_tovars_list(self, **kwargs):
        """
        Получение списка товара по параметрам
        :param kwargs:
            url = "https://catalog.wb.ru/catalog/electronic20/v2/catalog"
            price_ot = 2000000
            price_do = 9000000
            q1 =  "nm%3A216373122%2Bkey%3A%D0%A1%D0%BC%D0%B0%D1%80%D1%82%D1%84%D0%BE%D0%BD_Redmi_Note_10_Pro"
        :return:
        """

        url = "https://catalog.wb.ru/catalog/electronic20/v2/catalog"
        price_ot = 0
        price_do = 90000000
        q1 = ""
        if "url" in kwargs:
            url = kwargs.get('url')
        if "price_ot" in kwargs:
            price_ot = kwargs.get('price_ot')
        if "price_do" in kwargs:
            price_do = kwargs.get('price_do')
        if "q1" in kwargs:
            q1 = "&q1=" + kwargs.get('q1')
        url = f"{url}?ab_testing=false&appType=1&curr=rub&dest=-1255987&hide_dtype=10&lang=ru&page=1&priceU={price_ot};{price_do}{q1}&sort=priceup&spp=30&subject=516"
        json_data = self.get_json_from_url(url)
        if json_data:
            return json_data
        else:
            #print("Не удалось получить JSON-данные списка товаров.")
            return None

    def tovar_add_table_brands(self, db, brand):
        # wb_brands: _id, brandId, siteBrandId, brand(str)
        results = db.select_query(f"SELECT _id FROM wb_brands WHERE `brandId`={brand[0]};")
        if results is None or len(results) == 0:
            id = db.insert_query(f"INSERT INTO wb_brands (brandId, siteBrandId, brand) VALUES (%s, %s, %s)", brand)
            return id
        else:
            return 0

    def tovar_add_table_suppliers(self, db, supplier):
        # wb_suppliers: _id, supplierId, supplierRating(float), supplierFlags, supplier(str)
        results = db.select_query(f"SELECT _id FROM wb_suppliers WHERE `supplierId`={supplier[0]};")
        if results is None or len(results) == 0:
            id = db.insert_query(f"INSERT INTO wb_suppliers (supplierId, supplierRating, supplierFlags, supplier) VALUES (%s, %s, %s, %s)", supplier)
            return id
        else:
            return 0

    def tovar_add_table_products(self, db, tovar):
        # wb_products: brands_id, suppliers_id, time1, time2, wh, dtype, dist, id, root, kindId, colors(str), subjectId, subjectParentId, name(str), entity(str), matchId, pics, rating, reviewRating, nmReviewRating, feedbacks, nmFeedbacks, panelPromoId, promoTextCard(str), promoTextCat(str), volume, viewFlags, sizes_saleConditions, sizes_payload(str), totalQuantity,meta(text)

        if 'brandId' not in tovar:
            tovar['brandId'] = 0
        if 'supplierId' not in tovar:
            tovar['supplierId'] = 0
        if 'time1' not in tovar:
            tovar['time1'] = 0
        if 'time2' not in tovar:
            tovar['time2'] = 0
        if 'wh' not in tovar:
            tovar['wh'] = 0
        if 'dtype' not in tovar:
            tovar['dtype'] = 0
        if 'dist' not in tovar:
            tovar['dist'] = 0
        if 'id' not in tovar:
            tovar['id'] = 0
        if 'root' not in tovar:
            tovar['root'] = 0
        if 'kindId' not in tovar:
            tovar['kindId'] = 0
        if 'colors' not in tovar:
            tovar['colors'] = '[]'
        if 'subjectId' not in tovar:
            tovar['subjectId'] = 0
        if 'subjectParentId' not in tovar:
            tovar['subjectParentId'] = 0
        if 'name' not in tovar:
            tovar['name'] = ''
        if 'entity' not in tovar:
            tovar['entity'] = ''
        if 'matchId' not in tovar:
            tovar['matchId'] = 0
        if 'pics' not in tovar:
            tovar['pics'] = 0
        if 'rating' not in tovar:
            tovar['rating'] = 0
        if 'reviewRating' not in tovar:
            tovar['reviewRating'] = 0
        if 'nmReviewRating' not in tovar:
            tovar['nmReviewRating'] = 0
        if 'feedbacks' not in tovar:
            tovar['feedbacks'] = 0
        if 'panelPromoId' not in tovar:
            tovar['panelPromoId'] = 0
        if 'promoTextCard' not in tovar:
            tovar['promoTextCard'] = ''
        if 'promoTextCat' not in tovar:
            tovar['promoTextCat'] = ''
        if 'volume' not in tovar:
            tovar['volume'] = 0
        if 'viewFlags' not in tovar:
            tovar['viewFlags'] = 0
        if 'totalQuantity' not in tovar:
            tovar['totalQuantity'] = 0
        if 'meta' not in tovar:
            tovar['meta'] = '[]'

        product = (
            tovar['brandId'],
            tovar['supplierId'],
            tovar['time1'],
            tovar['time2'],
            tovar['wh'],
            tovar['dtype'],
            tovar['dist'],
            tovar['id'],
            tovar['root'],
            tovar['kindId'],
            json.dumps(tovar['colors']),
            tovar['subjectId'],
            tovar['subjectParentId'],
            tovar['name'],
            tovar['entity'],
            tovar['matchId'],
            tovar['pics'],
            tovar['rating'],
            tovar['reviewRating'],
            tovar['nmReviewRating'],
            tovar['feedbacks'],
            tovar['nmFeedbacks'],
            tovar['panelPromoId'],
            tovar['promoTextCard'],
            tovar['promoTextCat'],
            tovar['volume'],
            tovar['viewFlags'],
            tovar['totalQuantity'],
            json.dumps(tovar['meta'])
        )

        results = db.select_query(f"SELECT _id FROM wb_products WHERE `id`={product[7]};")
        if results is None or len(results) == 0:
            id = db.insert_query(f"INSERT INTO wb_products (brands_id, suppliers_id, time1, time2, wh, dtype, dist, id, root, kindId, colors, subjectId, subjectParentId, name, entity, matchId, pics, rating, reviewRating, nmReviewRating, feedbacks, nmFeedbacks, panelPromoId, promoTextCard, promoTextCat, volume, viewFlags, totalQuantity, meta) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", product)
            return id
        else:
            return 0

    def tovar_add_table_sizes(self, db, id_product, tovar):
        #_id	products_id	name	origName	rank	optionId	wh	time1	time2	dtype	price_basic	price_product	price_total	price_logistics	price_return	saleConditions	payload

        if 'sizes' in tovar:
            for size in tovar['sizes']:
                if 'name' not in size:
                    size['name'] = ''
                if 'origName' not in size:
                    size['origName'] = ''
                if 'rank' not in size:
                    size['rank'] = 0
                if 'optionId' not in size:
                    size['optionId'] = 0
                if 'wh' not in size:
                    size['wh'] = 0
                if 'time1' not in size:
                    size['time1'] = 0
                if 'time2' not in size:
                    size['time2'] = 0
                if 'dtype' not in size:
                    size['dtype'] = 0
                if 'price' not in size:
                    size['price_basic'] = 0
                    size['price_product'] = 0
                    size['price_total'] = 0
                    size['price_logistics'] = 0
                    size['price_return'] = 0
                else:
                    size['price_basic'] = size['price']['basic']
                    size['price_product'] = size['price']['product']
                    size['price_total'] = size['price']['total']
                    size['price_logistics'] = size['price']['logistics']
                    size['price_return'] = size['price']['return']
                if 'saleConditions' not in size:
                    size['saleConditions'] = 0
                if 'payload' not in size:
                    size['payload'] = ''
                product_size = (
                    id_product,
                    size['name'],
                    size['origName'],
                    size['rank'],
                    size['optionId'],
                    size['wh'],
                    size['time1'],
                    size['time2'],
                    size['dtype'],
                    size['price_basic'],
                    size['price_product'],
                    size['price_total'],
                    size['price_logistics'],
                    size['price_return'],
                    size['saleConditions'],
                    size['payload']
                )

                # results = db.select_query(f"SELECT _id FROM wb_products_sizes WHERE `products_id`={id_product} AND `optionId`={size['optionId']};")
                # if results is None or len(results) == 0:
                id = db.insert_query(f"INSERT INTO wb_products_sizes (products_id, name, origName, rank, optionId, wh, time1, time2, dtype, price_basic, price_product, price_total, price_logistics, price_return, saleConditions, payload) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", product_size)
                return id
                # else:
                #     return 0

    def tovar_add_table(self, **kwargs):
        if "tovar" in kwargs:
            tovar = kwargs.get('tovar')
            db = MySQLDatabase(host="localhost", user="root", password="", database="market_cheks")
            db.connect()
            id = tovar['id']
            results = db.select_query(f"SELECT _id FROM wb_products WHERE `id`={id};")
            if results is None or len(results) == 0:
                self.tovar_add_table_brands(db, (tovar['brandId'], tovar['siteBrandId'], tovar['brand']))
                self.tovar_add_table_suppliers(db, (tovar['supplierId'], tovar['supplierRating'], tovar['supplierFlags'], tovar['supplier']))

                id_product = self.tovar_add_table_products(db, tovar)
                if id_product != 0:
                    self.tovar_add_table_sizes(db, id_product, tovar)
                #print("No products found")
            db.close_connection()
        else:
            return "Не указан товар!"
