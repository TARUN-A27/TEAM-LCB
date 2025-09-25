// src/App.jsx
import { useState } from "react";
import axios from "axios";
import MapView from "./components/MapView"; // optional component; see notes below
import "./App.css";

function App() {
  const [debugData, setDebugData] = useState(null);
  const [aoi, setAoi] = useState(null);
  const [loading, setLoading] = useState(false);

  // Fetch the simple debug endpoint
  const fetchDebugSample = async () => {
    setLoading(true);
    try {
      const res = await axios.get("http://127.0.0.1:8000/debug-sample");
      setDebugData(res.data);
    } catch (err) {
      console.error("Error fetching debug-sample:", err);
      alert("Error fetching debug-sample (see console).");
    } finally {
      setLoading(false);
    }
  };

  // Call compute-flood-by-loc and display returned AOI GeoJSON
  const runCompute = async () => {
    setLoading(true);
    try {
      const payload = {
        lat: 19.1190,
        lon: 72.8970,
        radius_m: 500,
        rainfall_mm: 50,
      };
      const res = await axios.post("http://127.0.0.1:8000/api/compute-flood-by-loc", payload);
      // API returns { aoi_geojson, dem_info, debug }
      setAoi(res.data.aoi_geojson);
    } catch (err) {
      console.error("Error computing AOI/DEM:", err);
      alert("Error computing AOI/DEM (see console).");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App" style={{ padding: 16 }}>
      <h1>TEAM-LCB Flood Demo</h1>

      <div style={{ marginBottom: 12 }}>
        <button onClick={fetchDebugSample} disabled={loading}>
          {loading ? "Loading..." : "Fetch Debug Sample"}
        </button>

        <button onClick={runCompute} disabled={loading} style={{ marginLeft: 8 }}>
          {loading ? "Running..." : "Compute AOI + DEM"}
        </button>
      </div>

      {debugData && (
        <div className="debug-panel" style={{ marginBottom: 12 }}>
          <h2>Debug Sample Response</h2>
          <pre style={{ maxHeight: 200, overflow: "auto" }}>{JSON.stringify(debugData, null, 2)}</pre>
        </div>
      )}

      <div style={{ marginTop: 12 }}>
        {/* MapView is an optional component. If you don't have it, you can inline the MapContainer here. */}
        <MapView center={[19.1190, 72.8970]} aoi={aoi} />
      </div>
    </div>
  );
}

export default App;
