export type Tunnel = { id:number; code:string; name:string; sector:string; risk:string; workers:number; supervisor:string; inspection:string };
export type Sensor = { id:number; code:string; type:string; tunnel_id:number; value:number; unit:string; threshold:number; status:string; updated_at:string };
export type Alert = { id:number; title:string; severity:string; tunnel:string; message:string; status:string; assigned_to:string; created_at:string };
export type Hazard = { id:number; title:string; category:string; description:string; tunnel:string; priority:string; reporter:string; assigned_to:string; status:string; created_at:string };
export type Notification = { id:number; title:string; message:string; severity:string; tunnel:string; read:boolean; created_at:string };
