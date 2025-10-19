from fastapi import FastAPI, Depends, HTTPException, Path
from sqlalchemy.orm import Session
#from sqlalchemy.exc import IntegrityError
from typing import List
import schemas
from database import Base, engine, SessionLocal
import models
from models import Battery, Device

app = FastAPI()
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/get_all_batteries", response_model=List[schemas.BatteryBase])
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
def update_battery_by_id(battery_id: int = Path(..., title="Battery_id"),
                          battery_update: schemas.BatteryUpdete = None,
                            db: Session = Depends(get_db)):
    db_battery = db.query(Battery).filter(Battery.id == battery_id).first()
    if not db_battery:
        raise HTTPException(status_code=404, detail="Battery not found")

    # поля которые можно менять
    allowed = {"name", "voltage", "capacity", "lifetime", "device_id"}
    update_data = battery_update.dict(exclude_unset=True)

    # если передали device_id — можно доп. валидировать устройство
    if "device_id" in update_data and update_data["device_id"] is not None:
        device = db.query(models.Device).filter(models.Device.id == update_data["device_id"]).first()
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")
        if len(device.batteries) >= 5:
            raise HTTPException(status_code=400, detail="Device already has 5 batteries")

    # применяем только разрешённые поля
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
        raise HTTPException(status_code=404, detail="Battery not founf")
    db.delete(db_battery)
    db.commit()
    return db_battery

#---Device---
@app.get("/get_all_device", response_model=List[schemas.Device])
def get_all_device(db: Session = Depends(get_db)):
    db_device = db.query(Device).all()
    if not db_device:
        raise HTTPException(status_code=404, detail="No Device")
    return db_device
    

@app.get("/get_device_by_id/{device_id}", response_model=schemas.DeviceBase)
def get_device_by_id(device_id: int = Path(..., title="Device id"), db: Session = Depends(get_db)):
    db_device = db.query(Device).filter(Device.id == device_id).first()
    if not db_device:
        raise HTTPException(status_code=404, detail="Device not found")



    
    


 