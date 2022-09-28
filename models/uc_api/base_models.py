from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import List, Optional, Union, Any
from pydantic import BaseModel, Field, conint, constr


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


class ChatIdType(BaseModel):
    __root__: str = Field(
        ...,
        description='Внутренний уникальный идентификатор P2P чата UC',
        example="10952",
        )


class UcChatEventIdType(BaseModel):
    __root__: str = Field(
        ...,
        description='Уникальный идентификатор события чата',
        example="18446744073709551615",
        )


class ChatEventPinNotifyType(Enum):
    type = 'chatEventPinNotifyType'


class Type6(Enum):
    EVENT_PIN = 'EVENT_PIN'
    EVENT_UNPIN = 'EVENT_UNPIN'


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


class UcUserIdType(BaseModel):
    __root__: str = Field(
        None,
        description='Внутренний уникальный идентификатор пользователя UC',
        example="18446744073709551615",
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


class ChatEventForwardType(Enum):
    type = 'chatEventForwardType'


class ChatEventForward(BaseModel):
    original_sender_id: UcUserIdType = Field(
        ...,
        description='Идентификатор пользователя, который изначально отправлял сообщение')
    type: ChatEventForwardType = Field(default=ChatEventForwardType.type, alias='$type', description='тип данных')


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


class Attachment(BaseModel):
    attachment_id: str = Field(
        ...,
        description='Уникальный идентификатор attachment',
        example='6f98739f-c362-1b9a-ab8b-52c21d50d2fb',
        )
    filename: constr(min_length=1) = Field(
        ..., description='Имя прикрепленного файла', example='protei.meetings.txt'
        )
    mimetype: constr(min_length=1) = Field(
        ..., description='Mime-тип прикрепленного файла', example='text/plain'
        )
    size: conint(ge=0, le=1073741824) = Field(
        ..., description='Размер прикрепленного файла, в настоящий момент ограничен 1Gb'
        )


class ChatType(Enum):
    P2P = 'P2P'
    GROUP = 'GROUP'


class ChatEventType(Enum):
    type = 'chatEventType'


class JsonStringType(BaseModel):
    __root__: dict = Field(
        description='Представление json в строке',
        example='{json_key1: 1, json_key2: "value2"}',
        )


class ChatEventNotifyType(Enum):
    type = 'chatEventNotifyType'


class ChatEventNotify(BaseModel):
    chat_id: ChatIdType
    begin_event_id: Optional[UcChatEventIdType] = None
    end_event_id: UcChatEventIdType
    notified_at: str = Field(
        ...,
        description='Время относящееся к событию',
        example='2021-01-28T15:51:43.511Z',
        )
    type: str = Field(
        "DELIVERED" or "READ",
        description='Тип нотификации: <br/>DELIVERED - указанный диапазон событий был доставлен;'
                    ' <br/>READ - указанный диапазон событий был прочитан;',
        )
    sender_id: UcUserIdType
    options: Optional[JsonStringType] = None
    type_1: ChatEventNotifyType = Field(default=ChatEventNotifyType.type, alias='$type', description='тип данных')


class MembersType(BaseModel):
    __root__: List[UcUserIdType] = Field(..., description='Список участников')


class JsonOptionType(BaseModel):
    pass


class GroupChatType(Enum):
    type = 'groupChatType'


class StatusChat(Enum):
    CREATED = 'CREATED'
    BLOCKED = 'BLOCKED'
    DELETED = 'DELETED'
    ARCHIVED = 'ARCHIVED'
    UPDATED = 'UPDATED'
    TYPING = 'TYPING'


class P2pChatType(Enum):
    type = 'p2pChatType'


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


class CallIdType(BaseModel):
    __root__: constr(min_length=1) = Field(
        ...,
        description='Идентификатор вызова',
        example='f973769f-c4f6-44ce-984e-9fbf628beb7f',
        )


class SideType(Enum):
    ORIGINATION = 'ORIGINATION'
    TERMINATION = 'TERMINATION'
    SYSTEM = 'SYSTEM'


class CallReleaseReasonType(Enum):
    normal = 'normal'
    unsupportedMedia = 'unsupportedMedia'
    noAnswer = 'noAnswer'
    busy = 'busy'
    rejected = 'rejected'
    temporaryFailure = 'temporaryFailure'
    systemFailure = 'systemFailure'
    noAnswerTimeout = 'noAnswerTimeout'

class ChatEventConferenceOptionType(Enum):
    type = "chatEventConferenceOptionType"

class ChatEventConferenceOption(BaseModel):
    conference_id: str
    start_time: str
    end_time: Optional[str]
    reason: Optional[str]
    with_video: Optional[bool]
    members: Optional[List[str]]
    reason: Optional[CallReleaseReasonType] = None
    _type: ChatEventConferenceOptionType = Field(ChatEventConferenceOptionType.type, alias='$type', description='тип данных')


class chatEventCallOptionType(Enum):
    type = 'chatEventCallOptionType'


class ChatEventCallOption(BaseModel):
    call_id: CallIdType
    owner_id: UcUserIdType
    side: Optional[SideType] = Field(
        None,
        description='Направление вызова. ORIGINATION - для исходящего вызова; TERMINATION - для входящего вызова.',
        example='ORIGINATION',
    )
    start_time: datetime = Field(..., description='Время начала вызова')
    answer_time: Optional[datetime] = Field(None, description='Время ответа на вызов')
    release_time: Optional[datetime] = Field(
        None, description='Время завершения вызова'
    )
    release_side: Optional[SideType] = Field(
        None, description='Сторона которая завершила вызов.'
    )
    reason: Optional[CallReleaseReasonType] = None
    with_video: Optional[bool] = Field(
        False, description='Признак того, что был видеовызов'
    )
    _type: chatEventCallOptionType = Field(chatEventCallOptionType.type, alias='$type', description='тип данных')


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
    notify: Optional[Union[GroupChatMemberPresenceNotify, ChatEventPinNotify]] = Field(
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
    nickname: Optional[str] = Field (description="Имя из-под которого было послано сообщение (используется для хуков)")
    avatar_url: Optional[str] = Field(description="Аватар ля сообщения (используется в хуках")
    call: Optional[ChatEventCallOption] = None
    conference: Optional[ChatEventConferenceOption]


class ChatEvent(BaseModel):
    event_id: Optional[UcChatEventIdType] = None
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
    options: Optional[EventOptionsType] = None
    chat_type: ChatType
    type_1: ChatEventType = Field(default=ChatEventType.type, alias='$type', description='тип данных')


class P2pChat(BaseModel):
    chat_id: ChatIdType
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
    avatar_url: Optional[str] = Field(
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
    user_mentions: Optional[List[UcChatEventIdType]] = Field(
        None,
        description='Список идентификаторов непрочитанных event-ов, в которых было упоминание текущего пользователя',
    )
    type: GroupChatType = Field(GroupChatType.type, alias='$type', description='тип данных')


class ChatNotifyType(Enum):
    type = 'chatNotifyType'


class ChatNotify(BaseModel):
    chat_id: ChatIdType
    chat_type: ChatType
    type_1: StatusChat = Field(..., alias='type', description='Тип нотификации')
    options: Union[GroupChat, P2pChat]
    type: ChatNotifyType = Field(ChatNotifyType.type, alias='$type', description='тип данных')


class activeConferenceType(Enum):
    type = 'activeConferenceType'


class ActiveConferenceType(BaseModel):
    chat_id: ChatIdType
    start_time: Optional[str] = Field(
        None, description='Время начала конференции', example='2021-05-14T10:41:43.511Z'
    )
    _type: activeConferenceType = Field(activeConferenceType.type, alias='$type', description='тип данных')


class ActiveCallType(Enum):
    type = 'activeCallType'


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


class SubTypeSdp(Enum):
    SDP_OFFER = 'SDP_OFFER'
    SDP_ANSWER = 'SDP_ANSWER'


class SdpType(BaseModel):
    body: str = Field(..., description='Текстовое представление SDP', example='v=0...')
    type: SubTypeSdp = Field(..., description='Направление SDP')


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


class ChatDeleteEventNotifyType(Enum):
    type = 'chatDeleteEventNotifyType'


class ChatDeleteEventNotify(BaseModel):
    chat_id: ChatIdType
    events_id: List[UcChatEventIdType]
    options: Optional[JsonStringType] = None
    type: ChatDeleteEventNotifyType = Field(default=ChatDeleteEventNotifyType.type, alias='$type',
                                            description='тип данных')


class ChatEventPinEventType(Enum):
    type = 'chatEventPinEventType'


class ChatEventPinEvent(ChatEventPinNotify):
    chat_id: ChatIdType
    user_id: UcUserIdType = Field(
        ..., description='Идентификатор пользователя UC, который закрепил сообщение'
    )
    _type: ChatEventPinEventType = Field(ChatEventPinEventType.type, alias='$type', description='тип данных')


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


class AddMembersToGroupNotifyType(Enum):
    type = 'addMembersToGroupNotifyType'


class AddMembersToGroupNotify(BaseModel):
    chat_id: ChatIdType
    members: List[UcUserIdType]
    type: AddMembersToGroupNotifyType = Field(AddMembersToGroupNotifyType.type, alias='$type', description='тип данных')


class DeleteMembersFromGroupNotifyType(Enum):
    type = 'deleteMembersFromGroupNotifyType'


class DeleteMembersFromGroupNotify(BaseModel):
    chat_id: ChatIdType
    members: List[UcUserIdType]
    type: DeleteMembersFromGroupNotifyType = Field(DeleteMembersFromGroupNotifyType.type, alias='$type',
                                                   description='тип данных')


class GetMcpttGroupRequestType(Enum):
    type = 'getMcpttGroupRequest'


class GetMcpttGroupRequest(BaseModel):
    uri: Optional[str] = None
    uc_group_id: Optional[ChatIdType] = None
    type: GetMcpttGroupRequestType = Field(GetMcpttGroupRequestType.type, alias='$type', description='тип данных')


class UserFloorControlRequestType(Enum):
    type = 'userFloorControlRequestType'


class UserFloorControlRequest(BaseModel):
    source_id: str
    type: UserFloorControlRequestType = Field(UserFloorControlRequestType.type, alias='$type', description='тип данных')


class UserFloorControlReleaseType(Enum):
    type = 'userFloorControlReleaseType'


class UserFloorControlRelease(BaseModel):
    source_id: str
    type: UserFloorControlReleaseType = Field(UserFloorControlReleaseType.type, alias='$type', description='тип данных')


class GroupFloorControlRequestType(Enum):
    type = 'groupFloorControlRequestType'


class GroupFloorControlRequest(BaseModel):
    uri: str
    source_id: str
    type: GroupFloorControlRequestType = Field(GroupFloorControlRequestType.type, alias='$type', description='тип данных')


class GroupFloorControlReleaseType(Enum):
    type = 'groupFloorControlReleaseType'


class GroupFloorControlRelease(BaseModel):
    uri: str
    source_id: str
    type: GroupFloorControlReleaseType = Field(GroupFloorControlReleaseType.type, alias='$type', description='тип данных')


class UserSubscribeResponseType(Enum):
    type = 'userSubscribeResponseType'


class UserStatusType(Enum):
    type = 'userStatusType'


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


class UserStatus(BaseModel):
    user_id: UcUserIdType
    scope: UserScopeType
    seq: SeqType
    status: UserStatusValueType
    timestamp: str = Field(..., description='Время активности', example='2021-01-28T15:51:43.511Z')
    _type: UserStatusType = Field(UserStatusType.type, alias='$type', description='тип данных')


class UserSubscribeResponse(BaseModel):
    _type: UserSubscribeResponseType = Field(UserSubscribeResponseType.type, alias='$type', description='тип данных')
    statuses: Optional[List[UserStatus]] = None


class UserStatusNotifyType(Enum):
    type = 'userStatusNotifyType'


class UserStatusNotify(BaseModel):
    statuses: List[UserStatus]
    type: UserStatusNotifyType = Field(UserStatusNotifyType.type, alias='$type', description='тип данных')


class Type10(Enum):
    COUNT = 'COUNT'
    EVENTS = 'EVENTS'
    WAIT_CONTINUE = 'WAIT_CONTINUE'
    STOP = 'STOP'


class Event(BaseModel):
    event_id: UcChatEventIdType
    chat_id: ChatIdType
    chat_type: ChatType


class ChatEventTypeArray(BaseModel):
    events: List[ChatEvent]



class ChatEventShortTypeArray(BaseModel):
    events: List[Event]


class _Type81(Enum):
    searchStopNotifyType = 'searchStopNotifyType'


class SearchStopNotifyType(BaseModel):
    reason: str
    _type: _Type81 = Field(None, alias='$type', description='тип данных')


class SearchFoundMessagesCountNotifyType(Enum):
    type = 'searchFoundMessagesCountNotifyType'


class SearchFoundMessagesCountNotify(BaseModel):
    count: int
    type: SearchFoundMessagesCountNotifyType = Field(SearchFoundMessagesCountNotifyType.type, alias='$type', description='тип данных')


class ChatEventSearchNotifyType(Enum):
    type = 'chatEventSearchNotifyType'


class ChatEventSearchNotify(BaseModel):
    search_id: str = Field(
        ...,
        description='Идентификатор поиска который создается при вызове команды /chat/event/search',
        example='f7eb430a-358f-4023-9939-c9360cd06ec6',
    )
    type: Type10
    options: Optional[Union[ChatEventTypeArray, ChatEventShortTypeArray, SearchStopNotifyType, SearchFoundMessagesCountNotify]]
    _type: ChatEventSearchNotifyType = Field(ChatEventSearchNotifyType.type, alias='$type', description='тип данных')


class ApiRequestIdType(BaseModel):
    __root__: conint(ge=1) = Field(
        ...,
        description='Уникальный идентификатор запроса. Служит для связки запрос/ответ',
        example=1234,
    )


class _Type1(Enum):
    generalResponseType = 'generalResponseType'


class GeneralResponseType(Enum):
    type = 'generalResponseType'


class ChatEventResponseType(Enum):
    type = 'chatEventResponseType'


class DeleteMcpttGroupResponseType(Enum):
    type = 'deleteMcpttGroupResponse'


class PriorityType(BaseModel):
    __root__: conint(ge=0, le=255) = Field(..., example=56)


class UriType(BaseModel):
    __root__: str = Field(..., example='uri@example.ru')


class DisplayNameType(BaseModel):
    __root__: str = Field(..., example='Some Display Name')


class ImeiType(BaseModel):
    __root__: str = Field(
        ...,
        description='В случае, если MCPTT пользователь привязан к конкретному устройству, то в данном поле записывается IMEI устройства',
        example=547035512218823,
    )


class AllowEmergencyCallRules(BaseModel):
    allow_mcptt_emergency_call: Optional[bool] = None
    allow_mcptt_emergency_alert: Optional[bool] = None


class GroupEntryType(BaseModel):
    uri: Optional[UriType] = None
    uc_user_id: Optional[UcUserIdType] = None
    user_priority: Optional[PriorityType] = None
    display_name: Optional[DisplayNameType] = None
    on_network_required: Optional[bool] = None
    on_network_recvonly: Optional[bool] = None
    multi_talker_allowed: Optional[bool] = None
    on_network_affiliation_to_group_required: Optional[bool] = None


class DeleteMcpttGroupResponse1(BaseModel):
    not_deleted: bool = Field(description='Удалена ли группа')
    type: DeleteMcpttGroupResponseType = Field(default=DeleteMcpttGroupResponseType.type, alias='$type',
                                               description='тип данных')


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
    uri: UriType = Field(..., description="URI группы")
    uc_group_id: Optional[ChatIdType] = None
    _type: GroupProfileType = Field(GroupProfileType.type, alias='$type', description='тип данных')


class McpttLoginResponseType(Enum):
    type = "MCPTTLoginResponse"


class MCPTTUserType(Enum):
    type = 'MCPTTUserType'


class MCPTTUser(BaseModel):
    uc_user_id: UcUserIdType
    uri_entry: UriType
    imei: Optional[ImeiType] = None
    display_name: Optional[DisplayNameType] = None
    _type: MCPTTUserType = Field(MCPTTUserType.type, alias='$type', description='тип данных')


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


class MCPTTUsersListResponseType(Enum):
    type = 'MCPTTUsersListResponse'


class MCPTTUsersListResponsePayload(BaseModel):
    users: List[MCPTTUser]
    _type: MCPTTUsersListResponseType = Field(MCPTTUsersListResponseType.type, alias='$type', description='тип данных')


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


class _Type16(Enum):
    userProfileType = 'userProfileType'


class AllowCallRules(BaseModel):
    allow_private_call: Optional[bool] = None
    allow_emergency_private_call: Optional[bool] = None
    allow_emergency_group_call: Optional[bool] = None


class EntryType(BaseModel):
    uri: UriType
    uc_user_id: Optional[UcUserIdType] = None
    display_name: Optional[DisplayNameType] = None


class OnNetworkType(BaseModel):
    groups: Optional[List[EntryType]] = None


class OffNetworkType(BaseModel):
    groups: Optional[List[EntryType]] = None


class UserProfileType(BaseModel):
    uri: UriType
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


class UserProfileListResponseType(Enum):
    type = "userProfileListResponse"


class UserProfileListResponse(BaseModel):
    profiles: List = Field(None, description="Список профилей пользователя")
    _type: UserProfileListResponseType = Field(UserProfileListResponseType.type, alias='$type', description='тип данных')


class UCUsersListType(Enum):
    type = 'UCUsersListType'


class UCUsersList(BaseModel):
    users_list: List[UCUserType]
    _type: UCUsersListType = Field(UCUsersListType.type, alias='$type', description='тип данных')


class GeneralEventType(Enum):
    type = 'generalEventType'


class InodeIdType(BaseModel):
    __root__: str = Field(
        ...,
        description='Внутренний уникальный идентификатор inode в рамках UC',
        example='inode-uild-12345',
    )


class folderRootResponseType(Enum):
    type = 'folderRootResponseType'


class FolderRoot(BaseModel):
    inode: InodeIdType
    type: folderRootResponseType = Field(folderRootResponseType.type, alias='$type', description='тип данных')


class _Type148(Enum):
    callMakeResponseType = 'callMakeResponseType'


class CallMakeResponseType(BaseModel):
    call_id: CallIdType
    _type: _Type148 = Field(..., alias='$type', description='тип данных')


class callHistoryResponseType(Enum):
    type = 'callHistoryResponseType'


class CallType(BaseModel):
    pass


class callHistoryResponse(BaseModel):
    tag: Optional[str] = Field(
        None,
        description='Тег для продолжения поиска (в случае использования паджинации). Если тег не вернулся, значит вызовов под заданные критерии поиска больше нет.',
        example='UHJvdGVpIE5TSw==',
    )
    calls: List[CallType] = Field(..., description='Список вызовов')
    _type: callHistoryResponseType = Field(callHistoryResponseType.type, alias='$type', description='тип данных')


class UserCreateResponseType(Enum):
    type = 'userCreateResponseType'


class UserCreateResponse(BaseModel):
    uc_user_id: UcUserIdType = Field(..., description='Идентификатор созданного пользователя UC.')
    _type: UserCreateResponseType = Field(UserCreateResponseType.type, alias='$type', description='тип данных')


class ConferenceIdType(BaseModel):
    __root__: str = Field(
        ..., description='Идентификатор конференции', example='134095221'
    )


class ConferenceStartResponseType(Enum):
    type = 'chatGroupConferenceStartResponseType'


class ConferenceStartResponse(BaseModel):
    _type: Optional[ConferenceStartResponseType] = Field(None, alias='$type', description='тип данных')
    conference_id: ConferenceIdType


class _Type134(Enum):
    chatGroupConferenceStatusNotifyType = 'chatGroupConferenceStatusNotifyType'


class ConferenceStatusType(Enum):
    ACTIVATING = 'ACTIVATING'
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'


class ConferenceAbonentIdType(BaseModel):
    __root__: conint(ge=0) = Field(
        ..., description='Идентификатор абонентов в конференции', example=5
    )


class ConferenceAbonentStatusType(Enum):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    CALLING = 'CALLING'


class ScreenDivisionType(Enum):
    ALL_EQUALLY = 'ALL_EQUALLY'
    ALL_ENLARGE_SPEAKER = 'ALL_ENLARGE_SPEAKER'
    SPEAKER_ONLY = 'SPEAKER_ONLY'
    PRESENTATION_ONLY = 'PRESENTATION_ONLY'


class LayoutType(BaseModel):
    screen_division_type: Optional[ScreenDivisionType] = Field(
        None, description='Статус пользователя'
    )


class ConferenceMemberStatusType(BaseModel):
    user_id: Optional[UcUserIdType] = None
    id: ConferenceAbonentIdType
    status: ConferenceAbonentStatusType
    layout: Optional[LayoutType] = None
    send_audio: bool = Field(..., example=True)
    recv_audio: bool = Field(..., example=True)
    send_video: bool = Field(..., example=False)
    recv_video: bool = Field(..., example=False)


class ChatGroupConferenceStatusNotifyType(BaseModel):
    chat_id: ChatIdType
    conference_id: ConferenceIdType
    start_time: datetime = Field(..., description='Время начала конференции')
    status: ConferenceStatusType
    screen_demo_member_id: Optional[ConferenceAbonentIdType] = None
    speaker_id: Optional[ConferenceAbonentIdType] = None
    members: Optional[List[ConferenceMemberStatusType]] = None
    _type: _Type134 = Field(..., alias='$type', description='тип данных')