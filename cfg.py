import os

query = ['лубрикант', 'вибратор']  # Список запросов
table_id = '1KJBarCH76G2EyCPH7x6XyH2HK5QNfgKnkRerX73RFAM'  # ID текущего Google Sheet
# Ссылка на ключ Google Sheet API
creds_json = os.path.dirname(__file__) + '/keys/creds.json'

# Запросы для магазина
list_headers = {
    'authority': 'dshop.kznexpress.ru',
    'accept': '*/*',
    'accept-language': 'ru-RU',
    'apollographql-client-name': 'web-customers',
    'apollographql-client-version': '1.29.9',
    'authorization': 'Basic a2F6YW5leHByZXNzLWN1c3RvbWVyOmN1c3RvbWVyU2VjcmV0S2V5',
    # Already added when you pass json=
    # 'content-type': 'application/json',
    'origin': 'https://kazanexpress.ru',
    'referer': 'https://kazanexpress.ru/',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'x-iid': '0a2bf1a1-1581-47f8-8b4a-6d0c3cbe0c9d',
}

products_headers = {
    'authority': 'api.kazanexpress.ru',
    'accept': 'application/json',
    'accept-language': 'ru-RU',
    'access-content-allow-origin': '*',
    'authorization': 'Basic a2F6YW5leHByZXNzLWN1c3RvbWVyOmN1c3RvbWVyU2VjcmV0S2V5',
    'content-type': 'application/json',
    'origin': 'https://kazanexpress.ru',
    'referer': 'https://kazanexpress.ru/',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'x-iid': '0a2bf1a1-1581-47f8-8b4a-6d0c3cbe0c9d',
}


def json_data(query, offset):
    return {
        'operationName': 'getMakeSearch',
        'variables': {
            'queryInput': {
                'text': query,
                'showAdultContent': 'TRUE',
                'filters': [],
                'sort': 'BY_RELEVANCE_DESC',
                'pagination': {
                    'offset': offset,
                    'limit': 48,
                },
            },
        },
        'query': 'query getMakeSearch($queryInput: MakeSearchQueryInput!) {\n  makeSearch(query: $queryInput) {\n    id\n    queryId\n    queryText\n    category {\n      ...CategoryShortFragment\n      __typename\n    }\n    categoryTree {\n      category {\n        ...CategoryFragment\n        __typename\n      }\n      total\n      __typename\n    }\n    items {\n      catalogCard {\n        __typename\n        ...SkuGroupCardFragment\n      }\n      __typename\n    }\n    facets {\n      ...FacetFragment\n      __typename\n    }\n    total\n    mayHaveAdultContent\n    __typename\n  }\n}\n\nfragment FacetFragment on Facet {\n  filter {\n    id\n    title\n    type\n    measurementUnit\n    description\n    __typename\n  }\n  buckets {\n    filterValue {\n      id\n      description\n      image\n      name\n      __typename\n    }\n    total\n    __typename\n  }\n  range {\n    min\n    max\n    __typename\n  }\n  __typename\n}\n\nfragment CategoryFragment on Category {\n  id\n  icon\n  parent {\n    id\n    __typename\n  }\n  seo {\n    header\n    metaTag\n    __typename\n  }\n  title\n  adult\n  __typename\n}\n\nfragment CategoryShortFragment on Category {\n  id\n  parent {\n    id\n    title\n    __typename\n  }\n  title\n  __typename\n}\n\nfragment SkuGroupCardFragment on SkuGroupCard {\n  ...DefaultCardFragment\n  photos {\n    key\n    link(trans: PRODUCT_540) {\n      high\n      low\n      __typename\n    }\n    previewLink: link(trans: PRODUCT_240) {\n      high\n      low\n      __typename\n    }\n    __typename\n  }\n  badges {\n    ... on BottomTextBadge {\n      backgroundColor\n      description\n      id\n      link\n      text\n      textColor\n      __typename\n    }\n    __typename\n  }\n  characteristicValues {\n    id\n    value\n    title\n    characteristic {\n      values {\n        id\n        title\n        value\n        __typename\n      }\n      title\n      id\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment DefaultCardFragment on CatalogCard {\n  adult\n  favorite\n  feedbackQuantity\n  id\n  minFullPrice\n  minSellPrice\n  offer {\n    due\n    icon\n    text\n    textColor\n    __typename\n  }\n  badges {\n    backgroundColor\n    text\n    textColor\n    __typename\n  }\n  ordersQuantity\n  productId\n  rating\n  title\n  __typename\n}',
    }


head_rows = ["Ссылка", "Магазин", "Название товара",
             "id", "Заказов сегодня", "В наличии",
             "Рейтинг", "Отзывы", "Цена"
             ]
