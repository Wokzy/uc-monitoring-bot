# -*- coding: utf-8 -*-

from __future__ import annotations
from enum import Enum
from typing import Any, List, Optional, Union
from pydantic import BaseModel, Field, conint
from models.uc_api.uc_api_models import CallEvent, UcChatSuccessEvent, UcChatFailedEvent, ChatEvent, MarkP2PChatEvent, \
    ChatTypingEventNotify, ChatEventNotify, ChatNotify, RealtimeStatusEvent, CallMakeResponse, P2pChat, UserInfo, \
    Chats, UnreadMessages, ContactSearchResponse, Settings, GenerateWSToken, ChatDeleteEventNotify, \
    AddMembersToGroupNotify, DeleteMembersFromGroupNotify, GroupChat, ChatGroupMemberAddResponse, \
    ChatGroupMemberRemoveResponse, ActiveCall, ChatEventForwardResponse, ChatEventForwardRequest, \
    UserSubscribeResponse, UserStatusNotify


class GeneralResponseType(Enum):
    type = 'generalResponseType'


class GeneralResponse(BaseModel):
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
    payload: Optional[
        Union[
            ChatEventForwardResponse,
            CallMakeResponse,
            P2pChat,
            UserInfo,
            Chats,
            UnreadMessages,
            ContactSearchResponse,
            Settings,
            GenerateWSToken,
            ChatEvent,
            GroupChat,
            ChatGroupMemberAddResponse,
            ChatGroupMemberRemoveResponse,
            ActiveCall,
            UserSubscribeResponse]
                    ] = Field(None, description='Тело ответа')
    type: GeneralResponseType = Field(default=GeneralResponseType.type, alias='$type', description='тип данных')


class GeneralEventType(Enum):
    type = 'generalEventType'


class GeneralEvent(BaseModel):
    type: GeneralEventType = Field(default=GeneralEventType.type, alias='$type', description='тип данных')
    events: Optional[List[
        Union[
            UserStatusNotify,
            CallEvent,
            UcChatSuccessEvent,
            UcChatFailedEvent,
            ChatEvent,
            MarkP2PChatEvent,
            ChatTypingEventNotify,
            ChatEventNotify,
            ChatNotify,
            RealtimeStatusEvent,
            ChatDeleteEventNotify,
            AddMembersToGroupNotify,
            DeleteMembersFromGroupNotify]
                        ]] = Field(description="Список ивентов")


class GeneralRequestType(Enum):
    type = 'generalRequestType'


class GeneralRequest(BaseModel):
    method: str = Field(..., description='Название команды, которую необходимо вызвать')
    id: conint(ge=1) = Field(
        ...,
        description='Уникальный идентификатор запроса. Служит для связки запрос/ответ',
        example=1234,
        )
    payload: Optional[Any] = Field(None, description='Тело запроса')
    type: GeneralRequestType = Field(default=GeneralRequestType.type, alias='$type', description='тип данных')


class GeneralErrorType(Enum):
    type = 'generalErrorType'


class GeneralError(BaseModel):
    id: conint(ge=0) = Field(
        ...,
        description='Уникальный идентификатор запроса, на который посылается данный ответ от ошибке.'
                    ' Служит для связки запрос/ответ',
        example=1234,
        )
    result_code: Optional[conint(ge=300, le=599)] = Field(
        None,
        description='Код с результатом выполнения запроса. Аналог HTTP status code.',
        example='[3-5]XX',
        )
    description: Optional[str] = Field(
        None,
        description='Текстовое описание ошибки',
        example='Упс, что то пошло не так',
        )
    command: str = Field(
        ...,
        description='Внутренняя команда (в рамках UC core) в рамках которой произошла ошибка.'
                    ' Данное поле полезно для разбора причин возникновения ошибки.',
        example='uc_web_access_layer_websocket_cmd',
        )
    reason: str = Field(
        ...,
        description='Внутренняя причина ошибки (в текстовом виде). Иногда не совсем удобно разводить ошибки'
                    ' по result_code (под одним result_code хочется объединить разные ошибки), но при этом иметь'
                    ' возможность пользователю показывать разные сообщения об ошибке.'
                    ' В этом случае стоит закладываться на reason',
        example='unsupported_version',
        )
    entity: Optional[List] = Field(
        None,
        description='Бывает так, что для корректного отображения ошибки пользователю необходимо со стороны'
                    ' backend-а передать UI дополнительный аргументы. В данном поле и содержатся данные аргументы.'
                    '<br/>Например: у нас стоит ограничение на 2 одновременных сессии пользователя.'
                    ' Пользователь заходит с третьего устройства, ему это не позволяют сделать, но при этом выводят'
                    ' список текущих сессий (который возвращается на UI в поле entity).',
        )
    type: GeneralErrorType = Field(GeneralErrorType.type, alias='$type', description='тип данных')
