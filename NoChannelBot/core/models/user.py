from typing import Optional

from pydantic import BaseModel


class UserModel(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str]
    username: Optional[str]
    language_code: Optional[str]
