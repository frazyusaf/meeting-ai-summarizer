import { useState } from "react";
import { useRouter } from "next/router";
import Head from "next/head";
import axios from "axios";
import {
  Upload,
  Zap,
  FileText,
  CheckSquare,
  Download,
  Mic,
  ArrowRight,
  Sparkles,
} from "lucide-react";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function Home() {
  const router = useRouter();
  const [dragging, setDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState("");

  const handleFile = async (file: File) => {
    const ext = file.name.split(".").pop()?.toLowerCase();
    if (!["mp3", "wav", "mp4"].includes(ext || "")) {
      setError("Only .mp3, .wav, and .mp4 files are supported.");
      return;
    }

    setError("");
    setUploading(true);
    setProgress(10);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const uploadRes = await axios.post(`${API}/api/upload`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
        onUploadProgress: (e) => {
          if (e.total) setProgress(Math.round((e.loaded / e.total) * 40));
        },
      });

      const { meeting_id } = uploadRes.data;
      setProgress(45);

      await axios.post(`${API}/api/transcribe`, { meeting_id });
      setProgress(75);

      await axios.post(`${API}/api/summarize`, { meeting_id });
      setProgress(100);

      router.push(`/dashboard/${meeting_id}`);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Something went wrong. Please try again.");
      setUploading(false);
      setProgress(0);
    }
  };

  const onDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragging(false);
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  };

  const onFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) handleFile(file);
  };

  const features = [
    { icon: Mic, title: "AI Transcription", desc: "Powered by OpenAI Whisper — industry-leading accuracy across accents and languages." },
    { icon: Sparkles, title: "Smart Summarization", desc: "GPT-4o-mini extracts the summary, action items, decisions, and key points automatically." },
    { icon: CheckSquare, title: "Action Items", desc: "Every task is extracted with its assignee and deadline — nothing falls through the cracks." },
    { icon: Download, title: "Export Anywhere", desc: "Download your notes as PDF, DOCX, or plain text in one click." },
  ];

  return (
    <>
      <Head>
        <title>AI Meeting Notes Summarizer</title>
        <meta name="description" content="Upload any meeting recording and get structured AI-generated notes instantly." />
      </Head>

      <div className="min-h-screen" style={{ background: "var(--bg)" }}>
        {/* Nav */}
        <nav className="border-b" style={{ borderColor: "var(--border)", background: "var(--card)" }}>
          <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Mic className="w-6 h-6 text-blue-600" />
              <span className="font-semibold text-lg" style={{ color: "var(--text)" }}>MeetingAI</span>
            </div>
            <a
              href="/history"
              className="text-sm font-medium flex items-center gap-1 hover:text-blue-600 transition-colors"
              style={{ color: "var(--text-muted)" }}
            >
              Past Meetings <ArrowRight className="w-4 h-4" />
            </a>
          </div>
        </nav>

        {/* Hero */}
        <div className="max-w-4xl mx-auto px-6 pt-20 pb-16 text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-sm font-medium mb-6 text-blue-700 bg-blue-50 border border-blue-100">
            <Zap className="w-3.5 h-3.5" />
            Powered by OpenAI Whisper + GPT-4o-mini
          </div>
          <h1 className="text-5xl font-bold mb-5 leading-tight" style={{ color: "var(--text)" }}>
            Meeting notes,<br />
            <span className="text-blue-600">written by AI.</span>
          </h1>
          <p className="text-xl mb-12" style={{ color: "var(--text-muted)" }}>
            Upload any meeting recording and get a structured summary, action items,
            key decisions, and more — in seconds.
          </p>

          {/* Upload Zone */}
          <div
            onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
            onDragLeave={() => setDragging(false)}
            onDrop={onDrop}
            className={`relative border-2 border-dashed rounded-2xl p-12 transition-all cursor-pointer ${
              dragging ? "border-blue-500 bg-blue-50" : "border-gray-200 hover:border-blue-400 hover:bg-blue-50/30"
            }`}
            style={{ background: dragging ? "#eff6ff" : "var(--card)" }}
            onClick={() => document.getElementById("file-input")?.click()}
          >
            <input
              id="file-input"
              type="file"
              accept=".mp3,.wav,.mp4"
              className="hidden"
              onChange={onFileChange}
              disabled={uploading}
            />

            {uploading ? (
              <div className="space-y-4">
                <div className="flex justify-center">
                  <div className="w-14 h-14 rounded-full border-4 border-blue-200 border-t-blue-600 animate-spin" />
                </div>
                <p className="font-medium text-blue-600">
                 {progress < 30 ? "Uploading file..." : progress < 45 ? "Sending to Groq Whisper..." : progress < 75 ? "Transcribing audio with AI..." : "Generating structured notes..."}
                </p>
                <div className="w-full bg-gray-100 rounded-full h-2 max-w-xs mx-auto overflow-hidden">
                  <div
                    className="h-2 rounded-full bg-blue-600 transition-all duration-500"
                    style={{ width: `${progress}%` }}
                  />
                </div>
                <p className="text-sm" style={{ color: "var(--text-muted)" }}>{progress}% complete</p>
              </div>
            ) : (
              <div className="space-y-3">
                <div className="flex justify-center">
                  <div className="w-16 h-16 rounded-2xl bg-blue-50 flex items-center justify-center">
                    <Upload className="w-8 h-8 text-blue-600" />
                  </div>
                </div>
                <p className="text-lg font-semibold" style={{ color: "var(--text)" }}>
                  Drop your meeting recording here
                </p>
                <p style={{ color: "var(--text-muted)" }}>
                  or click to browse — supports <strong>.mp3</strong>, <strong>.wav</strong>, <strong>.mp4</strong>
                </p>
                <p className="text-sm" style={{ color: "var(--text-muted)" }}>Max 100 MB</p>
              </div>
            )}
          </div>

          {error && (
            <div className="mt-4 p-3 rounded-lg bg-red-50 border border-red-200 text-red-700 text-sm">
              {error}
            </div>
          )}
        </div>

        {/* Features */}
        <div className="max-w-6xl mx-auto px-6 pb-24">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map(({ icon: Icon, title, desc }) => (
              <div key={title} className="card p-6">
                <div className="w-10 h-10 rounded-xl bg-blue-50 flex items-center justify-center mb-4">
                  <Icon className="w-5 h-5 text-blue-600" />
                </div>
                <h3 className="font-semibold mb-2" style={{ color: "var(--text)" }}>{title}</h3>
                <p className="text-sm leading-relaxed" style={{ color: "var(--text-muted)" }}>{desc}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </>
  );
}
