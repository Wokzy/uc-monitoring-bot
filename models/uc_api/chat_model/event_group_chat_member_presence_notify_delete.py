# -*- coding: utf-8 -*-

from __future__ import annotations
from enum import Enum
from typing import List
from pydantic import BaseModel, Field
from models.uc_api.base_models import GeneralEventType, ChatEvent


class EventGroupChatMemberPresenceNotify(BaseModel):
    type: GeneralEventType = Field(default=GeneralEventType.type, alias='$type', description='тип данных')
    events: List[ChatEvent] = Field(description="Список ивентов")
