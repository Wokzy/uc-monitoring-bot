# -*- coding: utf-8 -*-

from __future__ import annotations
from enum import Enum
from typing import Any, List, Optional, Union, Literal
from pydantic import BaseModel, Field, conint, constr, SecretStr
from pydantic.dataclasses import dataclass


# TODO uiControlEventType pushDataEventType chatGroupConferenceMemberJoinResponseType
#  chatGroupConferenceMemberUnjoinResponseType
class ChatIdType(BaseModel):
    __root__: str = Field(
        ...,
        description='Внутренний уникальный идентификатор чата UC',
        example="10952",
        )


class ChatType(Enum):
    P2P = 'P2P'
    GROUP = 'GROUP'


class StatusChat(Enum):
    CREATED = 'CREATED'
    BLOCKED = 'BLOCKED'
    DELETED = 'DELETED'
    ARCHIVED = 'ARCHIVED'
    UPDATED = 'UPDATED'
    TYPING = 'TYPING'


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
    payload: Optional[Any] = Field(None, description='Тело ответа')
    type: GeneralResponseType = Field(default=GeneralResponseType.type, alias='$type', description='тип данных')


class GeneralEventType(Enum):
    type = 'generalEventType'


class GeneralEvent(BaseModel):
    type: GeneralEventType = Field(default=GeneralEventType.type, alias='$type', description='тип данных')
    events: Optional[List[Any]] = Field(description="Список ивентов")


class GeneralErrorType(Enum):
    type = 'generalErrorType'


class GeneralError(BaseModel):
    id: conint(ge=0) = Field(
        ...,
        description='Уникальный идентификатор запроса, на который посылается данный ответ от ошибке.'
                    ' Служит для связки запрос/ответ',
        example=1234,
        )
    description: Optional[str] = Field(
        None,
        description='Текстовое описание ошибки',
        example='Упс, что то пошло не так',
        )
    command: str = Field(
        None,
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


class JsonStringType(BaseModel):
    __root__: dict = Field(
        description='Представление json в строке',
        example='{json_key1: 1, json_key2: "value2"}',
        )


class UcUserIdType(BaseModel):
    __root__: str = Field(
        None,
        description='Внутренний уникальный идентификатор пользователя UC',
        example="18446744073709551615",
        )


class UcExternalUserIdType(BaseModel):
    __root__: constr(min_length=1) = Field(
        ...,
        description='Внешний идентификатор пользователя UC',
        example='vasya@example.ru',
        )


class UcChatEventIdType(BaseModel):
    __root__: str = Field(
        ...,
        description='Уникальный идентификатор события чата',
        example="18446744073709551615",
        )

class Thumbnail(BaseModel):
    source: Optional[str] = Field(None, example='base64....')
    width: Optional[int] = Field(None, example=120)
    height: Optional[int] = Field(None, example=60)


class Size(BaseModel):
    size: Optional[str] = Field(None, example='s')
    width: Optional[int] = Field(None, example=120)
    height: Optional[int] = Field(None, example=60)


class ImageType(BaseModel):
    attachment_id: Optional[str] = Field(None, example='111111111111')
    width: Optional[int] = Field(None, example=1920)
    height: Optional[int] = Field(None, example=1080)
    thumbnail: Optional[Thumbnail] = None
    sizes: Optional[List[Size]] = None


class UcChatSuccessEventType(Enum):
    type = 'ucChatSuccessEventType'


class UcChatSuccessEvent(BaseModel):
    uuid: UcChatEventIdType
    ts: str = Field(
        ..., description='Время отправки события', example='2021-01-28T15:49:43.511Z'
        )
    type: UcChatSuccessEventType = Field(default=UcChatSuccessEventType.type, alias='$type', description='тип данных')


class UcChatFailedEventType(Enum):
    type = 'ucChatFailedEventType'


class UcChatFailedEvent(BaseModel):
    uuid: UcChatEventIdType
    reason: str = Field(
        ...,
        description='Внутренняя причина ошибки (в текстовом виде)',
        example='unsupported_version',
        )
    description: Optional[str] = Field(None, description='Текстовое описание ошибки')
    command: Optional[str] = Field(
        None,
        description='Внутренняя команда в uc.core в рамках выполнения которой произошла ошибка',
        )
    type: UcChatFailedEventType = Field(UcChatFailedEventType.type, alias='$type', description='тип данных')


class P2pChatIdType(BaseModel):
    __root__: str = Field(
        ...,
        description='Внутренний уникальный идентификатор P2P чата UC',
        example="10952",
        )


class LoginRequestType(Enum):
    type = 'loginRequestType'


class LoginRequest(BaseModel):
    login: constr(min_length=1) = Field(
        ..., description='Логин пользователя UC', example='vasya'
        )
    password: str = Field(
        ..., description='Пароль пользователя UC', example='vasya-password'
        )
    stay_signed_in: Optional[bool] = Field(
        True, description='Означает, нужно ли сохранять токен в БД'
        )
    type: LoginRequestType = Field(default=LoginRequestType.type, alias='$type', description='тип данных')


class GetUserInfoRequestType(Enum):
    type = 'getUserInfoRequestType'


class GetUserInfoRequest(BaseModel):
    user_id: Optional[UcUserIdType] = None
    external_user_id: Optional[UcExternalUserIdType] = None
    type: Optional[GetUserInfoRequestType] = Field(default=GetUserInfoRequestType.type, alias='$type',
                                                   description='тип данных')


class CreateP2PChatRequestType(Enum):
    type = 'createP2PChatRequestType'


class CreateP2PChatRequest(BaseModel):
    participant_id: UcUserIdType
    type: Optional[CreateP2PChatRequestType] = Field(default=CreateP2PChatRequestType.type, alias='$type',
                                                     description='тип данных')


class DeleteP2PChatRequestType(Enum):
    type = 'deleteP2PChatRequestType'


class DeleteP2PChatRequest(BaseModel):
    chat_id: P2pChatIdType
    type: DeleteP2PChatRequestType = Field(DeleteP2PChatRequestType.type, alias='$type', description='тип данных')


class UserInfoType(Enum):
    type = 'userInfoType'


class UserInfo(BaseModel):
    user_id: Optional[UcUserIdType] = None
    external_user_id: str = Field(
        None,
        description='Внешний идентификатор пользователя (e-mail, login...)',
        example='vasya@example.ru',
        )
    nickname: Optional[str] = Field(
        None, description='Псевдоним пользователя в рамках UC (ФИО)', example='Вася'
        )
    phone: Optional[str] = Field(
        None,
        description='Телефон пользователя, привязанный к UC',
        example='71234567890',
        )
    description: Optional[str] = Field(
        None,
        description='Какая то дополнительная информация о пользователе.',
        example='Коротко о себе...',
        )
    avatar_url: Optional[str] = Field(None, description='Ссылка на аватар')
    blocked: Optional[bool] = Field(
        None, description='Означает, заблокирован ли данный пользователь', example=False
        )
    last_activity_at: Optional[str] = Field(
        None,
        description='Время последней активности пользователя',
        example='2021-01-28T15:49:43.511Z',
        )
    created_at: Optional[str] = Field(
        None,
        description='Время создания пользователя',
        example='2021-01-28T15:49:43.511Z',
        )
    email: Optional[str] = Field(
        None,
        description='Адрес электронной почты пользователя',
        example='user@example.ru',
        )
    type: UserInfoType = Field(default=UserInfoType.type, alias='$type', description='тип данных')


class UserInfoNoRequired(UserInfo):
    user_id: conint(ge=1) = Field(
        None,
        description='Внутренний уникальный идентификатор пользователя UC',
        example=18446744073709551615,
        )
    external_user_id: str = Field(
        None,
        description='Внешний идентификатор пользователя (e-mail, login...)',
        example='vasya@example.ru',
        )


class P2pChatType(Enum):
    type = 'p2pChatType'


class Status(Enum):
    online = 'online'
    offline = 'offline'


class RealtimeStatusEventType(Enum):
    type = 'realtimeStatusEventType'


class RealtimeStatusEvent(BaseModel):
    status: Status = Field(..., description='Статус доступности realtime нотификаций')
    type: RealtimeStatusEventType = Field(RealtimeStatusEventType.type, alias='$type', description='тип данных')


class CreateUserType(Enum):
    type = 'createUserType'


class CreateUser(BaseModel):
    user_id: Optional[UcUserIdType] = None
    type: CreateUserType = Field(default=CreateUserType.type, alias='$type', description='тип данных')


class Type(Enum):
    TEXT = 'TEXT'
    IMAGE = 'IMAGE'
    STICKER = 'STICKER'
    AUDIO = 'AUDIO'
    VIDEO = 'VIDEO'
    FILE = 'FILE'
    LOCATION = 'LOCATION'
    CONTACT = 'CONTACT'
    FORWARD = 'FORWARD'
    CALENDAR_EVENT = 'CALENDAR_EVENT'
    NOTIFY = 'NOTIFY'
    CALL = 'CALL'
    GENERAL = 'GENERAL'


class Attachment(BaseModel):
    attachment_id: str = Field(
        ...,
        description='Уникальный идентификатор attachment',
        example='6f98739f-c362-1b9a-ab8b-52c21d50d2fb',
        )
    filename: constr(min_length=1) = Field(
        ..., description='Имя прикрепленного файла', example='protei.meetings.txt'
        )
    mimetype: Optional[constr(min_length=1)] = Field(description='Mime-тип прикрепленного файла', example='text/plain')
    size: conint(ge=0, le=1073741824) = Field(
        ..., description='Размер прикрепленного файла, в настоящий момент ограничен 1Gb'
        )

class Type4(Enum):
    ADD = 'ADD'
    DELETE = 'DELETE'


class GroupChatMemberPresenceNotifyType(Enum):
    type = 'groupChatMemberPresenceNotifyType'


class GroupChatMemberPresenceNotify(BaseModel):
    type: Type4
    user_id: UcUserIdType
    _type: GroupChatMemberPresenceNotifyType = Field(type=GroupChatMemberPresenceNotifyType.type,
                                                     alias='$type', description='тип данных')


class Type2(Enum):
    DELIVERED = 'DELIVERED'
    READ = 'READ'


class DeleteEventsResponseType(Enum):
    type = 'deleteEventsResponseType'


class DeleteEventsResponse(BaseModel):
    type: DeleteEventsResponseType = Field(default=DeleteEventsResponseType.type, alias='$type',
                                           description='тип данных')
    failed_events: List[UcChatEventIdType]


class ChatEventForwardType(Enum):
    type = 'chatEventForwardType'


class ChatEventForward(BaseModel):
    original_sender_id: UcUserIdType = Field(
        ...,
        description='Идентификатор пользователя, который изначально отправлял сообщение')
    type: ChatEventForwardType = Field(default=ChatEventForwardType.type, alias='$type', description='тип данных')


class EventOptionsType(BaseModel):
    correlation_id: Optional[UcChatEventIdType] = None
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
    events_group_id: Optional[str] = Field(
        None, description='Идентификатор для объединения в группу нескольких сообщений'
    )
    forward: Optional[ChatEventForward] = None
    images: Optional[List[ImageType]] = None
    attachments: Optional[List[Attachment]] = Field(
        None,
        description='Список идентификаторов attachment-ов, и их описаний, привязанных к данному сообщению.',
    )


class Event(BaseModel):
    event_id: UcChatEventIdType
    chat_id: ChatIdType
    chat_type: ChatType


class ChatEventShortTypeArray(BaseModel):
    events: List[Event]

class UuidEventType(BaseModel):
    __root__: str = Field(
        ...,
        description='Уникальный идентификатор события (в рамках конкретного клиента), выставляемый на стороне клиента.',
        example='unique_id_string',
    )


class ChatEventType(Enum):
    type = 'chatEventType'


class ChatEvent(BaseModel):
    event_id: Optional[UcChatEventIdType]
    uuid: str = Field(
        ...,
        description='Уникальный идентификатор события (в рамках конкретного клиента), выставляемый на стороне клиента.',
        example='unique_id_string',
    )
    sender_id: str = Field(
        ..., description='Идентификатор отправителя сообщения', example=2532
    )
    chat_id: ChatIdType
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
    options: Optional[EventOptionsType] = Field(
        None,
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


class ChatEventResponseType(Enum):
    type = 'chatEventResponseType'


class ChatEventResponse(BaseModel):
    success_events: Optional[List[UcChatSuccessEvent]] = Field(
        None, description='Список идентификаторов успешно переданных сообщений'
        )
    failed_events: Optional[List[UcChatFailedEvent]] = Field(
        None, description='Список идентификаторов не переданных сообщений'
        )
    type: ChatEventResponseType = Field(default=ChatEventResponseType.type, alias='$type', description='тип данных')


class UserAlreadyExistsErrorType(BaseModel):
    entity: Optional[List[UserInfoType]] = Field(None, example=['userInfoType'])


class P2pChat(BaseModel):
    chat_id: P2pChatIdType
    archived: Optional[bool] = Field(False, description='Архивация чата', example=False)
    blocked: Optional[bool] = Field(
        False, description='Указывает что данный чат заблокирован', example=False
    )
    participant_id: conint(ge=0) = Field(
        ...,
        description='Внутренний идентификатор пользователя, с которым установлен данный чат',
        example=100,
    )
    name: Optional[str] = Field(
        None, description='Название данного чата', example='Дмитрий Петров'
    )
    description: Optional[str] = Field(
        None,
        description='Текстовое описание данного чата',
        example='Чат с Дмитрием Петровым',
    )
    avatar_uri: Optional[str] = Field(
        None,
        description='Ссылка на аватар данного чата',
        example='/resources/SDGFLKGLKASD.jpg',
    )
    last_read_event_id: int = Field(
        ...,
        description='Идентификатор последнего прочитанного сообщения в данном чате (встречной стороной)',
        example=715,
    )
    last_delivered_event_id: int = Field(
        ...,
        description='Идентификатор последнего доставленного сообщения в данном чате (встречной стороне)',
        example=798,
    )
    unread_messages: Optional[conint(ge=0)] = Field(
        0,
        description='Количество непрочитанных сообщений в рамках данного чата',
        example=3,
    )
    owner_id: Optional[UcUserIdType] = None
    options: Optional[JsonOptionType] = None
    last_event: Optional[ChatEvent] = None
    events: Optional[List[ChatEvent]] = None
    pinned_events: Optional[List[UcChatEventIdType]] = Field(
        None, description='Закрепленные сообщения в чате'
    )
    draft: Optional[ChatEventDraft] = Field(
        None,
        description='Черновик для данного чата. Заполняется только в случае получения снапшота.',
    )
    user_mentions: Optional[List[UcChatEventIdType]] = Field(
        None,
        description='Список идентификаторов непрочитанных event-ов, в которых было упоминание текущего пользователя',
    )
    type: P2pChatType = Field(default=P2pChatType.type, alias='$type', description='тип данных')


class MarkP2PChatEventType(Enum):
    type = 'markP2PChatEventType'


class MarkP2PChatEvent(BaseModel):
    chat_id: P2pChatIdType
    event_id: UcChatEventIdType
    chat_type: ChatType
    type: MarkP2PChatEventType = Field(default=MarkP2PChatEventType.type, alias='$type', description='тип данных')


class ChatEventNotifyType(Enum):
    type = 'chatEventNotifyType'


class ChatTypingEventNotifyType(Enum):
    type = 'chatTypingEventNotifyType'


class ChatTypingEventNotify(BaseModel):
    chat_id: P2pChatIdType
    chat_type: ChatType
    sender_id: Optional[UcUserIdType]
    timeout: Optional[int] = Field(
        3000,
        description='Таймаут в миллисекундах, который клиент передает на другого клиента, для указания сколько'
                    ' времени нужно показывать сообщение о наборе текста. Нужно для того, чтобы перестать показывать'
                    ' сообщение о наборе текста, если сообщение (остановки) потерялось.',
        example=5000,
        )
    type: Literal['START', 'STOP']
    options: Optional[JsonStringType] = None
    type_1: ChatTypingEventNotifyType = Field(ChatTypingEventNotifyType.type, alias='$type', description='тип данных')


class ChatEventNotify(BaseModel):
    chat_id: P2pChatIdType
    begin_event_id: Optional[UcChatEventIdType] = None
    end_event_id: UcChatEventIdType
    notified_at: str = Field(
        ...,
        description='Время относящееся к событию',
        example='2021-01-28T15:51:43.511Z',
        )
    type: Type2 = Field(
        ...,
        description='Тип нотификации: <br/>DELIVERED - указанный диапазон событий был доставлен;'
                    ' <br/>READ - указанный диапазон событий был прочитан;',
        )
    sender_id: UcUserIdType
    options: Optional[JsonStringType] = None
    type_1: ChatEventNotifyType = Field(default=ChatEventNotifyType.type, alias='$type', description='тип данных')


class ChatDeleteEventNotifyType(Enum):
    type = 'chatDeleteEventNotifyType'


class ChatDeleteEventNotify(BaseModel):
    chat_id: P2pChatIdType
    events_id: List[UcChatEventIdType]
    options: Optional[JsonStringType] = None
    type: ChatDeleteEventNotifyType = Field(default=ChatDeleteEventNotifyType.type, alias='$type',
                                            description='тип данных')


class JsonOptionType(BaseModel):
    pass


class ChatNotifyType(Enum):
    type = 'chatNotifyType'


class SettingsType(Enum):
    type = 'settingsType'


class Theme(Enum):
    theme = 'dark'


class Lang(Enum):
    lang_ru = 'ru'
    lang_en = 'en'
    lang = 'lang'


class SettingsDeep(BaseModel):
    deep_prop_1: Theme = Field(default=Theme.theme, alias='uc/api/theme')
    deep_prop_2: Lang = Field(default=Lang.lang_ru, alias='uc/lang/ru')
    deep_prop_3: Lang = Field(default=Lang.lang_en, alias='uc/lang/en')
    deep_prop_4: Lang = Field(default=Lang.lang, alias='uc/lang')

    type: SettingsType = Field(default=SettingsType.type, alias='$type', description='тип данных')


class Settings(BaseModel):
    str_prop: Optional[str] = None
    int_prop: Optional[int] = None
    json_prop: Optional[JsonStringType] = None

    type: SettingsType = Field(default=SettingsType.type, alias='$type', description='тип данных')


class SettingsRequestType(Enum):
    type = 'settingsRequestType'


class SettingsRequest(BaseModel):
    type: SettingsRequestType = Field(default=SettingsRequestType.type, alias='$type', description='тип данных')
    keys: List[str] = Field(
        ...,
        example=[
            'settingKey',
            'settingKey2/settingSubKey',
            'settingKey2/settingSubKey2/',
            ],
        )


class Severity(Enum):
    INFO = 'INFO'
    DEBUG = 'DEBUG'
    TRACE = 'TRACE'
    WARNING = 'WARNING'
    ERROR = 'ERROR'


class LogRequestType(Enum):
    type = 'logRequestType'


class LogRequest(BaseModel):
    severity: Severity = Field(..., description='Уровень логирования', example='INFO')
    string: str = Field(
        ..., description='Строка логирования', example='Какая-то информация...'
        )
    type: LogRequestType = Field(LogRequestType.type, alias='$type', description='тип данных')


class ChatEventChangeType(Enum):
    type = 'chatEventChangeType'


class ChatEventChange(BaseModel):
    event_id: UcUserIdType
    plaintext: Optional[str] = Field(
        None,
        description='Строковое представление сообщения (отформатированное текстовое сообщение, название файла,'
                    ' подпись к изображению и т.п.)',
        example='Текст сообщения...',
        )
    chat_id: Optional[ChatIdType] = None
    chat_type: Optional[ChatType] = None
    urls: Optional[List[str]] = Field(
        None,
        description='Список ссылок, присутствующих в данном сообщении',
        example=['https://www.example.ru/path1', 'https://www.example.ru/path2'],
        )
    mentions: Optional[List[UcUserIdType]] = Field(
        None,
        description='Список идентификаторов пользователей, упомянутых в данном сообщении',
        example=[789456123654, 123654789987],
        )
    type: ChatEventChangeType = Field(ChatEventChangeType.type, alias='$type', description='тип данных')


class ContactSearchRequestType(Enum):
    type = 'contactSearchRequestType'


class ContactSearchRequest(BaseModel):
    search: Optional[str] = Field(
        None,
        description='Строка поиска (поиск по любому из полей контакта, по подстроке, включая номер телефона.'
                    ' Регистронезависимый поиск.)',
        example='петр',
        )
    page_size: Optional[conint(ge=1)] = Field(
        50,
        description='Количество возвращаемых записей в запросе поиска (технически, в зависимости от backend-а'
                    ' возможна ситуация, когда на запрос вернется большее количество записей)',
        example=50,
        )
    search_timeout: Optional[conint(ge=250)] = Field(
        5000,
        description='Максимальное время выполнения запроса (в миллисекундах). В случае, если время запроса'
                    ' будет превышать заданное значение, то Swagger_API вернет только то количество записей,'
                    ' что удалось найти к текущему моменту.',
        example=2500,
        )
    tag: Optional[str] = Field(
        None,
        description="Тег поиска. Тег используется в случае 'прокрутки', при запросе второй страницы и далее."
                    " В случае, если в запросе задан тег, остальные параметры запроса <b>игнорируются!</b>",
        example='UHJvdGVpIE5TSw==',
        )
    type: ContactSearchRequestType = Field(ContactSearchRequestType.type, alias='$type', description='тип данных')


class DestinationChat(BaseModel):
    chat_type: ChatType
    chat_id: ChatIdType


class ChatEventForwardRequestType(Enum):
    type = 'chatEventForwardRequestType'


class ChatEventForwardRequest(BaseModel):
    destination_chats: List[DestinationChat] = Field(..., description='Массив чатов куда нужно переслать сообщение')
    event_ids: List[UcChatEventIdType] = Field(..., description='Массив идентификаторов сообщений, которые нужно '
                                                                'переслать')
    additional_message: Optional[str] = Field(None, description='Дополнительное сообщение. Из данного текста будет '
                                                                'сформировано сообщение chatEventType и отправлено в '
                                                                'каждый из destination_chats. Сообщение которое будет '
                                                                'отправлено, будет содержать в опциях тот же '
                                                                'events_group_id, что и все остальные сообщения, '
                                                                'относящиеся к конкретной пересылке.',
                                              example='Какой-то дополнительный текст...',)
    silent: Optional[bool]
    type: ChatEventForwardRequestType = Field(ChatEventForwardRequestType.type,
                                              alias='$type', description='тип данных')


class NotForwardedItem(BaseModel):
    event_id: UcChatEventIdType
    chat_ids: List[ChatIdType] = Field(..., description='Массив чатов в которые не удалось переслать сообщения')


class ChatEventForwardResponseType(Enum):
    type = 'chatEventForwardResponseType'


class ChatEventForwardResponse(BaseModel):
    forward_group_id: str = Field(..., description='Идентификатор для объединения в группу нескольких пересланных '
                                                   'сообщений. Данный параметр будет приходит в поле '
                                                   'ChatEventType.options.events_group_id',)
    not_forwarded: Optional[List[NotForwardedItem]] = Field(
        None, description='Сообщения которые не удалось переслать')
    type: ChatEventForwardResponseType = Field(default=ChatEventForwardResponseType.type, alias='$type',
                                               description='тип данных')


class Gender(Enum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    NOT_SPECIFIED = 'NOT_SPECIFIED'


class ContactNumberType(Enum):
    type = 'contactNumberType'


class ContactNumber(BaseModel):
    id: int = Field(
        ..., description='Внутренний идентификатор номер контакта', example=40
        )
    numberType: Optional[str] = Field(None, description='Тип номера', example='WORK')
    phone: str = Field(..., description='Номер телефона', example='79675963156')
    options: Optional[JsonOptionType] = None
    type: ContactNumberType = Field(ContactNumberType, alias='$type', description='тип данных')


class TypeContact(Enum):
    PRIVATE = 'PRIVATE'
    PUBLIC = 'PUBLIC'


class ContactType(Enum):
    type = 'contactType'


class Contact(BaseModel):
    id: str = Field(..., description='Внутренний идентификатор контакта', example='40')
    type: Optional[TypeContact] = Field(
        None, description='Тип контакта (личный / корпоративный)', example='PUBLIC'
        )
    first_name: Optional[str] = Field(None, description='Имя', example='Петр')
    middle_name: Optional[str] = Field(None, description='Отчество', example='Петрович')
    last_name: Optional[str] = Field(None, description='Фамилия', example='Петров')
    organization: Optional[str] = Field(
        None, description='Организация', example='Протей'
        )
    gender: Optional[Gender] = Field(
        None, description='Организация', example='NOT_SPECIFIED'
        )
    position: Optional[str] = Field(None, description='Должность', example='инженер')
    subdivision: Optional[str] = Field(
        None, description='Отдел', example='Лаборатория №7'
        )
    uc_user_id: Optional[UcUserIdType] = None
    numbers: Optional[List[ContactNumber]] = Field(
        None, description='Номера телефона'
        )
    options: Optional[JsonOptionType] = None
    type_1: ContactType = Field(ContactType.type, alias='$type', description='тип данных')


class ContactSearchResponseType(Enum):
    type = 'contactSearchResponseType'


class ContactSearchResponse(BaseModel):
    tag: Optional[str] = Field(
        None,
        description='Тег для продолжения поиска (в случае использования паджинации).'
                    ' Если тег не вернулся, значит под заданные критерии поиска больше нет контактов.',
        example='UHJvdGVpIE5TSw==',
        )
    contacts: List[Contact] = Field(..., description='Список контактов')
    type: ContactSearchResponseType = Field(ContactSearchResponseType.type, alias='$type', description='тип данных')


class GenerateWSTokenType(Enum):
    type = 'generateWSTokenType'


class GenerateWSToken(BaseModel):
    token: str = Field(..., description='Одноразовый токен для установления ws соединения',
                       example='g2gCZ2QADW5vbm9kZUBub2hvc3QAAABOAAAAAABrAAdVQyBOU0su')
    type: GenerateWSTokenType = Field(GenerateWSTokenType.type, alias='$type', description='тип данных')


class CreateGroupRequestType(Enum):
    type = 'createGroupRequestType'


class GroupNameType(BaseModel):
    __root__: str = Field(
        ..., description='Название группы', example='Группа разработки'
        )


class GroupDescriptionType(BaseModel):
    __root__: str = Field(
        ..., description='Описание группы', example='Группа разработки'
        )


class MembersType(BaseModel):
    __root__: List[UcUserIdType] = Field(..., description='Список участников')


class AvatarUrlType(BaseModel):
    __root__: str = Field(
        ...,
        description='URL аватара, также поддерживается data-url',
        example='uc-attach://unique_attachment_id',
    )


class CreateGroupRequest(BaseModel):
    name: GroupNameType
    description: Optional[GroupDescriptionType] = None
    members: Optional[MembersType] = None
    avatar_url: Optional[AvatarUrlType] = None
    type: Optional[CreateGroupRequestType] = Field(CreateGroupRequestType.type, alias='$type', description='тип данных')


class ChatGroupCreateResponseType(Enum):
    type = 'chatGroupCreateResponseType'


class ChatGroupCreateResponse(BaseModel):
    group_id: ChatIdType
    type: ChatGroupCreateResponseType = Field(ChatGroupCreateResponseType.type, alias='$type', description='тип данных')


class ChatGroupInfoResponseType(Enum):
    type = 'chatGroupInfoResponseType'


class ChatGroupInfoResponse(BaseModel):
    type: ChatGroupInfoResponseType = Field(ChatGroupInfoResponseType.type, alias='$type', description='тип данных')
    group_id: Optional[ChatIdType] = None
    name: Optional[GroupNameType] = None
    description: Optional[GroupDescriptionType] = None
    owner_id: Optional[UcUserIdType] = None
    members: Optional[MembersType] = None
    creation_datetime: Optional[str] = Field(
        None,
        description='Время создания группового чата',
        example='2021-05-14T10:41:48.511Z',
        )


class GroupChatType(Enum):
    type = 'groupChatType'


class GroupChat(BaseModel):
    chat_id: ChatIdType
    archived: Optional[bool] = Field(False, description='Архивация чата', example=False)
    blocked: Optional[bool] = Field(
        False, description='Указывает что данная группа заблокирована', example=False
    )
    deleted: Optional[bool] = Field(
        False, description='Указывает что данная группа удалена', example=False
        )
    members: Optional[MembersType] = None
    name: Optional[str] = Field(
        None, description='Название данного чата', example='Группа разработки'
    )
    description: Optional[str] = Field(
        None,
        description='Текстовое описание данного чата',
        example='Чат группы разработки',
    )
    avatar_uri: Optional[str] = Field(
        None,
        description='Ссылка на аватар данного чата',
        example='/resources/SDGFLKGLKASD.jpg',
    )
    last_read_event_id: str = Field(
        ...,
        description='Идентификатор последнего прочитанного сообщения в данном чате (встречной стороной)',
        example=715,
    )
    last_delivered_event_id: str = Field(
        ...,
        description='Идентификатор последнего доставленного сообщения в данном чате (встречной стороне)',
        example=798,
    )
    unread_messages: Optional[conint(ge=0)] = Field(
        0,
        description='Количество непрочитанных сообщений в рамках данного чата',
        example=3,
    )
    owner_id: Optional[UcUserIdType] = None
    options: Optional[JsonOptionType] = None
    last_event: Optional[ChatEvent] = None
    events: Optional[List[ChatEvent]] = None
    pinned_events: Optional[List[UcChatEventIdType]] = Field(
        None, description='Закрепленные сообщения в чате'
    )
    draft: Optional[ChatEventDraft] = Field(
        None,
        description='Черновик для данного чата. Заполняется только в случае получения снапшота.',
    )
    user_mentions: Optional[List[UcChatEventIdType]] = Field(
        None,
        description='Список идентификаторов непрочитанных event-ов, в которых было упоминание текущего пользователя',
    )
    type: GroupChatType = Field(GroupChatType.type, alias='$type', description='тип данных')


class Values(BaseModel):
    muted: Optional[bool] = Field(
        None, description='Говорит о том, что нотификации в чате отключены'
    )


class _Type4(Enum):
    updateOptionsType = 'updateOptionsType'


class UpdateOptionsType(BaseModel):
    values: Optional[Values] = None
    _type: Optional[_Type4] = Field(None, alias='$type', description='тип данных')


class ChatNotify(BaseModel):
    chat_id: P2pChatIdType
    chat_type: ChatType
    type_1: StatusChat = Field(..., alias='type', description='Тип нотификации')
    options: Optional[Union[GroupChat, P2pChat, UpdateOptionsType, JsonOptionType]] = None
    type: ChatNotifyType = Field(ChatNotifyType.type, alias='$type', description='тип данных')


class DeleteGroupChatRequestType(Enum):
    type = 'deleteGroupChatRequestType'


class DeleteGroupChatRequest(BaseModel):
    chat_id: ChatIdType
    type: DeleteGroupChatRequestType = Field(DeleteGroupChatRequestType.type, alias='$type',
                                             description='тип данных')


class ChatGroupMemberAddRequestType(Enum):
    type = 'chatGroupMemberAddRequestType'


class ChatGroupMemberAddRequest(BaseModel):
    chat_id: ChatIdType
    type: ChatGroupMemberAddRequestType = Field(ChatGroupMemberAddRequestType.type, alias='$type',
                                                description='тип данных')
    members: MembersType


class ChatGroupMemberAddResponseType(Enum):
    type = 'chatGroupMemberAddResponseType'


class ChatGroupMemberAddResponse(BaseModel):
    type: ChatGroupMemberAddResponseType = Field(ChatGroupMemberAddResponseType.type, alias='$type',
                                                 description='тип данных')
    not_added: Optional[MembersType] = None


class ChatGroupMemberRemoveRequestType(Enum):
    type = 'chatGroupMemberRemoveRequestType'


class ChatGroupMemberRemoveRequest(BaseModel):
    chat_id: ChatIdType
    type: ChatGroupMemberRemoveRequestType = Field(ChatGroupMemberRemoveRequestType.type, alias='$type',
                                                   description='Тип данных')
    members: MembersType


class ChatGroupMemberRemoveResponseType(Enum):
    type = 'chatGroupMemberRemoveResponseType'


class ChatGroupMemberRemoveResponse(BaseModel):
    type: ChatGroupMemberRemoveResponseType = Field(ChatGroupMemberRemoveResponseType.type, alias='$type',
                                                    description='тип данных')
    not_removed: Optional[MembersType] = None


class DeleteMembersFromGroupNotifyType(Enum):
    type = 'deleteMembersFromGroupNotifyType'


class DeleteMembersFromGroupNotify(BaseModel):
    chat_id: ChatIdType
    members: List[UcUserIdType]
    type: DeleteMembersFromGroupNotifyType = Field(DeleteMembersFromGroupNotifyType.type, alias='$type',
                                                   description='тип данных')


class AddMembersToGroupNotifyType(Enum):
    type = 'addMembersToGroupNotifyType'


class AddMembersToGroupNotify(BaseModel):
    chat_id: ChatIdType
    members: List[UcUserIdType]
    type: AddMembersToGroupNotifyType = Field(AddMembersToGroupNotifyType.type, alias='$type', description='тип данных')


# Вспомогательные модели для Call

class CallIdType(BaseModel):
    __root__: constr(min_length=1) = Field(
        ...,
        description='Идентификатор вызова',
        example='f973769f-c4f6-44ce-984e-9fbf628beb7f',
        )


class CallUriType(BaseModel):
    __root__: constr(
        regex=r'^(sips?:[^@]+@[^@]+|tel:\+?[0-9ABCD\*#]+|uc-user:\d{1,19})$',
        min_length=1,
        ) = Field(
        ...,
        description='SIP-URI, TEL-URI или UC-URI',
        example='sip:Bob@192.168.100.13:6050 | tel:+79039110001 | uc-user:725',
        )


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


# Модели для реквестов Call их ответы


class CallMakeRequestType(Enum):
    type = 'callMakeRequestType'


class CallMakeRequest(BaseModel):
    call_id: Optional[CallIdType] = None
    uri: CallUriType
    sdp: str = Field(..., description='Offer SDP вызывающей стороны', example='v=0...')
    type: CallMakeRequestType = Field(default=CallMakeRequestType.type, alias='$type', description='тип данных')


class CallAnswerRequestType(Enum):
    type = 'callAnswerRequestType'


class CallAnswerRequest(BaseModel):
    call_id: CallIdType
    sdp: str = Field(..., description='Answer SDP вызываемой стороны', example='v=0...')
    type: CallAnswerRequestType = Field(default=CallAnswerRequestType.type, alias='$type', description='тип данных')


class CallSendInfoRequestType(Enum):
    type = 'callSendInfoRequestType'


class CallSendInfoRequest(BaseModel):
    call_id: CallIdType
    type: str = Field(
        ...,
        description='Тип отправляемых данных (имеет формат mimetype)',
        example='message/ice',
        )
    content: str = Field(
        ...,
        description='Отправляемые данные',
        example='a=candidate:4234997325 1 udp 2043278322 192.168.23.87 44323 typ host',
        )
    type_1: CallSendInfoRequestType = Field(default=CallSendInfoRequestType.type, alias='$type', description='тип '
                                                                                                             'данных')


class CallReleaseRequestType(Enum):
    type = 'callReleaseRequestType'


class CallReleaseRequest(BaseModel):
    call_id: CallIdType
    type: CallReleaseRequestType = Field(default=CallReleaseRequestType.type, alias='$type', description='тип '
                                                                                                         'данных')


class CallUpdateRequestType(Enum):
    type = 'callUpdateRequestType'


class CallUpdateRequest(BaseModel):
    call_id: CallIdType
    sdp: str = Field(..., description='Offer SDP вызывающей стороны', example='v=0...')
    type: CallUpdateRequestType = Field(default=CallUpdateRequestType.type, alias='$type', description='тип данных')


class CallUpdateAnswerRequestType(Enum):
    type = 'callUpdateAnswerRequestType'


class CallUpdateAnswerRequest(BaseModel):
    call_id: CallIdType
    sdp: str = Field(..., description='Answer SDP вызываемой стороны', example='v=0...')
    type: CallUpdateAnswerRequestType = Field(default=CallUpdateAnswerRequestType.type, alias='$type',
                                              description='тип данных')


class CallUpdateFailedRequestType(Enum):
    type = 'callUpdateFailedRequestType'


class CallUpdateFailedRequest(BaseModel):
    call_id: CallIdType
    code: int = Field(..., description="Код ответа", example=425)
    reason: str = Field(..., description="Причина", example="Unsupported Media Type")
    type: CallUpdateFailedRequestType = Field(default=CallUpdateFailedRequestType.type, alias='$type',
                                              description='тип данных')


class CallMediaStatusType(Enum):
    type = 'callMediaStatusType'


class CallMediaStatus(BaseModel):
    content: str = Field(..., description="", example='microphone')
    type: str = Field(..., description="", example='video')
    mid: int = Field(..., description="", example=1)
    description: str = Field(..., description="Описание", example="Дополнительный микрофон на зал")
    type_1: CallMediaStatusType = Field(default=CallMediaStatusType.type, alias='$type',
                                        description='тип данных')


class CallMediaStatusUpdatedRequestType(Enum):
    type = 'callMediaStatusUpdatedRequestType'


class CallMediaStatusUpdatedRequest(BaseModel):
    call_id: CallIdType
    content: List[CallMediaStatusType]
    type: CallMediaStatusUpdatedRequestType = Field(default=CallMediaStatusUpdatedRequestType.type, alias='$type',
                                                    description='тип данных')


# Модели для евентов Call

class ConferenceIdType(BaseModel):
    __root__: str = Field(
        ..., description='Идентификатор конференции', example='134095221'
    )


class ConferenceAbonentIdType(BaseModel):
    __root__: conint(ge=0) = Field(
        ..., description='Идентификатор абонентов в конференции', example=5
    )


class SideType(Enum):
    ORIGINATION = 'ORIGINATION'
    TERMINATION = 'TERMINATION'
    SYSTEM = 'SYSTEM'


class _Type75(Enum):
    vcsCallInfoType = 'vcsCallInfoType'


class VcsCallInfoType(BaseModel):
    conference_id: ConferenceIdType
    member_id: ConferenceAbonentIdType
    _type: _Type75 = Field(..., alias='$type', description='тип данных')


class CallSetupEventType(Enum):
    type = 'callSetupEventType'


class CallSetupEvent(BaseModel):
    callee_display_name: Optional[str] = Field(
        None, description='Отображаемое имя встречной стороны', example='User B'
        )
    sdp: Optional[SdpType] = None
    side: SideType
    vcs_info: Optional[VcsCallInfoType] = None
    uri: Optional[CallUriType] = None
    type: CallSetupEventType = Field(default=CallSetupEventType.type, alias='$type', description='тип данных')


class CallAlertingEventType(Enum):
    type = 'callAlertingEventType'


class CallAlertingEvent(BaseModel):
    callee_display_name: Optional[str] = Field(
        None, description='Отображаемое имя встречной стороны', example='User B'
        )
    sdp: Optional[SdpType] = None
    type: CallAlertingEventType = Field(default=CallAlertingEventType.type, alias='$type', description='тип данных')


class CallProgressEventType(Enum):
    type = 'callProgressEventType'


class CallProgressEvent(BaseModel):
    callee_display_name: Optional[str] = Field(
        None, description='Отображаемое имя встречной стороны', example='User B'
        )
    sdp: Optional[SdpType] = None
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
    sdp: Optional[SdpType] = None
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


class CallMediaUpdatedEvent(BaseModel):
    side: Side = Field(
        ..., description='сторона вызова, которая прислала данную нотификацию'
        )
    content: List[CallMediaStatusType]
    type: CallMediaUpdatedEventType = Field(default=CallMediaUpdatedEventType.type, alias='$type', description='тип '
                                                                                                               'данных')


class CallStatusEventType(Enum):
    type = 'callStatusEventType'


class CallStatusEvent(BaseModel):
    o_user_id: UcUserIdType
    o_display_name: Optional[UcUserIdType] = None
    o_sdp: SdpType
    t_user_id: Optional[UcUserIdType] = None
    t_display_name: Optional[UcUserIdType] = None
    t_sdp: Optional[SdpType] = None
    start_time: str = Field(
        ..., description='Время начала вызова', example='2021-05-14T10:41:43.511Z'
        )
    answer_time: Optional[str] = Field(
        None,
        description='Время ответа на входящий вызов',
        example='2021-05-14T10:41:48.511Z',
        )
    phase: Phase = Field(..., description='Текущая фаза вызова', example='ANSWER')
    type: CallStatusEventType = Field(default=CallStatusEventType.type, alias='$type', description='тип данных')


class CallEventType(Enum):
    type = "callEventType"


class CallEvent(BaseModel):
    call_id: CallIdType
    owner_id: Optional[UcUserIdType] = None
    participant_id: Optional[UcUserIdType] = None
    chat_id: Optional[ChatIdType] = None
    chat_type: Optional[ChatType] = None
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
                ] = None
    type: CallEventType = Field(default=CallEventType.type, alias='$type', description='тип данных')


# модели ответов Call

class CallMakeResponseType(Enum):
    type = "callMakeResponseType"


class CallMakeResponse(BaseModel):
    call_id: CallIdType
    type: CallMakeResponseType = Field(default=CallMakeResponseType.type, alias='$type', description='тип данных')


class UnreadMessages(BaseModel):
    unread_messages: Optional[int]


class Chats(BaseModel):
    chats: Optional[P2pChat]


class ActiveCallType(Enum):
    type = 'activeCallType'


class ActiveCall(BaseModel):
    call_id: CallIdType
    chat_id: ChatIdType
    owner_id: UcUserIdType
    participant_id: Optional[UcUserIdType] = None
    start_time: str = Field(
        ..., description='Время начала вызова', example='2021-05-14T10:41:43.511Z'
        )
    phase: PhaseType
    sdp: Optional[SdpType] = None
    ice: Optional[List[str]] = Field(
        None,
        description='Массив с ICE кандидатами для данного вызова (в предответном состоянии)',
        example=[
            '{"candidate":"candidate:3720739803 1 tcp 1518214911 172.18.242.152 9 typ host tcptype active generation '
            '0 ufrag 3WT5 network-id 2","sdpMid":"0","sdpMLineIndex":0}',
            '{"candidate":"candidate:3720739803 1 tcp 1518214911 172.18.242.152 9 typ host tcptype active generation '
            '0 ufrag 3WT5 network-id 2","sdpMid":"0","sdpMLineIndex":1}',
            ],
        )
    _type: ActiveCallType = Field(..., alias='$type', description='тип данных')
    side: Side
    callee_display_name: Optional[str] = Field(
        None, description='Отображаемое имя встречной стороны', example='User B'
        )





class ChatEventDraftType(Enum):
    type = 'chatEventDraftType'


class ChatEventDraft(BaseModel):
    user_id: Optional[UcUserIdType] = None
    chat_id: ChatIdType
    chat_type: ChatType
    ts: Optional[str] = Field(
        None, description='Время отправки события', example='2021-01-28T15:49:43.511Z'
                            )
    plaintext: Optional[str] = Field(
        None,
        description='Строковое представление сообщения',
        example='Текст сообщения...',
                                    )
    _type: ChatEventDraftType = Field(ChatEventDraftType.type, alias='$type', description='тип данных')


class ChatEventDraftNotifyType(Enum):
    type = 'chatEventDraftNotifyType'


class Type5(Enum):
    SAVE = 'SAVE'
    DELETE = 'DELETE'


class ChatEventDraftNotify(BaseModel):
    type: Type5
    draft: ChatEventDraft
    _type: ChatEventDraftNotifyType = Field(ChatEventDraftNotifyType.type, alias='$type', description='тип данных')


class ChatEventSearchType(Enum):
    type = 'chatEventSearchType'


class ChatEventSearch(BaseModel):
    events_count: Optional[int] = Field(
        50, description='Количество сообщений, которое нужно найти.'
    )
    search_string: Optional[str] = Field(
        None,
        description='Строка поиска. Важно передавать так, как ввел пользователь. При вводе строки поиска в двойных '
                    'ковычках, будут найдены все сообщения, которые содержат такую подстроку.',
        example='Привет, как дела? "Пойдешь гулять?"',
    )
    chat_id: Optional[ChatIdType] = Field(
        None,
        description='Заполняется только в том случае, когда надо искать в определенном чате. Является обязательным, '
                    'если заполняется chat_type.',
    )
    chat_type: Optional[ChatType] = Field(
        None,
        description='Заполняется только в том случае, когда надо искать в определенном чате. Является обязательным, '
                    'если заполняется chat_id',
    )
    get_events_count_at_chat: Optional[bool] = Field(
        False,
        description='флаг указывающий, что первым сообщением необходимо отправить общее количество найденных сообщений (параметр анализируется только для поиска в чате)',
    )
    event_id_only: Optional[bool] = Field(
        False,
        description='флаг указывающий, что в результате поиска необходимо возвращать только идентификаторы event-ов (chat_id + event_id)',
    )
    _type: Optional[ChatEventSearchType] = Field(ChatEventSearchType.type, alias='$type', description='тип данных')


class ChatEventControlSearchType(Enum):
    type = 'chatEventControlSearchType'


class ChatEventControlSearch(BaseModel):
    search_id: Optional[str] = Field(
        None,
        description='Идентификатор поиска который создается при вызове команды /chat/event/search',
        example='f7eb430a-358f-4023-9939-c9360cd06ec6',
    )
    _type: Optional[ChatEventControlSearchType] = Field(ChatEventControlSearchType.type, alias='$type',
                                                        description='тип данных')


class ChatEventSearchNotifyType(Enum):
    type = 'chatEventSearchNotifyType'


class _Type81(Enum):
    searchStopNotifyType = 'searchStopNotifyType'


class SearchStopNotifyType(BaseModel):
    reason: str = Field(
        None,
        description='Причина остановки поиска. Если причина остановки SEARCH_COMPLETE, то это значит что в базе больше нет данных для поиска. Во всех остальных случаях вернется ошибка, из-за которой был приостановлен поиск.',
        example='SEARCH_COMPLETE',
    )
    _type: _Type81 = Field(None, alias='$type', description='тип данных')


class Type10(Enum):
    EVENTS = 'EVENTS'
    WAIT_CONTINUE = 'WAIT_CONTINUE'
    STOP = 'STOP'


class ChatEventSearchNotifyType(Enum):
    type = 'chatEventSearchNotifyType'


class ChatEventTypeArray(BaseModel):
    events: List[ChatEvent]


class ChatEventSearchNotify(BaseModel):
    search_id: str = Field(
        ...,
        description='Идентификатор поиска который создается при вызове команды /chat/event/search',
        example='f7eb430a-358f-4023-9939-c9360cd06ec6',
    )
    type: Type10
    options: Optional[Union[ChatEventTypeArray, ChatEventShortTypeArray, SearchStopNotifyType]]
    _type: ChatEventSearchNotifyType = Field(ChatEventSearchNotifyType.type, alias='$type', description='тип данных')


class WebsocketIsAliveRequestType(Enum):
    type = 'websocketIsAliveRequestType'


class WebsocketIsAliveRequest(BaseModel):
    token: str = Field(
        ...,
        description='ws токен который необходимо проверить',
        example='eyJQaWQiOnsiQWRkcmVzcyI6Im5vbmhvc3QiLCJJZCI6Ikh0dHBVc2VyU2Vzc2lvbk5hbWUvcm91dGVyLyQxVCJ9LCJEaWQiOiI'
                '2NTYyNzM5Zi04ZjAxLTQwODctYjYzZC01NjE2MjY5N2JlOTAiLCJUb2tlbiI6Ill6WTVZbUV3TTJRdFpXUXhNUzAwTnpRM0xXST'
                'JNVE10WkdNNU16Um1OelUxWWpGbSJ9Cg==',
    )
    _type: WebsocketIsAliveRequestType = Field(WebsocketIsAliveRequestType.type, alias='$type',description='тип данных')


class UsersIdsType(BaseModel):
    __root__: List[UcUserIdType] = Field(..., description='Список пользователей')


class UserSubscribeRequestType(Enum):
    type = 'userSubscribeRequestType'


class Payload10(BaseModel):
    _type: UserSubscribeRequestType = Field(UserSubscribeRequestType.type, alias='$type', description='тип данных')
    users: UsersIdsType


class UserSubscribeRequest(BaseModel):
    _type: UserSubscribeRequestType = Field(UserSubscribeRequestType.type, alias='$type', description='тип данных')
    users: List[UcUserIdType] = Field(..., description='Список пользователей')


class UserSubscribeResponseType(Enum):
    type = 'userSubscribeResponseType'


class UserScopeType(Enum):
    UC = 'UC'
    SIP = 'SIP'
    MCPTT = 'MCPTT'
    ALL = 'ALL'


class SeqType(BaseModel):
    __root__: conint(ge=1) = Field(
        ..., description='Порядковый номер смены статуса', example=12
    )


class UserStatusValueType(Enum):
    ONLINE = 'ONLINE'
    BUSY = 'BUSY'
    AWAY = 'AWAY'
    OFFLINE = 'OFFLINE'


class UserStatusType(Enum):
    type = 'userStatusType'


class UserStatus(BaseModel):
    user_id: UcUserIdType
    scope: UserScopeType
    seq: SeqType
    status: UserStatusValueType
    timestamp: str = Field(..., description='Время активности', example='2021-01-28T15:51:43.511Z')
    _type: UserStatusType = Field(UserStatusType.type, alias='$type', description='тип данных')


class Payload12(BaseModel):
    _type: UserSubscribeResponseType = Field(UserSubscribeResponseType.type, alias='$type', description='тип данных')
    statuses: Optional[List[UserStatus]] = None


class UserSubscribeResponse(BaseModel):
    payload: Payload12


class UserStatusNotifyType(Enum):
    type = 'userStatusNotifyType'


class UserStatusNotify(BaseModel):
    statuses: List[UserStatus]
    type: UserStatusNotifyType = Field(UserStatusNotifyType.type, alias='$type', description='тип данных')


class UserUnsubscribeRequestType(Enum):
    type = 'userUnsubscribeRequestType'


class UserUnsubscribeRequest(BaseModel):
    users: UsersIdsType
    type: UserUnsubscribeRequestType = Field(UserUnsubscribeRequestType.type, alias='$type', description='тип данных')


class UserStatusSetRequestType(Enum):
    type = 'userStatusSetRequestType'


class UserStatusSetRequest(BaseModel):
    type: UserStatusSetRequestType = Field(UserStatusSetRequestType.type, alias='$type', description='тип данных')
    status: UserStatusValueType


class UserStatusGetRequestType(Enum):
    type = 'userStatusGetRequestType'


class UserStatusGetRequest(BaseModel):
    users: UsersIdsType
    type: UserStatusGetRequestType = Field(UserStatusGetRequestType.type, alias='$type', description='тип данных')


class UserSnapshotResponse(BaseModel):
    unread_messages: conint(ge=0) = Field(
        ..., description='Общее количество непрочитанных сообщений во всех чатах'
    )
    chats: List[Union[P2pChat, GroupChat]] = Field(
        ..., description='Список чатов пользователя, для которых пришел snapshot'
    )
    conferences: Optional[List[ActiveConferenceType]] = Field(
        None, description='Список конференций пользователя, для которых пришел snapshot'
    )
    calls: Optional[List[ActiveCallType]] = Field(
        None, description='Список вызовов пользователя, для которых пришел snapshot'
    )


class activeConferenceType(Enum):
    type = 'activeConferenceType'


class ActiveConferenceType(BaseModel):
    chat_id: ChatIdType
    start_time: Optional[str] = Field(
        None, description='Время начала конференции', example='2021-05-14T10:41:43.511Z'
    )
    _type: activeConferenceType = Field(activeConferenceType.type, alias='$type', description='тип данных')


class ChatEventPin(Enum):
    type = 'chatEventPinRequest'


class ChatEventPinRequest(BaseModel):
    chat_id: ChatIdType
    chat_type: ChatType
    event_id: UcChatEventIdType
    notify_participant: Optional[bool] = Field(
        True, description='Нужно ли уведомлять участника(ов) о закрепленном сообщении'
    )
    _type: ChatEventPin = Field(ChatEventPin.type, alias='$type', description='тип данных')


class ChatEventUnpin(Enum):
    type = 'chatEventUnpinRequest'


class ChatEventUnpinRequest(BaseModel):
    chat_id: ChatIdType
    chat_type: ChatType
    event_ids: List[UcChatEventIdType]
    _type: ChatEventUnpin = Field(ChatEventUnpin.type, alias='$type', description='тип данных')


class Type6(Enum):
    EVENT_PIN = 'EVENT_PIN'
    EVENT_UNPIN = 'EVENT_UNPIN'


class ChatEventPinNotifyType(Enum):
    type = 'chatEventPinNotifyType'


class ChatEventPinNotify(BaseModel):
    type: Type6
    silent: Optional[bool] = Field(
        None,
        description='Нужно ли нотифицировать участников группы о закрепленном сообщении (нотификация должна появляться в чате, но без звукового звукового оповещения)',
    )
    event_id: UcChatEventIdType = Field(
        ...,
        description='идентификатор сообщения, которое необходимо закрепить/открепить',
    )
    _type: ChatEventPinNotifyType = Field(ChatEventPinNotifyType.type, alias='$type', description='тип данных')


class chatEventUnpinResponseType(Enum):
    type = 'chatEventUnpinResponse'


class chatEventUnpinResponse(BaseModel):
    not_unpinned: Optional[List[UcChatEventIdType]] = Field(
        None, description='Сообщения которые не удалось открепить'
    )
    _type: chatEventUnpinResponseType = Field(chatEventUnpinResponseType.type, alias='$type', description='тип данных')


class chatEventPinEventType(Enum):
    type = 'chatEventPinEventType'


class ChatEventPinEvent(ChatEventPinNotify):
    chat_id: ChatIdType
    user_id: UcUserIdType = Field(
        ..., description='Идентификатор пользователя UC, который закрепил сообщение'
    )
    _type: chatEventPinEventType = Field(chatEventPinEventType.type, alias='$type', description='тип данных')


class Extra(str, Enum):
    allow = 'allow'
    ignore = 'ignore'
    forbid = 'forbid'


class updateChatRequestType(Enum):
    type = 'updateChatRequestType'


class Update(BaseModel):
    class Config:
        extra = Extra.allow

    name: Optional[GroupNameType] = None
    avatar_url: Optional[AvatarUrlType] = None
    description: Optional[GroupDescriptionType] = None


class UpdateChatRequest(BaseModel):
    chat_id: ChatIdType
    update: Update = Field(..., description='свойства которые нужно обновить')
    type: updateChatRequestType = Field(updateChatRequestType.type, alias='$type', description='тип данных')


class updateChatNotifyType(Enum):
    type = 'updateChatNotifyType'


class Updated(BaseModel):
    class Config:
        extra = Extra.allow

    name: Optional[str] = None
    description: Optional[str] = None
    avatar_url: Optional[AvatarUrlType] = None

class UpdateChatNotifyType(BaseModel):
    user_id: Optional[UcUserIdType] = None
    chat_id: Optional[ChatIdType] = None
    updated: Updated = Field(..., description='обновленные свойства чата')
    _type: updateChatNotifyType = Field(updateChatNotifyType.type, alias='$type', description='тип данных')


class deleteUserRequestType(Enum):
    type = 'deleteUserRequest'


class DeleteUserRequest(BaseModel):
    purge: Optional[bool] = Field(
        False, description='Полное удаление пользователя с БД UC'
    )
    type: deleteUserRequestType = Field(deleteUserRequestType.type, alias='$type', description='тип данных')


class InodeIdType(BaseModel):
    __root__: str = Field(
        ...,
        description='Внутренний уникальный идентификатор inode в рамках UC',
        example='inode-uild-12345',
    )


class FolderRootResponseType(Enum):
    type = 'folderRootResponseType'


class FolderRootResponse(BaseModel):
    inode: InodeIdType
    _type: FolderRootResponseType = Field(FolderRootResponseType.type, alias='$type', description='тип данных')


class FolderRootRequestType(Enum):
    type = "folderRootRequestType"


class FolderRootRequest(BaseModel):
    system: str = Field(..., description="для какой подсистемы запрашивается корневая папка", example="integration")
    integration_name: Optional[str]
    _type: FolderRootRequestType = Field(FolderRootRequestType.type, alias='$type', description='тип данных')


class _Type17(Enum):
    inodeType = 'inodeType'


class InodeType(BaseModel):
    id: InodeIdType = Field(
        ..., description='Уникальный в рамках системе идентификатор inode'
    )
    parent: Optional[InodeIdType] = Field(
        None,
        description='Идентификатор inode папки, в которой находится данный inode. Если папка находится в корне, поле не будет заполнено',
    )
    name: str = Field(
        ..., description='Человекочитабельное имя узла на файловой системе'
    )
    access: Optional[int] = Field(
        None,
        description='Права доступа для данного пользователя на текущий inode в POSIX формате.',
    )
    _type: _Type17 = Field(..., alias='$type', description='тип данных')


class _Type20(Enum):
    linkInodeType = 'linkInodeType'


class _Type18(Enum):
    inodeIdType = 'inodeIdType'


class ToItem(BaseModel):
    inode: InodeIdType
    _type: _Type18 = Field(..., alias='$type')


class _Type19(Enum):
    chatLinkType = 'chatLinkType'


class ToItem1(BaseModel):
    chat_id: ChatIdType
    chat_type: ChatType
    _type: _Type19 = Field(..., alias='$type')


class LinkInodeType(InodeType):
    to: Optional[Union[ToItem, ToItem1]] = None
    _type: _Type20 = Field(..., alias='$type', description='тип данных')


class IncludedChat(BaseModel):
    chat_id: ChatIdType
    chat_type: ChatType


class _Type21(Enum):
    dirInodeType = 'dirInodeType'


class DirInodeType(InodeType):
    childs: Optional[List[Union[InodeType, LinkInodeType, DirInodeType]]] = Field(
        None,
        description='список inode которые находятся в данной папке. Данный параметр заполняется только для команды info.',
    )
    childs_count: int = Field(..., description='количество элементов внутри папки')
    included_chats: Optional[List[IncludedChat]] = Field(
        None,
        description='Список идентификаторов чатов, которые входят в данную папку (либо её подпапки). Данный параметр заполняется только в том случае, если команда info была вызвана с параметром with_chats=true',
    )
    _type: _Type21 = Field(..., alias='$type', description='тип данных')


class FolderListResponseType(BaseModel):
    List[Union[InodeType, LinkInodeType, DirInodeType]]


class FolderInfoResponseType(BaseModel):
    Union[DirInodeType, InodeType, LinkInodeType]


class FolderListRequestType(Enum):
    type = "folderListRequestType"


class FolderListRequest(BaseModel):
    path: str = Field(..., description="абсолютный путь до папки, в рамках которой необходимо получить список элементов", example="/integration/projects/СФО/Новосибирская обл")
    _type: FolderListRequestType = Field(FolderListRequestType.type, alias='$type', description='тип данных')


class FolderInfoRequestType(Enum):
    type = "folderInfoRequestType"


class FolderInfoRequest(BaseModel):
    id: str = Field(..., description="Внутренний уникальный идентификатор inode в рамках UC", example="inode-uild-12345")
    with_chats: Optional[bool] = Field(False, description="Если флаг выставлен, то по каждой из inode типа dirInodeType будет заполнен список чатов, которые есть в данной inode (включая поддиректории)")
    _type: FolderInfoRequestType = Field(FolderInfoRequestType.type, alias='$type', description='тип данных')


class FolderCreateResponse(BaseModel):
    id: InodeIdType = Field(
        ..., description='Уникальный в рамках системе идентификатор inode'
    )
    parent: Optional[InodeIdType] = Field(
        None,
        description='Идентификатор inode папки, в которой находится данный inode. Если папка находится в корне, поле не будет заполнено',
    )
    name: str = Field(
        ..., description='Человекочитабельное имя узла на файловой системе'
    )
    access: Optional[int] = Field(
        None,
        description='Права доступа для данного пользователя на текущий inode в POSIX формате.',
    )
    _type: _Type17 = Field(..., alias='$type', description='тип данных')


class FolderCreateRequestType(Enum):
    type = "folderCreateRequestType"


class FolderCreateRequest(BaseModel):
    root: Optional[str] = Field(None, description="Внутренний уникальный идентификатор inode в рамках UC", example="inode-uild-12345")
    inode: Union[DirInodeType, LinkInodeType]
    _type: FolderCreateRequestType = Field(FolderCreateRequestType.type, alias='$type', description='тип данных')


class FolderCreateRequestType(Enum):
    type = "folderCreateRequestType"


class FolderCreateRequest(BaseModel):
    root: Optional[str] = Field(None, description="Внутренний уникальный идентификатор inode в рамках UC", example="inode-uild-12345")
    inode: Union[DirInodeType, LinkInodeType]
    _type: FolderCreateRequestType = Field(FolderCreateRequestType.type, alias='$type', description='тип данных')


class FolderDeleteRequestType(Enum):
    type = "folderDeleteRequestType"


class FolderDeleteRequest(BaseModel):
    ids: List[InodeIdType]
    force: Optional[bool] = Field(False, description="Флаг, показывающий, надо или нет удалять данную папку в случае, если у неё есть подэлементы", example="False")
    _type: FolderDeleteRequestType = Field(FolderDeleteRequestType.type, alias='$type', description='тип данных')


class FolderMoveRequestType(Enum):
    type = "folderMoveRequestType"


class FolderMoveRequest(BaseModel):
    ids: List[InodeIdType]
    to: InodeIdType
    _type: FolderMoveRequestType = Field(FolderMoveRequestType.type, alias='$type', description='тип данных')


class FolderRenameRequestType(Enum):
    type = "folderRenameRequestType"


class FolderRenameRequest(BaseModel):
    ids: InodeIdType
    name: str = Field(..., description="Новое имя для inode", example="New Name")
    _type: FolderRenameRequestType = Field(FolderRenameRequestType.type, alias='$type', description='тип данных')


class UserAddRequestType(Enum):
    type = 'userAddRequestType'


class UserAddRequest(BaseModel):
    user_id: Optional[str] = Field(
        None,
        description='Идентификатор пользователя UC за которым будет закреплена учетная запись. Если не передан, '
                    'пользователь закрепится за пользователем UC который вызвал команду.',
    )
    uri_entry: str = Field(..., example='uri@example.ru')
    display_name: Optional[str] = Field(example='Some Display Name')
    imei: Optional[str] = Field(
        description='В случае, если MCPTT пользователь привязан к конкретному устройству, то в данном поле записывается'
                    ' IMEI устройства',
        example=547035512218823,
    )
    _type: UserAddRequestType = Field(UserAddRequestType.type, alias='$type', description='тип данных')


class _Type16(Enum):
    userProfileType = 'userProfileType'


class UriType(BaseModel):
    __root__: str = Field(..., example='uri@example.ru')


class DisplayNameType(BaseModel):
    __root__: str = Field(..., example='Some Display Name')


class PriorityType(BaseModel):
    __root__: conint(ge=0, le=255) = Field(..., example=56)


class ImeiType(BaseModel):
    __root__: str = Field(
        ...,
        description='В случае, если MCPTT пользователь привязан к конкретному устройству, то в данном поле записывается IMEI устройства',
        example=547035512218823,
    )


class AllowCallRules(BaseModel):
    allow_private_call: Optional[bool] = None
    allow_emergency_private_call: Optional[bool] = None
    allow_emergency_group_call: Optional[bool] = None


class EntryType(BaseModel):
    uri: UriType
    display_name: Optional[DisplayNameType] = None


class OnNetworkType(BaseModel):
    groups: Optional[List[EntryType]] = None


class OffNetworkType(BaseModel):
    groups: Optional[List[EntryType]] = None


class UserProfileType(BaseModel):
    uri: Optional[UriType]
    uc_user_id: Optional[UcUserIdType] = None
    display_name: DisplayNameType = None
    priority: Optional[PriorityType] = None
    imei: Optional[ImeiType] = None
    allow_call_rules: Optional[AllowCallRules] = Field(
        None, description='разрешенные звонки'
    )
    emergency_private_call: Optional[EntryType] = Field(
        None, description='Экстренный вызов на частный номер'
    )
    emergency_group_call: Optional[EntryType] = Field(
        None, description='Экстренный вызов на группу'
    )
    on_network: Optional[OnNetworkType] = None
    off_network: Optional[OffNetworkType] = None
    private_call_list: Optional[List[EntryType]] = Field(
        None, description='Список контактов'
    )
    _type: _Type16 = Field(..., alias='$type', description='тип данных')


class UserProfileDeleteRequestType(Enum):
    type = 'userProfileDeleteRequest'


class UserProfileDeleteRequest(BaseModel):
    user_uri: Optional[UriType] = None
    uc_user_id: Optional[UcUserIdType] = None
    type: UserProfileDeleteRequestType = Field(UserProfileDeleteRequestType.type, alias='$type',
                                               description='тип данных')


class _Type14(Enum):
    UCUserType = 'UCUserType'


class UCUserType(BaseModel):
    user_id: UcUserIdType
    nickname: Optional[str] = None
    phone: Optional[str] = None
    is_mcptt_user: Optional[bool] = Field(
        None, description='Пользователь является пользователем MCPTT'
    )
    email: Optional[str] = Field(None, description='Электронный адрес пользователя')
    _type: _Type14 = Field(..., alias='$type', description='тип данных')


class _Type6(Enum):
    userProfileListRequest = 'userProfileListRequest'


class UserProfileListRequest(BaseModel):
    user_uri: Optional[UriType] = None
    _type: _Type6 = Field(..., alias='$type', description='тип данных')


class UserProfileListResponseType(Enum):
    type = "userProfileListResponse"


class UserProfileListResponse(BaseModel):
    profiles: List = Field(None, description="Список профилей пользователя")
    _type: UserProfileListResponseType = Field(UserProfileListResponseType.type, alias='$type', description='тип данных')


class GroupEntryType(BaseModel):
    uri: Optional[UriType] = None
    uc_user_id: Optional[UcUserIdType] = None
    user_priority: Optional[PriorityType] = None
    display_name: Optional[DisplayNameType] = None
    on_network_required: Optional[bool] = None
    on_network_recvonly: Optional[bool] = None
    multi_talker_allowed: Optional[bool] = None
    on_network_affiliation_to_group_required: Optional[bool] = None


class AllowEmergencyCallRules(BaseModel):
    allow_mcptt_emergency_call: Optional[bool] = None
    allow_mcptt_emergency_alert: Optional[bool] = None


class GroupProfileType(Enum):
    type = 'groupProfileType'


class GroupProfile(BaseModel):
    display_name: DisplayNameType = None
    list: Optional[List[GroupEntryType]] = None
    allow_emergency_call_rules: Optional[AllowEmergencyCallRules] = Field(
        None, description='экстренный вызов'
    )
    on_network_temporary: Optional[bool] = Field(
        None, description='признак временной группы'
    )
    on_network_maximum_duration: Optional[int] = Field(
        None, description='таймер удержания тангенты (ms)'
    )
    uri: Optional[UriType] = None
    uc_group_id: Optional[ChatIdType] = None
    _type: GroupProfileType = Field(GroupProfileType.type, alias='$type', description='тип данных')


class UserProfileGetRequestType(Enum):
    type = 'userProfileGetRequest'


class ProfileResourceNameType(BaseModel):
    __root__: str = Field(
        ...,
        description='Ресурсное имя профиля пользователя (будет попадать в uri ресурса данного профиля)',
        example='user_profile',
    )


class UserProfileGetRequest(BaseModel):
    user_uri: Optional[UriType] = None
    uc_user_id: Optional[UcUserIdType] = None
    type: UserProfileGetRequestType = Field(default=UserProfileGetRequestType.type, alias='$type',
                                            description='тип данных')


class DeleteMcpttGroupType(Enum):
    type = 'deleteMcpttGroupRequest'


class DeleteMcpttGroup(BaseModel):
    uri: Optional[UriType] = None
    uc_group_id: Optional[ChatIdType] = None
    type: DeleteMcpttGroupType = Field(default=DeleteMcpttGroupType.type, alias='$type', description='тип данных')


class WebhookType(BaseModel):
    id: str = Field(description='Идентификатор вебхука', example='134095221')
    create_at: Optional[str] = Field(
        None, description='Время создания вебхука', example='2021-05-14T10:41:43.511Z'
    )
    update_at: Optional[str] = Field(
        None, description='Время обновления вебхука', example='2021-05-14T10:41:43.511Z'
    )
    user_id: str
    chat_id: Optional[str]
    name: str = Field(description='Название вебхука', example='webhook name')
    description: Optional[str]


class _Type35(Enum):
    webhookListRequestType = 'webhookListRequestType'


class Payload6(BaseModel):
    _type: _Type35 = Field(..., alias='$type', description='тип данных')


class _Type36(Enum):
    webhookListResponseType = 'webhookListResponseType'


class Payload7(BaseModel):
    _type: _Type36 = Field(..., alias='$type', description='тип данных')
    webhooks: List[WebhookType] = Field(..., description='Список вебхуков')


class _Type37(Enum):
    webhookDeleteRequestType = 'webhookDeleteRequestType'


class Payload8(BaseModel):
    id: str = Field(..., description='Идентификатор вебхука', example='134095221')
    _type: _Type37 = Field(..., alias='$type', description='тип данных')


class WebhookUpdateRequestType(Enum):
    type = 'webhookUpdateRequestType'


class WebhookCreateRequestType(Enum):
    type = 'webhookCreateRequestType'


class WebhookCreateRequest(BaseModel):
    chat_id: Optional[str]
    name: str = Field(description='Название вебхука', example='webhook name')
    description: Optional[str]
    _type: WebhookCreateRequestType = Field(WebhookCreateRequestType.type, alias='$type', description='тип данных')


class WebhookCreateResponseType(Enum):
    type = 'webhookCreateResponseType'


class WebhookCreateResponse(BaseModel):
    _type: WebhookCreateResponseType = Field(WebhookCreateResponseType.type, alias='$type', description='тип данных')
    webhook: WebhookType


class WebhookListRequestType(Enum):
    type = 'webhookListRequestType'


class WebhookListRequest(BaseModel):
    _type: WebhookListRequestType = Field(WebhookListRequestType.type, alias='$type', description='тип данных')


class WebhookListResponseType(Enum):
    type = 'webhookListResponseType'


class WebhookListResponse(BaseModel):
    _type: WebhookListResponseType = Field(WebhookListResponseType.type, alias='$type', description='тип данных')
    webhooks: List[WebhookType] = Field(..., description='Список вебхуков')


class WebhookDeleteRequestType(Enum):
    type = 'webhookDeleteRequestType'


class WebhookDeleteRequest(BaseModel):
    id: str = Field(..., description='Идентификатор вебхука', example='134095221')
    _type: WebhookDeleteRequestType = Field(WebhookDeleteRequestType.type, alias='$type', description='тип данных')


class WebhookUpdateRequest(BaseModel):
    id: str = Field(..., description='Идентификатор вебхука', example='134095221')
    name: Optional[str]
    description: Optional[str]
    chat_id: Optional[str]
    _type: WebhookUpdateRequestType = Field(WebhookUpdateRequestType.type, alias='$type', description='тип данных')


class WebhookUpdateResponseType(Enum):
    type = 'webhookUpdateResponseType'


class WebhookUpdateResponse(BaseModel):
    _type: WebhookUpdateResponseType = Field(WebhookUpdateResponseType.type, alias='$type', description='тип данных')


class ChatMuteControlType(Enum):
    type = 'chatMuteControlType'


class ChatMuteControl(BaseModel):
    chat_id: ChatIdType
    chat_type: ChatType
    duration: Optional[int] = Field(
        None,
        description='На какое время отключить нотификации (в миллисекундах). Использует только для метода disable.',
        example=3600000,
    )
    _type: ChatMuteControlType = Field(ChatMuteControlType.type, alias='$type', description='тип данных')


class MCPTTUserType(Enum):
    type = 'MCPTTUserType'


class MCPTTUser(BaseModel):
    uc_user_id: UcUserIdType
    uri_entry: UriType
    imei: Optional[ImeiType] = None
    display_name: Optional[DisplayNameType] = None
    _type: MCPTTUserType = Field(MCPTTUserType.type, alias='$type', description='тип данных')


class UpdateMCPTT(BaseModel):
    user_uri: Optional[UriType] = None
    display_name: Optional[DisplayNameType] = None


class MCPTTUserUpdateRequestType(Enum):
    type = 'MCPTTUserUpdateRequestType'


class MCPTTUserUpdateRequest(BaseModel):
    uc_user_id: Optional[UcUserIdType] = None
    user_uri: Optional[UriType] = None
    update: Optional[UpdateMCPTT] = None
    _type: MCPTTUserUpdateRequestType = Field(MCPTTUserUpdateRequestType.type, alias='$type', description='тип данных')


class User(BaseModel):
    uc_user_id: Optional[UcUserIdType] = None
    user_uri: Optional[UriType] = None


class MCPTTUserDeleteRequestType(Enum):
    type = 'MCPTTUserDeleteRequestType'


class MCPTTUserDeleteRequest(BaseModel):
    users: Optional[List[User]] = Field(
        None,
        description='список пользователей, которых нужно удалить. Если не передан, удалится пользователь, который вызывает команду.',
    )
    _type: MCPTTUserDeleteRequestType = Field(MCPTTUserDeleteRequestType.type, alias='$type', description='тип данных')


class NotDeletedItem(BaseModel):
    user_uri: Optional[UriType] = None
    reason: Optional[str] = Field(
        None, description='причина, почему пользователя не удалось удалить'
    )


class MCPTTUserDeleteResponseType(Enum):
    type = 'MCPTTUserDeleteResponseType'


class MCPTTUserDeleteResponse(BaseModel):
    not_deleted: Optional[List[NotDeletedItem]] = Field(
        None, description='пользователи, которых не удалось удалить'
    )
    _type: MCPTTUserDeleteResponseType = Field(MCPTTUserDeleteResponseType.type, alias='$type', description='тип данных')


class callHistoryRequestType(Enum):
    type = 'callHistoryRequestType'


class callHistoryRequest(BaseModel):
    search: Optional[str] = Field(
        None,
        description='Строка поиска (поиск по любому из полей записи о вызове (это может быть имя любого из участников вызова, номер телефона и т.п.). Регистронезависимый поиск.)',
        example='7903911',
    )
    page_size: Optional[conint(ge=1)] = Field(
        50,
        description='Количество возвращаемых записей в запросе поиска (технически, в зависимости от backend-а возможна ситуация, когда на запрос вернется большее количество записей)',
        example=50,
    )
    search_timeout: Optional[conint(ge=250)] = Field(
        5000,
        description='Максимальное время выполнения запроса (в миллисекундах). В случае, если время запроса будет превышать заданное значение, то API вернет только то количество записей, что удалось найти к текущему моменту.',
        example=2500,
    )
    tag: Optional[str] = Field(
        None,
        description="Тег поиска. Тег используется в случае 'прокрутки', при запросе второй страницы и далее. В случае, если в запросе задан тег, остальные параметры запроса <b>игнорируются!</b>",
        example='UHJvdGVpIE5TSw==',
    )
    _type: callHistoryRequestType = Field(callHistoryRequestType.type, alias='$type', description='тип данных')



class PasswordType(BaseModel):
    __root__: SecretStr = Field(
        ..., description='Пароль пользователя UC', example='vasya-password'
    )


class UserCreateRequestType(Enum):
    type = 'userCreateRequestType'


class PhoneType(BaseModel):
    __root__: str = Field(..., description='Номер телефон', example='71234567890')


class EmailType(BaseModel):
    __root__: str = Field(
        ..., description='Адрес электронной почты', example='user@example.ru'
    )


class UserCreateRequest(BaseModel):
    uc_external_user_id: UcExternalUserIdType
    password: Optional[PasswordType] = None
    uc_phone: Optional[PhoneType] = None
    uc_avatar_url: Optional[AvatarUrlType] = None
    uc_email: Optional[EmailType] = None
    uri_entry: UriType
    display_name: Optional[DisplayNameType] = None
    user_profile: Optional[UserProfileType] = None
    _type: UserCreateRequestType = Field(UserCreateRequestType.type, alias='$type', description='тип данных')


class ChatGroupConferenceStartType(Enum):
    type = 'chatGroupConferenceStart'


class ChatGroupConferenceStart(BaseModel):
    chat_id: ChatIdType
    _type: ChatGroupConferenceStartType = Field(ChatGroupConferenceStartType.type, alias='$type', description='тип данных')


class ChatGroupConferenceStopType(Enum):
    type = 'chatGroupConferenceStop'


class ChatGroupConferenceStop(BaseModel):
    conference_id: ConferenceIdType
    _type: ChatGroupConferenceStopType = Field(ChatGroupConferenceStopType.type, alias='$type', description='тип данных')
