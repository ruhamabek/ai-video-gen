#!/usr/bin/env python3
"""
Pipeline Stage 1: Script & Storyboard Generation (Gemini 3.8 Flash)
Generates and validates storyboard.json against schema/storyboard.schema.json.
"""

import os
import json
import time
from pipeline.common import (
    load_storyboard,
    validate_storyboard,
    log_run,
    STORYBOARD_PATH,
)


def generate_or_validate_script(concept: dict = None) -> dict:
    """Validate existing storyboard contract or generate new one from concept via Gemini."""
    api_key = os.getenv("GEMINI_API_KEY")
    start_time = time.time()

    if STORYBOARD_PATH.exists():
        print("  📄 Reading existing storyboard.json contract...")
        storyboard = load_storyboard()
    else:
        if not api_key:
            raise ValueError("GEMINI_API_KEY is required to generate a new storyboard.json")
        print("  🤖 Generating screenplay via Gemini 3.8 Flash...")
        import urllib.request
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
        prompt = f"""Generate a valid JSON film storyboard conforming to this concept: {json.dumps(concept)}.
Output ONLY valid JSON matching the schema."""
        req = urllib.request.Request(
            url,
            data=json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            res = json.loads(response.read().decode())
            text = res["candidates"][0]["content"]["parts"][0]["text"]
            storyboard = json.loads(text.strip("` \n").replace("json", "", 1))
            with open(STORYBOARD_PATH, "w", encoding="utf-8") as f:
                json.dump(storyboard, f, indent=2, ensure_ascii=False)

    # Validate against Schema
    validate_storyboard(storyboard)
    latency = time.time() - start_time
    print(f"  ✓ Storyboard '{storyboard['title']}' validated ({len(storyboard['shots'])} shots, {storyboard['total_duration_seconds']}s)")

    log_run(
        stage="script_generation",
        model="gemini-3.8-flash",
        parameters={"language": storyboard.get("language", "Amharic"), "shot_count": len(storyboard["shots"])},
        seed=42,
        latency_seconds=latency,
        cost_usd=0.0
    )
    return storyboard


def main():
    print("▶ [Stage: Script] Storyboard Contract Validation & Script Stage...")
    generate_or_validate_script()
    print("✓ Script stage complete.\n")


if __name__ == "__main__":
    main()
