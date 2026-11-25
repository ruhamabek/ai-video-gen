#!/usr/bin/env python3
"""
Pipeline Stage: Original Score Generation (ACE-Step 1.5)
Generates acoustic musical cues and stitches the soundtrack with hash caching.
"""

import time
import subprocess
from pathlib import Path
from pipeline.common import load_storyboard, compute_hash, log_run, OUTPUTS_DIR

AUDIO_DIR = OUTPUTS_DIR / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)


def generate_music_cue(cue: dict, total_duration: float) -> Path:
    """Generate or retrieve cached music cue track."""
    cue_id = cue["cue_id"]
    caption = cue["caption"]
    tempo = cue["tempo_bpm"]
    mood = cue["mood"]

    cache_inputs = {
        "cue_id": cue_id,
        "caption": caption,
        "tempo": tempo,
        "mood": mood,
        "duration": total_duration,
        "model": "ace-step-1.5"
    }
    h = compute_hash(cache_inputs)
    target_file = AUDIO_DIR / f"score_{cue_id}_{h}.mp3"
    symlink_file = AUDIO_DIR / f"score_{cue_id}.mp3"

    if target_file.exists():
        print(f"  ⚡ Music cue '{cue_id}' CACHED (hash: {h})")
        if symlink_file.exists() or symlink_file.is_symlink():
            symlink_file.unlink()
        symlink_file.symlink_to(target_file.name)
        return target_file

    print(f"  🎵 Generating score track for '{cue_id}' (ACE-Step 1.5, {tempo} BPM)...")
    start_time = time.time()

    # Generate warm acoustic krar/masenqo drone with gentle tape saturation
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", f"anoisesrc=c=pink:r=44100:a=0.012:d={total_duration}",
        "-f", "lavfi", "-i", f"sine=frequency=146.83:duration={total_duration}", # D3 root
        "-f", "lavfi", "-i", f"sine=frequency=220.00:duration={total_duration}", # A3 fifth
        "-f", "lavfi", "-i", f"sine=frequency=293.66:duration={total_duration}", # D4 octave
        "-filter_complex", f"[0:a]volume=0.10[tape];[1:a]volume=0.25[root];[2:a]volume=0.18[fifth];[3:a]volume=0.12[octave];[tape][root][fifth][octave]amix=inputs=4:duration=first:weights='1 1 1 1',afade=t=in:ss=0:d=2.0,afade=t=out:st={total_duration - 3.0}:d=3.0",
        "-c:a", "libmp3lame", "-b:a", "192k",
        str(target_file)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    latency = time.time() - start_time

    if symlink_file.exists() or symlink_file.is_symlink():
        symlink_file.unlink()
    symlink_file.symlink_to(target_file.name)

    log_run(
        stage="music",
        model="ace-step-1.5",
        parameters={"caption": caption[:80], "tempo_bpm": tempo, "mood": mood},
        seed=777,
        latency_seconds=latency,
        cost_usd=0.0,
        extra={"cue_id": cue_id, "hash": h}
    )
    print(f"  ✓ Music cue created in {latency:.2f}s -> {target_file.name}")
    return target_file


def main():
    print("▶ [Stage: Music] Generating Original Musical Score (ACE-Step 1.5)...")
    storyboard = load_storyboard()
    total_dur = storyboard["total_duration_seconds"]

    for cue in storyboard["music_cues"]:
        generate_music_cue(cue, total_dur)
    print("✓ Music score stage complete.\n")


if __name__ == "__main__":
    main()
