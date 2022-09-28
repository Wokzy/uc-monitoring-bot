# -*- coding: utf-8 -*-

from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field
from models.uc_api.base_models import GeneralEventType
from models.uc_api.uc_api_models import CallIdType, UcUserIdType, ChatIdType, ChatType, CallReleaseEvent,\
     CallEventType, Phase


class CallEvent(BaseModel):
    call_id: CallIdType
    owner_id: Optional[UcUserIdType] = None
    participant_id: Optional[UcUserIdType] = None
    chat_id: Optional[ChatIdType] = None
    chat_type: Optional[ChatType] = None
    phase: Phase = Field(..., description='Фаза вызова')
    body: Optional[CallReleaseEvent] = None
    type: CallEventType = Field(default=CallEventType.type, alias='$type', description='тип данных')


class ConfEventPhaseReleaseNotify(BaseModel):
    type: GeneralEventType = Field(default=GeneralEventType.type, alias='$type', description='тип данных')
    events: List[CallEvent] = Field(description="Список ивентов")
