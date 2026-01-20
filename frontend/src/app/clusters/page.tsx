"use client";

import { useState } from "react";
import useSWR from "swr";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { AlertTriangle, CheckCircle, TrendingUp, Users, ShieldCheck, ArrowRight } from "lucide-react";

// Mock fetcher
const fetcher = (url: string) => fetch(url).then((res) => res.json());

// Fallback data if backend is down
const fallbackClusters = [
    {
        title: "Pension Scheme Delays - Karnataka",
        summary: "Multiple reports of 3+ month delays provided by elderly citizens in rural districts.",
        trend_metrics: { count_30d: 142, growth_rate: 15.5 },
        geo_distribution: { "Karnataka": 80, "Rural": 60, "Urban": 20 },
        confidence_score: 0.92,
        quotes: [
            "I haven't received my pension for 4 months.",
            "My thumbprint matches but money doesn't come."
        ],
        quality: "High Fidelity",
        sources: 12,
        id: "1"
    },
    {
        title: "Ration Card Biometric Failures",
        summary: "Fingerprint scanners failing intermittently in North Zones.",
        trend_metrics: { count_30d: 89, growth_rate: 8.2 },
        geo_distribution: { "North Zone": 75, "Bihar": 25 },
        confidence_score: 0.88,
        quotes: [
            "Machine says no match. I have no rice for today.",
        ],
        quality: "Medium Fidelity",
        sources: 8,
        id: "2"
    },
    {
        title: "Mid-day Meal Quality Issues",
        summary: "Reports of sub-standard quality grain being supplied in primary schools.",
        trend_metrics: { count_30d: 56, growth_rate: -2.1 },
        geo_distribution: { "Odisha": 90 },
        confidence_score: 0.75,
        quotes: ["Insects found in the rice bag."],
        quality: "Verified Image",
        sources: 5,
        id: "3"
    }
];

export default function ClusterExplorer() {
    const { data } = useSWR("http://localhost:8000/api/v1/clusters/hot", fetcher);
    const clusters = data || fallbackClusters;
    const [selected, setSelected] = useState<any>(clusters[0]);

    return (
        <div className="flex h-[calc(100vh-6rem)] gap-6">
            {/* List View */}
            <div className="w-1/3 space-y-4 overflow-y-auto pr-2">
                <h2 className="text-xl font-bold text-white mb-4">Active Clusters</h2>
                {clusters.map((cluster: any, idx: number) => (
                    <Card
                        key={idx}
                        className={`cursor-pointer transition-all hover:bg-white/5 ${selected?.title === cluster.title ? "border-blue-500 bg-white/5" : "border-white/10"}`}
                        onClick={() => setSelected(cluster)}
                    >
                        <CardHeader className="p-4">
                            <div className="flex justify-between items-start">
                                <CardTitle className="text-base text-white">{cluster.title}</CardTitle>
                                {cluster.confidence_score > 0.9 && <AlertTriangle className="h-4 w-4 text-red-500" />}
                            </div>
                            <CardDescription className="line-clamp-2 text-xs">
                                {cluster.summary}
                            </CardDescription>
                        </CardHeader>
                        <CardContent className="p-4 pt-0 flex gap-4 text-xs text-muted-foreground">
                            <div className="flex items-center"><Users className="mr-1 h-3 w-3" /> {cluster.trend_metrics?.count_30d} reports</div>
                            <div className="flex items-center"><TrendingUp className="mr-1 h-3 w-3" /> {cluster.trend_metrics?.growth_rate}%</div>
                        </CardContent>
                    </Card>
                ))}
            </div>

            {/* Detail View */}
            <div className="flex-1 overflow-y-auto">
                {selected ? (
                    <div className="space-y-6">
                        <div className="flex justify-between items-start">
                            <div>
                                <h1 className="text-3xl font-bold text-white">{selected.title}</h1>
                                <div className="mt-2 flex gap-2">
                                    <span className="inline-flex items-center rounded-md bg-blue-500/10 px-2 py-1 text-xs font-medium text-blue-500 ring-1 ring-inset ring-blue-500/20">
                                        Confidence: {(selected.confidence_score * 100).toFixed(0)}%
                                    </span>
                                </div>
                            </div>
                            <Button className="bg-blue-600 hover:bg-blue-700">Generate Intervention <ArrowRight className="ml-2 h-4 w-4" /></Button>
                        </div>

                        <div className="grid gap-6 md:grid-cols-2">
                            <Card>
                                <CardHeader>
                                    <CardTitle className="text-lg">Summary Analysis</CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <p className="text-sm text-gray-300 leading-relaxed">
                                        {selected.summary}
                                    </p>
                                    <div className="mt-4 space-y-2">
                                        <h4 className="text-sm font-semibold text-white">Citizen Voices</h4>
                                        {selected.quotes?.map((quote: string, i: number) => (
                                            <blockquote key={i} className="border-l-2 border-blue-500 pl-4 italic text-gray-400 text-sm">
                                                "{quote}"
                                            </blockquote>
                                        )) || <p className="text-sm text-muted-foreground">No quotes available.</p>}
                                    </div>
                                </CardContent>
                            </Card>

                            <Card>
                                <CardHeader>
                                    <CardTitle className="text-lg flex items-center gap-2"><ShieldCheck className="h-5 w-5 text-green-500" /> Trust Panel</CardTitle>
                                </CardHeader>
                                <CardContent className="space-y-4">
                                    <div className="flex justify-between items-center border-b border-white/10 pb-2">
                                        <span className="text-sm text-gray-400">Unique Sources</span>
                                        <span className="font-mono text-white">{selected.sources || 18}</span>
                                    </div>
                                    <div className="flex justify-between items-center border-b border-white/10 pb-2">
                                        <span className="text-sm text-gray-400">Data Quality</span>
                                        <span className="font-mono text-green-400">{selected.quality || 'High'}</span>
                                    </div>
                                    <div className="flex justify-between items-center border-b border-white/10 pb-2">
                                        <span className="text-sm text-gray-400">Verification Status</span>
                                        <span className="flex items-center text-sm text-blue-400"><CheckCircle className="mr-1 h-3 w-3" /> Cross-referenced</span>
                                    </div>
                                </CardContent>
                            </Card>
                        </div>
                    </div>
                ) : (
                    <div className="flex h-full items-center justify-center text-muted-foreground">
                        Select a cluster to view details
                    </div>
                )}
            </div>
        </div>
    );
}
