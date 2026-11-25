#!/usr/bin/env python3
"""
Master Pipeline Orchestrator
Executes all stages in sequence to regenerate the film from storyboard.json.
Stages:
  1. pipeline.script
  2. pipeline.narration
  3. pipeline.keyframes
  4. pipeline.shots
  5. pipeline.music
  6. pipeline.assemble
"""

import sys
import time
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from pipeline import script, narration, keyframes, shots, music, assemble


def run_pipeline():
    print("=" * 70)
    print("🎬 AI HERITAGE SHORT FILM PIPELINE: THE FREQUENCY OF MEMORY")
    print("=" * 70)
    start_total = time.time()

    # 1. Script & Contract Validation
    script.main()

    # 2. Narration (Gemini Neural TTS)
    narration.main()

    # 3. Keyframes (FLUX.1 schnell AI Photorealism)
    keyframes.main()

    # 4. Moving Shots (Wan 2.2 / Cinematic Motion)
    shots.main()

    # 5. Musical Score (ACE-Step 1.5 Acoustic Score)
    music.main()

    # 6. Master Assembly & Dual Exports (FFmpeg)
    assemble.main()

    total_time = time.time() - start_total
    print("=" * 70)
    print(f"🎉 Pipeline execution complete in {total_time:.2f}s!")
    print("Outputs available in:")
    print("  - 16:9 Cinema/YouTube: outputs/final_heritage_short_16x9.mp4")
    print("  - 9:16 Mobile/Reels:   outputs/final_heritage_short_9x16.mp4")
    print("=" * 70)


if __name__ == "__main__":
    run_pipeline()
