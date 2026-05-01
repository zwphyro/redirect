import uvicorn

from src.args import get_args
from src.settings import get_settings


if __name__ == "__main__":
    settings = get_settings()
    args = get_args()

    uvicorn.run("src.main:app", host=settings.host, port=settings.port, reload=args.dev)
