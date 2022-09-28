from __future__ import annotations
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, conint
from models.uc_api.base_models import ImageType, Attachment, Type, Type4
from models.uc_api.uc_api_models import WebhookUpdateResponse

class WebhookData(BaseModel):
    text: str
    avatar_url: Optional[str]
    nickname: Optional[str]
    chat_id: Optional[str]