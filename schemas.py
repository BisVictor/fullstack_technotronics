from pydantic import BaseModel
from typing import Optional, List

#---АКБ---
class BatteryBase(BaseModel):
    name: str
    voltage: float
    capacity: float
    lifetime: int
    device_id: Optional[int] = None

class BatteryUpdete(BaseModel):
    name: Optional[str] = None
    voltage: Optional[float] = None
    capacity: Optional[float] = None
    lifetime: Optional[int] = None
    device_id: Optional[int] = None

class BatteryCreate(BatteryBase):
    pass

class BatteryDelete(BatteryCreate):
    message: str = "Battery was deleted"

class Battery(BatteryBase):
    id: int

#---Устройство---
class DeviceBase(BaseModel):
    name: str
    firmware_version: str
    is_active: bool = True

class DeviceCreate(DeviceBase):
    pass

class Device(DeviceBase):
    id: int
    batteries: List[Battery] = []
