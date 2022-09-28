# -*- coding: utf-8 -*-

from __future__ import annotations
from enum import Enum
from typing import List, Optional, Union
from pydantic import BaseModel, Field, constr


class GeneralEventType(Enum):
    type = 'generalEventType'


class SubTypeSdp(Enum):
    SDP_OFFER = 'SDP_OFFER'
    SDP_ANSWER = 'SDP_ANSWER'


class SdpType(BaseModel):
    body: str = Field(..., description='Текстовое представление SDP', example='v=0...')
    type: SubTypeSdp = Field(..., description='Направление SDP')


class PhaseType(Enum):
    INITIATING = 'INITIATING'
    ALERTING = 'ALERTING'
    ANSWER = 'ANSWER'
    RELEASE = 'RELEASE'
    UPDATE_MEDIA = 'UPDATE_MEDIA'


class Side(Enum):
    ORIGINATION = 'ORIGINATION'
    TERMINATION = 'TERMINATION'
    SYSTEM = 'SYSTEM'


class Phase(Enum):
    INITIATING = 'INITIATING'
    ALERTING = 'ALERTING'
    ANSWER = 'ANSWER'
    RELEASE = 'RELEASE'
    UPDATE_MEDIA = 'UPDATE_MEDIA'


class CallSetupEventType(Enum):
    type = 'callSetupEventType'


class CallSetupEvent(BaseModel):
    callee_display_name: Optional[str] = Field(
        None, description='Отображаемое имя встречной стороны', example='User B'
        )
    sdp: Optional[SdpType]
    side: Side = Field(
        ..., description='сторона вызова на которую идет данное событие (O или T)'
        )
    type: CallSetupEventType = Field(default=CallSetupEventType.type, alias='$type', description='тип данных')


class CallAlertingEventType(Enum):
    type = 'callAlertingEventType'


class CallAlertingEvent(BaseModel):
    callee_display_name: Optional[str] = Field(
        None, description='Отображаемое имя встречной стороны', example='User B'
        )
    sdp: Optional[SdpType]
    type: CallAlertingEventType = Field(default=CallAlertingEventType.type, alias='$type', description='тип данных')


class CallProgressEventType(Enum):
    type = 'callProgressEventType'


class CallProgressEvent(BaseModel):
    callee_display_name: Optional[str] = Field(
        None, description='Отображаемое имя встречной стороны', example='User B'
        )
    sdp: Optional[SdpType]
    type: CallProgressEventType = Field(default=CallProgressEventType.type, alias='$type', description='тип данных')


class CallInfoEventType(Enum):
    type = 'callInfoEventType'


class CallInfoEvent(BaseModel):
    type: str = Field(
        ...,
        description='Тип посылаемых данных (имеет формат mimetype)',
        example='message/ice',
        )
    content: str = Field(
        ...,
        description='Посылаемые данные',
        example='a=candidate:4234997325 1 udp 2043278322 192.168.23.87 44323 typ host',
        )
    type: CallInfoEventType = Field(default=CallInfoEventType.type, alias='$type', description='тип данных')


class CallAnswerEventType(Enum):
    type = 'callAnswerEventType'


class CallAnswerEvent(BaseModel):
    callee_display_name: Optional[str] = Field(
        None, description='Отображаемое имя встречной стороны', example='User B'
        )
    sdp: Optional[SdpType]
    type: CallAnswerEventType = Field(default=CallAnswerEventType.type, alias='$type', description='тип данных')


class CallUpdateEventType(Enum):
    type = 'callUpdateEventType'


class CallUpdateEvent(BaseModel):
    sdp: SdpType
    type: CallUpdateEventType = Field(default=CallUpdateEventType.type, alias='$type', description='тип данных')


class CallUpdateFailedEventType(Enum):
    type = 'callUpdateFailedEventType'


class CallUpdateFailedEvent(BaseModel):
    code: Optional[int] = Field(
        None, description='Причина не успешность пересогласования медии', example='415'
        )
    reason: Optional[str] = Field(
        None, description='Текстовое описание причины', example='Unsupported Media Type'
        )
    type: CallUpdateFailedEventType = Field(default=CallUpdateFailedEventType.type, alias='$type',
                                            description='тип данных')


class CallReleaseEventType(Enum):
    type = 'callReleaseEventType'


class CallReleaseEvent(BaseModel):
    reason: Optional[str] = Field(
        None, description='Причина завершения вызова', example='Normal call clean'
        )
    side: Optional[Side] = Field(
        'SYSTEM', description='сторона которая была инициатором завершения вызова'
        )
    type: CallReleaseEventType = Field(default=CallReleaseEventType.type, alias='$type', description='тип данных')


class CallMediaUpdatedEventType(Enum):
    type = 'callMediaUpdatedEventType'


class CallMediaStatusType(Enum):
    type = 'callMediaStatusType'


class CallMediaStatus(BaseModel):
    content: str = Field(..., description="", example='microphone')
    type: str = Field(..., description="", example='video')
    mid: int = Field(..., description="", example=1)
    description: str = Field(..., description="Описание", example="Дополнительный микрофон на зал")
    type_1: CallMediaStatusType = Field(default=CallMediaStatusType.type, alias='$type',
                                        description='тип данных')


class CallMediaUpdatedEvent(BaseModel):
    side: Side = Field(
        ..., description='сторона вызова, которая прислала данную нотификацию'
        )
    content: List[CallMediaStatus]
    type: CallMediaUpdatedEventType = Field(default=CallMediaUpdatedEventType.type, alias='$type', description='тип '
                                                                                                               'данных')


class CallStatusEventType(Enum):
    type = 'callStatusEventType'


class CallStatusEvent(BaseModel):
    o_user_id: str = Field(..., description='Внутренний уникальный идентификатор пользователя UC',
                           example="18446744073709551615", )
    o_display_name: Optional[str] = Field(..., description='Внутренний уникальный идентификатор пользователя UC',
                                          example="18446744073709551615", )
    o_sdp: SdpType
    t_user_id: Optional[str] = Field(..., description='Внутренний уникальный идентификатор пользователя UC',
                                     example="18446744073709551615", )
    t_display_name: Optional[str] = Field(..., description='Внутренний уникальный идентификатор пользователя UC',
                                          example="18446744073709551615", )
    t_sdp: Optional[SdpType] = None
    start_time: str = Field(..., description='Время начала вызова', example='2021-05-14T10:41:43.511Z')
    answer_time: Optional[str] = Field(..., description='Время ответа на входящий вызов',
                                       example='2021-05-14T10:41:48.511Z', )
    phase: Phase = Field(..., description='Текущая фаза вызова', example='ANSWER')
    type: CallStatusEventType = Field(default=CallStatusEventType.type, alias='$type', description='тип данных')


class CallEventType(Enum):
    type = "callEventType"


class CallEvent(BaseModel):
    call_id: constr(min_length=1) = Field(..., description='Идентификатор вызова',
                                          example='f973769f-c4f6-44ce-984e-9fbf628beb7f', )
    owner_id: Optional[str] = Field(None, description='Внутренний уникальный идентификатор пользователя UC',
                                    example="18446744073709551615", )
    participant_id: Optional[str] = Field(None, description='Внутренний уникальный идентификатор пользователя UC',
                                          example="18446744073709551615", )
    chat_id: Optional[str] = Field(..., description='Внутренний уникальный идентификатор чата UC',
                                   example="10952", )
    phase: Phase = Field(..., description='Фаза вызова')
    body: Optional[
        Union[
            CallSetupEvent,
            CallAlertingEvent,
            CallProgressEvent,
            CallInfoEvent,
            CallAnswerEvent,
            CallUpdateEvent,
            CallUpdateFailedEvent,
            CallReleaseEvent,
            CallStatusEvent,
            CallMediaUpdatedEvent,
            ]
                ]
    type: CallEventType = Field(default=CallEventType.type, alias='$type', description='тип данных')


class GeneralCallEvent(BaseModel):
    type: GeneralEventType = Field(default=GeneralEventType.type, alias='$type', description='тип данных')
    events: List[CallEvent] = Field(description="Список ивентов")


class CallEventSetup(BaseModel):
    call_id: constr(min_length=1) = Field(..., description='Идентификатор вызова',
                                          example='f973769f-c4f6-44ce-984e-9fbf628beb7f', )
    owner_id: Optional[str] = Field(None, description='Внутренний уникальный идентификатор пользователя UC',
                                    example="18446744073709551615", )
    participant_id: Optional[str] = Field(None, description='Внутренний уникальный идентификатор пользователя UC',
                                          example="18446744073709551615", )
    chat_id: Optional[str] = Field(..., description='Внутренний уникальный идентификатор чата UC',
                                   example="10952", )
    phase: Phase = Field(..., description='Фаза вызова')
    body: CallSetupEvent
    type: CallEventType = Field(default=CallEventType.type, alias='$type', description='тип данных')


class GeneralCallSetupEvent(BaseModel):
    type: GeneralEventType = Field(default=GeneralEventType.type, alias='$type', description='тип данных')
    events: List[CallEventSetup] = Field(description="Список ивентов")


class CallEventAlerting(BaseModel):
    call_id: constr(min_length=1) = Field(..., description='Идентификатор вызова',
                                          example='f973769f-c4f6-44ce-984e-9fbf628beb7f', )
    owner_id: Optional[str] = Field(None, description='Внутренний уникальный идентификатор пользователя UC',
                                    example="18446744073709551615", )
    participant_id: Optional[str] = Field(None, description='Внутренний уникальный идентификатор пользователя UC',
                                          example="18446744073709551615", )
    chat_id: Optional[str] = Field(..., description='Внутренний уникальный идентификатор чата UC',
                                   example="10952", )
    phase: Phase = Field(..., description='Фаза вызова')
    body: CallAlertingEvent
    type: CallEventType = Field(default=CallEventType.type, alias='$type', description='тип данных')


class GeneralCallAlertingEvent(BaseModel):
    type: GeneralEventType = Field(default=GeneralEventType.type, alias='$type', description='тип данных')
    events: List[CallEventAlerting] = Field(description="Список ивентов")


class CallEventProgress(BaseModel):
    call_id: constr(min_length=1) = Field(..., description='Идентификатор вызова',
                                          example='f973769f-c4f6-44ce-984e-9fbf628beb7f', )
    owner_id: Optional[str] = Field(None, description='Внутренний уникальный идентификатор пользователя UC',
                                    example="18446744073709551615", )
    participant_id: Optional[str] = Field(None, description='Внутренний уникальный идентификатор пользователя UC',
                                          example="18446744073709551615", )
    chat_id: Optional[str] = Field(..., description='Внутренний уникальный идентификатор чата UC',
                                   example="10952", )
    phase: Phase = Field(..., description='Фаза вызова')
    body: CallProgressEvent
    type: CallEventType = Field(default=CallEventType.type, alias='$type', description='тип данных')


class GeneralCallProgressEvent(BaseModel):
    type: GeneralEventType = Field(default=GeneralEventType.type, alias='$type', description='тип данных')
    events: List[CallEventProgress] = Field(description="Список ивентов")


class CallEventInfo(BaseModel):
    call_id: constr(min_length=1) = Field(..., description='Идентификатор вызова',
                                          example='f973769f-c4f6-44ce-984e-9fbf628beb7f', )
    owner_id: Optional[str] = Field(None, description='Внутренний уникальный идентификатор пользователя UC',
                                    example="18446744073709551615", )
    participant_id: Optional[str] = Field(None, description='Внутренний уникальный идентификатор пользователя UC',
                                          example="18446744073709551615", )
    chat_id: Optional[str] = Field(..., description='Внутренний уникальный идентификатор чата UC',
                                   example="10952", )
    phase: Phase = Field(..., description='Фаза вызова')
    body: CallInfoEvent
    type: CallEventType = Field(default=CallEventType.type, alias='$type', description='тип данных')


class GeneralCallInfoEvent(BaseModel):
    type: GeneralEventType = Field(default=GeneralEventType.type, alias='$type', description='тип данных')
    events: List[CallEventInfo] = Field(description="Список ивентов")


class CallEventAnswer(BaseModel):
    call_id: constr(min_length=1) = Field(..., description='Идентификатор вызова',
                                          example='f973769f-c4f6-44ce-984e-9fbf628beb7f', )
    owner_id: Optional[str] = Field(None, description='Внутренний уникальный идентификатор пользователя UC',
                                    example="18446744073709551615", )
    participant_id: Optional[str] = Field(None, description='Внутренний уникальный идентификатор пользователя UC',
                                          example="18446744073709551615", )
    chat_id: Optional[str] = Field(..., description='Внутренний уникальный идентификатор чата UC',
                                   example="10952", )
    phase: Phase = Field(..., description='Фаза вызова')
    body: CallAnswerEvent
    type: CallEventType = Field(default=CallEventType.type, alias='$type', description='тип данных')


class GeneralCallAnswerEvent(BaseModel):
    type: GeneralEventType = Field(default=GeneralEventType.type, alias='$type', description='тип данных')
    events: List[CallEventAnswer] = Field(description="Список ивентов")


class CallEventUpdate(BaseModel):
    call_id: constr(min_length=1) = Field(..., description='Идентификатор вызова',
                                          example='f973769f-c4f6-44ce-984e-9fbf628beb7f', )
    owner_id: Optional[str] = Field(None, description='Внутренний уникальный идентификатор пользователя UC',
                                    example="18446744073709551615", )
    participant_id: Optional[str] = Field(None, description='Внутренний уникальный идентификатор пользователя UC',
                                          example="18446744073709551615", )
    chat_id: Optional[str] = Field(..., description='Внутренний уникальный идентификатор чата UC',
                                   example="10952", )
    phase: Phase = Field(..., description='Фаза вызова')
    body: CallUpdateEvent
    type: CallEventType = Field(default=CallEventType.type, alias='$type', description='тип данных')


class GeneralCallUpdateEvent(BaseModel):
    type: GeneralEventType = Field(default=GeneralEventType.type, alias='$type', description='тип данных')
    events: List[CallEventUpdate] = Field(description="Список ивентов")


class CallEventUpdateFailed(BaseModel):
    call_id: constr(min_length=1) = Field(..., description='Идентификатор вызова',
                                          example='f973769f-c4f6-44ce-984e-9fbf628beb7f', )
    owner_id: Optional[str] = Field(None, description='Внутренний уникальный идентификатор пользователя UC',
                                    example="18446744073709551615", )
    participant_id: Optional[str] = Field(None, description='Внутренний уникальный идентификатор пользователя UC',
                                          example="18446744073709551615", )
    chat_id: Optional[str] = Field(..., description='Внутренний уникальный идентификатор чата UC',
                                   example="10952", )
    phase: Phase = Field(..., description='Фаза вызова')
    body: CallUpdateFailedEvent
    type: CallEventType = Field(default=CallEventType.type, alias='$type', description='тип данных')


class GeneralCallUpdateFailedEvent(BaseModel):
    type: GeneralEventType = Field(default=GeneralEventType.type, alias='$type', description='тип данных')
    events: List[CallEventUpdateFailed] = Field(description="Список ивентов")


class CallEventRelease(BaseModel):
    call_id: constr(min_length=1) = Field(..., description='Идентификатор вызова',
                                          example='f973769f-c4f6-44ce-984e-9fbf628beb7f', )
    owner_id: Optional[str] = Field(None, description='Внутренний уникальный идентификатор пользователя UC',
                                    example="18446744073709551615", )
    participant_id: Optional[str] = Field(None, description='Внутренний уникальный идентификатор пользователя UC',
                                          example="18446744073709551615", )
    chat_id: Optional[str] = Field(..., description='Внутренний уникальный идентификатор чата UC',
                                   example="10952", )
    phase: Phase = Field(..., description='Фаза вызова')
    body: CallReleaseEvent
    type: CallEventType = Field(default=CallEventType.type, alias='$type', description='тип данных')


class GeneralCallReleaseEvent(BaseModel):
    type: GeneralEventType = Field(default=GeneralEventType.type, alias='$type', description='тип данных')
    events: List[CallEventRelease] = Field(description="Список ивентов")


class CallEventStatus(BaseModel):
    call_id: constr(min_length=1) = Field(..., description='Идентификатор вызова',
                                          example='f973769f-c4f6-44ce-984e-9fbf628beb7f', )
    owner_id: Optional[str] = Field(None, description='Внутренний уникальный идентификатор пользователя UC',
                                    example="18446744073709551615", )
    participant_id: Optional[str] = Field(None, description='Внутренний уникальный идентификатор пользователя UC',
                                          example="18446744073709551615", )
    chat_id: Optional[str] = Field(..., description='Внутренний уникальный идентификатор чата UC',
                                   example="10952", )
    phase: Phase = Field(..., description='Фаза вызова')
    body: CallStatusEvent
    type: CallEventType = Field(default=CallEventType.type, alias='$type', description='тип данных')


class GeneralCallStatusEvent(BaseModel):
    type: GeneralEventType = Field(default=GeneralEventType.type, alias='$type', description='тип данных')
    events: List[CallEventStatus] = Field(description="Список ивентов")


class CallEventMediaUpdate(BaseModel):
    call_id: constr(min_length=1) = Field(..., description='Идентификатор вызова',
                                          example='f973769f-c4f6-44ce-984e-9fbf628beb7f', )
    owner_id: Optional[str] = Field(None, description='Внутренний уникальный идентификатор пользователя UC',
                                    example="18446744073709551615", )
    participant_id: Optional[str] = Field(None, description='Внутренний уникальный идентификатор пользователя UC',
                                          example="18446744073709551615", )
    chat_id: Optional[str] = Field(..., description='Внутренний уникальный идентификатор чата UC',
                                   example="10952", )
    phase: Phase = Field(..., description='Фаза вызова')
    body: CallMediaUpdatedEvent
    type: CallEventType = Field(default=CallEventType.type, alias='$type', description='тип данных')


class GeneralCallMediaUpdateEvent(BaseModel):
    type: GeneralEventType = Field(default=GeneralEventType.type, alias='$type', description='тип данных')
    events: List[CallEventMediaUpdate] = Field(description="Список ивентов")
