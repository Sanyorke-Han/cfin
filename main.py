from typing import Optional
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from finance import finance
from article import article

description = """
CFin - yfinance for china
"""

contact = {"name": "Sanyorke Han", "email": "sanyorke@126.com"}

tags_metadata = [
    {
        "name": "Finance",
        "description": "Query stock prices via yfinnce"
    },
    {
        "name": "Article",
        "description": "Article in markdown"
    },
]

root_dir = Path(__file__).parent.resolve()

app = FastAPI(debug=True,
              title="CFin",
              description=description,
              contact=contact,
              version="0.1.0",
              openapi_tags=tags_metadata)

app.add_middleware(GZipMiddleware, minimum_size=2048)

app.include_router(finance.router)
app.include_router(article.router)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/static/index.html")


@app.get("/docs", include_in_schema=False)
async def get_documentation():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Swagger")


@app.get("/openapi.json", include_in_schema=False)
async def openapi():
    return get_openapi(title=app.title, version=app.version, routes=app.routes)


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/images/favicon.png")


@app.get("/health", include_in_schema=False)
async def health_check():
    return {"status": "Ok!"}


app.mount("/static",
          StaticFiles(directory=root_dir.joinpath("static")),
          name="static")
