# -*- coding: utf-8 -*-
from __future__ import annotations
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from models.uc_api.base_models import ChatEventNotify


class GeneralEventType(Enum):
    type = 'generalEventType'


class EventNotify(BaseModel):
    type: GeneralEventType = Field(default=GeneralEventType.type, alias='$type', description='тип данных')
    events: Optional[List[ChatEventNotify]] = Field(description="Список ивентов")
