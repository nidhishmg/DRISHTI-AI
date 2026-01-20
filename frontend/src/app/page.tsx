import { Suspense } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import Heatmap from "@/components/Heatmap";
import { ArrowUpRight, Activity, Users, AlertTriangle, FileText, Info } from "lucide-react";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import { fetchWithRetry } from "@/lib/utils"; // Importing from api.ts via alias if configured, else relative

import { fetchWithRetry as fetchAPI } from "@/lib/api";
import { Cluster, DashboardStats } from "@/types";
import { Skeleton } from "@/components/ui/skeleton";

async function getDashboardData() {
  try {
    const statsPromise = fetchAPI<DashboardStats>("/dashboard/stats");
    const clustersPromise = fetchAPI<Cluster[]>("/clusters/hot");

    // Parallel fetch
    const [stats, clusters] = await Promise.all([statsPromise, clustersPromise]);
    return { stats, clusters };
  } catch (error) {
    console.error("Failed to fetch dashboard data:", error);
    return null;
  }
}

function LoadingCard() {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <Skeleton className="h-4 w-[100px]" />
        <Skeleton className="h-4 w-4 rounded-full" />
      </CardHeader>
      <CardContent>
        <Skeleton className="h-8 w-[60px] mb-2" />
        <Skeleton className="h-3 w-[120px]" />
      </CardContent>
    </Card>
  );
}

export default async function Home() {
  const data = await getDashboardData();

  if (!data) {
    return <div className="p-8 text-red-500">Failed to load dashboard data. Please try again.</div>;
  }

  const { stats, clusters } = data;

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white">Dashboard Overview</h1>
          <p className="text-muted-foreground">Real-time situational awareness of scheme delivery performance.</p>
        </div>
        <div className="flex gap-2">
          <span className="mr-1.5 h-2 w-2 rounded-full bg-green-500"></span>
          System Healthy
        </span>
        <TooltipProvider>
          <Tooltip>
            <TooltipTrigger asChild>
              <button className="inline-flex items-center rounded-md bg-white/10 px-3 py-1 text-sm font-medium text-white hover:bg-white/20">
                <Info className="mr-2 h-4 w-4" />
                Explain This Insight
              </button>
            </TooltipTrigger>
            <TooltipContent>
              <p className="w-[300px] text-xs">
                <strong>AI Analysis:</strong> System performance is stable.
                Complaint velocity is within normal range (sigma &lt; 1.0).
                No immediate interventions recommended.
              </p>
            </TooltipContent>
          </Tooltip>
        </TooltipProvider>
      </div>
    </div>



      {/* KPI Cards */ }
  <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
    <Suspense fallback={<LoadingCard />}>
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Total Voice Reports</CardTitle>
          <Users className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold text-white">{stats.total_reports.toLocaleString()}</div>
          <p className="text-xs text-green-500 flex items-center">
            <ArrowUpRight className="mr-1 h-3 w-3" /> +{stats.reports_trend}% from last week
          </p>
        </CardContent>
      </Card>
    </Suspense>

    <Suspense fallback={<LoadingCard />}>
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Active Clusters</CardTitle>
          <Activity className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold text-white">{stats.active_clusters}</div>
          <p className="text-xs text-orange-500 flex items-center">
            <AlertTriangle className="mr-1 h-3 w-3" /> {stats.critical_clusters} Critical Severity
          </p>
        </CardContent>
      </Card>
    </Suspense>

    <Suspense fallback={<LoadingCard />}>
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Avg. Trust Score</CardTitle>
          <FileText className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold text-white">{(stats.avg_trust_score * 100).toFixed(1)}%</div>
          <p className="text-xs text-muted-foreground">Based on verifications</p>
        </CardContent>
      </Card>
    </Suspense>

    <Suspense fallback={<LoadingCard />}>
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Causal Conf. Index</CardTitle>
          <Activity className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold text-white">{stats.causal_confidence}</div>
          <p className="text-xs text-green-500">High Reliability</p>
        </CardContent>
      </Card>
    </Suspense>
  </div>

  {/* Main Content Grid */ }
  <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
    {/* Heatmap Section */}
    <Card className="col-span-4 max-h-[600px] overflow-hidden">
      <CardHeader>
        <CardTitle>Regional Failure Heatmap</CardTitle>
      </CardHeader>
      <CardContent className="pl-2">
        <Suspense fallback={<Skeleton className="h-[500px] w-full" />}>
          <Heatmap clusters={clusters} />
        </Suspense>
      </CardContent>
    </Card>

    {/* Live Feed / Recent Activity */}
    <Card className="col-span-3">
      <CardHeader>
        <CardTitle>Recent Alerts</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {clusters.slice(0, 5).map((cluster, i) => (
            <div key={i} className="flex items-start space-x-4 rounded-md border border-white/5 bg-white/5 p-3 hover:bg-white/10 transition">
              <div className={`mt-1 h-2 w-2 rounded-full ${cluster.confidence_score > 0.8 ? 'bg-red-500' : 'bg-orange-500'}`} />
              <div className="space-y-1">
                <p className="text-sm font-medium leading-none text-white">{cluster.title}</p>
                <p className="text-xs text-muted-foreground">{cluster.summary.substring(0, 60)}...</p>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  </div>
    </div >
  );
}

