import requests

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

    def tovar_add_table(self):
        # wb_brands: _id, brandId, siteBrandId, brand(str)
        # wb_suppliers: _id, supplierId, supplierRating(float), supplierFlags, supplier(str)
        # wb_products_sizes: _id, products_id, name(str), origName(str), rank, optionId, wh, time1, time2, dtype, price_basic, price_product, price_total, price_logistics, price_return
        # wb_products: brands_id, suppliers_id, time1, time2, wh, dtype, dist, id, root, kindId, colors(str), subjectId, subjectParentId, name(str), entity(str), matchId, pics, rating, reviewRating, nmReviewRating, feedbacks, nmFeedbacks, panelPromoId, promoTextCard(str), promoTextCat(str), volume, viewFlags, sizes_saleConditions, sizes_payload(str), totalQuantity,meta(text)
        pass