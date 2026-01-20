"use client";

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { FileDown, FileText, CheckCircle } from "lucide-react";

export default function EvidencePage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h1 className="text-3xl font-bold text-white">Trust & Evidence Export</h1>
                <Button className="gap-2 bg-blue-600"><FileDown size={16} /> Export Full Report (PDF)</Button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 h-[600px]">
                {/* File Preview */}
                <Card className="border-white/10 bg-white h-full overflow-hidden relative group">
                    <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex items-end justify-center pb-10">
                        <Button variant="secondary">Preview Document</Button>
                    </div>
                    <CardContent className="p-8 text-black font-serif space-y-4">
                        <div className="border-b-2 border-black pb-4 mb-4">
                            <h1 className="text-2xl font-bold uppercase">Incident Inquiry Report</h1>
                            <p className="text-sm">Ref: RG-2026-XQ-992</p>
                        </div>
                        <div className="space-y-2 text-sm">
                            <p><strong>Subject:</strong> Systemic Pension Disbursement Failure in Karnataka Rural.</p>
                            <p><strong>Date:</strong> 20 Jan 2026</p>
                            <p><strong>Severity:</strong> Critical (CCI: 0.87)</p>
                        </div>
                        <div className="space-y-2 mt-6">
                            <h3 className="font-bold border-b border-gray-300">1. Executive Summary</h3>
                            <p className="text-xs leading-relaxed">
                                Analysis reveals a high-confidence cluster of 142 reports indicating failures in the Direct Benefit Transfer (DBT) layer.
                                Root cause analysis points to API timeouts at the state banking gateway level (Node #2).
                            </p>
                        </div>
                        <div className="space-y-2 mt-6">
                            <h3 className="font-bold border-b border-gray-300">2. Evidence Trace</h3>
                            <ul className="text-xs list-disc pl-4">
                                <li>142 Verified Voice Reports (SHA-256 Signed)</li>
                                <li>Geo-tagged cluster density {'>'} 80% in Rural districts</li>
                                <li>Corroborated by 2 partner NGO field audits</li>
                            </ul>
                        </div>
                    </CardContent>
                </Card>

                {/* Verification Chain */}
                <div className="space-y-4">
                    <Card className="border-white/10 bg-black/40">
                        <CardHeader><CardTitle>Audit Trail</CardTitle><CardDescription>Immutable record of intelligence generation</CardDescription></CardHeader>
                        <CardContent className="space-y-4">
                            {[
                                { step: "Data Ingestion", time: "20 Jan 14:00", status: "Verified", hash: "0x8f...2a" },
                                { step: "PII Redaction", time: "20 Jan 14:02", status: "Verified", hash: "0x1d...9c" },
                                { step: "Causal Inference", time: "20 Jan 14:05", status: "Verified", hash: "0x4b...e1" },
                                { step: "Human Review", time: "20 Jan 14:30", status: "Pending", hash: "---" },
                            ].map((item, i) => (
                                <div key={i} className="flex items-center justify-between border-b border-white/5 pb-2">
                                    <div className="flex items-center gap-3">
                                        <CheckCircle className={`h-4 w-4 ${item.status === 'Verified' ? 'text-green-500' : 'text-gray-500'}`} />
                                        <div>
                                            <p className="text-sm font-medium text-white">{item.step}</p>
                                            <p className="text-xs text-muted-foreground">{item.time}</p>
                                        </div>
                                    </div>
                                    <code className="text-[10px] text-gray-500">{item.hash}</code>
                                </div>
                            ))}
                        </CardContent>
                    </Card>

                    <Card className="border-white/10 bg-black/40">
                        <CardHeader><CardTitle>Download Options</CardTitle></CardHeader>
                        <CardContent className="grid grid-cols-2 gap-4">
                            <Button variant="outline" className="h-20 flex flex-col gap-2">
                                <FileText className="h-6 w-6" />
                                Summary PDF
                            </Button>
                            <Button variant="outline" className="h-20 flex flex-col gap-2">
                                <FileText className="h-6 w-6" />
                                Raw Data (CSV)
                            </Button>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    );
}
