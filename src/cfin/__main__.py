"""Run the CFin service with uvicorn."""

import uvicorn

from cfin.config import HOST, PORT, RELOAD


def main() -> None:
    uvicorn.run("cfin.main:app", host=HOST, port=PORT, reload=RELOAD)


if __name__ == "__main__":
    main()
