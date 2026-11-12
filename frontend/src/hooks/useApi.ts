import { useCallback, useEffect, useState } from 'react';
import { get } from '../services/api';
export function useApi<T>(path:string, refreshKey=0) { const [data,setData]=useState<T|null>(null); const [loading,setLoading]=useState(true); const [error,setError]=useState(''); const reload=useCallback(()=>{setLoading(true);get<T>(path).then(v=>{setData(v);setError('')}).catch(e=>setError(e.message)).finally(()=>setLoading(false))},[path]); useEffect(()=>{reload()},[reload,refreshKey]); return {data,loading,error,reload,setData}; }
