"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { LayoutDashboard, Map, Activity, MessageSquare, FileText, Settings, ShieldAlert } from "lucide-react";
import { cn } from "@/lib/utils";

const navItems = [
    { name: "Heatmap Overview", href: "/", icon: Map },
    { name: "Cluster Explorer", href: "/clusters", icon: LayoutDashboard },
    { name: "Causal Graph", href: "/graph", icon: Activity },
    { name: "Policy Simulator", href: "/simulator", icon: Settings },
    { name: "Citizen Demo", href: "/demo", icon: MessageSquare },
    { name: "Trust & Evidence", href: "/evidence", icon: ShieldAlert },
];

export function Sidebar() {
    const pathname = usePathname();

    return (
        <div className="flex h-screen w-64 flex-col border-r border-white/10 bg-black/40 backdrop-blur-xl">
            <div className="flex h-16 items-center border-b border-white/10 px-6">
                <div className="flex items-center gap-2">
                    <div className="h-6 w-6 rounded-full bg-blue-500 shadow-[0_0_10px_rgba(59,130,246,0.5)]" />
                    <span className="text-lg font-bold tracking-tight text-white">Reality Gap AI</span>
                </div>
            </div>
            <nav className="flex-1 space-y-1 px-3 py-4">
                {navItems.map((item) => {
                    const isActive = pathname === item.href;
                    return (
                        <Link
                            key={item.href}
                            href={item.href}
                            className={cn(
                                "group flex items-center rounded-lg px-3 py-2 text-sm font-medium transition-all duration-200",
                                isActive
                                    ? "bg-white/10 text-white shadow-[0_0_15px_rgba(255,255,255,0.1)]"
                                    : "text-muted-foreground hover:bg-white/5 hover:text-white"
                            )}
                        >
                            <item.icon
                                className={cn(
                                    "mr-3 h-5 w-5 transition-colors",
                                    isActive ? "text-blue-400" : "text-muted-foreground group-hover:text-blue-400"
                                )}
                            />
                            {item.name}
                        </Link>
                    );
                })}
            </nav>
            <div className="border-t border-white/10 p-4">
                <div className="flex items-center gap-3 rounded-lg bg-white/5 p-3">
                    <div className="h-9 w-9 rounded-full bg-gradient-to-br from-purple-500 to-blue-600" />
                    <div className="flex flex-col">
                        <span className="text-sm font-medium text-white">Admin User</span>
                        <span className="text-xs text-muted-foreground">Analyst Role</span>
                    </div>
                </div>
            </div>
        </div>
    );
}
