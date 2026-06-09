<div align="center">

<img src="https://img.shields.io/badge/version-1.0.0-0ea5e9?style=flat-square" />
<img src="https://img.shields.io/badge/license-MIT-22c55e?style=flat-square" />
<img src="https://img.shields.io/badge/status-live-22c55e?style=flat-square" />
<img src="https://img.shields.io/badge/PRs-welcome-f59e0b?style=flat-square" />
<img src="https://img.shields.io/badge/cost-$0.00-22c55e?style=flat-square" />

<br/><br/>

# 🎙️ AI Meeting Notes Summarizer

### Upload any meeting recording. Get structured, professional notes — instantly.

**No manual effort. No missed action items. No forgotten decisions.**

[🚀 Live Demo](https://meeting-ai-summarizer.vercel.app) · [⚙️ API Docs](https://meeting-ai-summarizer.onrender.com/docs) · [🐛 Report Bug](https://github.com/frazyusaf/meeting-ai-summarizer/issues) · [✨ Request Feature](https://github.com/frazyusaf/meeting-ai-summarizer/issues)

<br/>

!\[Tech Stack](https://skillicons.dev/icons?i=python,fastapi,nextjs,ts,tailwind,postgres,docker)

<br/>



!\[Upload Page](screenshots/upload.png)

!\[Dashboard](screenshots/dashboard.png)

</div>

\---

## 📋 Table of Contents

* [About the Project](#-about-the-project)
* [Features](#-features)
* [Tech Stack](#-tech-stack)
* [System Architecture](#-system-architecture)
* [Getting Started](#-getting-started)

  * [Prerequisites](#prerequisites)
  * [Installation (Docker)](#installation-with-docker-recommended)
  * [Installation (Manual)](#manual-installation)
* [Environment Variables](#-environment-variables)
* [API Reference](#-api-reference)
* [Database Schema](#-database-schema)
* [Project Structure](#-project-structure)
* [Roadmap](#-roadmap)
* [Contributing](#-contributing)
* [License](#-license)

\---

## 🧠 About the Project

Meetings generate enormous value — but that value is lost if no one properly documents what was said. Participants spend hours reviewing recordings or relying on incomplete handwritten notes, and critical decisions or action items slip through the cracks.

**AI Meeting Notes Summarizer** solves this. Upload an audio or video recording of any meeting and receive a fully structured set of notes within seconds:

* ✅ A concise **meeting summary**
* ✅ All **action items** with assignees and deadlines
* ✅ **Key decisions** made during the meeting
* ✅ Important **discussion points**
* ✅ Downloadable **PDF, DOCX, or TXT** export

Built as a full-stack, production-deployed application using modern technologies — this project demonstrates end-to-end product thinking, AI integration, and real-world deployment on free-tier infrastructure.

\---

## ✨ Features

|Feature|Description|
|-|-|
|🎵 **Multi-format Upload**|Supports `.mp3`, `.wav`, and `.mp4` files up to 100MB|
|🗣️ **AI Transcription**|Powered by Groq Whisper Large v3 — fast, accurate, multi-language|
|📝 **Smart Summarization**|Llama 3.3 70B extracts summaries, action items, and decisions|
|📤 **Export Options**|Download notes as PDF, DOCX, or plain TXT|
|🔍 **Meeting History**|Browse and revisit all past meeting notes|
|🔐 **Authentication**|Secure JWT-based login and registration|
|🐳 **Docker Support**|Full stack runs with a single `docker compose up`|
|📱 **Responsive Design**|Works seamlessly on desktop and mobile|
|💸 **100% Free to Run**|Entirely on free-tier services — $0/month infrastructure cost|

\---

## 🛠️ Tech Stack

|Layer|Technology|Why|
|-|-|-|
|**Backend**|FastAPI (Python)|Async, modern, auto-generates API docs|
|**Frontend**|Next.js 15 + TypeScript|SEO-friendly, Vercel-deployable, production-ready|
|**UI**|shadcn/ui + Tailwind CSS|Professional polish with minimal custom CSS|
|**Transcription**|Groq Whisper Large v3|Best-in-class accuracy, runs on Groq servers (no RAM cost)|
|**Summarization**|Groq Llama 3.3 70B|Fast, free, structured JSON output|
|**Database**|PostgreSQL|Production-grade relational DB|
|**Auth**|JWT + bcrypt|Secure, stateless authentication|
|**Exports**|ReportLab + python-docx|PDF and DOCX generation|
|**Containerization**|Docker + Compose|One-command local setup|
|**Backend Hosting**|Render.com (free tier)|Auto-deploy from GitHub|
|**Frontend Hosting**|Vercel (free tier)|Global CDN, instant deploys|
|**DB Hosting**|Render PostgreSQL (free tier)|Managed, zero-config|

\---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│           Frontend — Next.js 15 (Vercel)                    │
│      https://meeting-ai-summarizer.vercel.app               │
└───────────────────────┬─────────────────────────────────────┘
                        │ HTTPS / REST
┌───────────────────────▼─────────────────────────────────────┐
│           Backend API — FastAPI (Render.com)                 │
│      https://meeting-ai-summarizer.onrender.com             │
└──────────┬────────────┬────────────────┬────────────────────┘
           │            │                │
    ┌──────▼──────┐  ┌──▼────────────┐  ┌─────▼──────────┐
    │    Groq     │  │     Groq      │  │  PostgreSQL    │
    │  Whisper    │  │  Llama 3.3    │  │  (Render DB)   │
    │  Large v3   │  │    70B        │  │                │
    │ (Speech→Text)│  │ (Summarize)  │  │ (Persistence)  │
    └─────────────┘  └───────────────┘  └────────────────┘
```

**Processing Pipeline:**

```
User uploads file (MP3 / WAV / MP4)
        ↓
File saved to server
        ↓
Groq Whisper Large v3 → full transcript
        ↓
Groq Llama 3.3 70B → structured JSON notes
        ↓
Results stored in PostgreSQL
        ↓
Frontend renders dashboard + export options
```

\---

## 🚀 Getting Started

### Prerequisites

* [Docker \& Docker Compose](https://docs.docker.com/get-docker/) *(recommended)*
* Or: Python 3.11+, Node.js 18+, PostgreSQL 15
* A free [Groq API key](https://console.groq.com) *(no credit card needed)*

### Installation with Docker *(Recommended)*

```bash
# 1. Clone the repository
git clone https://github.com/frazyusaf/meeting-ai-summarizer.git
cd meeting-ai-summarizer

# 2. Set up environment variables
cp .env.example .env
# Open .env and add your GROQ\_API\_KEY

# 3. Start the full stack
docker compose up
```

The app will be available at:

* **Frontend:** http://localhost:3000
* **Backend API:** http://localhost:8000
* **API Docs:** http://localhost:8000/docs

\---

### Manual Installation

**Backend (FastAPI)**

```bash
cd backend

python -m venv venv
source venv/bin/activate        # Windows: venv\\Scripts\\activate

pip install -r requirements.txt

cp .env.example .env
# Fill in your GROQ\_API\_KEY and DATABASE\_URL

uvicorn main:app --reload --port 8000
```

**Frontend (Next.js)**

```bash
cd frontend

npm install

echo "NEXT\_PUBLIC\_API\_URL=http://localhost:8000" > .env.local

npm run dev
```

\---

## 🔑 Environment Variables

### Backend (`backend/.env`)

```env
# Required
GROQ\_API\_KEY=gsk\_your\_groq\_key\_here
DATABASE\_URL=postgresql://postgres:password@localhost:5432/meeting\_ai
JWT\_SECRET\_KEY=your-random-32-character-secret-key
FRONTEND\_URL=http://localhost:3000
```

### Frontend (`frontend/.env.local`)

```env
NEXT\_PUBLIC\_API\_URL=http://localhost:8000
```

> ⚠️ Never commit `.env` files to GitHub. They are already in `.gitignore`.

> 💡 Get your free Groq API key at https://console.groq.com — no credit card required.

\---

## 📡 API Reference

|Method|Endpoint|Description|
|-|-|-|
|`POST`|`/api/upload`|Upload a meeting audio/video file|
|`POST`|`/api/transcribe`|Transcribe via Groq Whisper Large v3|
|`POST`|`/api/summarize`|Summarize via Groq Llama 3.3 70B|
|`GET`|`/api/export/{id}?format=pdf`|Export notes (pdf / docx / txt)|
|`GET`|`/api/meetings`|List all meetings|
|`GET`|`/api/meetings/{id}`|Get single meeting with transcript + summary|
|`POST`|`/api/auth/register`|Register a new user|
|`POST`|`/api/auth/login`|Login and receive JWT token|

Full interactive docs: **https://meeting-ai-summarizer.onrender.com/docs**

**Sample AI Output:**

```json
{
  "summary": "The team reviewed Q3 targets and approved a budget increase for the marketing campaign launching in October.",
  "action\_items": \[
    { "task": "Prepare Q3 sales report", "assignee": "Ali", "deadline": "Friday" },
    { "task": "Contact vendor for pricing", "assignee": "Sara", "deadline": "Next Monday" }
  ],
  "decisions": \[
    "Launch new campaign in October",
    "Approve 20% marketing budget increase"
  ],
  "key\_points": \[
    "Revenue down 12% compared to Q2",
    "Two new sales hires approved"
  ]
}
```

\---

## 🗄️ Database Schema

```sql
CREATE TABLE users (
    id            UUID PRIMARY KEY DEFAULT gen\_random\_uuid(),
    email         VARCHAR(255) UNIQUE NOT NULL,
    password\_hash VARCHAR(255) NOT NULL,
    name          VARCHAR(100),
    created\_at    TIMESTAMP DEFAULT NOW()
);

CREATE TABLE meetings (
    id               UUID PRIMARY KEY DEFAULT gen\_random\_uuid(),
    user\_id          UUID REFERENCES users(id) ON DELETE CASCADE,
    title            VARCHAR(255),
    file\_path        TEXT,
    status           VARCHAR(50) DEFAULT 'uploaded',
    duration\_seconds INTEGER,
    created\_at       TIMESTAMP DEFAULT NOW()
);

CREATE TABLE transcripts (
    id         UUID PRIMARY KEY DEFAULT gen\_random\_uuid(),
    meeting\_id UUID REFERENCES meetings(id) ON DELETE CASCADE,
    full\_text  TEXT,
    language   VARCHAR(20),
    created\_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE summaries (
    id           UUID PRIMARY KEY DEFAULT gen\_random\_uuid(),
    meeting\_id   UUID REFERENCES meetings(id) ON DELETE CASCADE,
    summary      TEXT,
    action\_items JSONB,
    decisions    JSONB,
    key\_points   JSONB,
    created\_at   TIMESTAMP DEFAULT NOW()
);
```

\---

## 📁 Project Structure

```
meeting-ai-summarizer/
│
├── backend/
│   ├── api/routes/
│   │   ├── auth.py           # JWT login \& registration
│   │   ├── upload.py         # File upload endpoint
│   │   ├── transcribe.py     # Groq Whisper transcription
│   │   ├── summarize.py      # Groq Llama summarization
│   │   └── export.py         # PDF / DOCX / TXT export
│   ├── models/               # SQLAlchemy ORM + Pydantic schemas
│   ├── services/
│   │   ├── whisper\_service.py   # Groq Whisper integration
│   │   ├── gpt\_service.py       # Groq Llama integration
│   │   └── export\_service.py    # File generation logic
│   ├── database/             # DB connection + SQL schema
│   ├── main.py               # FastAPI app entry point
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── pages/
│   │   ├── index.tsx             # Upload page
│   │   ├── dashboard/\[id].tsx    # Results dashboard
│   │   └── history.tsx           # Meeting history
│   ├── styles/globals.css
│   └── Dockerfile
│
├── docker-compose.yml
├── render.yaml
├── .gitignore
└── README.md
```

\---

## 🗓️ Roadmap

### ✅ Completed (v1.0)

* \[x] Audio/video upload (MP3, WAV, MP4)
* \[x] AI transcription via Groq Whisper Large v3
* \[x] AI summarization via Groq Llama 3.3 70B
* \[x] Export as PDF, DOCX, TXT
* \[x] Meeting history dashboard
* \[x] JWT authentication
* \[x] Docker support
* \[x] Deployed on Render + Vercel — 100% free

### 🔄 Phase 2 (Upcoming)

* \[ ] Speaker diarization — identify who said what
* \[ ] Analytics dashboard — speaking time, participation %
* \[ ] Full-text search across all past meetings
* \[ ] Email summaries to participants
* \[ ] Zoom / Google Meet direct integration
* \[ ] Multi-language UI support

\---

## 🤝 Contributing

```bash
git checkout -b feat/your-feature
git commit -m 'feat: add your feature'
git push origin feat/your-feature
# Open a Pull Request
```

\---

## 📄 License

Distributed under the MIT License. See `LICENSE` for details.

\---

## 👤 Author

**Muhammad Yusaf**

* GitHub: [@frazyusaf](https://github.com/frazyusaf)
* LinkedIn: [Muhammad Yusaf](https://www.linkedin.com/in/m-yusaf/)

\---

<div align="center">

⭐ **If this project helped you, please give it a star!** ⭐

*Built with FastAPI · Next.js 15 · Groq Whisper · Llama 3.3 · PostgreSQL · Docker*

*Deployed on Render + Vercel — $0.00/month*

</div>

