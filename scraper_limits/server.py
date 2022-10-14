from aiohttp import web
from aiohttp.web import Request, Response


async def hello(request: Request) -> Response:
    return web.Response(text="Hello, world")


app = web.Application()
app.add_routes([web.get("/", hello)])
web.run_app(app)
