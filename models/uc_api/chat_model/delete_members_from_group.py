from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field
from models.uc_api.base_models import DeleteMembersFromGroupNotify, GeneralEventType


class DeleteMembersFromGroup(BaseModel):
    type: GeneralEventType = Field(default=GeneralEventType.type, alias='$type', description='тип данных')
    events: Optional[List[DeleteMembersFromGroupNotify]] = Field(description="Список ивентов")
