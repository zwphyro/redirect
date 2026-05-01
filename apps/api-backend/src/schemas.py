from pydantic import BaseModel, ConfigDict


class HTTPExceptionSchema(BaseModel):
    detail: str

    model_config = ConfigDict(
        json_schema_extra={"example": {"detail": "Error message"}}
    )
