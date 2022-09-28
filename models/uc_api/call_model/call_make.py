# -*- coding: utf-8 -*-

from __future__ import annotations
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from models.uc_api.base_models import CallMakeResponseType


class GeneralResponse(Enum):
    type = 'generalResponseType'


class CallMakeResponse(BaseModel):
    type: GeneralResponse = Field(default=GeneralResponse.type, alias='$type', description='тип данных')
    payload: CallMakeResponseType = Field(description="Список ивентов")
