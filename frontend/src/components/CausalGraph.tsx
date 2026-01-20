"use client";

import { useEffect, useRef, useState } from "react";
import { Network } from "vis-network";
import { Card } from "@/components/ui/card";

export default function CausalGraphComponent() {
    const containerRef = useRef<HTMLDivElement>(null);
    const networkRef = useRef<Network | null>(null);

    useEffect(() => {
        if (!containerRef.current) return;

        const nodes = [
            { id: 1, label: "Biometric Failure", group: "failure", color: "#ef4444", shape: "dot", size: 30 },
            { id: 2, label: "Network Outage", group: "root_cause", color: "#f97316", shape: "triangle", size: 20 },
            { id: 3, label: "Pension Denial", group: "outcome", color: "#eab308", shape: "diamond", size: 25 },
            { id: 4, label: "Staff Training", group: "intervention", color: "#3b82f6", shape: "box", size: 20 },
            { id: 5, label: "Offline Auth Fallback", group: "intervention", color: "#3b82f6", shape: "box", size: 20 },
            { id: 6, label: "Server Latency", group: "root_cause", color: "#f97316", shape: "triangle", size: 20 },
        ];

        const edges = [
            { from: 2, to: 1, label: "causes", arrows: "to" },
            { from: 6, to: 1, label: "causes", arrows: "to" },
            { from: 1, to: 3, label: "leads_to", arrows: "to" },
            { from: 4, to: 2, label: "mitigates", arrows: "to", dashes: true },
            { from: 5, to: 1, label: "mitigates", arrows: "to", dashes: true },
        ];

        const data = { nodes, edges };
        const options = {
            nodes: {
                font: { color: "#ffffff" },
                borderWidth: 2,
                shadow: true,
            },
            edges: {
                color: "#64748b",
                shadow: true,
            },
            physics: {
                enabled: true,
                stabilization: false,
            },
            interaction: {
                hover: true,
            },
            groups: {
                failure: { color: { background: "#ef4444", border: "#991b1b" } },
                root_cause: { color: { background: "#f97316", border: "#c2410c" } },
                outcome: { color: { background: "#eab308", border: "#a16207" } },
                intervention: { color: { background: "#3b82f6", border: "#1e40af" } },
            }
        };

        networkRef.current = new Network(containerRef.current, data, options);

        return () => {
            if (networkRef.current) {
                networkRef.current.destroy();
            }
        };
    }, []);

    return (
        <div className="h-full w-full" ref={containerRef} />
    );
}
