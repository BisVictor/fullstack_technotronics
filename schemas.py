from pydantic import BaseModel
from typing import Optional, List

#---АКБ---
class BatteryBase(BaseModel):
    name: str
    voltage: float
    capacity: float
    lifetime: int
    device_id: Optional[int] = None

class BatteryUpdate(BaseModel):
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
    batteries_len: Optional[int] = 0

class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    firmware_version: Optional[str] = None
    is_active: Optional[bool] = True    

class DeviceCreate(DeviceBase):
    pass

class DeviceDelete(DeviceCreate):
    message: str = "Device was deleted"

class Device(DeviceBase):
    id: int
    batteries: List[Battery] = []
