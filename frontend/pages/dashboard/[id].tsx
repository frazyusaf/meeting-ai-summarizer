import { useEffect, useState } from "react";
import { useRouter } from "next/router";
import Head from "next/head";
import axios from "axios";
import {
  CheckSquare, Lightbulb, MessageSquare, Download,
  ArrowLeft, Loader2, FileText, Clock, Mic
} from "lucide-react";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface ActionItem {
  task: string;
  assignee: string | null;
  deadline: string | null;
}

interface MeetingData {
  id: string;
  title: string;
  status: string;
  created_at: string;
  transcript: { text: string; language: string } | null;
  summary: {
    summary: string;
    action_items: ActionItem[];
    decisions: string[];
    key_points: string[];
  } | null;
}

export default function Dashboard() {
  const router = useRouter();
  const { id } = router.query;
  const [meeting, setMeeting] = useState<MeetingData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [activeTab, setActiveTab] = useState<"summary" | "transcript">("summary");
  const [exporting, setExporting] = useState("");

  useEffect(() => {
  if (!id) return;
  const sessionId = localStorage.getItem("meeting_session_id") || "";
  axios.get(`${API}/api/meetings/${id}`, {
    headers: { "x-session-id": sessionId }
  })
    .then(res => { setMeeting(res.data); setLoading(false); })
    .catch(() => { setError("Could not load meeting."); setLoading(false); });
  }, [id]);

  const handleExport = async (format: string) => {
  setExporting(format);
  const sessionId = localStorage.getItem("meeting_session_id") || "";
  try {
    const res = await axios.get(`${API}/api/export/${id}?format=${format}`, {
      responseType: "blob",
      headers: { "x-session-id": sessionId }
    });
    const url = window.URL.createObjectURL(new Blob([res.data]));
    const a = document.createElement("a");
    a.href = url;
    a.download = `${meeting?.title || "meeting"}.${format}`;
    a.click();
    window.URL.revokeObjectURL(url);
  } catch {
    alert("Export failed. Please try again.");
  }
  setExporting("");
  };

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center" style={{ background: "var(--bg)" }}>
      <div className="text-center space-y-3">
        <Loader2 className="w-10 h-10 text-blue-600 animate-spin mx-auto" />
        <p style={{ color: "var(--text-muted)" }}>Loading meeting notes...</p>
      </div>
    </div>
  );

  if (error || !meeting) return (
    <div className="min-h-screen flex items-center justify-center" style={{ background: "var(--bg)" }}>
      <div className="text-center space-y-4">
        <p className="text-red-500">{error || "Meeting not found."}</p>
        <button onClick={() => router.push("/")} className="text-blue-600 hover:underline">← Go back</button>
      </div>
    </div>
  );

  const s = meeting.summary;

  return (
    <>
      <Head><title>{meeting.title} — MeetingAI</title></Head>
      <div className="min-h-screen" style={{ background: "var(--bg)" }}>

        {/* Header */}
        <div className="border-b" style={{ background: "var(--card)", borderColor: "var(--border)" }}>
          <div className="max-w-6xl mx-auto px-6 py-4">
            <button
              onClick={() => router.push("/")}
              className="flex items-center gap-2 text-sm mb-3 hover:text-blue-600 transition-colors"
              style={{ color: "var(--text-muted)" }}
            >
              <ArrowLeft className="w-4 h-4" /> Back to Upload
            </button>
            <div className="flex items-start justify-between flex-wrap gap-4">
              <div>
                <h1 className="text-2xl font-bold" style={{ color: "var(--text)" }}>{meeting.title}</h1>
                <div className="flex items-center gap-4 mt-1">
                  <span className="flex items-center gap-1 text-sm" style={{ color: "var(--text-muted)" }}>
                    <Clock className="w-3.5 h-3.5" />
                    {new Date(meeting.created_at).toLocaleDateString("en-US", { dateStyle: "medium" })}
                  </span>
                  {meeting.transcript?.language && (
                    <span className="flex items-center gap-1 text-sm" style={{ color: "var(--text-muted)" }}>
                      <Mic className="w-3.5 h-3.5" /> {meeting.transcript.language.toUpperCase()}
                    </span>
                  )}
                  <span className="px-2 py-0.5 rounded-full text-xs font-medium bg-green-50 text-green-700 border border-green-100">
                    ✓ Done
                  </span>
                </div>
              </div>
              {/* Export Buttons */}
              <div className="flex items-center gap-2">
                {["pdf", "docx", "txt"].map(fmt => (
                  <button
                    key={fmt}
                    onClick={() => handleExport(fmt)}
                    disabled={!!exporting}
                    className="flex items-center gap-1.5 px-3 py-2 rounded-lg border text-sm font-medium hover:bg-blue-50 hover:border-blue-300 hover:text-blue-700 transition-all disabled:opacity-50"
                    style={{ borderColor: "var(--border)", color: "var(--text)" }}
                  >
                    {exporting === fmt
                      ? <Loader2 className="w-3.5 h-3.5 animate-spin" />
                      : <Download className="w-3.5 h-3.5" />}
                    {fmt.toUpperCase()}
                  </button>
                ))}
              </div>
            </div>

            {/* Tabs */}
            <div className="flex gap-1 mt-4">
              {(["summary", "transcript"] as const).map(tab => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`px-4 py-2 rounded-lg text-sm font-medium capitalize transition-colors ${
                    activeTab === tab
                      ? "bg-blue-600 text-white"
                      : "hover:bg-gray-100"
                  }`}
                  style={activeTab !== tab ? { color: "var(--text-muted)" } : {}}
                >
                  {tab === "summary" ? "AI Notes" : "Full Transcript"}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Content */}
        <div className="max-w-6xl mx-auto px-6 py-8">
          {activeTab === "summary" && s ? (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

              {/* Summary — wide */}
              <div className="lg:col-span-3 card p-6">
                <div className="flex items-center gap-2 mb-3">
                  <FileText className="w-5 h-5 text-blue-600" />
                  <h2 className="font-semibold text-lg" style={{ color: "var(--text)" }}>Summary</h2>
                </div>
                <p className="leading-relaxed" style={{ color: "var(--text-muted)" }}>{s.summary}</p>
              </div>

              {/* Action Items */}
              <div className="lg:col-span-2 card p-6">
                <div className="flex items-center gap-2 mb-4">
                  <CheckSquare className="w-5 h-5 text-blue-600" />
                  <h2 className="font-semibold text-lg" style={{ color: "var(--text)" }}>
                    Action Items
                    <span className="ml-2 px-2 py-0.5 rounded-full text-xs bg-blue-50 text-blue-700">
                      {s.action_items?.length || 0}
                    </span>
                  </h2>
                </div>
                {s.action_items?.length ? (
                  <div className="space-y-3">
                    {s.action_items.map((item, i) => (
                      <div key={i} className="flex items-start gap-3 p-3 rounded-lg" style={{ background: "var(--bg)" }}>
                        <div className="w-5 h-5 rounded border-2 border-blue-300 mt-0.5 flex-shrink-0" />
                        <div>
                          <p className="font-medium text-sm" style={{ color: "var(--text)" }}>{item.task}</p>
                          <div className="flex gap-3 mt-1">
                            {item.assignee && (
                              <span className="text-xs px-2 py-0.5 rounded-full bg-blue-50 text-blue-700">{item.assignee}</span>
                            )}
                            {item.deadline && (
                              <span className="text-xs px-2 py-0.5 rounded-full bg-amber-50 text-amber-700">{item.deadline}</span>
                            )}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : <p className="text-sm" style={{ color: "var(--text-muted)" }}>No action items found.</p>}
              </div>

              {/* Decisions */}
              <div className="card p-6">
                <div className="flex items-center gap-2 mb-4">
                  <Lightbulb className="w-5 h-5 text-amber-500" />
                  <h2 className="font-semibold text-lg" style={{ color: "var(--text)" }}>Decisions</h2>
                </div>
                {s.decisions?.length ? (
                  <ul className="space-y-2">
                    {s.decisions.map((d, i) => (
                      <li key={i} className="flex items-start gap-2 text-sm" style={{ color: "var(--text-muted)" }}>
                        <span className="text-amber-500 mt-0.5">•</span>{d}
                      </li>
                    ))}
                  </ul>
                ) : <p className="text-sm" style={{ color: "var(--text-muted)" }}>No decisions recorded.</p>}
              </div>

              {/* Key Points */}
              <div className="lg:col-span-3 card p-6">
                <div className="flex items-center gap-2 mb-4">
                  <MessageSquare className="w-5 h-5 text-purple-500" />
                  <h2 className="font-semibold text-lg" style={{ color: "var(--text)" }}>Key Discussion Points</h2>
                </div>
                {s.key_points?.length ? (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                    {s.key_points.map((kp, i) => (
                      <div key={i} className="flex items-start gap-2 text-sm p-3 rounded-lg" style={{ background: "var(--bg)", color: "var(--text-muted)" }}>
                        <span className="text-purple-500 mt-0.5">→</span>{kp}
                      </div>
                    ))}
                  </div>
                ) : <p className="text-sm" style={{ color: "var(--text-muted)" }}>No key points extracted.</p>}
              </div>

            </div>
          ) : activeTab === "transcript" && meeting.transcript ? (
            <div className="card p-6">
              <h2 className="font-semibold text-lg mb-4" style={{ color: "var(--text)" }}>Full Transcript</h2>
              <pre className="whitespace-pre-wrap text-sm leading-relaxed font-sans" style={{ color: "var(--text-muted)" }}>
                {meeting.transcript.text}
              </pre>
            </div>
          ) : (
            <div className="card p-12 text-center">
              <p style={{ color: "var(--text-muted)" }}>No data available for this tab.</p>
            </div>
          )}
        </div>
      </div>
    </>
  );
}
