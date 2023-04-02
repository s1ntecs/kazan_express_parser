import asyncpg
import asyncio
from random import randint
from typing import List
from random import sample


async def get_shops_name():
    connection = await asyncpg.connect(host='127.0.0.1',
                                       port=5432,
                                       user='postgres',
                                       database='kzn',
                                       password='susel')
    promt_query = """
    SELECT name, shop_id FROM shops WHERE name NOT LIKE '%\_copy';
    """
    promt_id = await connection.fetch(promt_query)
    name = [x[0] for x in promt_id]
    shop_id = [x[1] for x in promt_id]
    return name, shop_id
