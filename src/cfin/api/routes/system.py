"""Routes for the site root, health check and favicon."""

from fastapi import APIRouter
from fastapi.responses import FileResponse, RedirectResponse

from cfin.config import STATIC_DIR

router = APIRouter(include_in_schema=False)


@router.get("/")
async def root() -> RedirectResponse:
    return RedirectResponse("/static/index.html")


@router.get("/favicon.ico")
async def favicon() -> FileResponse:
    return FileResponse(STATIC_DIR / "images" / "favicon.png")


@router.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "Ok!"}
