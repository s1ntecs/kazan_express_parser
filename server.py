import asyncio
import aiohttp_jinja2
import jinja2
from aiohttp import web
from table import create_sheet
from parser import parser_and_google
from db.insert_data import insert_shop_data
from db.get_data import get_shops_name
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor()

app = web.Application()
aiohttp_jinja2.setup(app,
                     loader=jinja2.FileSystemLoader('.'))


async def get_shop(request):
    value = request.match_info['value']
    shops_name, shops_id = await get_shops_name()
    shops_dict = dict(zip(shops_name, shops_id))
    context = {'value': value, 'shops_name': shops_dict}
    template = '/templates/index.html'
    return aiohttp_jinja2.render_template(template,
                                          request,
                                          context)


async def post_shop(request):
    data = await request.post()
    store_name = data.get('store_name')
    sheet = '_copy'
    for _ in range(2):
        sheet_url, sheet_id = await asyncio.get_event_loop().run_in_executor(
            executor, create_sheet, store_name+sheet)
        await insert_shop_data(name=store_name+sheet,
                               url=sheet_url, sheet_id=sheet_id)
        sheet = ''
    return web.HTTPFound(location=f'/shop/{sheet_id}')

app.add_routes([web.get('/shop/{value}', get_shop),
                web.post('/shop', post_shop)])


async def parser_loop(app):
    while True:
        shops_name, shops_id = await get_shops_name()
        await asyncio.get_event_loop().run_in_executor(
                executor, parser_and_google, shops_name, shops_id)


async def background_tasks(app):
    app['parser_listener'] = asyncio.create_task(parser_loop(app))

    yield

    app['parser_listener'].cancel()
    await app['parser_listener']

# app.cleanup_ctx.append(background_tasks)
web.run_app(app)
