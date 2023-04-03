import time
from selenium import webdriver
from typing import Dict, List
from bs4 import BeautifulSoup
from get_shops import get_product
from cfg import head_rows, UserAgent
from table import (refresh_data, write_list_data, get_data,
                   copy_sheet, compare_data, sort_and_group)
from urllib.parse import quote
from datetime import datetime


def get_search_products(query: str) -> Dict:
    """ Search products in kazan-express """
    query_url = "https://kazanexpress.ru/search?query={0}".format(quote(query))
    domain = "https://kazanexpress.ru"
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={UserAgent}")
    options.add_argument("--headless")
    browser = webdriver.Chrome(options=options)
    result = dict()
    page = 1
    try:
        query_url = f"{query_url}&currentPage={page}"
        browser.get(query_url)
        time.sleep(2)
        response = browser.page_source
        bs_object = BeautifulSoup(response, "lxml")
        cards_on_page = bs_object.find_all(
            name="div", class_="col-mbs-12 col-mbm-6 col-xs-4 col-md-3")
        card_urls_on_page = [
            card.a["href"].split("?")[0].split(
                '-')[-1] for card in cards_on_page]
        products_id = [
            card.a["href"].split("?")[0].split(
                '-')[-1] for card in cards_on_page]
        card_urls_on_page = [
            domain+card.a["href"].split("?")[0] for card in cards_on_page]
        d = dict(zip(products_id, card_urls_on_page))
        result = result | d
    finally:
        browser.close()
        browser.quit()
        return result


def get_product_from_shop(shop_name: str) -> Dict:
    """Get products in Shop=shop_name"""
    start_url = f'https://kazanexpress.ru/{shop_name}'
    domain = "https://kazanexpress.ru"
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={UserAgent}")
    options.add_argument("--headless")
    browser = webdriver.Chrome(options=options)
    page = 1
    products_dict = dict()
    check = True
    try:
        while check:
            url = f"{start_url}?currentPage={page}"
            browser.get(url)
            time.sleep(2)
            response = browser.page_source
            bs_object = BeautifulSoup(response, "lxml")
            cards_on_page = bs_object.find_all(
                name="div",
                class_="col-mbs-12 col-mbm-6 col-xs-4 col-md-3"
                )
            products_id = [
                card.a["href"].split("?")[0].split(
                 '-')[-1] for card in cards_on_page]
            card_urls_on_page = [
                domain+card.a["href"].split("?")[0] for card in cards_on_page]
            d = dict(zip(products_id, card_urls_on_page))
            products_dict = products_dict | d
            navigation_button = bs_object.find(
                name="div",
                class_="pagination-wrapper"
                )
            if "style" in navigation_button.attrs:
                check = False
            else:
                page += 1
    finally:
        browser.close()
        browser.quit()
        return products_dict


def merge_products(main_product, same_products: Dict) -> List:
    """ Create List of main product (from our shop) and the same products """
    list_of_products = [main_product]
    for product_id, product_url in same_products.items():
        if int(main_product.payload.data.id) != int(product_id):
            product = get_product(product_id, product_url)
            list_of_products.append(product)
    return list_of_products


def parser_and_google(shops_name: List = ["makeyou"],
                      shops_id: List = ["0"]):

    for i, shop_name in enumerate(shops_name):
        products_in_shop = get_product_from_shop(shop_name)
        write_list_data(list_data=head_rows, range="A2:I2")
        pos = 3
        my_products_pos = list()
        print(products_in_shop)
        for product_id, product_url in products_in_shop.items():
            product = get_product(product_id, product_url)
            query = product.payload.data.title
            same_products = get_search_products(query=query)
            list_products = merge_products(main_product=product,
                                           same_products=same_products)
            my_products_pos.append(pos)
            pos = refresh_data(products=list_products,
                               position=pos,
                               sheet_name=shop_name,
                               sheet_id=shops_id[i])
            pos += 1

        last_write = get_data(start="E1", end="E1", sheet=shop_name)
        date = datetime.now().strftime('%d.%m.%Y')

        if last_write is None or date != last_write[0][0]:
            copy_sheet(sheet_name=shop_name)
            write_list_data(list_data=[str(date)], range="D1:D1")

        sort_and_group(my_products_pos, sheet_id=shops_id[i])
        compare_data(shop_name, shops_id[i])
        time.sleep(300)

parser_and_google()