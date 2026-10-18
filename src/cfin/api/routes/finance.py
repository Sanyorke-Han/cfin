"""Stock price routes backed by yfinance."""

from fastapi import APIRouter
import yfinance as yf

router = APIRouter()


@router.get("/stock/{ticker}", tags=["Finance"])
def get_stock(ticker: str) -> str:
    df = yf.download(ticker, period="max")
    return df.to_json()
