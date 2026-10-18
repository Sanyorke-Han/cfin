"""Markdown article management routes."""

import shutil
from pathlib import Path

import markdown
from fastapi import APIRouter, File, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from cfin.config import CSS_DIR, MARKDOWN_DIR, RESOURCES_DIR, TEMPLATES_DIR

router = APIRouter()
templates = Jinja2Templates(directory=TEMPLATES_DIR)


def list_file(subfolder: str) -> list[dict[str, str]]:
    """List markdown files available in a resource subfolder."""
    sub_path = RESOURCES_DIR / subfolder
    return [
        {"path": str(path.relative_to(sub_path)), "name": path.name}
        for path in sorted(sub_path.glob("*.md"))
    ]


def _resolve_markdown_path(article_name: str | Path) -> Path:
    """Resolve a markdown path and keep it inside the markdown directory."""
    markdown_root = MARKDOWN_DIR.resolve()
    path = (markdown_root / article_name).resolve()
    if not path.is_relative_to(markdown_root):
        raise HTTPException(status_code=404, detail="File not found")
    return path


@router.get(
    "/resource/{article_name:path}",
    response_class=HTMLResponse,
    tags=["Article"],
)
def resource(article_name: Path) -> HTMLResponse:
    markdown_path = _resolve_markdown_path(article_name)
    if not markdown_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    head_part = (CSS_DIR / "github.css").read_text(encoding="utf-8")
    html_fragment = markdown.markdown(markdown_path.read_text(encoding="utf-8"))
    html_content = f"""
        <html>
        <head>
        <style type='text/css'>
        <!--
        {head_part}
        //-->
        </style>
        </head>
        <body>
        <div class='markdown-body'>
        {html_fragment}
        </div>
        </body>
        </html>
    """

    return HTMLResponse(content=html_content, status_code=200)


@router.get("/markspace", tags=["Article"])
def markspace(request: Request):
    contents = list_file("markdown")
    return templates.TemplateResponse(
        request=request,
        name="markspace.html",
        context={"msg": "File Management", "contents": contents},
    )


@router.post("/upload", include_in_schema=False)
def upload(uploadFile: UploadFile = File(...)) -> dict[str, int]:
    filename = Path(uploadFile.filename or "").name.replace(" ", "-")
    if not filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    file_path = MARKDOWN_DIR / filename
    try:
        with file_path.open("wb") as dest_file:
            shutil.copyfileobj(uploadFile.file, dest_file)
        return {"status": 200}
    finally:
        uploadFile.file.close()


@router.get("/download/{article_name:path}", include_in_schema=False)
def download(article_name: str) -> FileResponse:
    filepath = _resolve_markdown_path(article_name)
    if filepath.is_file():
        return FileResponse(
            filepath,
            media_type="application/octet-stream",
            filename=filepath.name,
        )
    raise HTTPException(status_code=404, detail="File not found")
