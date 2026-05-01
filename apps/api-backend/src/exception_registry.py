from fastapi import FastAPI
from fastapi.responses import JSONResponse


class ExceptionRegistry:
    _registry: dict[type[Exception], int] = {}

    @staticmethod
    def register(status_code: int):
        def decorator(exc_class: type[Exception]) -> type[Exception]:
            ExceptionRegistry._registry[exc_class] = status_code
            return exc_class

        return decorator

    @classmethod
    def apply(cls, app: FastAPI) -> None:
        for exc_class, code in cls._registry.items():

            def handler_factory(status_code=code):
                def handler(_, exception):
                    return JSONResponse(
                        status_code=status_code,
                        content={"detail": str(exception)},
                    )

                return handler

            app.add_exception_handler(exc_class, handler_factory())
