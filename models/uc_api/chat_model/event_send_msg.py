# -*- coding: utf-8 -*-

from __future__ import annotations
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from models.uc_api.base_models import ChatEvent


class GeneralEventType(Enum):
    type = 'generalEventType'


class EventSendMsg(BaseModel):
    type: GeneralEventType = Field(default=GeneralEventType.type, alias='$type', description='тип данных')
    events: List[ChatEvent] = Field(description="Список ивентов")
