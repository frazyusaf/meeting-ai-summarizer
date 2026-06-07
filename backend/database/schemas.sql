-- AI Meeting Notes Summarizer — Database Schema
-- Run this against your PostgreSQL database to initialize all tables.

-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Users
CREATE TABLE IF NOT EXISTS users (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email         VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name          VARCHAR(100),
    created_at    TIMESTAMP DEFAULT NOW()
);

-- Meetings
CREATE TABLE IF NOT EXISTS meetings (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id          UUID REFERENCES users(id) ON DELETE CASCADE,
    title            VARCHAR(255),
    file_path        TEXT,
    status           VARCHAR(50) DEFAULT 'uploaded',  -- uploaded | transcribing | summarizing | done | error
    duration_seconds INTEGER,
    created_at       TIMESTAMP DEFAULT NOW()
);

-- Transcripts
CREATE TABLE IF NOT EXISTS transcripts (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    meeting_id UUID REFERENCES meetings(id) ON DELETE CASCADE,
    full_text  TEXT,
    language   VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Summaries
CREATE TABLE IF NOT EXISTS summaries (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    meeting_id   UUID REFERENCES meetings(id) ON DELETE CASCADE,
    summary      TEXT,
    action_items JSONB,
    decisions    JSONB,
    key_points   JSONB,
    created_at   TIMESTAMP DEFAULT NOW()
);

-- Full-text search index on summaries (Phase 2)
CREATE INDEX IF NOT EXISTS summaries_text_idx
    ON summaries USING GIN (to_tsvector('english', summary));
