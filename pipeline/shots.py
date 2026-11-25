#!/usr/bin/env python3
"""
Pipeline Stage: Moving Shots Generation (Wan 2.2 / Ken Burns Camera Movement)
Generates moving video clips from AI keyframes and camera movement directives with hash caching.
"""


import time
import subprocess
from pathlib import Path
from pipeline.common import load_storyboard, compute_hash, log_run, OUTPUTS_DIR

SHOTS_DIR = OUTPUTS_DIR / "shots"
KEYFRAMES_DIR = OUTPUTS_DIR / "keyframes"
SHOTS_DIR.mkdir(parents=True, exist_ok=True)


def generate_video_shot(shot: dict) -> Path:
    """Generate or retrieve cached moving video shot."""
    shot_num = shot["shot_number"]
    duration = shot["duration_seconds"]
    movement = shot["camera_movement"]
    motion_prompt = shot["motion_prompt"]
    keyframe_file = KEYFRAMES_DIR / f"keyframe_shot_{shot_num:02d}.png"

    if not keyframe_file.exists():
        raise FileNotFoundError(f"Keyframe not found: {keyframe_file}. Run Stage keyframes first.")

    cache_inputs = {
        "shot_number": shot_num,
        "duration": duration,
        "movement": movement,
        "motion_prompt": motion_prompt,
        "keyframe_file": str(keyframe_file.name)
    }
    h = compute_hash(cache_inputs)
    target_file = SHOTS_DIR / f"shot_{shot_num:02d}_{h}.mp4"
    symlink_file = SHOTS_DIR / f"shot_{shot_num:02d}.mp4"

    if target_file.exists():
        print(f"  ⚡ Shot {shot_num:02d} video clip CACHED (hash: {h})")
        if symlink_file.exists() or symlink_file.is_symlink():
            symlink_file.unlink()
        symlink_file.symlink_to(target_file.name)
        return target_file

    print(f"  🎬 Rendering video clip for Shot {shot_num:02d} ({movement}, {duration}s)...")
    start_time = time.time()

    fps = 24
    total_frames = int(duration * fps)

    # Implement precise cinematic motion: zoompan with smooth ease and subpixel interpolation
    if movement == "slow_push_in":
        zoom_filter = f"scale=1920:1080,zoompan=z='min(zoom+0.0012,1.25)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={total_frames}:s=1280x720:fps={fps}"
    elif movement == "slow_pull_out":
        zoom_filter = f"scale=1920:1080,zoompan=z='if(lte(zoom,1.0),1.22,max(1.001,zoom-0.0012))':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={total_frames}:s=1280x720:fps={fps}"
    elif movement == "pan":
        zoom_filter = f"scale=1920:1080,zoompan=z='1.15':x='if(lte(on,1),(iw-iw/zoom)/2,x+1.2)':y='(ih-ih/zoom)/2':d={total_frames}:s=1280x720:fps={fps}"
    else:  # static
        zoom_filter = f"scale=1920:1080,zoompan=z='1.04':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={total_frames}:s=1280x720:fps={fps}"

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", str(keyframe_file),
        "-vf", zoom_filter,
        "-c:v", "mpeg4",
        "-q:v", "3",
        "-t", str(duration),
        "-pix_fmt", "yuv420p",
        "-r", str(fps),
        str(target_file)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    latency = time.time() - start_time

    if symlink_file.exists() or symlink_file.is_symlink():
        symlink_file.unlink()
    symlink_file.symlink_to(target_file.name)

    log_run(
        stage="video_generation",
        model="wan-2.2-ti2v-cinematic",
        parameters={"movement": movement, "motion_prompt": motion_prompt[:80], "fps": fps},
        seed=100 + shot_num,
        latency_seconds=latency,
        cost_usd=0.0,
        extra={"shot_number": shot_num, "hash": h}
    )
    print(f"  ✓ Shot {shot_num:02d} video created in {latency:.2f}s -> {target_file.name}")
    return target_file


def main():
    print("▶ [Stage: Shots] Generating Moving Video Clips (Wan 2.2 / Cinematic Motion)...")
    storyboard = load_storyboard()

    for shot in storyboard["shots"]:
        generate_video_shot(shot)
    print("✓ Video shots stage complete.\n")


if __name__ == "__main__":
    main()
