# -*- coding: utf-8 -*-

from __future__ import annotations

from enum import Enum
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from models.uc_api.base_models import GeneralEventType, ChatIdType, ConferenceIdType, ConferenceAbonentIdType,\
     ConferenceMemberStatusType, _Type134


class ConferenceStatusType(Enum):
    INACTIVE = 'INACTIVE'


class ChatGroupConferenceStatusNotifyType(BaseModel):
    chat_id: ChatIdType
    conference_id: ConferenceIdType
    start_time: datetime = Field(..., description='Время начала конференции')
    status: ConferenceStatusType
    screen_demo_member_id: Optional[ConferenceAbonentIdType] = None
    speaker_id: Optional[ConferenceAbonentIdType] = None
    members: Optional[List[ConferenceMemberStatusType]] = None
    _type: _Type134 = Field(..., alias='$type', description='тип данных')


class ChatGroupCnfStatusNtfInactive(BaseModel):
    type: GeneralEventType = Field(default=GeneralEventType.type, alias='$type', description='тип данных')
    events: List[ChatGroupConferenceStatusNotifyType] = Field(description="Список ивентов")
