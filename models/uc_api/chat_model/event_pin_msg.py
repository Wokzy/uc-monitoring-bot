# -*- coding: utf-8 -*-

from __future__ import annotations
from enum import Enum
from typing import List, Optional, Union
from pydantic import BaseModel, Field
from models.uc_api.base_models import ChatEventPinEvent, ChatEvent


class GeneralEventType(Enum):
    type = 'generalEventType'


class EventPinMsg(BaseModel):
    type: GeneralEventType = Field(default=GeneralEventType.type, alias='$type', description='тип данных')
    events: Optional[List[Union[ChatEvent, ChatEventPinEvent]]] = Field(description="Список ивентов")