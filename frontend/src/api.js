import axios from "axios";
const BASE = "http://127.0.0.1:8000";
export const getDebugSample = () =>
    axios.get('${BASE}/debug-Sample');
export const computeFloodByLoc = (payload) =>
    axios.post('${BASE}/api/compute-flood-by-loc', payload);
