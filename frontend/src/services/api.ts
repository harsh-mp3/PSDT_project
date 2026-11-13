import type { Resource, Row } from '../types'

// Frontend-only prototype store. No network requests or physical sensors are used.
const STORAGE_KEY = 'minesafe-demo-v1'
const HISTORY_KEY = `${STORAGE_KEY}-sensor-history`
type Store = Record<Resource, Row[]>
type ReadingSample = { id: string; tunnel: string; sensor: string; value: number; time: string }

const additionalWorkers = [
  ['1304','Rohan Kumar','Roof Support Technician','A','Day','A. Kumar','North Muster Point'],
  ['1305','Isha Verma','Survey Assistant','A','Night','A. Kumar','North Muster Point'],
  ['1306','Kabir Singh','Drill Operator','A','Day','A. Kumar','North Muster Point'],
  ['1307','Tara Joshi','First Aid Responder','A','Night','A. Kumar','North Muster Point'],
  ['1308','Aarav Das','Ventilation Technician','B','Night','S. Das','East Muster Point'],
  ['1309','Nisha Roy','Electrical Technician','B','Day','S. Das','East Muster Point'],
  ['1310','Vivaan Shah','Roof Support Technician','B','Night','S. Das','East Muster Point'],
  ['1311','Anaya Patel','Mine Surveyor','B','Day','S. Das','East Muster Point'],
  ['1312','Reyansh Gupta','Longwall Operator','C','Day','R. Singh','Central Muster Point'],
  ['1313','Diya Nair','Equipment Technician','C','Night','R. Singh','Central Muster Point'],
  ['1314','Aditya Rao','Emergency Response Officer','C','Day','R. Singh','Central Muster Point'],
  ['1315','Myra Khan','Conveyor Operator','D','Day','M. Ali','West Muster Point'],
  ['1316','Arnav Mehta','Ground Control Technician','D','Night','M. Ali','West Muster Point'],
  ['1317','Kiara Sen','First Aid Responder','D','Day','M. Ali','West Muster Point'],
  ['1318','Ishaan Roy','Methane Monitoring Technician','E','Night','P. Roy','South Muster Point'],
  ['1319','Aditi Sharma','Pump Operator','E','Day','P. Roy','South Muster Point'],
  ['1320','Krish Malhotra','Mine Electrician','E','Night','P. Roy','South Muster Point'],
  ['1321','Saanvi Kapoor','Ventilation Assistant','F','Day','N. Sharma','South Return Muster'],
  ['1322','Dhruv Bose','Haulage Operator','F','Night','N. Sharma','South Return Muster'],
  ['1323','Meera Iyer','Safety Assistant','F','Day','N. Sharma','South Return Muster'],
].map(([workerId,name,designation,tunnel,shift,supervisor,muster],index)=>({id:5+index,worker_id:`JCF-${workerId}`,name,designation,tunnel,shift,supervisor,emergency_contact:`+91 90000 ${20104+index}`,muster}))

const initial: Store = {
  mines: [{ id: 1, name: 'Jharia Coalfield', code: 'JCF-01' }],
  tunnels: [
    { id: 1, code: 'A', name: 'North Main', level: 'Level 1 · 240 m', risk: 'Normal', supervisor: 'A. Kumar', workers: 18 },
    { id: 2, code: 'B', name: 'East Return', level: 'Level 1 · 265 m', risk: 'Warning', supervisor: 'S. Das', workers: 14 },
    { id: 3, code: 'C', name: 'Central Longwall', level: 'Level 2 · 310 m', risk: 'Normal', supervisor: 'R. Singh', workers: 22 },
    { id: 4, code: 'D', name: 'West Development', level: 'Level 2 · 295 m', risk: 'Normal', supervisor: 'M. Ali', workers: 11 },
    { id: 5, code: 'E', name: 'South Main', level: 'Level 3 · 340 m', risk: 'Critical', supervisor: 'P. Roy', workers: 16 },
    { id: 6, code: 'F', name: 'South Return', level: 'Level 3 · 355 m', risk: 'Normal', supervisor: 'N. Sharma', workers: 9 },
  ],
  sensors: [
    { id: 1, type: 'CH4', name: 'Methane', tunnel: 'A', value: 0.42, unit: '%', status: 'Normal' },
    { id: 2, type: 'CO', name: 'Carbon monoxide', tunnel: 'A', value: 8, unit: 'ppm', status: 'Normal' },
    { id: 3, type: 'O2', name: 'Oxygen', tunnel: 'A', value: 20.8, unit: '%', status: 'Normal' },
    { id: 4, type: 'TEMP', name: 'Temperature', tunnel: 'A', value: 27.3, unit: '°C', status: 'Normal' },
    { id: 5, type: 'HUM', name: 'Humidity', tunnel: 'A', value: 68, unit: '%', status: 'Normal' },
    { id: 6, type: 'AIR', name: 'Ventilation', tunnel: 'A', value: 1.8, unit: 'm/s', status: 'Normal' },
    ...['B', 'C', 'D', 'E', 'F'].flatMap((tunnel, ti) => [
      { id: 10 + ti * 6, type: 'CH4', name: 'Methane', tunnel, value: tunnel === 'E' ? 1.08 : 0.35 + ti * 0.08, unit: '%', status: tunnel === 'E' ? 'Critical' : 'Normal' },
      { id: 11 + ti * 6, type: 'CO', name: 'Carbon monoxide', tunnel, value: 7 + ti, unit: 'ppm', status: 'Normal' },
      { id: 12 + ti * 6, type: 'O2', name: 'Oxygen', tunnel, value: 20.5, unit: '%', status: 'Normal' },
      { id: 13 + ti * 6, type: 'TEMP', name: 'Temperature', tunnel, value: 26 + ti, unit: '°C', status: 'Normal' },
      { id: 14 + ti * 6, type: 'HUM', name: 'Humidity', tunnel, value: 65 + ti, unit: '%', status: 'Normal' },
      { id: 15 + ti * 6, type: 'AIR', name: 'Ventilation', tunnel, value: 1.4 + ti * 0.1, unit: 'm/s', status: 'Normal' },
    ]),
  ],
  alerts: [
    { id: 1, title: 'Methane reading above demo threshold', tunnel: 'E', severity: 'Critical', source: 'CH4 sensor', assigned: 'P. Roy', status: 'Acknowledged', time: new Date(Date.now() - 3600000).toISOString(), notes: '' },
    { id: 2, title: 'Ventilation trend requires review', tunnel: 'B', severity: 'Warning', source: 'AIR sensor', assigned: 'S. Das', status: 'New', time: new Date(Date.now() - 7200000).toISOString(), notes: '' },
  ],
  hazards: [
    { id: 1, title: 'Loose material near support frame', category: 'Ground control', description: 'Demo observation for follow-up inspection.', tunnel: 'B', priority: 'High', reporter: 'S. Das', assigned: 'S. Das', date: new Date().toISOString().slice(0, 10), status: 'Under Review' },
    { id: 2, title: 'Water accumulation at crosscut', category: 'Housekeeping', description: 'Illustrative fictional hazard record.', tunnel: 'D', priority: 'Medium', reporter: 'M. Ali', assigned: 'M. Ali', date: new Date().toISOString().slice(0, 10), status: 'Assigned' },
  ],
  workers: [
    { id: 1, worker_id: 'JCF-1042', name: 'Arjun Mehta', designation: 'Mining Supervisor', tunnel: 'A', shift: 'Day', supervisor: 'A. Kumar', emergency_contact: '+91 90000 10042', muster: 'North Muster Point' },
    { id: 2, worker_id: 'JCF-1088', name: 'Sana Khan', designation: 'Ventilation Technician', tunnel: 'B', shift: 'Day', supervisor: 'S. Das', emergency_contact: '+91 90000 10088', muster: 'East Muster Point' },
    { id: 3, worker_id: 'JCF-1116', name: 'Dev Patel', designation: 'Electrical Technician', tunnel: 'C', shift: 'Night', supervisor: 'R. Singh', emergency_contact: '+91 90000 10116', muster: 'Central Muster Point' },
    { id: 4, worker_id: 'JCF-1201', name: 'Mira Das', designation: 'Safety Officer', tunnel: 'E', shift: 'Day', supervisor: 'P. Roy', emergency_contact: '+91 90000 10201', muster: 'South Muster Point' },
    ...additionalWorkers,
  ],
  inspections: [
    { id: 1, title: 'Weekly ventilation walkthrough', tunnel: 'B', inspector: 'S. Das', date: new Date(Date.now() + 86400000).toISOString().slice(0, 10), status: 'Scheduled', findings: '', corrective_action: '' },
    { id: 2, title: 'Ground support review', tunnel: 'E', inspector: 'P. Roy', date: new Date(Date.now() - 86400000).toISOString().slice(0, 10), status: 'Findings Recorded', findings: 'Demo follow-up required', corrective_action: 'Review support plan' },
  ],
  compliance: [
    { id: 1, title: 'Ventilation inspection log review', category: 'Internal checklist', owner: 'A. Kumar', due: new Date(Date.now() + 86400000 * 4).toISOString().slice(0, 10), priority: 'High', status: 'Pending' },
    { id: 2, title: 'Emergency drill record', category: 'Internal checklist', owner: 'S. Das', due: new Date(Date.now() + 86400000 * 8).toISOString().slice(0, 10), priority: 'Medium', status: 'In Progress' },
    { id: 3, title: 'Shift handover register', category: 'Document register', owner: 'P. Roy', due: new Date().toISOString().slice(0, 10), priority: 'Low', status: 'Complete' },
  ],
  notifications: [{ id: 1, title: 'Demo methane alert acknowledged', message: 'Supervisor P. Roy acknowledged the illustrative threshold event.', tunnel: 'E', severity: 'Critical', read: false, time: new Date(Date.now() - 3600000).toISOString() }],
  activity: [{ id: 1, title: 'Demo workspace initialized', detail: 'Fictional local records loaded.', time: new Date().toISOString() }],
}

function readStore(): Store {
  try {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved) {
      const restored = { ...structuredClone(initial), ...JSON.parse(saved) } as Store
      const savedWorkerIds = new Set((restored.workers || []).map(worker => worker.worker_id))
      const missingSeedWorkers = initial.workers.filter(worker => !savedWorkerIds.has(worker.worker_id))
      if (missingSeedWorkers.length) {
        restored.workers = [...(restored.workers || []), ...missingSeedWorkers]
        localStorage.setItem(STORAGE_KEY, JSON.stringify(restored))
      }
      return restored
    }
  } catch { /* Use the seed data if browser storage is unavailable or malformed. */ }
  return structuredClone(initial)
}
function writeStore(store: Store) {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(store)) } catch { /* Private browsing may disable storage. */ }
}
let store = readStore()
function readHistory(): ReadingSample[] {
  try { return JSON.parse(localStorage.getItem(HISTORY_KEY) || '[]') as ReadingSample[] } catch { return [] }
}
let history = readHistory()
const persist = () => writeStore(store)
const stamp = () => new Date().toISOString()
const persistHistory = () => { try { localStorage.setItem(HISTORY_KEY, JSON.stringify(history)) } catch { /* Browser storage can be unavailable in private mode. */ } }
const recordReadings = (time = stamp()) => {
  for (const sensor of store.sensors) history.push({ id: `${sensor.tunnel}-${sensor.type}-${Date.now()}-${Math.random()}`, tunnel: String(sensor.tunnel), sensor: String(sensor.type), value: Number(sensor.value), time })
  history = history.slice(-36 * 120)
  persistHistory()
}
if (history.length === 0) {
  const now = Date.now()
  for (const sensor of store.sensors) {
    const amp = sensor.type === 'CO' ? 0.38 : sensor.type === 'TEMP' ? 0.24 : sensor.type === 'HUM' ? 0.9 : sensor.type === 'O2' ? 0.055 : 0.025
    for (let i = 29; i >= 0; i--) {
      const value = Math.max(0, Number((Number(sensor.value) + Math.sin(i * 0.53 + Number(sensor.id)) * amp + Math.cos(i * 0.21) * amp * 0.35).toFixed(2)))
      history.push({ id: `${sensor.tunnel}-${sensor.type}-seed-${i}`, tunnel: String(sensor.tunnel), sensor: String(sensor.type), value, time: new Date(now - i * 5000).toISOString() })
    }
  }
  persistHistory()
}
const log = (title: string, detail: string) => { store.activity.unshift({ id: Date.now(), title, detail, time: stamp() }); store.activity = store.activity.slice(0, 100) }
const notify = (title: string, message: string, tunnel: string, severity = 'Info') => store.notifications.unshift({ id: Date.now() + Math.random(), title, message, tunnel, severity, read: false, time: stamp() })

export const api = { defaults: { baseURL: 'local demo storage' } }
export const list = async (resource: Resource) => store[resource].map(row => ({ ...row }))
export const create = async (resource: Resource, data: Record<string, unknown>) => {
  const row = { id: Date.now(), ...data } as Row
  store[resource].unshift(row)
  const tunnel = String(data.tunnel || 'A')
  if (resource === 'hazards') { log('Hazard reported', `${data.title || 'New hazard'} · Section ${tunnel}`); notify('New hazard reported', String(data.title || 'A hazard was registered.'), tunnel, String(data.priority || 'Warning')) }
  else if (resource === 'inspections') log('Inspection scheduled', `${data.title || 'Inspection'} · Section ${tunnel}`)
  else if (resource === 'compliance') log('Compliance action added', String(data.title || 'New internal checklist item'))
  persist(); return { ...row }
}
export const update = async (resource: Resource, id: number, data: Record<string, unknown>) => {
  const index = store[resource].findIndex(row => row.id === id)
  if (index < 0) throw new Error('Record not found')
  store[resource][index] = { ...store[resource][index], ...data }
  const row = store[resource][index]
  if (resource === 'alerts' && data.status) log(`Alert ${String(data.status).toLowerCase()}`, String(row.title || `Alert ${id}`))
  if (resource === 'compliance' && data.status === 'Complete') { log('Compliance action completed', String(row.title)); notify('Compliance action completed', String(row.title), String(row.tunnel || 'A')) }
  if (data.assigned) { log('Supervisor assigned', `${String(data.assigned)} · ${String(row.title || resource)}`); notify('Action assigned', `${String(row.title || resource)} assigned to ${String(data.assigned)}.`, String(row.tunnel || 'A'), 'Warning') }
  persist(); return { ...row }
}
export const simulate = async (tunnel: string, sensor: string, threshold?: number) => {
  const reading = store.sensors.find(row => row.tunnel === tunnel && row.type === sensor)
  if (!reading) throw new Error('Sensor channel not found')
  const configured = Number(threshold || 1)
  reading.value = Number((configured * 1.12).toFixed(2)); reading.status = 'Critical'; reading.updated = stamp()
  recordReadings(reading.updated)
  const target = store.tunnels.find(row => row.code === tunnel)
  if (target) target.risk = 'Critical'
  const title = `${sensor} demo threshold breach`
  store.alerts.unshift({ id: Date.now(), title, tunnel, severity: 'Critical', source: `${sensor} sensor`, assigned: target?.supervisor || 'Unassigned', status: 'New', time: stamp(), notes: '' })
  notify('Critical simulated sensor event', `${sensor} reading exceeded the illustrative threshold in Section ${tunnel}.`, tunnel, 'Critical')
  log('Threshold event simulated', `${sensor} · Section ${tunnel} · ${reading.value} ${reading.unit}`)
  persist(); return { reading: { ...reading }, tunnel: target }
}
export const resetSimulation = async () => {
  store = structuredClone(initial)
  persist()
  history = []
  const now = Date.now()
  for (const sensor of store.sensors) {
    for (let i = 29; i >= 0; i--) history.push({ id: `${sensor.tunnel}-${sensor.type}-seed-${i}`, tunnel: String(sensor.tunnel), sensor: String(sensor.type), value: Number(sensor.value), time: new Date(now - i * 5000).toISOString() })
  }
  persistHistory()
  return true
}
export const getReadings = async () => ({ items: store.sensors.map(row => ({ ...row, sensor: row.type, time: row.updated || stamp() })), history: history.map(point => ({ ...point })), simulated: true })
export const tickSimulation = async () => {
  store.sensors = store.sensors.map(row => {
    if (row.status === 'Critical') return row
    const delta = (Math.random() - 0.5) * (row.type === 'CO' ? 0.9 : 0.035)
    const value = Math.max(0, Number((Number(row.value) + delta).toFixed(2)))
    return { ...row, value, updated: stamp() }
  })
  recordReadings()
  persist()
}
