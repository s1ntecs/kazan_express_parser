import asyncpg


async def insert_shop_data(name: str, url: str, sheet_id: str):
    connection = await asyncpg.connect(host='127.0.0.1',
                                       port=5432,
                                       user='postgres',
                                       database='kzn',
                                       password='susel')

    insert_promt = "INSERT INTO shops VALUES($1, $2, $3)"
    await connection.execute(insert_promt, name, url, sheet_id)
    await connection.close()
