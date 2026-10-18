"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles

from cfin import __version__
from cfin.api.routes import article, finance, system
from cfin.config import DEBUG, STATIC_DIR

description = """
CFin - yfinance for china
"""

contact = {"name": "Sanyorke Han", "email": "sanyorke@126.com"}

tags_metadata = [
    {
        "name": "Finance",
        "description": "Query stock prices via yfinnce",
    },
    {
        "name": "Article",
        "description": "Article in markdown",
    },
]


def create_app() -> FastAPI:
    app = FastAPI(
        debug=DEBUG,
        title="CFin",
        description=description,
        contact=contact,
        version=__version__,
        openapi_tags=tags_metadata,
    )

    app.add_middleware(GZipMiddleware, minimum_size=2048)

    app.include_router(finance.router)
    app.include_router(article.router)
    app.include_router(system.router)

    app.mount(
        "/static",
        StaticFiles(directory=STATIC_DIR),
        name="static",
    )

    return app


app = create_app()
