from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional
from pathlib import Path
import uuid
from app.database import Base, engine, get_db
from app.models import *
from app.services.seed import seed
from app.schemas import Payload
Base.metadata.create_all(bind=engine)
with next(get_db()) as db: seed(db)
app=FastAPI(title='Coal Mine Smart Governance API',version='1.0.0',description='Fictional SIH26024 demonstration API')
app.add_middleware(CORSMiddleware,allow_origins=['http://localhost:5173','http://127.0.0.1:5173'],allow_credentials=True,allow_methods=['*'],allow_headers=['*'])
def serialize(obj):
    out={c.name:getattr(obj,c.name) for c in obj.__table__.columns}
    for k,v in out.items():
        if hasattr(v,'isoformat'): out[k]=v.isoformat()
    return out
def list_rows(model,db): return [serialize(x) for x in db.query(model).order_by(desc(model.id)).all()]
def log(db,msg,cat='Operations',actor='Control room'): db.add(Activity(message=msg,category=cat,actor=actor))
@app.get('/health')
def health(): return {'status':'ok','mode':'simulated demonstration','database':'sqlite'}
@app.get('/api/summary')
def summary(db:Session=Depends(get_db)):
    tunnels=db.query(Tunnel).all(); alerts=db.query(Alert).filter(Alert.status!='Resolved').count(); hazards=db.query(Hazard).filter(Hazard.status!='Verified').count(); tasks=db.query(Compliance).filter(Compliance.status!='Complete').count()
    return {'tunnels':len(tunnels),'safe':sum(t.risk=='Safe' for t in tunnels),'warning':sum(t.risk=='Warning' for t in tunnels),'critical':sum(t.risk=='Critical' for t in tunnels),'hazards':hazards,'pending_actions':alerts+tasks,'workers':sum(t.workers for t in tunnels),'compliance':round(db.query(Compliance).filter(Compliance.status=='Complete').count()/max(db.query(Compliance).count(),1)*100)}
@app.get('/api/tunnels')
def tunnels(db:Session=Depends(get_db)): return list_rows(Tunnel,db)
@app.get('/api/mines')
def mines(): return [{'id':1,'name':'Kestrel Mine','region':'Central India','mode':'Simulated demonstration'}]
@app.get('/api/supervisors')
def supervisors(db:Session=Depends(get_db)):
    return [{'name':name,'sectors':[t.sector for t in db.query(Tunnel).filter(Tunnel.supervisor==name).all()]} for name in sorted({t.supervisor for t in db.query(Tunnel).all()})]
@app.get('/api/sensors')
def sensors(db:Session=Depends(get_db)): return list_rows(Sensor,db)
@app.patch('/api/sensors/{item_id}')
def update_sensor(item_id:int,p:Payload,db:Session=Depends(get_db)):
    x=db.get(Sensor,item_id)
    if not x: raise HTTPException(404,'Sensor not found')
    if p.threshold is None or p.threshold<=0: raise HTTPException(422,'Threshold must be greater than zero')
    x.threshold=p.threshold; log(db,f'Illustrative demo threshold for {x.code} updated to {x.threshold} {x.unit}.','Simulation configuration'); db.commit(); return serialize(x)
@app.get('/api/readings')
def readings(sensor_id:Optional[int]=None,db:Session=Depends(get_db)):
    query=db.query(Reading)
    if sensor_id is not None: query=query.filter(Reading.sensor_id==sensor_id)
    rows=query.order_by(Reading.id.desc()).limit(720).all(); return [serialize(x) for x in reversed(rows)]
@app.post('/api/simulation/tick')
def tick(db:Session=Depends(get_db)):
    import random
    for s in db.query(Sensor).all():
        factor={'Methane':.08,'Carbon monoxide':3,'Oxygen':.25,'Temperature':1.1,'Humidity':2.2,'Air velocity':.12}.get(s.type,.5)
        s.value=max(0,round(s.value+random.uniform(-factor,factor),2)); s.status='Critical' if (s.type=='Oxygen' and s.value<s.threshold) or (s.type!='Oxygen' and s.type!='Air velocity' and s.value>=s.threshold) or (s.type=='Air velocity' and s.value<s.threshold) else 'Normal'; s.updated_at=now(); db.add(Reading(sensor_id=s.id,value=s.value))
    db.commit(); return list_rows(Sensor,db)
@app.post('/api/simulation/breach')
def breach(db:Session=Depends(get_db)):
    s=db.query(Sensor).filter(Sensor.type=='Methane').first()
    if not s: raise HTTPException(404,'Methane channel unavailable')
    t=db.get(Tunnel,s.tunnel_id); s.value=round(s.threshold*1.35,2); s.status='Critical'; s.updated_at=now(); t.risk='Critical'
    a=Alert(title='Simulated threshold breach — '+s.type,severity='Critical',tunnel=t.name,message=f'{s.type} reading {s.value}{s.unit} exceeded illustrative demo threshold {s.threshold}{s.unit}.',assigned_to=t.supervisor)
    db.add(a); db.flush(); db.add(Notification(title=a.title,message=a.message,severity='Critical',tunnel=t.name)); log(db,f'Simulated {s.type} threshold breach at {t.name}; alert #{a.id} created.','Emergency simulation'); db.add(Reading(sensor_id=s.id,value=s.value)); db.commit(); return {'sensor':serialize(s),'tunnel':serialize(t),'alert':serialize(a)}
@app.post('/api/simulation/reset')
def reset(db:Session=Depends(get_db)):
    for t in db.query(Tunnel).all(): t.risk='Safe'
    for s in db.query(Sensor).all():
        bases={'Methane':.42,'Carbon monoxide':18,'Oxygen':20.7,'Temperature':28.4,'Humidity':64,'Air velocity':1.8}; s.value=bases.get(s.type,s.value); s.status='Normal'; s.updated_at=now()
    log(db,'Sensor demo values reset to baseline.','Simulation'); db.commit(); return {'status':'reset','sensors':list_rows(Sensor,db)}
@app.get('/api/alerts')
def alerts(db:Session=Depends(get_db)): return list_rows(Alert,db)
@app.patch('/api/alerts/{item_id}')
def update_alert(item_id:int,p:Payload,db:Session=Depends(get_db)):
    x=db.get(Alert,item_id)
    if not x: raise HTTPException(404,'Alert not found')
    for k,v in p.model_dump(exclude_unset=True).items(): setattr(x,k,v)
    log(db,f'Alert #{item_id} updated: {p.model_dump(exclude_unset=True)}','Alert management'); db.commit(); return serialize(x)
@app.get('/api/hazards')
def hazards(db:Session=Depends(get_db)): return list_rows(Hazard,db)
@app.post('/api/hazards')
def create_hazard(p:Payload,db:Session=Depends(get_db)):
    data=p.model_dump(exclude_unset=True); x=Hazard(**{k:v for k,v in data.items() if k in Hazard.__table__.columns.keys()}); db.add(x); db.flush(); db.add(Notification(title='New hazard report',message=x.title,severity=x.priority,tunnel=x.tunnel)); log(db,f'Hazard #{x.id} reported: {x.title}','Hazard management'); db.commit(); return serialize(x)
@app.patch('/api/hazards/{item_id}')
def update_hazard(item_id:int,p:Payload,db:Session=Depends(get_db)):
    x=db.get(Hazard,item_id)
    if not x: raise HTTPException(404,'Hazard not found')
    for k,v in p.model_dump(exclude_unset=True).items(): setattr(x,k,v)
    log(db,f'Hazard #{item_id} updated','Hazard management'); db.commit(); return serialize(x)
@app.get('/api/workers')
def workers(db:Session=Depends(get_db)): return list_rows(Worker,db)
@app.get('/api/inspections')
def inspections(db:Session=Depends(get_db)): return list_rows(Inspection,db)
@app.post('/api/inspections')
def create_inspection(p:Payload,db:Session=Depends(get_db)):
    x=Inspection(**p.model_dump(exclude_unset=True)); db.add(x); log(db,'Inspection record created','Inspection management'); db.commit(); db.refresh(x); return serialize(x)
@app.get('/api/compliance')
def compliance(db:Session=Depends(get_db)): return list_rows(Compliance,db)
@app.patch('/api/compliance/{item_id}')
def update_compliance(item_id:int,p:Payload,db:Session=Depends(get_db)):
    x=db.get(Compliance,item_id)
    if not x: raise HTTPException(404,'Compliance item not found')
    for k,v in p.model_dump(exclude_unset=True).items(): setattr(x,k,v)
    log(db,f'Compliance item #{item_id} updated','Compliance'); db.commit(); return serialize(x)
@app.post('/api/compliance/{item_id}/document')
async def upload_document(item_id:int,file:UploadFile=File(...),db:Session=Depends(get_db)):
    x=db.get(Compliance,item_id)
    if not x: raise HTTPException(404,'Compliance item not found')
    if not file.filename: raise HTTPException(422,'Choose a file to upload')
    safe_name=Path(file.filename).name
    folder=Path(__file__).resolve().parents[1]/'data'/'uploads'; folder.mkdir(parents=True,exist_ok=True)
    stored=f'{uuid.uuid4().hex[:12]}_{safe_name}'; (folder/stored).write_bytes(await file.read())
    x.document=safe_name; log(db,f'Demo compliance document uploaded for item #{item_id}: {safe_name}','Compliance'); db.commit(); return serialize(x)
@app.get('/api/notifications')
def notifications(db:Session=Depends(get_db)): return list_rows(Notification,db)
@app.patch('/api/notifications/{item_id}')
def read_notification(item_id:int,db:Session=Depends(get_db)):
    x=db.get(Notification,item_id)
    if not x: raise HTTPException(404,'Notification not found')
    x.read=True; db.commit(); return serialize(x)
@app.get('/api/activity')
def activity(db:Session=Depends(get_db)): return list_rows(Activity,db)
@app.get('/api/reports/{report_type}')
def report(report_type:str,start:Optional[str]=None,end:Optional[str]=None,tunnel:Optional[str]=None,db:Session=Depends(get_db)):
    allowed={'daily-safety','weekly-hazards','monthly-inspections','sensor-monitoring','tunnel-risk','compliance'}
    if report_type not in allowed: raise HTTPException(404,'Unknown report')
    key={'daily-safety':'tunnels','weekly-hazards':'hazards','monthly-inspections':'inspections','sensor-monitoring':'sensors','tunnel-risk':'tunnels','compliance':'compliance'}[report_type]
    items={'tunnels':list_rows(Tunnel,db),'sensors':list_rows(Sensor,db),'alerts':list_rows(Alert,db),'hazards':list_rows(Hazard,db),'inspections':list_rows(Inspection,db),'compliance':list_rows(Compliance,db)}[key]
    if tunnel: items=[r for r in items if tunnel.lower() in str(r.get('name',r.get('tunnel',''))).lower()]
    if start or end:
        date_field='scheduled' if key=='inspections' else 'due_date' if key=='compliance' else 'created_at'
        items=[r for r in items if r.get(date_field) and (not start or str(r[date_field])[:10]>=start) and (not end or str(r[date_field])[:10]<=end)]
    return {'report_type':report_type,'generated_at':now().isoformat(),'summary':items}
@app.get('/api/activity-log')
def activity_log(db:Session=Depends(get_db)): return list_rows(Activity,db)
