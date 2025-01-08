"""
Инфа о разделе товара
https://www.wildberries.ru/webapi/product/216373122/data?subject=516&kind=0&brand=19467
https://www.wildberries.ru/webapi/product/186893094/data?subject=516&kind=0&brand=24840
{
    "resultState": 0,
    "value": {
        "data": {
            "brandAndSubjectUrl": "/brands/xiaomi/mobilnye-telefony",
            "targetInfo": {
                "targetUrl": "EX",
                "targetCode": 0,
                "sort": 0,
                "targetUrlExtended": "EX|||||||||"
            },
            "sitePath": [
                {
                    "id": 4830,
                    "name": "Электроника",
                    "sort": 45,
                    "pageUrl": "/catalog/elektronika",
                    "topMenuRenderer": 0,
                    "leftMenuRenderer": 0,
                    "landingPage": false,
                    "hash": -1004390760,
                    "xshardKey": "blackhole",
                    "xquery": "subject=1152",
                    "noFollow": true,
                    "excludeFromBreadcrumbs": false,
                    "isTop": false,
                    "isDenyLink": true,
                    "rawQuery": "subject=1152"
                },
                {
                    "id": 9455,
                    "parentId": 4830,
                    "name": "Смартфоны и телефоны",
                    "sort": 60,
                    "pageUrl": "/catalog/elektronika/smartfony-i-telefony",
                    "topMenuRenderer": 0,
                    "leftMenuRenderer": 0,
                    "landingPage": false,
                    "hash": -2078475858,
                    "xshardKey": "blackhole",
                    "xquery": "cat=9455",
                    "noFollow": true,
                    "excludeFromBreadcrumbs": false,
                    "isTop": false,
                    "isDenyLink": true,
                    "rawQuery": "subject=453;466;468;515;516;517;518;519;526;533;545;593;765;777;787;844;911;1239;1241;1258;1309;1375;1407;1422;1470;1514;1529;1571;2138;2320;2376;2436;2483;2559;2561;2800;2833;3061;3095;3153;3699;3822;4117;4580;4680;4874;5486;5487;5488;5489;5547;5594;5801;6311;6492;6530;6560;4501;7642;7645;7646;7647"
                },
                {
                    "id": 9464,
                    "parentId": 9455,
                    "name": "Мобильные телефоны",
                    "sort": 45,
                    "pageUrl": "/catalog/elektronika/telefony-i-gadzhety/mobilnye-telefony",
                    "topMenuRenderer": 0,
                    "leftMenuRenderer": 0,
                    "landingPage": false,
                    "hash": 1849245871,
                    "xshardKey": "electronic20",
                    "xquery": "subject=516",
                    "noFollow": false,
                    "excludeFromBreadcrumbs": false,
                    "isTop": false,
                    "rawQuery": "subject=516"
                },
                {
                    "id": 0,
                    "name": "Xiaomi",
                    "sort": 0,
                    "pageUrl": "/brands/xiaomi",
                    "topMenuRenderer": 0,
                    "leftMenuRenderer": 0,
                    "landingPage": false,
                    "hash": -191959343,
                    "noFollow": false,
                    "excludeFromBreadcrumbs": false,
                    "isTop": false
                }
            ]
        }
    }
}
"""

"""
https://basket-14.wbbasket.ru/vol2163/part216373/216373122/info/price-history.json
https://basket-12.wbbasket.ru/vol1868/part186893/186893094/info/price-history.json
[{"dt":1726358400,"price":{"RUB":1832100}}]
"""
from WB_tovar import WB_tovar

WB = WB_tovar()
# Список товаров
tovars = WB.get_json_tovars_list(
    url="https://catalog.wb.ru/catalog/electronic20/v2/catalog",
    price_ot=0,
    price_do=90000000
)
if tovars is not None:
    for tovar in tovars['data']['products']:
        WB.tovar_add_table(tovar=tovar)



# Ирнформация и ЦЕНА товара
# result = get_json_tovars_detail(id=216373122)
# Ирнформация товара
# result = get_json_tovar_info(url="https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-1255987&spp=30&hide_dtype=10&ab_testing=false&nm=216373122")
# result = get_json_tovar_info(domen="card.wb.ru", id=216373122)

# Карточка товара
# result = get_json_tovar(url="https://basket-14.wbbasket.ru/vol2163/part216373/216373122/info/ru/card.json")
# get_json_tovar_card(domen="basket-14.wbbasket.ru", vol="2163", part="216373", id=216373122)

