# -*- coding: utf-8 -*-

from __future__ import annotations

from typing import List
from pydantic import BaseModel, Field
from models.uc_api.base_models import GeneralEventType, ChatEvent


class ConfMsgInChat(BaseModel):
    type: GeneralEventType = Field(default=GeneralEventType.type, alias='$type', description='тип данных')
    events: List[ChatEvent] = Field(description="Список ивентов")
