from __future__ import annotations
from enum import Enum
from pydantic import BaseModel, Field
from models.uc_api.base_models import FolderRoot


class generalResponseType(Enum):
    type = 'generalResponseType'


class FolderRootResponse(BaseModel):
    payload: FolderRoot
    type: generalResponseType = Field(default=generalResponseType.type, alias='$type', description='тип данных')
