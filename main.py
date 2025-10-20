from fastapi import FastAPI, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import List
import schemas
from database import Base, engine, SessionLocal
import models
from models import Battery, Device
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#---статистика---
@app.get("/stats")
def stats(db: Session = Depends(get_db)):
    count_devices = db.query(Device).count()
    count_batteries = db.query(Battery).count()
    return{
        "devices_total": count_devices,
        "batteries_total": count_batteries
    }

@app.put("/link_battery/{battery_id}/{device_id}")
def link_battery(battery_id: int = Path(..., title="Battery_id"),
                 device_id: int = Path(..., title="Device_id"),
                 db: Session = Depends(get_db)):
    db_battery = db.query(Battery).filter(Battery.id == battery_id).first()
    if not db_battery:
        raise HTTPException(status_code=404, detail="No battery")
    db_device = db.query(Device).filter(Device.id == device_id).first()
    if not db_device:
        raise HTTPException(status_code=404, detail="No device")
    
    if len(db_device.batteries) >= 5:
        raise HTTPException(status_code=400, detail="Device already has 5 batteries")
    
    db_battery.device_id = device_id

    try:
        db.commit()
        db.refresh(db_battery)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error linking battery: {str(e)}")

    return {"message": f"Battery {battery_id} linked to Device {device_id}"}


@app.get("/get_all_batteries", response_model=List[schemas.Battery])
def get_all_batteries(db: Session = Depends(get_db)):
    db_batteries = db.query(Battery).all()
    if not db_batteries:
        raise HTTPException(status_code=404, detail="No battery")
    return db_batteries

@app.get("/get_battery_by_id/{battery_id}", response_model=schemas.Battery)
def get_battery_by_id(battery_id: int = Path(..., title="Battery_id"), db: Session = Depends(get_db)):    
    battery = db.query(Battery).filter(Battery.id == battery_id).first()
    if not battery:
        raise HTTPException(status_code=404, detail="Battery not found")
    return battery

@app.post("/add_new_battery", response_model=schemas.Battery)
def add_new_battery(battery: schemas.BatteryCreate, db: Session = Depends(get_db)):    
    if battery.device_id:
        device = db.query(models.Device).filter(models.Device.id == battery.device_id).first()
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")
        if len(device.batteries) >= 5:
            raise HTTPException(status_code=400, detail="Device already has 5 batteries")
        
    db_battery = Battery(
        name=battery.name,
        voltage=battery.voltage,
        capacity=battery.capacity,
        lifetime=battery.lifetime,
        device_id=battery.device_id
    )
    try:
        db.add(db_battery)
        db.commit()
        db.refresh(db_battery)  # обновляем объект, чтобы получить id
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating battery: {str(e)}")

    return db_battery

@app.put("/update_battery_by_id/{battery_id}", response_model=schemas.BatteryBase)
def update_battery_by_id(
    battery_id: int = Path(..., title="Battery id"),
    battery_update: schemas.BatteryUpdate = None,
    db: Session = Depends(get_db)
):
    # Находим батарею по ID
    db_battery = db.query(models.Battery).filter(models.Battery.id == battery_id).first()
    if not db_battery:
        raise HTTPException(status_code=404, detail="Battery not found")

    # Список разрешённых для обновления полей
    allowed = {"name", "voltage", "capacity", "lifetime", "device_id"}
    update_data = battery_update.dict(exclude_unset=True)

    # Проверка device_id
    if "device_id" in update_data:
        device_id = update_data["device_id"]
        if device_id != 0:  # если не 0 — проверяем, что устройство существует
            device = db.query(models.Device).filter(models.Device.id == device_id).first()
            if not device:
                raise HTTPException(status_code=404, detail="Device not found")
            if len(device.batteries) >= 5:
                raise HTTPException(status_code=400, detail="Device already has 5 batteries")
        # если device_id == 0 — просто разрешаем записать 0 (без проверки)

    # Обновляем только разрешённые поля
    for key, value in update_data.items():
        if key in allowed:
            setattr(db_battery, key, value)

    try:
        db.commit()
        db.refresh(db_battery)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating battery: {str(e)}")

    return db_battery


@app.delete("/delete_battery_by_id/{battery_id}", response_model=schemas.BatteryDelete)
def delete_battery_by_id(battery_id: int = Path(..., title="Battery_id"), db: Session = Depends(get_db)):
    db_battery = db.query(Battery).filter(Battery.id == battery_id).first()
    if not db_battery:
        raise HTTPException(status_code=404, detail="Battery not found")
    db.delete(db_battery)
    db.commit()
    return db_battery

#---Device---
@app.get("/get_all_device", response_model=List[schemas.Device])
def get_all_device(db: Session = Depends(get_db)):
    devices = db.query(Device).all()
    if not devices:
        raise HTTPException(status_code=404, detail="No Device")
    result = []
    for device in devices:
        count_batteries = len(device.batteries)
        result.append(schemas.Device(
            id=device.id,
            name = device.name,
            firmware_version = device.firmware_version,
            is_active = device.is_active,
            batteries_len = count_batteries
        ))
    
    return result
    

@app.get("/get_device_by_id/{device_id}", response_model=schemas.Device)
def get_device_by_id(device_id: int = Path(..., title="Device id"), db: Session = Depends(get_db)):
    db_device = db.query(Device).filter(Device.id == device_id).first()
    if not db_device:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device
    
@app.post("/add_new_device", response_model=schemas.Device)
def add_new_device(new_devie: schemas.DeviceCreate, db: Session = Depends(get_db)):
    db_device = models.Device(
        name=new_devie.name,
        firmware_version=new_devie.firmware_version,
        is_active= new_devie.is_active
    )
    try:
        db.add(db_device)
        db.commit()
        db.refresh(db_device)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating device: {str(e)}")
    
    return db_device

@app.put("/update_device_by_id/{device_id}", response_model=schemas.DeviceBase)
def update_device_by_id(device_id: int = Path(..., title="Device id"),
                        update_device: schemas.DeviceUpdate = None,
                        db: Session = Depends(get_db)
                        ):    
    db_device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if not db_device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    update_data = update_device.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_device, key, value)
    
    try:
        db.commit()
        db.refresh(db_device)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating device: {str(e)}")
    
    return db_device

@app.delete("/delete_device_by_id{device_id}", response_model=schemas.DeviceDelete)
def delete_device_by_id(device_id: int = Path(..., title="Device_id"), db: Session = Depends(get_db)):
    db_device = db.query(Device).filter(Device.id == device_id).first()
    if not db_device:
        raise HTTPException(status_code=404, detail="Device not found")
    db.delete(db_device)
    db.commit()
    return db_device