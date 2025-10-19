from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    firmware_version = Column(String)
    is_active = Column(Boolean, default=True)

    batteries = relationship("Battery", back_populates="device")

class Battery(Base):
    __tablename__ = "batteries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    voltage = Column(Float)
    capacity = Column(Float)
    lifetime = Column(Integer)

    device_id = Column(Integer, ForeignKey("devices.id"))
    device = relationship("Device", back_populates="batteries")