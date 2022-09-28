# -*- coding: utf-8 -*-

from __future__ import annotations

from pydantic import BaseModel, Field, conint
from models.uc_api.base_models import GeneralResponseType
from models.uc_api.base_models import ConferenceStartResponse as ConferenceStartResponse_1


class ConferenceStartResponse(BaseModel):
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
    payload: ConferenceStartResponse_1 = Field(description='Тело ответа')
    type: GeneralResponseType = Field(default=GeneralResponseType.type, alias='$type', description='тип данных')
