"use client";

import CausalGraphComponent from "@/components/CausalGraph";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function GraphPage() {
    return (
        <div className="space-y-6 h-[calc(100vh-6rem)]">
            <div className="flex justify-between items-center">
                <h1 className="text-3xl font-bold text-white">Causal Analysis</h1>
                <div className="flex gap-4 text-xs font-semibold">
                    <div className="flex items-center gap-1"><div className="h-3 w-3 rounded-full bg-red-500" /> Failure</div>
                    <div className="flex items-center gap-1"><div className="h-3 w-3 rounded-full bg-orange-500" /> Root Cause</div>
                    <div className="flex items-center gap-1"><div className="h-3 w-3 rounded-full bg-yellow-500" /> Outcome</div>
                    <div className="flex items-center gap-1"><div className="h-3 w-3 rounded-sm bg-blue-500" /> Intervention</div>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 h-full">
                <Card className="col-span-3 h-[600px] border-white/10 bg-black/40">
                    <CardContent className="h-full p-0">
                        <CausalGraphComponent />
                    </CardContent>
                </Card>

                <Card className="col-span-1 border-white/10 bg-black/40">
                    <CardHeader>
                        <CardTitle>Inference Details</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4 text-sm text-gray-300">
                        <p>
                            <strong>Primary Root Cause:</strong><br />
                            Network Outage (Node #2) has the highest centrality in affecting Biometric Failure.
                        </p>
                        <p>
                            <strong>Suggested Intervention:</strong><br />
                            Implementation of "Offline Auth Fallback" is predicted to reduce failure rate by 85%.
                        </p>
                        <div className="rounded-md bg-blue-500/10 p-3 border border-blue-500/20">
                            <p className="text-blue-400 font-semibold">CCI Score: 0.87</p>
                            <p className="text-xs text-blue-300/80">Causal confidence is high due to consistent temporal precedence in 142 reports.</p>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
