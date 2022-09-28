from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Extra, Field, SecretStr, conint, constr
from models.uc_api.uc_api_models import GeneralRequestType, GeneralResponseType

class Type(Enum):
    SDP_OFFER = 'SDP_OFFER'
    SDP_ANSWER = 'SDP_ANSWER'

class SdpType(BaseModel):
    body: str = Field(..., description='Текстовое представление SDP', example='v=0...')
    type: Type = Field(..., description='Направление SDP')

class PhaseType(Enum):
    INITIATING = 'INITIATING'
    ALERTING = 'ALERTING'
    ANSWER = 'ANSWER'
    RELEASE = 'RELEASE'
    UPDATE_MEDIA = 'UPDATE_MEDIA'

class _Type17(Enum):
    callInfoType = 'callInfoType'

class CallInfoType(BaseModel):
    call_id: str
    owner_id: str
    participant_id: Optional[str] = None
    chat_id: str
    owner_display_name: Optional[str] = Field(
        None, description='Имя пользователя-владельца вызова'
    )
    participant_display_name: Optional[str] = Field(
        None, description='Имя второго участника вызова'
    )
    phase: PhaseType
    start_time: str = Field(
        ..., description='Время начала вызова', example='2021-01-28T15:51:43.511Z'
    )
    answer_time: Optional[str] = Field(
        None, description='Время ответа на вызов', example='2021-01-28T15:51:43.511Z'
    )
    sdp: Optional[SdpType] = None
    _type: _Type17 = Field(..., alias='$type', description='тип данных')


class CallInfo(BaseModel):
    id: conint(ge=1) = Field(
        ...,
        description='Уникальный идентификатор запроса, на который посылается данный ответ.'
                    ' Служит для связки запрос/ответ',
        example=1234,
    )
    result_code: conint(ge=200, le=299) = Field(
        ...,
        description='Код с результатом выполнения запроса. Аналог HTTP status code.',
        example=200,
    )
    payload: CallInfoType
    type: GeneralResponseType = Field(default=GeneralResponseType.type, alias='$type', description='тип данных')


class CallInfoRequest(BaseModel):
    call_id: str
    _type: str = Field("callInfoRequestType", alias='$type')


# class CallInfoRequest(BaseModel):
#     payload: CallInfoRequestType
#     _type: GeneralRequestType = Field(GeneralRequestType.type, alias='$type')