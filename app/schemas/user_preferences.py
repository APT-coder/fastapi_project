from pydantic import BaseModel, ConfigDict
from typing import Optional


class UserPreferencesBase(BaseModel):
    display_name: Optional[str] = None
    email_notification_enabled: Optional[bool] = True
    profile_pic_link: Optional[str] = None


class UserPreferencesCreateUpdate(UserPreferencesBase):
    pass


class UserPreferencesRead(UserPreferencesBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)
