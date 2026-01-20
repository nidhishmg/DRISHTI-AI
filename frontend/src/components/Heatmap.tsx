"use client";

import { useEffect, useState } from "react";
import dynamic from "next/dynamic";
import "leaflet/dist/leaflet.css";

// Dynamic import to avoid SSR window is not defined error
const MapContainer = dynamic(() => import("react-leaflet").then((mod) => mod.MapContainer), { ssr: false });
const TileLayer = dynamic(() => import("react-leaflet").then((mod) => mod.TileLayer), { ssr: false });
const CircleMarker = dynamic(() => import("react-leaflet").then((mod) => mod.CircleMarker), { ssr: false });
const Popup = dynamic(() => import("react-leaflet").then((mod) => mod.Popup), { ssr: false });

const mockPoints = [
    { lat: 12.9716, lng: 77.5946, intensity: 0.9, title: "Bangalore: Pension API Failure" },
    { lat: 28.7041, lng: 77.1025, intensity: 0.7, title: "Delhi: Biometric Match Fail" },
    { lat: 19.0760, lng: 72.8777, intensity: 0.5, title: "Mumbai: Ration Server Down" },
    { lat: 25.5941, lng: 85.1376, intensity: 0.85, title: "Patna: Mid-day Meal Quality" },
    { lat: 22.5726, lng: 88.3639, intensity: 0.6, title: "Kolkata: PDS Exclusion" },
    { lat: 26.8467, lng: 80.9462, intensity: 0.8, title: "Lucknow: Scholarship Delays" }
];

export default function Heatmap() {
    const [mounted, setMounted] = useState(false);

    useEffect(() => {
        setMounted(true);
    }, []);

    if (!mounted) return <div className="h-[500px] w-full animate-pulse rounded-xl bg-muted/20" />;

    return (
        <div className="h-[500px] w-full overflow-hidden rounded-xl border border-white/10 shadow-2xl">
            <MapContainer
                center={[20.5937, 78.9629]}
                zoom={5}
                scrollWheelZoom={false}
                className="h-full w-full bg-slate-900"
            >
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
                    url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
                />
                {mockPoints.map((point, idx) => (
                    <CircleMarker
                        key={idx}
                        center={[point.lat, point.lng]}
                        radius={20 * point.intensity}
                        pathOptions={{
                            color: point.intensity > 0.8 ? "#ef4444" : point.intensity > 0.6 ? "#f97316" : "#eab308",
                            fillColor: point.intensity > 0.8 ? "#ef4444" : point.intensity > 0.6 ? "#f97316" : "#eab308",
                            fillOpacity: 0.6
                        }}
                    >
                        <Popup className="text-black">
                            <div className="font-bold">{point.title}</div>
                            <div className="text-xs">Intensity: {(point.intensity * 100).toFixed(0)}%</div>
                        </Popup>
                    </CircleMarker>
                ))}
            </MapContainer>
        </div>
    );
}
