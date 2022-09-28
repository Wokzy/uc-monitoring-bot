from __future__ import annotations
from enum import Enum
from typing import List, Optional, Union
from pydantic import BaseModel, Field, conint


class _Type67(Enum):
    chatEventReadParticipantsRequest = 'chatEventReadParticipantsRequest'

class ReadParticipantsRequest(BaseModel):
    event_id: str
    chat_id: str
    _type: _Type67 = Field(alias='$type', description='тип данных')


class _Type68(Enum):
    chatEventReadParticipantsResponse = 'chatEventReadParticipantsResponse'


class ReadParticipants(BaseModel):
    users: Optional[List[str]]
    _type: _Type68 = Field(alias='$type', description='тип данных')


class GeneralResponseType(Enum):
    generalResponseType = 'generalResponseType'


class ReadParticipantsResponse(BaseModel):
    id: conint(ge=1)
    result_code: conint(ge=200, le=299) = Field(
        description='Код с результатом выполнения запроса. Аналог HTTP status code.',
        example=200,)
    payload: ReadParticipants
    _type: GeneralResponseType = Field(..., alias='$type', description='тип данных')