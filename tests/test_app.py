from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from cfin.api.routes import article as article_routes
from cfin.api.routes import finance as finance_routes
from cfin.main import app


class FakeFrame:
    def to_json(self) -> str:
        return '{"close":{}}'


@pytest.fixture
def client() -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client


def test_health(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "Ok!"}


def test_root_redirects_to_static_index(client: TestClient) -> None:
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_static_index(client: TestClient) -> None:
    response = client.get("/static/index.html")

    assert response.status_code == 200
    assert "CFin" in response.text


def test_favicon(client: TestClient) -> None:
    response = client.get("/favicon.ico")

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"


def test_swagger_and_openapi(client: TestClient) -> None:
    docs = client.get("/docs")
    schema = client.get("/openapi.json").json()

    assert docs.status_code == 200
    assert "Swagger UI" in docs.text
    assert schema["info"]["title"] == "CFin"
    assert schema["info"]["version"] == "0.1.0"
    assert {"/stock/{ticker}", "/markspace", "/resource/{article_name}"} <= set(
        schema["paths"]
    )


def test_markspace_lists_sample(client: TestClient) -> None:
    response = client.get("/markspace")

    assert response.status_code == 200
    assert "File Management" in response.text
    assert "sample.md" in response.text


def test_render_and_download_sample(client: TestClient) -> None:
    rendered = client.get("/resource/sample.md")
    downloaded = client.get("/download/sample.md")

    assert rendered.status_code == 200
    assert "<h1>" in rendered.text
    assert downloaded.status_code == 200
    assert downloaded.headers["content-type"] == "application/octet-stream"


def test_missing_article_returns_404(client: TestClient) -> None:
    assert client.get("/resource/missing.md").status_code == 404
    assert client.get("/download/missing.md").status_code == 404


def test_upload(
    client: TestClient,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(article_routes, "MARKDOWN_DIR", tmp_path)

    response = client.post(
        "/upload",
        files={"uploadFile": ("hello world.md", b"# Hello\n", "text/markdown")},
    )

    assert response.status_code == 200
    assert response.json() == {"status": 200}
    assert (tmp_path / "hello-world.md").read_bytes() == b"# Hello\n"
    assert client.get("/resource/hello-world.md").status_code == 200
    assert client.get("/download/hello-world.md").status_code == 200


def test_stock(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[tuple[str, str]] = []

    def fake_download(ticker: str, period: str) -> FakeFrame:
        calls.append((ticker, period))
        return FakeFrame()

    monkeypatch.setattr(finance_routes.yf, "download", fake_download)

    response = client.get("/stock/AAPL")

    assert response.status_code == 200
    assert response.json() == '{"close":{}}'
    assert calls == [("AAPL", "max")]
