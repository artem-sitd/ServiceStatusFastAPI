from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime


class ServiceSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int | None = None
    name: str
    description: str


class ServiceStatusUpdate(BaseModel):
    status: str


class ServiceStatusSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int | None = None
    service_id: int
    status: str
    timestamp: datetime
