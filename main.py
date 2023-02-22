from typing import Optional

from fastapi import FastAPI
import yfinance as yf

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health_check():
    return {"status": "Ok!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.get("/stock/{ticker}")
def get_stock(ticker: str):
    df = yf.download(ticker, period='max')
    return df.to_json()
