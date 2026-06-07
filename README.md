<div align="center">

<img src="https://img.shields.io/badge/version-1.0.0-0ea5e9?style=flat-square" />
<img src="https://img.shields.io/badge/license-MIT-22c55e?style=flat-square" />
<img src="https://img.shields.io/badge/status-active-22c55e?style=flat-square" />
<img src="https://img.shields.io/badge/PRs-welcome-f59e0b?style=flat-square" />

<br/><br/>

# 🎙️ AI Meeting Notes Summarizer

### Upload any meeting recording. Get structured, professional notes — instantly.

**No manual effort. No missed action items. No forgotten decisions.**

[🚀 Live Demo](https://meeting-ai-summarizer-4dq636281-frazyusafs-projects.vercel.app) · [📖 Documentation](#-table-of-contents) · [🐛 Report Bug](https://github.com/yourusername/meeting-ai-summarizer/issues) · [✨ Request Feature](https://github.com/yourusername/meeting-ai-summarizer/issues)

<br/>

![Demo Screenshot](screenshots/dashboard-preview.png)

</div>

---

## 📋 Table of Contents

- [About the Project](#-about-the-project)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [System Architecture](#-system-architecture)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation (Docker)](#installation-with-docker-recommended)
  - [Installation (Manual)](#manual-installation)
- [Environment Variables](#-environment-variables)
- [API Reference](#-api-reference)
- [Database Schema](#-database-schema)
- [Project Structure](#-project-structure)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🧠 About the Project

Meetings generate enormous value — but that value is lost if no one properly documents what was said. Participants spend hours reviewing recordings or relying on incomplete handwritten notes, and critical decisions or action items slip through the cracks.

**AI Meeting Notes Summarizer** solves this. Upload an audio or video recording of any meeting and receive a fully structured set of notes within seconds:

- ✅ A concise **meeting summary**
- ✅ All **action items** with assignees and deadlines
- ✅ **Key decisions** made during the meeting
- ✅ Important **discussion points**
- ✅ Downloadable **PDF, DOCX, or TXT** export

Built as a full-stack, SaaS-ready application using modern technologies — this project demonstrates end-to-end product thinking, AI integration, and professional deployment.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎵 **Multi-format Upload** | Supports `.mp3`, `.wav`, and `.mp4` files |
| 🗣️ **AI Transcription** | Powered by OpenAI Whisper — industry-leading accuracy |
| 📝 **Smart Summarization** | GPT-4o-mini extracts summaries, action items, and decisions |
| 📤 **Export Options** | Download notes as PDF, DOCX, or plain TXT |
| 🔍 **Meeting History** | Search and filter all past meeting notes |
| 🔐 **Authentication** | Secure JWT-based login or Clerk integration |
| 🐳 **Docker Support** | Full stack runs with a single `docker compose up` |
| 📱 **Responsive Design** | Works seamlessly on desktop and mobile |
| 🌙 **Dark Mode** | Tailwind-powered dark/light theme toggle |

---

## 🛠️ Tech Stack

| Layer | Technology | Why |
|---|---|---|
| **Backend** | FastAPI (Python) | Async, modern, auto-generates API docs |
| **Frontend** | Next.js + TypeScript | SEO-friendly, Vercel-deployable, production-ready |
| **UI Components** | shadcn/ui + Tailwind CSS | Professional polish with zero custom CSS overhead |
| **Speech-to-Text** | OpenAI Whisper | Best-in-class accuracy, multi-language, open-source |
| **Summarization** | GPT-4o-mini | Structured output, cost-effective, reliable |
| **Database** | PostgreSQL | Production-grade relational DB via Supabase free tier |
| **Auth** | JWT / Clerk | Secure, SaaS-ready authentication |
| **File Processing** | FFmpeg | Industry standard for audio/video extraction |
| **Containerization** | Docker + Compose | One-command local setup |
| **Backend Hosting** | Render.com | Free tier, Python support, easy deploy |
| **Frontend Hosting** | Vercel | Auto-deploy from GitHub, global CDN |
| **DB Hosting** | Supabase | Free PostgreSQL with built-in auth and storage |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────┐
│              Frontend (Next.js on Vercel)            │
└───────────────────────┬─────────────────────────────┘
                        │ HTTP / REST
┌───────────────────────▼─────────────────────────────┐
│            Backend API (FastAPI on Render)           │
└──────────┬────────────┬────────────────┬────────────┘
           │            │                │
    ┌──────▼──────┐  ┌──▼──────┐  ┌─────▼──────────┐
    │  OpenAI     │  │  GPT    │  │  PostgreSQL     │
    │  Whisper    │  │  API    │  │  (Supabase)     │
    │  (STT)      │  │  (NLP)  │  │  (Persistence)  │
    └─────────────┘  └─────────┘  └────────────────┘
```

**Processing Pipeline:**

```
User uploads file (MP3 / WAV / MP4)
        ↓
FFmpeg extracts audio track
        ↓
Whisper converts speech → transcript
        ↓
GPT processes transcript → structured JSON
        ↓
Results stored in PostgreSQL
        ↓
Frontend renders dashboard + export options
```

---

## 🚀 Getting Started

### Prerequisites

- [Docker & Docker Compose](https://docs.docker.com/get-docker/) *(recommended)*
- Or: Python 3.11+, Node.js 18+, PostgreSQL 15, FFmpeg

### Installation with Docker *(Recommended)*

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/meeting-ai-summarizer.git
cd meeting-ai-summarizer

# 2. Set up environment variables
cp .env.example .env
# Open .env and add your OPENAI_API_KEY

# 3. Start the full stack
docker compose up
```

That's it. The app will be available at:
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

### Manual Installation

**Backend (FastAPI)**

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn python-multipart openai whisper ffmpeg-python \
            sqlalchemy psycopg2-binary python-dotenv python-jose bcrypt \
            reportlab python-docx

# Start the backend server
uvicorn main:app --reload --port 8000
```

**Frontend (Next.js)**

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

---

## 🔑 Environment Variables

Copy `.env.example` to `.env` and fill in your values:

```env
# Required
OPENAI_API_KEY=sk-your-openai-key-here
DATABASE_URL=postgresql://postgres:password@localhost:5432/meeting_ai
JWT_SECRET_KEY=your-super-secret-key-minimum-32-characters
FRONTEND_URL=http://localhost:3000

# Optional — Clerk Authentication (alternative to JWT)
CLERK_SECRET_KEY=
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=

# Optional — Email Notifications (SendGrid)
SENDGRID_API_KEY=
FROM_EMAIL=noreply@yourdomain.com
```

> ⚠️ **Never commit your `.env` file to GitHub.** It is already listed in `.gitignore`.

---

## 📡 API Reference

| Method | Endpoint | Description | Response |
|---|---|---|---|
| `POST` | `/api/upload` | Upload a meeting file | `{ file_id, filename, status }` |
| `POST` | `/api/transcribe` | Start transcription | `{ meeting_id, transcript }` |
| `POST` | `/api/summarize` | Generate AI notes | `{ summary, action_items, decisions }` |
| `GET` | `/api/export/{id}` | Export notes as file | File download (PDF / DOCX / TXT) |
| `GET` | `/api/meetings` | List all meetings | `[{ id, title, created_at }]` |
| `POST` | `/api/auth/register` | Register a new user | `{ access_token, user }` |
| `POST` | `/api/auth/login` | Log in | `{ access_token, user }` |

Full interactive docs available at `/docs` when running the backend.

**Sample AI Output:**

```json
{
  "summary": "The team discussed Q3 sales targets and approved a marketing budget increase...",
  "action_items": [
    { "task": "Prepare Q3 sales report", "assignee": "Ali", "deadline": "Friday" },
    { "task": "Contact vendor for pricing", "assignee": "Sara", "deadline": "Next Monday" }
  ],
  "decisions": [
    "Launch new campaign in October",
    "Hire 2 additional sales staff"
  ],
  "key_points": [
    "Revenue down 12% compared to Q2",
    "Marketing budget approved for increase"
  ]
}
```

---

## 🗄️ Database Schema

```sql
-- Users
CREATE TABLE users (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email         VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name          VARCHAR(100),
    created_at    TIMESTAMP DEFAULT NOW()
);

-- Meetings
CREATE TABLE meetings (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id          UUID REFERENCES users(id) ON DELETE CASCADE,
    title            VARCHAR(255),
    file_path        TEXT,
    status           VARCHAR(50) DEFAULT 'uploaded', -- uploaded | transcribing | summarizing | done
    duration_seconds INTEGER,
    created_at       TIMESTAMP DEFAULT NOW()
);

-- Transcripts
CREATE TABLE transcripts (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    meeting_id UUID REFERENCES meetings(id) ON DELETE CASCADE,
    full_text  TEXT,
    language   VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Summaries
CREATE TABLE summaries (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    meeting_id   UUID REFERENCES meetings(id) ON DELETE CASCADE,
    summary      TEXT,
    action_items JSONB,
    decisions    JSONB,
    key_points   JSONB,
    created_at   TIMESTAMP DEFAULT NOW()
);
```

---

## 📁 Project Structure

```
meeting-ai-summarizer/
│
├── backend/
│   ├── api/
│   │   └── routes/
│   │       ├── upload.py         # File upload endpoint
│   │       ├── transcribe.py     # Whisper transcription
│   │       ├── summarize.py      # GPT summarization
│   │       ├── export.py         # PDF/DOCX/TXT export
│   │       └── auth.py           # Login & registration
│   ├── models/
│   │   ├── meeting.py
│   │   └── user.py
│   ├── services/
│   │   ├── whisper_service.py    # Speech-to-text logic
│   │   ├── gpt_service.py        # Summarization logic
│   │   └── export_service.py     # File generation
│   ├── database/
│   │   ├── connection.py
│   │   └── schemas.py
│   ├── main.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── components/
│   │   ├── UploadZone.tsx
│   │   ├── TranscriptPanel.tsx
│   │   ├── SummaryCard.tsx
│   │   ├── ActionItems.tsx
│   │   ├── AnalyticsChart.tsx
│   │   └── ExportButton.tsx
│   ├── pages/
│   │   ├── index.tsx             # Landing page
│   │   ├── dashboard/[id].tsx    # Results dashboard
│   │   └── history.tsx           # Meeting history
│   └── package.json
│
├── docs/
├── screenshots/
├── docker-compose.yml
├── .gitignore
├── README.md
└── LICENSE
```

---

## 🗓️ Roadmap

### ✅ MVP (v1.0)
- [x] Audio/video file upload (MP3, WAV, MP4)
- [x] Speech-to-text via OpenAI Whisper
- [x] AI summarization via GPT-4o-mini
- [x] Export as PDF, DOCX, TXT
- [x] Meeting history dashboard
- [x] JWT authentication
- [x] Docker support
- [x] Deployment to Render + Vercel

### 🔄 Phase 2 (Upcoming)
- [ ] **Speaker diarization** — identify who said what using `pyannote.audio`
- [ ] **Analytics dashboard** — speaking time, participation %, keyword frequency
- [ ] **Smart search** — full-text search across all past meeting notes (PostgreSQL GIN index)
- [ ] **Email summaries** — auto-send notes to participants via SendGrid / Resend
- [ ] **Zoom / Google Meet integration** — direct import from meeting platforms
- [ ] **Multi-language UI** — Urdu and other languages
- [ ] **Sentiment analysis** — detect tone and meeting energy

---

## 🤝 Contributing

Contributions are welcome and appreciated.

```bash
# 1. Fork the repo
# 2. Create your feature branch
git checkout -b feat/speaker-diarization

# 3. Commit with a meaningful message
git commit -m 'feat: add pyannote speaker diarization'

# 4. Push and open a Pull Request
git push origin feat/speaker-diarization
```

**Commit message convention:**

| Prefix | Usage |
|---|---|
| `feat:` | New feature |
| `fix:` | Bug fix |
| `docs:` | Documentation |
| `style:` | UI/formatting changes |
| `refactor:` | Code cleanup |

---

## 📄 License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for details.

---

## 👤 Author

**Muhammad Yusaf**

- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [your-linkedin](https://linkedin.com/in/your-profile)

---

<div align="center">

⭐ **If this project helped you, please give it a star!** ⭐

*Built with FastAPI · Next.js · OpenAI Whisper · GPT-4o-mini · PostgreSQL · Docker*

</div>
