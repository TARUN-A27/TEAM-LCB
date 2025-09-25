import { MapContainer, TileLayer, Marker, Popup, GeoJSON } from "react-leaflet";
import "leaflet/dist/leaflet.css";
export default function MapView({ center = [19.1190, 72.8970], aoi = null }) {
    return (
        <div style={{ height: "500px", width: "100%" }}>
            <MapContainer
                center={center}
                zoom={12}
                style={{ height: "100%", width: "100%" }}
            >
                {/*Base Map*/}
                <TileLayer
                    attribution='&copy; <a href="https://osm.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                {/* Marker at AOI center */}
                <Marker position={center}>
                    <Popup>Mumbai (demo AOI center)</Popup>
                </Marker>
                {/* AOI polygon overlay*/}
                {aoi && (
                    <GeoJSON
                        data={aoi}
                        style={{
                            colour: "orange",
                            weight: 2,
                            fillcolour: "orange",
                            fillOpacity: 0.15,
                        }}
                    />
                )}
            </MapContainer>
        </div>
    );
}