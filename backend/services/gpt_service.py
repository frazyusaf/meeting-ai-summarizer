import os
import json
import logging
from typing import Optional
from openai import OpenAI

logger = logging.getLogger(__name__)

# Groq uses OpenAI-compatible API — just swap the base_url and key
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

SYSTEM_PROMPT = """You are a professional meeting note-taker and analyst.
Your job is to analyze meeting transcripts and produce clean, structured summaries.
Always return valid JSON — no markdown fences, no extra text."""

USER_PROMPT_TEMPLATE = """Analyze the following meeting transcript and return a JSON object with exactly these keys:

- "summary": A 3–5 sentence overview of what the meeting covered and the overall outcome
- "action_items": A list of tasks. Each item must have: "task" (string), "assignee" (string or null), "deadline" (string or null)
- "decisions": A list of strings — key decisions that were made
- "key_points": A list of strings — important discussion points worth remembering

Meeting Title: {title}

Transcript:
{transcript}

Return ONLY valid JSON. No extra text, no markdown."""


def summarize_transcript(transcript: str, meeting_title: Optional[str] = "Untitled Meeting") -> dict:
    if not transcript or len(transcript.strip()) < 50:
        raise ValueError("Transcript is too short to summarize.")

    prompt = USER_PROMPT_TEMPLATE.format(
        title=meeting_title,
        transcript=transcript[:12000],
    )

    logger.info(f"Sending transcript to Groq ({len(transcript)} chars)")

    response = client.chat.completions.create(
        model="llama3-8b-8192",  # Free, fast Llama 3 model on Groq
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=1500,
    )

    raw = response.choices[0].message.content.strip()

    # Strip markdown fences if model adds them
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    try:
        result = json.loads(raw)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse response: {e}\nRaw: {raw[:500]}")
        raise ValueError(f"Model returned invalid JSON: {e}")

    result.setdefault("summary", "")
    result.setdefault("action_items", [])
    result.setdefault("decisions", [])
    result.setdefault("key_points", [])

    return result