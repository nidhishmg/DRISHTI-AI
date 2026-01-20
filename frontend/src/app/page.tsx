"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import Heatmap from "@/components/Heatmap";
import { ArrowUpRight, Activity, Users, AlertTriangle, FileText } from "lucide-react";

export default function Home() {
  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white">Dashboard Overview</h1>
          <p className="text-muted-foreground">Real-time situational awareness of scheme delivery performance.</p>
        </div>
        <div className="flex gap-2">
          <span className="inline-flex items-center rounded-full bg-green-500/10 px-3 py-1 text-sm font-medium text-green-500 ring-1 ring-inset ring-green-500/20">
            <span className="mr-1.5 h-2 w-2 rounded-full bg-green-500"></span>
            System Healthy
          </span>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Voice Reports</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">12,345</div>
            <p className="text-xs text-green-500 flex items-center">
              <ArrowUpRight className="mr-1 h-3 w-3" /> +18.2% from last week
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Clusters</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">42</div>
            <p className="text-xs text-orange-500 flex items-center">
              <AlertTriangle className="mr-1 h-3 w-3" /> 5 Critical Severity
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Avg. Trust Score</CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">92.4%</div>
            <p className="text-xs text-muted-foreground">Based on 850 verifications</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Causal Conf. Index</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">0.87</div>
            <p className="text-xs text-green-500">High Reliability</p>
          </CardContent>
        </Card>
      </div>

      {/* Main Content Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
        {/* Heatmap Section */}
        <Card className="col-span-4 max-h-[600px] overflow-hidden">
          <CardHeader>
            <CardTitle>Regional Failure Heatmap</CardTitle>
          </CardHeader>
          <CardContent className="pl-2">
            <Heatmap />
          </CardContent>
        </Card>

        {/* Live Feed / Recent Activity */}
        <Card className="col-span-3">
          <CardHeader>
            <CardTitle>Recent Alerts</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                { title: "New Cluster: Ration Denial", loc: "Patna, Bihar", time: "2m ago", level: "high" },
                { title: "Spike: Pension API Errors", loc: "Bangalore Urban", time: "15m ago", level: "med" },
                { title: "Verified: School Infra", loc: "Lucknow, UP", time: "1h ago", level: "low" },
              ].map((item, i) => (
                <div key={i} className="flex items-start space-x-4 rounded-md border border-white/5 bg-white/5 p-3 hover:bg-white/10 transition">
                  <div className={`mt-1 h-2 w-2 rounded-full ${item.level === 'high' ? 'bg-red-500' : item.level === 'med' ? 'bg-orange-500' : 'bg-blue-500'}`} />
                  <div className="space-y-1">
                    <p className="text-sm font-medium leading-none text-white">{item.title}</p>
                    <p className="text-xs text-muted-foreground">{item.loc} • {item.time}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
