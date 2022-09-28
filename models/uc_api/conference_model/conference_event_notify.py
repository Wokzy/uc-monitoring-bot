# -*- coding: utf-8 -*-

from __future__ import annotations

from typing import List
from pydantic import BaseModel, Field
from models.uc_api.uc_api_models import CallEvent
from models.uc_api.base_models import GeneralEventType


class ConfEventNotify(BaseModel):
    type: GeneralEventType = Field(default=GeneralEventType.type, alias='$type', description='тип данных')
    events: List[CallEvent] = Field(description="Список ивентов")
