from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class DataModel(BaseModel):
    identifier: str
    extenders: List[str]
    extensions: Optional[dict]

class DataPoint(BaseModel):
    inward: str
    outward: str
    port: int
    type: str


class ExtensionParams(dict):
    pass

class Extension(BaseModel):
    name: str
    params: ExtensionParams


class DataQuery(BaseModel):
    version: str
    point: DataPoint
    models: List[DataModel]


class ServiceType(str, Enum):
    DATA = "DATA"
    PROVIDER = "PROVIDER"
    SERVICE = "SERVICE"

class Service(BaseModel):
    types: List[ServiceType]
    inward: str
    outward: str
    port: int
    name: str
    version: str
    dependencies: Optional[List[str]]
    
 