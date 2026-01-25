from pydantic import BaseModel


class HTTPExceptionSchema(BaseModel):
    detail: str

    class Config:
        json_schema_extra = {"example": {"detail": "Entity not found"}}
