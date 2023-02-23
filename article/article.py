from fastapi import APIRouter, File, UploadFile, Request, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import markdown
import shutil

root_dir = Path(__file__).parent.resolve()
resources_dir = root_dir.joinpath('resources')
templates = Jinja2Templates(directory=resources_dir.joinpath("templates"))

router = APIRouter()


def list_file(subfolder):
    sub_path = resources_dir.joinpath(subfolder)
    files = []
    for f in sub_path.glob('*'):
        if f.suffix == '.md':
            files.append({
                "path": str(f.relative_to(sub_path)),
                "name": f.name
            })
    return files


@router.get('/resource/{article_name:path}',
            response_class=HTMLResponse,
            tags=['Article'])
def resource(article_name: Path):
    if article_name == 'favicon.ico':
        return ''

    head_part = resources_dir.joinpath(
        'css', 'github.css').read_text(encoding='utf-8')
    markdown_path = resources_dir.joinpath("markdown", article_name)
    html_fragment = markdown.markdown(
        markdown_path.read_text(encoding='utf-8'))
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
    contents = list_file('markdown')
    return templates.TemplateResponse("markspace.html", {
        "request": request,
        "msg": 'File Management',
        "contents": contents
    })


@router.post("/upload", include_in_schema=False)
def upload(uploadFile: UploadFile = File(...)):
    try:
        file_path = resources_dir.joinpath(
            'markdown', uploadFile.filename.replace(" ", "-"))
        with file_path.open('wb') as dest_file:
            dest_file.write(uploadFile.file.read())
            shutil.copyfileobj(uploadFile.file, dest_file)

        return {"status": 200}
    finally:
        uploadFile.file.close()


@router.get("/download/{article_name:path}", include_in_schema=False)
def download(article_name):
    filepath = resources_dir.joinpath('markdown', article_name)
    if filepath.exists():
        return FileResponse(str(filepath),
                            media_type='application/octet-stream',
                            filename=filepath.name)
    else:
        raise HTTPException(status_code=404, detail="File not found")