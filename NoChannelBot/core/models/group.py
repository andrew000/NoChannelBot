from datetime import timedelta
from typing import Optional

from pydantic import BaseModel


class GroupSettings(BaseModel):
    ban_channels: bool = True
    until_date: Optional[timedelta] = None


class GroupModel(BaseModel):
    id: int
    member_count: Optional[int] = None
    link: Optional[str] = None
    settings: GroupSettings = GroupSettings()
