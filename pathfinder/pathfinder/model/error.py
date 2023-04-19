from typing import Any

from pydantic.main import BaseModel


class ErrorMessage(BaseModel):
    message: str
    additional_info: dict[str, Any] | None = None