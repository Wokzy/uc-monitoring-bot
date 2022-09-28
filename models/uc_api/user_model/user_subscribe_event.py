from __future__ import annotations

from enum import Enum
from typing import List
from pydantic import BaseModel, Field
from models.uc_api.base_models import UserStatusNotify


class GeneralEventType(Enum):
    type = 'generalEventType'


class SubscribeEvent(BaseModel):
    type: GeneralEventType = Field(default=GeneralEventType.type, alias='$type', description='тип данных')
    events: List[UserStatusNotify] = Field(description="Список ивентов")
