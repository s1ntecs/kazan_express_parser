import asyncpg
import asyncio
from random import randint
from typing import List
from random import sample


async def insert_shop_data(name: str, url: str, sheet_id: str):
    connection = await asyncpg.connect(host='127.0.0.1',
                                       port=5432,
                                       user='postgres',
                                       database='kzn',
                                       password='susel')
    
    insert_promt = "INSERT INTO shops VALUES($1, $2, $3)"
    await connection.execute(insert_promt, name, url, sheet_id)
    await connection.close()

# name = 'makeyou'
# url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vT3VC-kbAy5DViXJTBoAoOHnwrJ0vNIksn5nKZDEh3cNhy8COkoT6RF5mer2kwegzxSStOB1KDh96ey/pubhtml?gid=0&single=true'
# sheet_id = '0'
# asyncio.run(insert_data(name, url, sheet_id))

# async def insert_promt(name: str, text: str, connection_db):
#     client_id = await get_client_id(name, connection_db)
#     insert_promt = "INSERT INTO promt VALUES(DEFAULT, $1, $2)"
#     await connection_db.execute(insert_promt, text, client_id)
#     promt_query = "SELECT promt_id FROM promt WHERE promt_text = $1"
#     promt_id = await connection_db.fetchrow(promt_query, text)
#     return promt_id[0]


# async def choose_genre(name: str, genre_id: str,
#                        connection_db, create_genre=False):
#     client_id = await get_client_id(name, connection_db)
#     if create_genre:
#         create = "INSERT INTO genre VALUES(DEFAULT, $1, $2)"
#         return await connection_db.execute(create, genre_id, client_id)
#     insert_genre = "UPDATE genre SET genre_id = $1 WHERE client_id = $2"
#     return await connection_db.execute(insert_genre, int(genre_id), client_id)


# async def gen_with_model(name: str, connection_db, model_name=None):
#     client_id = await get_client_id(name, connection_db)
#     model_id = await get_model_id_token(model_name, connection_db)
#     insert_genre = "UPDATE with_model SET model_name = $1 WHERE client_id = $2"
#     await connection_db.execute(insert_genre, model_id, client_id)


# async def insert_model(name: str, model_name: str, connection_db):
#     client_id = await get_client_id(name, connection_db)
#     insert_brands = "INSERT INTO model VALUES(DEFAULT, $1, $2)"
#     await connection_db.execute(insert_brands, model_name, client_id)
#     model_query = "SELECT model_id FROM model WHERE model_name = $1"
#     model_id = await connection_db.fetchrow(model_query, model_name)
#     return model_id[0]


# async def get_text_with_model(connection_db):
#     query = "SELECT count(promt_text) FROM promt_example"
#     count_of_txt = await connection_db.fetchrow(query)
#     a = int(count_of_txt[0])
#     rand = randint(1, a)
#     model_query = "SELECT promt_text FROM promt_example WHERE promt_id = $1"
#     model_id = await connection_db.fetchrow(model_query, rand)
#     return model_id[0]


# async def get_text_simple_gen(connection_db):
#     query = "SELECT count(promt_text) FROM promt"
#     count_of_txt = await connection_db.fetchrow(query)
#     a = int(count_of_txt[0])
#     rand = randint(1, a)
#     model_query = "SELECT promt_text FROM promt WHERE promt_id = $1"
#     model_id = await connection_db.fetchrow(model_query, rand)
#     return model_id[0]


# async def insert_image(name: str,
#                        url,
#                        promt_text: str,
#                        connection_db,
#                        model_name=None):
#     client_id = await get_client_id(name, connection_db)
#     promt_id = await insert_promt(name, promt_text, connection_db)
#     if model_name:
#         model_id = await insert_model(name, model_name, connection_db)
#     else:
#         model_id = None
#     insert_image = "INSERT INTO image VALUES(DEFAULT, $1, $2, $3, $4)"
#     return await connection_db.execute(
#         insert_image, url, client_id, model_id, promt_id)
