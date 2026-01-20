export interface Cluster {
    id: string;
    title: string;
    summary: string;
    trend_metrics: {
        count_30d: number;
        growth_rate: number;
    };
    geo_distribution: Record<string, number>; // e.g., { "Karnataka": 80 }
    confidence_score: number;
    // For heatmap (mocking coordinates if not present in backend model yet)
    lat?: number;
    lng?: number;
}

export interface DashboardStats {
    total_reports: number;
    reports_trend: number;
    active_clusters: number;
    critical_clusters: number;
    avg_trust_score: number;
    causal_confidence: number;
}
