from app.models import *
from datetime import timedelta
def seed(db):
    if db.query(Tunnel).count():
        for sensor in db.query(Sensor).all():
            existing=db.query(Reading).filter(Reading.sensor_id==sensor.id).count()
            for i in range(max(0,12-existing)):
                db.add(Reading(sensor_id=sensor.id,value=round(sensor.value+(i-5.5)*0.012,2),recorded_at=now()-timedelta(minutes=(11-i)*5)))
        db.commit()
        return
    tunnels=[Tunnel(code=f'T-{i:02}',name=n,sector=s,risk=r,workers=w,supervisor=sp,inspection='2026-11-12') for i,(n,s,r,w,sp) in enumerate([('North Main','North','Safe',12,'A. Kumar'),('East Return','East','Warning',8,'S. Das'),('Panel 4B','Central','Critical',6,'R. Singh'),('South Development','South','Safe',9,'M. Roy'),('West Haulage','West','Safe',5,'P. Verma'),('Ventilation Drift','Central','Warning',3,'R. Singh')],1)]
    db.add_all(tunnels); db.flush()
    specs=[('CH4','Methane',0.42,'%',1.0),('CO','Carbon monoxide',18,'ppm',50),('O2','Oxygen',20.7,'%',19.5),('TEMP','Temperature',28.4,'°C',35),('RH','Humidity',64,'% RH',85),('VENT','Air velocity',1.8,'m/s',0.5)]
    for i,t in enumerate(tunnels):
        for j,(code,typ,val,unit,th) in enumerate(specs[:3] if i>2 else specs):
            v=val*(1.15 if t.risk=='Critical' and code=='CH4' else 1)
            db.add(Sensor(code=f'{code}-{t.code}',type=typ,tunnel_id=t.id,value=v,unit=unit,threshold=th,status='Critical' if v>=th else 'Normal'))
    db.add_all([Alert(title='Methane concentration elevated',severity='Critical',tunnel='Panel 4B',message='CH4 reading is above the illustrative demo threshold.',assigned_to='R. Singh'),Alert(title='Ventilation flow below advisory',severity='Warning',tunnel='East Return',message='Air velocity requires supervisor review.',assigned_to='S. Das')])
    db.add_all([Hazard(title='Loose roof material',category='Ground control',description='Fragments observed near support bay 12.',tunnel='East Return',priority='High',reporter='A. Kumar',assigned_to='S. Das',status='Under Review'),Hazard(title='Cable insulation wear',category='Electrical',description='Wear noted on trailing cable during routine walk-through.',tunnel='Panel 4B',priority='Medium',reporter='R. Singh',assigned_to='R. Singh',status='Assigned')])
    db.add_all([Worker(worker_id=f'W-{i:04}',name=n,designation=d,sector=s,shift='A / Day',supervisor=sp,emergency_contact=f'+91 98{i:08}',muster_point='North Portal Muster') for i,(n,d,s,sp) in enumerate([('Arjun Kumar','Mining Engineer','North','A. Kumar'),('Suman Das','Shift Supervisor','East','S. Das'),('Ravi Singh','Electrical Officer','Central','R. Singh'),('Mohan Roy','Ventilation Technician','South','M. Roy'),('Priya Verma','Safety Officer','West','P. Verma')],1)])
    db.add_all([Inspection(title='Weekly ground control review',tunnel='Panel 4B',inspector='R. Singh',scheduled='2026-11-14',status='Scheduled'),Inspection(title='Ventilation system check',tunnel='East Return',inspector='S. Das',scheduled='2026-11-13',status='In Progress')])
    db.add_all([Compliance(item=x,category=c,responsible=r,due_date=d,status=s,document=doc) for x,c,r,d,s,doc in [('Ventilation log review','Operations','S. Das','2026-11-18','Complete','ventilation-log.pdf'),('PPE inspection register','Worker safety','A. Kumar','2026-11-20','In Progress','—'),('Emergency drill record','Emergency readiness','R. Singh','2026-11-25','Pending','—'),('Equipment maintenance record','Maintenance','M. Roy','2026-11-28','Pending','maintenance.pdf')]])
    db.flush()
    for sensor in db.query(Sensor).all():
        for i in range(12):
            delta=round((i-5.5)*0.012,3)
            db.add(Reading(sensor_id=sensor.id,value=round(sensor.value+delta,2),recorded_at=now()-timedelta(minutes=(11-i)*5)))
    db.add(Notification(title='Demo system initialized',message='Fictional mine records loaded for demonstration.',severity='Info',tunnel='All sectors'))
    db.add(Activity(message='Demo records seeded for SIH26024 command centre.',actor='System',category='System')); db.commit()
