from __future__ import annotations
from enum import Enum
from typing import List, Optional, Union
from pydantic import BaseModel, Field
from models.uc_api.base_models import FolderRoot


class generalResponseType(Enum):
    type = 'generalResponseType'


class FolderListResponse(BaseModel):
    # payload: Union[]
    type: generalResponseType = Field(default=generalResponseType.type, alias='$type', description='тип данных')
