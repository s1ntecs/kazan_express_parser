import asyncpg
import asyncio
from sql_query import CREATE_SHOPS_TABLE


async def main():
    connection = await asyncpg.connect(host='127.0.0.1',
                                       port=5432,
                                       user='postgres',
                                       database='kzn',
                                       password='susel')
    statements = [CREATE_SHOPS_TABLE]

    print('sozdaetsya db product....')
    for statement in statements:
        status = await connection.execute(statement)
        print(status)
    print('db product sozdana')
    await connection.close()

asyncio.run(main())
