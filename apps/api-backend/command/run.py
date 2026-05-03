import uvicorn

from src.args import get_args
from src.logging import setup_logging
from src.settings import get_settings


if __name__ == "__main__":
    settings = get_settings()
    args = get_args()

    config = setup_logging(settings.log_level)
    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=args.dev,
        log_config=config,
    )
