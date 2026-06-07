import openai
import json
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
    """
    Send transcript to GPT-4o-mini and return structured meeting notes.

    Args:
        transcript: Full meeting transcript text
        meeting_title: Optional title for context

    Returns:
        dict with keys: summary, action_items, decisions, key_points
    """
    if not transcript or len(transcript.strip()) < 50:
        raise ValueError("Transcript is too short to summarize.")

    prompt = USER_PROMPT_TEMPLATE.format(
        title=meeting_title,
        transcript=transcript[:12000],  # Respect context limits
    )

    logger.info(f"Sending transcript to GPT ({len(transcript)} chars)")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=1500,
    )

    raw = response.choices[0].message.content.strip()

    # Strip markdown fences if model adds them anyway
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    try:
        result = json.loads(raw)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse GPT response: {e}\nRaw: {raw[:500]}")
        raise ValueError(f"GPT returned invalid JSON: {e}")

    # Ensure all expected keys exist
    result.setdefault("summary", "")
    result.setdefault("action_items", [])
    result.setdefault("decisions", [])
    result.setdefault("key_points", [])

    return result
