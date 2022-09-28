from __future__ import annotations
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, conint
from models.uc_api.base_models import ImageType, Attachment, Type, Type4


class ChatEventType(Enum):
    type = 'chatEventType'


class ChatType(Enum):
    P2P = 'P2P'
    GROUP = 'GROUP'


class GroupChatMemberPresenceNotifyType(Enum):
    type = 'groupChatMemberPresenceNotifyType'


class GroupChatMemberPresenceNotify(BaseModel):
    type: Type4
    user_id: str = Field(
        None,
        description='Внутренний уникальный идентификатор пользователя UC',
        example="18446744073709551615",
        )
    _type: GroupChatMemberPresenceNotifyType = Field(type=GroupChatMemberPresenceNotifyType.type,
                                                     alias='$type', description='тип данных')


class ChatEventForwardType(Enum):
    type = 'chatEventForwardType'


class ChatEventForward(BaseModel):
    original_sender_id: str = Field(description='Идентификатор пользователя, который изначально отправлял сообщение')
    type: ChatEventForwardType = Field(default=ChatEventForwardType.type, alias='$type', description='тип данных')


class EventOptionsType(BaseModel):
    correlation_id: str = Field(
        None,
        description='Уникальный идентификатор события чата',
        example="18446744073709551615",
        )
    changed: Optional[bool] = Field(
        None, description='Данное сообщение было отредактировано'
            )
    partial: Optional[bool] = Field(
        None, description='Говорит о том, что сообщение слишком большое и было обрезано'
        )
    silent: Optional[bool] = Field(
        None,
        description='Флаг говорит о том, что сообщение было отправлено в беззвучном режиме (UI, получил событие с данным признаком не должен делать звуковую нотификацию о получении сообщения)',
        )
    notify: Optional[GroupChatMemberPresenceNotify] = Field(
        None, description='Любая нотификация в рамках чата'
        )
    events_group_id: str
    forward: ChatEventForward
    images: Optional[List[ImageType]] = None
    attachments: Optional[List[Attachment]] = Field(
        None,
        description='Список идентификаторов attachment-ов, и их описаний, привязанных к данному сообщению.',
        )


class ChatEvent(BaseModel):
    event_id: str = Field(
        ...,
        description='Уникальный идентификатор события чата',
        example="18446744073709551615",
        )
    uuid: str = Field(
        ...,
        description='Уникальный идентификатор события (в рамках конкретного клиента), выставляемый на стороне клиента.',
        example='unique_id_string',
        )
    sender_id: str = Field(
        ..., description='Идентификатор отправителя сообщения', example=2532
        )
    chat_id: str = Field(
        ...,
        description='Внутренний уникальный идентификатор P2P чата UC',
        example="10952",
        )
    sent_at: Optional[str] = Field(
        description='Время образования event-а в системе (время выставляется на сервере)',
        example='2021-01-28T15:49:43.511Z',
        )
    received_at: Optional[str] = Field(
        None,
        description='Время получения event-а встречной стороной',
        example='2021-01-28T15:50:43.511Z',
        )
    read_at: Optional[str] = Field(
        None, description='Время прочтения event-а', example='2021-01-28T15:51:43.511Z'
        )
    parent_event_id: Optional[str] = Field(
        None,
        description='Поле в которое записывается идентификатор сообщения на которое пишется ответ',
        example='727',
        )
    type: Type = Field(..., description='Тип события')
    plaintext: str = Field(
        ...,
        description='Строковое представление сообщения (отформатированное текстовое сообщение, название файла, подпись к изображению и т.п.)',
        example='Текст сообщения...',
        )
    urls: Optional[List[str]] = Field(
        None,
        description='Список ссылок, присутствующих в данном сообщении',
        example=['https://www.example.ru/path1', 'https://www.example.ru/path2'],
        )
    mentions: Optional[List[str]] = Field(
        None,
        description='Список идентификаторов пользователей, упомянутых в данном сообщении',
        example=[789456123654, 123654789987],
        )
    options: EventOptionsType = Field(
        description='Возможные значения:<BR/><B>attachments</B> - Список описаний (id, имя, тип, размер) приложенных к данному сообщению файлов<BR/><b>images</b> - Изображения, отправленное в данном сообщении (id, размеры, превью)<BR/><b>partial</b> - флаг, если его значение равно true, означает, что пришло только начало сообщения. Полное сообщение можно получить командой /chat/event/get<BR/>',
        example={
            'attachments': [
                {
                    'attachment_id': '6f98739f-c362-1b9a-ab8b-52c21d50d2fb',
                    'filename': 'protei.meetings.txt',
                    'mimetype': 'text/plain',
                    'size': 1953952,
                    },
                {
                    'attachment_id': '1f38739f-c362-1b9a-ab4b-52c21d60d4fa',
                    'filename': 'protei.events.txt',
                    'mimetype': 'text/plain',
                    'size': 1864234,
                    },
                ],
            'images': {
                'attachment_id': '111111111111',
                'width': 1920,
                'height': 1080,
                'thumbnail': {'source': 'base64....', 'width': 120, 'height': 60},
                'sizes': [
                    {'size': 's', 'width': 120, 'height': 60},
                    {'size': 'm', 'width': 180, 'height': 90},
                    ],
                },
            },
        )
    chat_type: ChatType
    type_1: ChatEventType = Field(default=ChatEventType.type, alias='$type', description='тип данных')


class GeneralEventType(Enum):
    type = 'generalEventType'


class EventForward(BaseModel):
    type: GeneralEventType = Field(default=GeneralEventType.type, alias='$type', description='тип данных')
    events: List[ChatEvent] = Field(description="Список ивентов")

class NotForwardedItem(BaseModel):
    event_id: str
    chat_ids: List[str] = Field(..., description='Массив чатов в которые не удалось переслать сообщения')


class ChatEventForwardResponseType(Enum):
    type = 'chatEventForwardResponseType'


class ChatEventForwardResponse(BaseModel):
    forward_group_id: str
    not_forwarded: Optional[List[NotForwardedItem]] = Field(
        None, description='Сообщения которые не удалось переслать')
    type: ChatEventForwardResponseType = Field(default=ChatEventForwardResponseType.type, alias='$type',
                                               description='тип данных')

class GeneralResponseType(Enum):
    type = 'generalResponseType'


class ForwardResponse(BaseModel):
    id: conint(ge=1)
    result_code: conint(ge=200, le=299)
    payload: ChatEventForwardResponse
    type: GeneralResponseType = Field(default=GeneralResponseType.type, alias='$type', description='тип данных')

class NoneOptions(BaseModel):
    correlation_id: str = Field(
        None,
        description='Уникальный идентификатор события чата',
        example="18446744073709551615",
        )
    changed: Optional[bool] = Field(
        None, description='Данное сообщение было отредактировано'
            )
    partial: Optional[bool] = Field(
        None, description='Говорит о том, что сообщение слишком большое и было обрезано'
        )
    silent: Optional[bool] = Field(
        None,
        description='Флаг говорит о том, что сообщение было отправлено в беззвучном режиме (UI, получил событие с данным признаком не должен делать звуковую нотификацию о получении сообщения)',
        )
    notify: Optional[GroupChatMemberPresenceNotify] = Field(
        None, description='Любая нотификация в рамках чата'
        )
    events_group_id: str
    forward: Optional[bool]
    images: Optional[List[ImageType]] = None
    attachments: Optional[List[Attachment]] = Field(
        None,
        description='Список идентификаторов attachment-ов, и их описаний, привязанных к данному сообщению.',
        )


class SendMsgEvent(BaseModel):
    event_id: str = Field(
        ...,
        description='Уникальный идентификатор события чата',
        example="18446744073709551615",
        )
    uuid: str = Field(
        ...,
        description='Уникальный идентификатор события (в рамках конкретного клиента), выставляемый на стороне клиента.',
        example='unique_id_string',
        )
    sender_id: str = Field(
        ..., description='Идентификатор отправителя сообщения', example=2532
        )
    chat_id: str = Field(
        ...,
        description='Внутренний уникальный идентификатор P2P чата UC',
        example="10952",
        )
    sent_at: Optional[str] = Field(
        description='Время образования event-а в системе (время выставляется на сервере)',
        example='2021-01-28T15:49:43.511Z',
        )
    received_at: Optional[str] = Field(
        None,
        description='Время получения event-а встречной стороной',
        example='2021-01-28T15:50:43.511Z',
        )
    read_at: Optional[str] = Field(
        None, description='Время прочтения event-а', example='2021-01-28T15:51:43.511Z'
        )
    parent_event_id: Optional[str] = Field(
        None,
        description='Поле в которое записывается идентификатор сообщения на которое пишется ответ',
        example='727',
        )
    type: Type = Field(..., description='Тип события')
    plaintext: str = Field(
        ...,
        description='Строковое представление сообщения (отформатированное текстовое сообщение, название файла, подпись к изображению и т.п.)',
        example='Текст сообщения...',
        )
    urls: Optional[List[str]] = Field(
        None,
        description='Список ссылок, присутствующих в данном сообщении',
        example=['https://www.example.ru/path1', 'https://www.example.ru/path2'],
        )
    mentions: Optional[List[str]] = Field(
        None,
        description='Список идентификаторов пользователей, упомянутых в данном сообщении',
        example=[789456123654, 123654789987],
        )
    options: NoneOptions = Field(
        description='Возможные значения:<BR/><B>attachments</B> - Список описаний (id, имя, тип, размер) приложенных к данному сообщению файлов<BR/><b>images</b> - Изображения, отправленное в данном сообщении (id, размеры, превью)<BR/><b>partial</b> - флаг, если его значение равно true, означает, что пришло только начало сообщения. Полное сообщение можно получить командой /chat/event/get<BR/>',
        example={
            'attachments': [
                {
                    'attachment_id': '6f98739f-c362-1b9a-ab8b-52c21d50d2fb',
                    'filename': 'protei.meetings.txt',
                    'mimetype': 'text/plain',
                    'size': 1953952,
                    },
                {
                    'attachment_id': '1f38739f-c362-1b9a-ab4b-52c21d60d4fa',
                    'filename': 'protei.events.txt',
                    'mimetype': 'text/plain',
                    'size': 1864234,
                    },
                ],
            'images': {
                'attachment_id': '111111111111',
                'width': 1920,
                'height': 1080,
                'thumbnail': {'source': 'base64....', 'width': 120, 'height': 60},
                'sizes': [
                    {'size': 's', 'width': 120, 'height': 60},
                    {'size': 'm', 'width': 180, 'height': 90},
                    ],
                },
            },
        )
    chat_type: ChatType
    type_1: ChatEventType = Field(default=ChatEventType.type, alias='$type', description='тип данных')

class GeneralEventType(Enum):
    type = 'generalEventType'


class EventAdditionalMsg(BaseModel):
    type: GeneralEventType = Field(default=GeneralEventType.type, alias='$type', description='тип данных')
    events: Optional[List[SendMsgEvent]] = Field(description="Список ивентов")