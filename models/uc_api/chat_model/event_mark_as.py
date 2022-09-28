# -*- coding: utf-8 -*-

from __future__ import annotations
from enum import Enum
from typing import List
from pydantic import BaseModel, Field
from models.uc_api.base_models import ChatEventNotify


class GeneralEventType(Enum):
    type = 'generalEventType'


class EventMarkAs(BaseModel):
    type: GeneralEventType = Field(default=GeneralEventType.type, alias='$type', description='тип данных')
    events: List[ChatEventNotify] = Field(description="Список ивентов")
