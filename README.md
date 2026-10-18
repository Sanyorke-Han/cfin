# CFin

Use Python [FastAPI](https://fastapi.tiangolo.com) to build a service and deploy on Render for accessing stock price, convenient for research stock tech analysis.

The service runs on Python 3.14 and is packaged with `pyproject.toml`.

## Layout

```text
src/cfin/
├── __init__.py
├── __main__.py          # uvicorn launcher
├── config.py            # paths and runtime settings
├── main.py              # FastAPI application factory
├── api/
│   └── routes/
│       ├── article.py   # markdown article routes
│       ├── finance.py   # yfinance stock route
│       └── system.py    # root, favicon, health
├── resources/           # markdown, css, templates
└── static/              # static site
tests/
└── test_app.py
```

## Setup

```bash
# Install uv
python3 -m pip install --break-system-packages uv

# Install Python 3.14 and project dependencies
uv sync --extra dev
```

## Run

```bash
# Development
uv run cfin

# Or with uvicorn directly
uv run uvicorn cfin.main:app --reload
```

The service listens on `http://127.0.0.1:8000` by default. Override with
`CFIN_HOST`, `CFIN_PORT` (or `PORT`), `CFIN_RELOAD`, and `CFIN_DEBUG`.

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| GET | `/` | Redirect to `/static/index.html` |
| GET | `/health` | Health check |
| GET | `/docs` | Swagger UI |
| GET | `/openapi.json` | OpenAPI schema |
| GET | `/static/*` | Static files |
| GET | `/stock/{ticker}` | Stock history from yfinance |
| GET | `/markspace` | Markdown file manager |
| GET | `/resource/{article_name}` | Render markdown as HTML |
| POST | `/upload` | Upload a markdown file |
| GET | `/download/{article_name}` | Download a markdown file |

## Test

```bash
uv run pytest
```
