from pprint import pprint
from typing import Dict, List
import httplib2
import apiclient.discovery
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

PUB_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vT3VC-kbAy5DViXJTBoAoOHnwrJ0vNIksn5nKZDEh3cNhy8COkoT6RF5mer2kwegzxSStOB1KDh96ey'

# Файл, полученный в Google Developer Console
CREDENTIALS_FILE = 'credentials.json'
# ID Google Sheets документа (можно взять из его URL)
spreadsheet_id = '1o1dw6S9eQgxJOWg5Fb_TA36gISj4Bgb65fb2UKW1KUg'


def get_data(start, end, sheet='makeyou'):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=f'{sheet}!{start}:{end}',
        majorDimension='ROWS'
    ).execute()
    values = values.get('values', [])
    if not values:
        print('No data found.')
        values = None
    return values


def write_data(service, product, i, sheet_name):
    service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": f"{sheet_name}!A{i}:J{i}",
                 "majorDimension": "ROWS",
                 "values": [["URL", product.payload.data.seller.link,
                            product.payload.data.title,
                            product.payload.data.id,
                            None,
                            product.payload.data.totalAvailableAmount,
                            product.payload.data.rating,
                            product.payload.data.reviewsAmount,
                            product.payload.data.skuList[0].purchasePrice,
                            product.payload.data.ordersAmount]]}
                             ]
        }
    ).execute()


def write_list_data(list_data: List,
                    range: str,
                    rows_or_col: str = "ROWS"):
    print('write list data')
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
    service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": range,  # f"E3:E{(len(orders_today)+3)}",
                 "majorDimension": rows_or_col,
                 "values": [list_data]}]
        }
    ).execute()


def set_color(row_pos: int, column_pos: int, sheet_id: str,
              red=128, green=128, blue=128, endrow=1000):
    print('set_color')
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
    requests = [
        {
            "updateCells": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": row_pos-1,
                    "endRowIndex": endrow,
                    "startColumnIndex": column_pos,
                    "endColumnIndex": 9
                },
                "fields": "userEnteredFormat.backgroundColor",
                "rows": [
                    {
                        "values": [
                            {
                                "userEnteredFormat": {
                                    "backgroundColor": {
                                        "red": red,
                                        "green": green,
                                        "blue": blue
                                    }
                                }
                            }
                        ]
                    }
                ]
            }
        }
    ]
    body = {"requests": requests}
    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=body).execute()


def sort_and_group(my_products_pos: List, sheet_id: str):
    print('sort_and_group')
    my_products_pos.append(1000)
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
    for num in range(1, len(my_products_pos)):
        sort_range = {
            "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": my_products_pos[num-1],
                    "endRowIndex": my_products_pos[num]-1,
                    "startColumnIndex": 0,
                    "endColumnIndex": 9
                },
            "sortSpecs": [
                {
                    "dimensionIndex": 4,
                    "sortOrder": "DESCENDING"
                }
            ]
        }
        request = service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id, body={
             "requests": [
                {
                    "sortRange": sort_range
                }
             ]
            })
        request.execute()


def clear_data(sheet_name: str):
    print("clear data")
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
    request = service.spreadsheets().values().clear(
        spreadsheetId=spreadsheet_id,
        range=sheet_name,
        body={}
    )
    request.execute()


def compare_data(sheet_name: str, sheet_id: str):
    """ Функция в которой сравниваются цены продуктов со вчерашними ценами. """
    print('compare_data')
    id_products = get_data(start='D3', end='D500', sheet=sheet_name)
    present_prices = get_data(start='I3', end='I500', sheet=sheet_name)
    present_orders_count = get_data(start='J3', end='J500', sheet=sheet_name)
    past_id = get_data(start='D3', end='D500', sheet=f'{sheet_name}_copy')
    past_prices = get_data(start='I3', end='I500', sheet=f'{sheet_name}_copy')
    past_orders_count = get_data(start='J3',
                                 end='J500',
                                 sheet=f'{sheet_name}_copy')
    present_dict = dict()
    past_dict = dict()
    orders_list = list()
    for j in range(len(id_products)):
        price = present_prices[j][0]
        present_dict[id_products[j][0]] = [
            float(price.replace(',', '.')),
            int(present_orders_count[j][0])]
    for j in range(len(past_id)):
        price = past_prices[j][0]
        past_dict[past_id[j][0]] = [
            float(price.replace(',', '.')),
            int(past_orders_count[j][0])]
    for pos, i in enumerate(present_dict.keys()):
        orders_list.append(
            (present_dict.get(i, [0, 0])[1]) - (past_dict.get(i, [0, 0])[1]))
        if (present_dict.get(i, [0, 0])[0]) > (
             past_dict.get(i, [0, 0])[0]):
            set_color(row_pos=pos+3, column_pos=8,
                      sheet_id=sheet_id, green=0.5,
                      blue=0, red=0, endrow=pos+3)
        elif (present_dict.get(i, [0, 0])[0]) < (
              past_dict.get(i, [0, 0])[0]):
            set_color(row_pos=pos+3, column_pos=8,
                      green=0, blue=0, red=0.5,
                      sheet_id=sheet_id, endrow=pos+3)
    write_list_data(list_data=orders_list,
                    range=f"{sheet_name}!E3:E{(len(orders_list)+2)}",
                    rows_or_col="COLUMNS")


def refresh_data(products: List,
                 position: int,
                 sheet_name: str,
                 sheet_id: str) -> str:

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    for x in range(9):
        set_color(row_pos=position, column_pos=x, sheet_id=sheet_id)
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
    for i, product in enumerate(products):
        write_data(service, product, i+position, sheet_name)
    return (position + len(products)-1)


def create_sheet(sheet_name: str):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
    requests = [
        {
            'addSheet': {
                'properties': {
                    'title': sheet_name
                }
            }
        }
    ]
    try:
        resp = service.spreadsheets().batchUpdate(
                    spreadsheetId=spreadsheet_id,
                    body={'requests': requests}).execute()
    except HttpError:
        print(f'Магазин {sheet_name} уже есть')
    sheet_id = resp['replies'][0]['addSheet']['properties']['sheetId']
    sheet_url = f"{PUB_URL}/pubhtml?gid={sheet_id}&single=true"
    return (sheet_url, str(sheet_id))


def copy_sheet(sheet_name: str):
    print('copy_sheet')
    date = datetime.now().strftime("%Y-%m-%d")
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=f"{sheet_name}!A1:J500").execute()
    values = result.get('values', [])
    request = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=f"{sheet_name}_copy!A1:J500",
        valueInputOption='USER_ENTERED', body={'values': values})
    request.execute()
    a = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=f"{sheet_name}!E1",
        valueInputOption='USER_ENTERED', body={'values': [[date]]})
    a.execute()

# write_list_data(['29.3.2023'], "D1:D1")