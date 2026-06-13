import { useEffect, useState } from "react";
import { useRouter } from "next/router";
import Head from "next/head";
import axios from "axios";
import { Mic, ArrowLeft, Clock, CheckCircle, Loader2, AlertCircle, ChevronRight } from "lucide-react";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface Meeting {
  id: string;
  title: string;
  status: string;
  created_at: string;
}

const statusConfig: Record<string, { label: string; color: string; icon: any }> = {
  done:         { label: "Done",         color: "text-green-700 bg-green-50 border-green-100",  icon: CheckCircle },
  uploaded:     { label: "Uploaded",     color: "text-blue-700 bg-blue-50 border-blue-100",     icon: Loader2 },
  transcribing: { label: "Transcribing", color: "text-amber-700 bg-amber-50 border-amber-100",  icon: Loader2 },
  summarizing:  { label: "Summarizing",  color: "text-purple-700 bg-purple-50 border-purple-100", icon: Loader2 },
  error:        { label: "Error",        color: "text-red-700 bg-red-50 border-red-100",         icon: AlertCircle },
};

export default function History() {
  const router = useRouter();
  const [meetings, setMeetings] = useState<Meeting[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
  const sessionId = localStorage.getItem("meeting_session_id") || "";
  axios.get(`${API}/api/meetings`, {
    headers: { "x-session-id": sessionId }
  })
    .then(res => { setMeetings(res.data); setLoading(false); })
    .catch(() => setLoading(false));
  }, []);

  return (
    <>
      <Head><title>Meeting History — MeetingAI</title></Head>
      <div className="min-h-screen" style={{ background: "var(--bg)" }}>

        {/* Nav */}
        <div className="border-b" style={{ background: "var(--card)", borderColor: "var(--border)" }}>
          <div className="max-w-4xl mx-auto px-6 h-16 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Mic className="w-6 h-6 text-blue-600" />
              <span className="font-semibold text-lg" style={{ color: "var(--text)" }}>MeetingAI</span>
            </div>
            <button
              onClick={() => router.push("/")}
              className="flex items-center gap-1.5 text-sm hover:text-blue-600 transition-colors"
              style={{ color: "var(--text-muted)" }}
            >
              <ArrowLeft className="w-4 h-4" /> New Meeting
            </button>
          </div>
        </div>

        <div className="max-w-4xl mx-auto px-6 py-10">
          <h1 className="text-2xl font-bold mb-2" style={{ color: "var(--text)" }}>Meeting History</h1>
          <p className="mb-8" style={{ color: "var(--text-muted)" }}>All your past meetings and their AI-generated notes.</p>

          {loading ? (
            <div className="flex items-center justify-center py-20">
              <Loader2 className="w-8 h-8 text-blue-600 animate-spin" />
            </div>
          ) : meetings.length === 0 ? (
            <div className="card p-16 text-center">
              <Mic className="w-12 h-12 mx-auto mb-4 text-gray-300" />
              <p className="font-medium mb-2" style={{ color: "var(--text)" }}>No meetings yet</p>
              <p className="text-sm mb-6" style={{ color: "var(--text-muted)" }}>Upload your first recording to get started.</p>
              <button
                onClick={() => router.push("/")}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors"
              >
                Upload a Recording
              </button>
            </div>
          ) : (
            <div className="space-y-3">
              {meetings.map(m => {
                const cfg = statusConfig[m.status] || statusConfig.uploaded;
                const Icon = cfg.icon;
                return (
                  <div
                    key={m.id}
                    onClick={() => m.status === "done" && router.push(`/dashboard/${m.id}`)}
                    className={`card p-5 flex items-center justify-between transition-all ${
                      m.status === "done" ? "cursor-pointer hover:border-blue-300 hover:shadow-sm" : "opacity-70"
                    }`}
                  >
                    <div className="flex items-center gap-4">
                      <div className="w-10 h-10 rounded-xl bg-blue-50 flex items-center justify-center flex-shrink-0">
                        <Mic className="w-5 h-5 text-blue-600" />
                      </div>
                      <div>
                        <p className="font-medium" style={{ color: "var(--text)" }}>{m.title || "Untitled Meeting"}</p>
                        <div className="flex items-center gap-2 mt-1">
                          <Clock className="w-3.5 h-3.5" style={{ color: "var(--text-muted)" }} />
                          <span className="text-xs" style={{ color: "var(--text-muted)" }}>
                            {new Date(m.created_at).toLocaleDateString("en-US", { dateStyle: "medium" })}
                          </span>
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center gap-3">
                      <span className={`flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium border ${cfg.color}`}>
                        <Icon className={`w-3 h-3 ${m.status !== "done" && m.status !== "error" ? "animate-spin" : ""}`} />
                        {cfg.label}
                      </span>
                      {m.status === "done" && <ChevronRight className="w-4 h-4" style={{ color: "var(--text-muted)" }} />}
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </>
  );
}
