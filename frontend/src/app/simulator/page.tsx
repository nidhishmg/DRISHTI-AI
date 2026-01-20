"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from "chart.js";
import { Line } from "react-chartjs-2";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

export default function SimulatorPage() {
    const [docThreshold, setDocThreshold] = useState(80);
    const [autoApproveLimit, setAutoApproveLimit] = useState(5000);
    const [humanReviewCap, setHumanReviewCap] = useState(50);

    // Mock impact calculation
    const exclusionRate = (docThreshold / 100) * 15;
    const fraudRisk = (autoApproveLimit / 10000) * 12;
    const processingTime = (100 - humanReviewCap) * 0.5;

    const data = {
        labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        datasets: [
            {
                label: "Projected Beneficiaries (Thousands)",
                data: [12, 12.5, 13, 14, 15 - exclusionRate, 16 - exclusionRate],
                borderColor: "rgb(59, 130, 246)",
                backgroundColor: "rgba(59, 130, 246, 0.5)",
            },
            {
                label: "Projected Cost (₹ Crores)",
                data: [5, 5.2, 5.4, 5.8, 6 + fraudRisk / 5, 6.2 + fraudRisk / 5],
                borderColor: "rgb(239, 68, 68)",
                backgroundColor: "rgba(239, 68, 68, 0.5)",
            },
        ],
    };

    const options = {
        responsive: true,
        plugins: {
            legend: { position: "top" as const, labels: { color: "white" } },
            title: { display: true, text: "Policy Impact Projection", color: "white" },
        },
        scales: {
            y: { grid: { color: "rgba(255,255,255,0.1)" }, ticks: { color: "gray" } },
            x: { grid: { color: "rgba(255,255,255,0.1)" }, ticks: { color: "gray" } }
        }
    };

    return (
        <div className="space-y-6">
            <h1 className="text-3xl font-bold text-white">Policy Impact Simulator</h1>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card className="col-span-1 border-white/10 bg-black/40">
                    <CardHeader><CardTitle>Control Parameters</CardTitle></CardHeader>
                    <CardContent className="space-y-6">
                        <div>
                            <label className="text-sm font-medium text-gray-300">Document Stringency ({docThreshold}%)</label>
                            <input
                                type="range" min="0" max="100" value={docThreshold}
                                onChange={(e) => setDocThreshold(Number(e.target.value))}
                                className="w-full accent-blue-500 mt-2"
                            />
                        </div>
                        <div>
                            <label className="text-sm font-medium text-gray-300">Auto-Approve Limit (₹{autoApproveLimit})</label>
                            <input
                                type="range" min="1000" max="20000" step="1000" value={autoApproveLimit}
                                onChange={(e) => setAutoApproveLimit(Number(e.target.value))}
                                className="w-full accent-green-500 mt-2"
                            />
                        </div>
                        <div>
                            <label className="text-sm font-medium text-gray-300">AI vs Human Review ({humanReviewCap}% AI)</label>
                            <input
                                type="range" min="0" max="100" value={humanReviewCap}
                                onChange={(e) => setHumanReviewCap(Number(e.target.value))}
                                className="w-full accent-purple-500 mt-2"
                            />
                        </div>
                        <Button className="w-full mt-4">Run Simulation</Button>
                    </CardContent>
                </Card>

                <Card className="col-span-2 border-white/10 bg-black/40">
                    <CardContent className="pt-6">
                        <Line options={options} data={data} />
                    </CardContent>
                </Card>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Card className="border-white/10 bg-white/5">
                    <CardContent className="pt-6 text-center">
                        <div className="text-2xl font-bold text-red-500">{exclusionRate.toFixed(1)}%</div>
                        <div className="text-xs text-muted-foreground">Exclusion Error Rate</div>
                    </CardContent>
                </Card>
                <Card className="border-white/10 bg-white/5">
                    <CardContent className="pt-6 text-center">
                        <div className="text-2xl font-bold text-yellow-500">{fraudRisk.toFixed(1)}%</div>
                        <div className="text-xs text-muted-foreground">Fraud Leakage Risk</div>
                    </CardContent>
                </Card>
                <Card className="border-white/10 bg-white/5">
                    <CardContent className="pt-6 text-center">
                        <div className="text-2xl font-bold text-green-500">{processingTime.toFixed(1)} days</div>
                        <div className="text-xs text-muted-foreground">Avg. Turnaround Time</div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
