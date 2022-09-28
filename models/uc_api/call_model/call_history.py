# -*- coding: utf-8 -*-

from __future__ import annotations
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from models.uc_api.base_models import callHistoryResponse


class GeneralResponse(Enum):
    type = 'generalResponseType'


class callHistory(BaseModel):
    type: GeneralResponse = Field(default=GeneralResponse.type, alias='$type', description='тип данных')
    payload: callHistoryResponse = Field(description="Список ивентов")
