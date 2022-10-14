from typing import Any, Dict

from pydantic import BaseModel


class InputMessage(BaseModel):
    url: str
    message_source: Any
    headers: Dict[str, str]
