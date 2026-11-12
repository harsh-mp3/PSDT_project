from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from app.database import Base
def now(): return datetime.now(timezone.utc).replace(tzinfo=None)
class Tunnel(Base):
    __tablename__='tunnels'; id:Mapped[int]=mapped_column(Integer,primary_key=True); code:Mapped[str]=mapped_column(String,unique=True); name:Mapped[str]=mapped_column(String); sector:Mapped[str]=mapped_column(String); risk:Mapped[str]=mapped_column(String,default='Safe'); workers:Mapped[int]=mapped_column(Integer,default=0); supervisor:Mapped[str]=mapped_column(String); inspection:Mapped[str]=mapped_column(String)
class Sensor(Base):
    __tablename__='sensors'; id:Mapped[int]=mapped_column(Integer,primary_key=True); code:Mapped[str]=mapped_column(String,unique=True); type:Mapped[str]=mapped_column(String); tunnel_id:Mapped[int]=mapped_column(ForeignKey('tunnels.id')); value:Mapped[float]=mapped_column(Float); unit:Mapped[str]=mapped_column(String); threshold:Mapped[float]=mapped_column(Float); status:Mapped[str]=mapped_column(String,default='Normal'); updated_at:Mapped[datetime]=mapped_column(DateTime,default=now)
class Reading(Base):
    __tablename__='readings'; id:Mapped[int]=mapped_column(Integer,primary_key=True); sensor_id:Mapped[int]=mapped_column(ForeignKey('sensors.id')); value:Mapped[float]=mapped_column(Float); recorded_at:Mapped[datetime]=mapped_column(DateTime,default=now)
class Alert(Base):
    __tablename__='alerts'; id:Mapped[int]=mapped_column(Integer,primary_key=True); title:Mapped[str]=mapped_column(String); severity:Mapped[str]=mapped_column(String); tunnel:Mapped[str]=mapped_column(String); message:Mapped[str]=mapped_column(Text); status:Mapped[str]=mapped_column(String,default='Open'); assigned_to:Mapped[str]=mapped_column(String); notes:Mapped[str]=mapped_column(Text,default=''); created_at:Mapped[datetime]=mapped_column(DateTime,default=now)
class Hazard(Base):
    __tablename__='hazards'; id:Mapped[int]=mapped_column(Integer,primary_key=True); title:Mapped[str]=mapped_column(String); category:Mapped[str]=mapped_column(String); description:Mapped[str]=mapped_column(Text); tunnel:Mapped[str]=mapped_column(String); priority:Mapped[str]=mapped_column(String); reporter:Mapped[str]=mapped_column(String); assigned_to:Mapped[str]=mapped_column(String); status:Mapped[str]=mapped_column(String,default='Reported'); created_at:Mapped[datetime]=mapped_column(DateTime,default=now)
class Worker(Base):
    __tablename__='workers'; id:Mapped[int]=mapped_column(Integer,primary_key=True); worker_id:Mapped[str]=mapped_column(String,unique=True); name:Mapped[str]=mapped_column(String); designation:Mapped[str]=mapped_column(String); sector:Mapped[str]=mapped_column(String); shift:Mapped[str]=mapped_column(String); supervisor:Mapped[str]=mapped_column(String); emergency_contact:Mapped[str]=mapped_column(String); muster_point:Mapped[str]=mapped_column(String)
class Inspection(Base):
    __tablename__='inspections'; id:Mapped[int]=mapped_column(Integer,primary_key=True); title:Mapped[str]=mapped_column(String); tunnel:Mapped[str]=mapped_column(String); inspector:Mapped[str]=mapped_column(String); scheduled:Mapped[str]=mapped_column(String); status:Mapped[str]=mapped_column(String); observations:Mapped[str]=mapped_column(Text,default=''); findings:Mapped[str]=mapped_column(Text,default=''); checklist:Mapped[str]=mapped_column(Text,default='')
class Compliance(Base):
    __tablename__='compliance'; id:Mapped[int]=mapped_column(Integer,primary_key=True); item:Mapped[str]=mapped_column(String); category:Mapped[str]=mapped_column(String); responsible:Mapped[str]=mapped_column(String); due_date:Mapped[str]=mapped_column(String); status:Mapped[str]=mapped_column(String); document:Mapped[str]=mapped_column(String,default='—')
class Notification(Base):
    __tablename__='notifications'; id:Mapped[int]=mapped_column(Integer,primary_key=True); title:Mapped[str]=mapped_column(String); message:Mapped[str]=mapped_column(Text); severity:Mapped[str]=mapped_column(String); tunnel:Mapped[str]=mapped_column(String); read:Mapped[bool]=mapped_column(Boolean,default=False); created_at:Mapped[datetime]=mapped_column(DateTime,default=now)
class Activity(Base):
    __tablename__='activity'; id:Mapped[int]=mapped_column(Integer,primary_key=True); message:Mapped[str]=mapped_column(Text); actor:Mapped[str]=mapped_column(String); category:Mapped[str]=mapped_column(String); created_at:Mapped[datetime]=mapped_column(DateTime,default=now)
