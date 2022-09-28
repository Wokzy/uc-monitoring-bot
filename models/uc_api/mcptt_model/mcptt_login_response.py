from __future__ import annotations

from pydantic import BaseModel, Field
from models.uc_api.base_models import UCUserType, MCPTTUser, McpttLoginResponseType


class MCPTTUserLoginResponse(BaseModel):
    uc_user: UCUserType
    mcptt_user: MCPTTUser
    _type: McpttLoginResponseType = Field(McpttLoginResponseType.type, alias='$type', description='тип данных')
