import React, { useCallback, useEffect, useRef, useState } from "react";
import {
  Activity,
  Cpu,
  Database,
  GitBranch,
  type LucideProps,
  Terminal,
  TrendingUp,
  Zap
} from "lucide-react";
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";

type Stats = {
  totalSessions: number;
  activeProjects: number;
  recentWins: number;
  avgEnergy: number;
};

type Project = {
  key: string;
  name: string;
  description: string;
  completion: number;
  urgency: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW" | "NONE";
  priority: string;
  lastWorked: string;
  status?: string;
};

type ActivityItem = {
  time: string;
  message: string;
};

type MomentumPoint = {
  date: string;
  sessions: number;
};

type PredictionPoint = {
  project: string;
  predicted_days_to_complete: number;
  confidence: number;
  status: string;
};

type DashboardOverview = {
  stats: {
    total_sessions: number;
    active_projects: number;
    recent_wins: number;
    avg_energy: number;
  };
  projects: Project[];
  activity: Array<{ event_type: string; created_at: string; payload: Record<string, unknown> }>;
};

type AdvancedAnalytics = {
  momentum: { timeline: MomentumPoint[] };
  completion_predictions: PredictionPoint[];
  burnout: { risk: string; score: number; signals: string[] };
};

const API_BASE = import.meta.env.VITE_REL_API_BASE ?? "";
const DEFAULT_USERNAME = import.meta.env.VITE_REL_DEFAULT_USERNAME ?? "";
const DEFAULT_PASSWORD = import.meta.env.VITE_REL_DEFAULT_PASSWORD ?? "";

const getWebSocketUrl = () => {
  if (API_BASE) {
    const apiUrl = new URL(API_BASE, window.location.origin);
    const wsProtocol = apiUrl.protocol === "https:" ? "wss:" : "ws:";
    return `${wsProtocol}//${apiUrl.host}/ws/notifications`;
  }
  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  return `${protocol}//${window.location.host}/ws/notifications`;
};

const MatrixRain: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) {
      return;
    }
    const ctx = canvas.getContext("2d");
    if (!ctx) {
      return;
    }

    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    resize();
    window.addEventListener("resize", resize);

    const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()";
    const fontSize = 14;
    const columns = Math.max(Math.floor(canvas.width / fontSize), 1);
    const drops = Array(columns).fill(1);

    const draw = () => {
      ctx.fillStyle = "rgba(0,0,0,0.08)";
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      ctx.font = `${fontSize}px monospace`;

      for (let i = 0; i < drops.length; i += 1) {
        const char = chars[Math.floor(Math.random() * chars.length)];
        ctx.fillStyle = i % 3 === 0 ? "#22d3ee" : "#22c55e";
        ctx.fillText(char, i * fontSize, drops[i] * fontSize);
        if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
          drops[i] = 0;
        }
        drops[i] += 1;
      }
    };

    const interval = window.setInterval(draw, 33);
    return () => {
      window.clearInterval(interval);
      window.removeEventListener("resize", resize);
    };
  }, []);

  return <canvas ref={canvasRef} className="fixed inset-0 z-0 opacity-10" />;
};

const StatCard: React.FC<{
  icon: React.ComponentType<LucideProps>;
  label: string;
  value: string | number;
  trend?: number;
}> = ({ icon: Icon, label, value, trend }) => {
  return (
    <div className="relative group">
      <div className="absolute -inset-0.5 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-lg blur opacity-30 group-hover:opacity-100 transition duration-300" />
      <div className="relative bg-black border border-cyan-500/30 rounded-lg p-6 hover:border-cyan-500 transition-all duration-300">
        <div className="flex items-center justify-between mb-3">
          <Icon className="w-8 h-8 text-cyan-400" strokeWidth={1.5} />
          {typeof trend === "number" ? (
            <div className={`flex items-center text-sm ${trend >= 0 ? "text-green-400" : "text-red-400"}`}>
              <TrendingUp className="w-4 h-4 mr-1" />
              {trend > 0 ? "+" : ""}
              {trend}%
            </div>
          ) : null}
        </div>
        <div className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-400 mb-1">
          {value}
        </div>
        <div className="text-cyan-300/60 text-sm uppercase tracking-wider">{label}</div>
      </div>
    </div>
  );
};

const ProjectCard: React.FC<{ project: Project }> = ({ project }) => {
  const urgencyColors: Record<Project["urgency"], string> = {
    CRITICAL: "border-red-500 shadow-red-500/50",
    HIGH: "border-orange-500 shadow-orange-500/50",
    MEDIUM: "border-yellow-500 shadow-yellow-500/50",
    LOW: "border-cyan-500 shadow-cyan-500/50",
    NONE: "border-cyan-500 shadow-cyan-500/50"
  };

  const urgencyBadge: Record<Project["urgency"], string> = {
    CRITICAL: "bg-red-500/20 text-red-400",
    HIGH: "bg-orange-500/20 text-orange-400",
    MEDIUM: "bg-yellow-500/20 text-yellow-400",
    LOW: "bg-cyan-500/20 text-cyan-400",
    NONE: "bg-cyan-500/20 text-cyan-400"
  };

  return (
    <div
      className={`relative border-2 ${urgencyColors[project.urgency]} rounded-lg p-4 bg-black/80 backdrop-blur hover:shadow-lg transition-all duration-300`}
    >
      <div className="flex items-start justify-between mb-3 gap-4">
        <div>
          <h3 className="text-cyan-100 font-bold text-lg mb-1">{project.name}</h3>
          <p className="text-cyan-400/60 text-sm">{project.description}</p>
        </div>
        <div className={`px-3 py-1 rounded-full text-xs font-bold ${urgencyBadge[project.urgency]}`}>
          {project.urgency}
        </div>
      </div>

      <div className="space-y-2 mb-4">
        <div className="flex items-center justify-between text-sm">
          <span className="text-cyan-400/60">Progress</span>
          <span className="text-cyan-300 font-mono">{project.completion}%</span>
        </div>
        <div className="w-full bg-gray-800 rounded-full h-2 overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full transition-all duration-500"
            style={{ width: `${project.completion}%` }}
          />
        </div>
      </div>

      <div className="flex items-center justify-between text-xs">
        <span className="text-cyan-400/60">
          Priority: <span className="text-cyan-300 font-bold uppercase">{project.priority}</span>
        </span>
        <span className="text-cyan-400/60">
          Last: <span className="text-cyan-300">{project.lastWorked}</span>
        </span>
      </div>
    </div>
  );
};

const ActivityFeed: React.FC<{ activities: ActivityItem[] }> = ({ activities }) => {
  return (
    <div className="bg-black border border-green-500/30 rounded-lg p-4 font-mono text-sm">
      <div className="flex items-center gap-2 mb-4 pb-2 border-b border-green-500/30">
        <Terminal className="w-5 h-5 text-green-400" />
        <span className="text-green-400 font-bold">SYSTEM LOG</span>
        <div className="flex-1" />
        <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
      </div>
      <div className="space-y-2 max-h-64 overflow-y-auto">
        {activities.map((activity, idx) => (
          <div key={`${activity.time}-${idx}`} className="text-green-400/80 hover:text-green-300 transition-colors">
            <span className="text-green-500/50">[{activity.time}]</span> {activity.message}
          </div>
        ))}
      </div>
    </div>
  );
};

const formatActivity = (eventType: string, payload: Record<string, unknown>): string => {
  if (eventType === "session_logged") {
    return `Session: ${String(payload.summary ?? "updated")}`;
  }
  if (eventType === "project_shared") {
    return `Project shared with ${String(payload.user_id ?? "user")}`;
  }
  if (eventType === "comment_added") {
    return `Comment added to ${String(payload.project ?? "project")}`;
  }
  if (eventType === "tool_invoked") {
    return `Tool invoked: ${String(payload.tool ?? "unknown")}`;
  }
  return `${eventType.replace(/_/g, " ")} event`;
};

const toClock = (iso: string): string => {
  const parsed = new Date(iso);
  if (Number.isNaN(parsed.valueOf())) {
    return "00:00:00";
  }
  return parsed.toLocaleTimeString();
};

export default function RELMatrixDashboard() {
  const [stats, setStats] = useState<Stats>({
    totalSessions: 0,
    activeProjects: 0,
    recentWins: 0,
    avgEnergy: 0
  });
  const [projects, setProjects] = useState<Project[]>([]);
  const [activities, setActivities] = useState<ActivityItem[]>([]);
  const [momentum, setMomentum] = useState<MomentumPoint[]>([]);
  const [predictions, setPredictions] = useState<PredictionPoint[]>([]);
  const [burnout, setBurnout] = useState<{ risk: string; score: number; signals: string[] }>({
    risk: "unknown",
    score: 0,
    signals: []
  });
  const [time, setTime] = useState(new Date());
  const [token, setToken] = useState<string>(() => localStorage.getItem("rel_token") ?? "");
  const [username, setUsername] = useState(DEFAULT_USERNAME);
  const [password, setPassword] = useState(DEFAULT_PASSWORD);
  const [authError, setAuthError] = useState("");
  const [loading, setLoading] = useState(false);

  const buildAuthHeaders = useCallback((): Record<string, string> => {
    if (!token) {
      return {};
    }
    return { Authorization: `Bearer ${token}` };
  }, [token]);

  const fetchJson = useCallback(
    async (path: string): Promise<unknown> => {
      const response = await fetch(`${API_BASE}${path}`, { headers: buildAuthHeaders() });
      if (!response.ok) {
        throw new Error(`Request failed: ${response.status}`);
      }
      return response.json();
    },
    [buildAuthHeaders]
  );

  const invokeTool = useCallback(
    async (toolName: string, argumentsPayload: Record<string, unknown> = {}) => {
      const response = await fetch(`${API_BASE}/api/v1/tools/${toolName}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...buildAuthHeaders()
        },
        body: JSON.stringify({ arguments: argumentsPayload })
      });
      if (!response.ok) {
        throw new Error(`Tool call failed: ${response.status}`);
      }
      return response.json();
    },
    [buildAuthHeaders]
  );

  const loadDashboard = useCallback(async () => {
    if (!token) {
      return;
    }
    setLoading(true);
    try {
      const [overviewRaw, analyticsRaw] = await Promise.all([
        fetchJson("/api/v1/dashboard/overview"),
        fetchJson("/api/v1/analytics/advanced")
      ]);

      const overview = overviewRaw as DashboardOverview;
      const analytics = analyticsRaw as AdvancedAnalytics;

      setStats({
        totalSessions: overview.stats.total_sessions,
        activeProjects: overview.stats.active_projects,
        recentWins: overview.stats.recent_wins,
        avgEnergy: overview.stats.avg_energy
      });
      setProjects(overview.projects ?? []);
      setActivities(
        (overview.activity ?? [])
          .slice(-20)
          .map((item) => ({
            time: toClock(item.created_at),
            message: formatActivity(item.event_type, item.payload)
          }))
          .reverse()
      );
      setMomentum(analytics.momentum?.timeline ?? []);
      setPredictions(analytics.completion_predictions ?? []);
      setBurnout(analytics.burnout ?? { risk: "unknown", score: 0, signals: [] });
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to load dashboard";
      setAuthError(message);
    } finally {
      setLoading(false);
    }
  }, [fetchJson, token]);

  useEffect(() => {
    const timer = window.setInterval(() => setTime(new Date()), 1000);
    return () => window.clearInterval(timer);
  }, []);

  useEffect(() => {
    void loadDashboard();
    const poll = window.setInterval(() => {
      void loadDashboard();
    }, 15000);
    return () => window.clearInterval(poll);
  }, [loadDashboard]);

  useEffect(() => {
    if (!token) {
      return;
    }
    const ws = new WebSocket(getWebSocketUrl(), [
      "rel-notify",
      `bearer.${token}`
    ]);
    ws.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data) as {
          event_type: string;
          payload: Record<string, unknown>;
          created_at: string;
        };
        if (!payload.event_type) {
          return;
        }
        setActivities((prev) => [
          {
            time: toClock(payload.created_at),
            message: formatActivity(payload.event_type, payload.payload ?? {})
          },
          ...prev.slice(0, 30)
        ]);
      } catch {
        return;
      }
    };
    return () => ws.close();
  }, [token]);

  const login = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setAuthError("");
    const body = new URLSearchParams();
    body.set("username", username);
    body.set("password", password);
    try {
      const response = await fetch(`${API_BASE}/api/v1/auth/token`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body
      });
      if (!response.ok) {
        throw new Error("Authentication failed");
      }
      const payload = (await response.json()) as { access_token: string };
      localStorage.setItem("rel_token", payload.access_token);
      setToken(payload.access_token);
      void loadDashboard();
    } catch (err) {
      setAuthError(err instanceof Error ? err.message : "Authentication failed");
    }
  };

  const logout = () => {
    localStorage.removeItem("rel_token");
    setToken("");
    setProjects([]);
    setActivities([]);
  };

  if (!token) {
    return (
      <div className="min-h-screen bg-black text-cyan-100 flex items-center justify-center p-6">
        <MatrixRain />
        <form onSubmit={login} className="relative z-10 w-full max-w-md bg-black/85 border border-cyan-500/30 rounded-xl p-8">
          <h1 className="text-2xl font-bold text-cyan-300 mb-2">REL CODEX Dashboard</h1>
          <p className="text-cyan-400/70 text-sm mb-6">OAuth2 login required for API access.</p>
          <div className="space-y-4">
            <input
              className="w-full bg-black border border-cyan-500/40 rounded px-3 py-2 text-cyan-100"
              placeholder="Username"
              value={username}
              onChange={(event) => setUsername(event.target.value)}
            />
            <input
              className="w-full bg-black border border-cyan-500/40 rounded px-3 py-2 text-cyan-100"
              type="password"
              placeholder="Password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
            />
            <button className="w-full py-3 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-lg font-bold text-black">
              Sign In
            </button>
          </div>
          {authError ? <p className="text-red-400 text-sm mt-4">{authError}</p> : null}
        </form>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black text-cyan-100 overflow-hidden">
      <MatrixRain />

      <div className="relative z-10 border-b border-cyan-500/30 bg-black/80 backdrop-blur">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between gap-4">
            <div className="flex items-center gap-4">
              <div className="relative">
                <div className="absolute inset-0 bg-cyan-500 blur-lg opacity-50" />
                <Cpu className="relative w-10 h-10 text-cyan-400" strokeWidth={1.5} />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-blue-400 to-purple-400">
                  REL CODEX
                </h1>
                <p className="text-cyan-400/60 text-sm">Reality Engineering Laboratory</p>
              </div>
            </div>

            <div className="flex items-center gap-4">
              <div className="text-right">
                <div className="text-cyan-400 font-mono text-sm">{time.toLocaleTimeString()}</div>
                <div className="text-cyan-400/60 text-xs">{time.toLocaleDateString()}</div>
              </div>
              <button
                onClick={logout}
                className="px-3 py-2 bg-red-500/20 border border-red-500/40 rounded text-red-300 text-sm"
              >
                Sign Out
              </button>
            </div>
          </div>
          {authError ? <p className="text-red-400 text-xs mt-2">{authError}</p> : null}
        </div>
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard icon={Activity} label="Total Sessions" value={stats.totalSessions} trend={12} />
          <StatCard icon={GitBranch} label="Active Projects" value={stats.activeProjects} trend={-2} />
          <StatCard icon={Zap} label="Recent Wins" value={stats.recentWins} trend={8} />
          <StatCard icon={TrendingUp} label="Avg Energy" value={`${stats.avgEnergy}%`} trend={5} />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-4">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-400">
                ACTIVE PROJECTS
              </h2>
              <button
                onClick={() => void loadDashboard()}
                className="px-4 py-2 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-lg font-bold hover:shadow-lg hover:shadow-cyan-500/50 transition-all text-black"
              >
                {loading ? "REFRESHING..." : "REFRESH"}
              </button>
            </div>

            {projects.length === 0 ? (
              <div className="border border-cyan-500/20 rounded-lg p-6 text-cyan-300/70">No projects available.</div>
            ) : (
              projects.map((project) => <ProjectCard key={project.key} project={project} />)
            )}

            <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
              <div className="bg-black border border-cyan-500/30 rounded-lg p-4 h-72">
                <h3 className="text-cyan-300 font-bold mb-3">Momentum Timeline</h3>
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={momentum}>
                    <defs>
                      <linearGradient id="sessionsColor" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#22d3ee" stopOpacity={0.8} />
                        <stop offset="95%" stopColor="#22d3ee" stopOpacity={0.1} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#164e63" />
                    <XAxis dataKey="date" stroke="#67e8f9" />
                    <YAxis stroke="#67e8f9" />
                    <Tooltip />
                    <Area type="monotone" dataKey="sessions" stroke="#22d3ee" fill="url(#sessionsColor)" />
                  </AreaChart>
                </ResponsiveContainer>
              </div>

              <div className="bg-black border border-purple-500/30 rounded-lg p-4 h-72">
                <h3 className="text-purple-300 font-bold mb-3">Completion Predictions</h3>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={predictions.slice(0, 8)}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#312e81" />
                    <XAxis dataKey="project" stroke="#c4b5fd" />
                    <YAxis stroke="#c4b5fd" />
                    <Tooltip />
                    <Bar dataKey="predicted_days_to_complete" fill="#8b5cf6" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>

          <div className="space-y-6">
            <ActivityFeed activities={activities} />

            <div className="bg-black border border-purple-500/30 rounded-lg p-4">
              <h3 className="text-purple-400 font-bold mb-4 flex items-center gap-2">
                <Zap className="w-5 h-5" />
                QUICK ACTIONS
              </h3>
              <div className="space-y-2">
                <button
                  onClick={() => {
                    void invokeTool("get_current_session");
                  }}
                  className="w-full py-3 bg-purple-500/10 border border-purple-500/30 rounded hover:bg-purple-500/20 hover:border-purple-500 text-purple-300 font-bold transition-all"
                >
                  CHECK SESSION
                </button>
                <button
                  onClick={() => void fetchJson("/api/v1/analytics/recommendations")}
                  className="w-full py-3 bg-cyan-500/10 border border-cyan-500/30 rounded hover:bg-cyan-500/20 hover:border-cyan-500 text-cyan-300 font-bold transition-all"
                >
                  GET RECOMMENDATIONS
                </button>
                <button
                  onClick={() => void fetchJson("/api/v1/dashboard/context-pressure")}
                  className="w-full py-3 bg-green-500/10 border border-green-500/30 rounded hover:bg-green-500/20 hover:border-green-500 text-green-300 font-bold transition-all"
                >
                  CONTEXT PRESSURE
                </button>
              </div>
            </div>

            <div className="bg-black border border-green-500/30 rounded-lg p-4">
              <h3 className="text-green-400 font-bold mb-4 flex items-center gap-2">
                <Database className="w-5 h-5" />
                SYSTEM STATUS
              </h3>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-green-400/60">Burnout Risk</span>
                  <span className="text-green-300 font-mono">{burnout.risk.toUpperCase()}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-green-400/60">Burnout Score</span>
                  <span className="text-cyan-300 font-mono">{burnout.score}%</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-green-400/60">API</span>
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
                    <span className="text-green-400 text-sm">ONLINE</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div
        className="fixed inset-0 pointer-events-none z-20 bg-gradient-to-b from-transparent via-cyan-500/5 to-transparent animate-pulse"
        style={{ animationDuration: "4s" }}
      />
    </div>
  );
}
