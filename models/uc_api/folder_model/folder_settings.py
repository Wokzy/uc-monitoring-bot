from __future__ import annotations
from enum import Enum
from typing import Any, List, Optional, Union, Literal
from pydantic import BaseModel, Field, conint, constr


class SettingsType(Enum):
    type = 'settingsType'

class Settings(BaseModel):
    value: bool = Field(alias='integration/projects/support')

    type: SettingsType = Field(default=SettingsType.type, alias='$type', description='тип данных')