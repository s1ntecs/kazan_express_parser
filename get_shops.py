import math

import requests
from marshmallow_dataclass import class_schema
from schema import Data
from cfg import json_data, list_headers, products_headers
from table import refresh_data


def get_product(product_id, product_url=None):
    """ Выдает по id продукта словарь с данными о продукте """
    session = requests.Session()
    response = session.get(
            f'https://api.kazanexpress.ru/api/v2/product/{product_id}',
            headers=products_headers).json()
    schema = class_schema(Data)()
    product = schema.load(response)
    product.payload.data.product_url = product_url
    return product


def get_data(query: str):

    offset = 0

    session = requests.Session()
    response = session.post(
        'https://dshop.kznexpress.ru/',
        headers=list_headers,
        json=json_data(
            query,
            offset)).json()

    # Число товаров
    total_items = response.get('data').get('makeSearch').get('total')

    if total_items is None:
        return 'No items'

    pages_count = math.ceil(total_items / 48)  # Вычисляем число страниц
    products = []  # Список id товаров

    for i in range(pages_count):
        offset = i * 48
        response = session.post(
            'https://dshop.kznexpress.ru/',
            headers=list_headers,
            json=json_data(
                query,
                offset)).json()
        products_id = response.get('data').get('makeSearch').get('items')
        for product in products_id:
            product_id = product.get('catalogCard').get('productId')
            product = get_product(product_id)
            products.append(product)
    refresh_data(products)
    data = []  # Список с необходимыми полями товаров

    products_info = {
        'query': query,
        'data': data
    }

    return products_info
