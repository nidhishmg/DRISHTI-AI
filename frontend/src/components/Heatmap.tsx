"use client";

import { useEffect, useState } from "react";
import dynamic from "next/dynamic";
import "leaflet/dist/leaflet.css";

// Dynamic import to avoid SSR window is not defined error
const MapContainer = dynamic(() => import("react-leaflet").then((mod) => mod.MapContainer), { ssr: false });
const TileLayer = dynamic(() => import("react-leaflet").then((mod) => mod.TileLayer), { ssr: false });
const CircleMarker = dynamic(() => import("react-leaflet").then((mod) => mod.CircleMarker), { ssr: false });
const Popup = dynamic(() => import("react-leaflet").then((mod) => mod.Popup), { ssr: false });

import { Cluster } from "@/types";

interface HeatmapProps {
    clusters: Cluster[];
}

// Helper to get coordinates from cluster (mocking since backend doesn't send lat/lng yet)
function getClusterCoords(cluster: Cluster) {
    // Deterministic mock based on title char code
    const seed = cluster.title.charCodeAt(0);
    const lat = 20 + (seed % 10);
    const lng = 78 + (seed % 10);
    return { lat, lng };
}


export default function Heatmap({ clusters = [] }: HeatmapProps) {
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
                />
                {clusters.map((cluster, idx) => {
                    const coords = getClusterCoords(cluster);
                    const intensity = (cluster.confidence_score || 0.5);
                    return (
                        <CircleMarker
                            key={idx}
                            center={[coords.lat, coords.lng]}
                            radius={20 * intensity}
                            pathOptions={{
                                color: intensity > 0.8 ? "#ef4444" : intensity > 0.6 ? "#f97316" : "#eab308",
                                fillColor: intensity > 0.8 ? "#ef4444" : intensity > 0.6 ? "#f97316" : "#eab308",
                                fillOpacity: 0.6
                            }}
                        >
                            <Popup className="text-black">
                                <div className="font-bold">{cluster.title}</div>
                                <div className="text-xs">Intensity: {(intensity * 100).toFixed(0)}%</div>
                                <div className="text-xs">{cluster.summary.substring(0, 50)}...</div>
                            </Popup>
                        </CircleMarker>
                    )
                })}
            </MapContainer>
        </div>
    );
}

