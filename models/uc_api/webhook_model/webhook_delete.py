from __future__ import annotations
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, conint
from models.uc_api.base_models import ImageType, Attachment, Type, Type4
# from models.uc_api.uc_api_models import WebhookDeleteResponse

class GeneralResponseType(Enum):
    type = 'generalResponseType'


class WebhookDelete(BaseModel):
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
    type: GeneralResponseType = Field(default=GeneralResponseType.type, alias='$type', description='тип данных')