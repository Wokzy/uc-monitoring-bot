from __future__ import annotations
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from models.uc_api.base_models import UserSnapshotResponse


class GeneralResponseType(Enum):
    type = 'generalResponseType'


class Snapshot(BaseModel):
    payload: Optional[UserSnapshotResponse] = Field(description="Список ивентов")
    type: GeneralResponseType = Field(default=GeneralResponseType.type, alias='$type', description='тип данных')
    result_code: int
