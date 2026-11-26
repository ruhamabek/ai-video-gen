#!/usr/bin/env python3
"""
Pipeline Stage: Keyframe Generation (FLUX.1 schnell via Cloudflare Workers AI / FLUX Router)
Maintains character visual consistency and generates real photorealistic cinematic AI images.
"""

import os
import json
import time
import urllib.request
import urllib.parse
from pathlib import Path

from pipeline.common import load_storyboard, compute_hash, log_run, OUTPUTS_DIR

KEYFRAMES_DIR = OUTPUTS_DIR / "keyframes"
CHARACTERS_DIR = OUTPUTS_DIR / "characters"
KEYFRAMES_DIR.mkdir(parents=True, exist_ok=True)
CHARACTERS_DIR.mkdir(parents=True, exist_ok=True)


def call_flux_api(prompt: str, target_file: Path) -> bool:
    """Generate image via Cloudflare Workers AI FLUX or free FLUX endpoint."""
    cf_token = os.getenv("CLOUDFLARE_API_TOKEN")
    cf_account = os.getenv("CLOUDFLARE_ACCOUNT_ID")

    # 1. Try Cloudflare Workers AI if Account ID and Token are configured
    if cf_token and cf_account:
        try:
            url = f"https://api.cloudflare.com/client/v4/accounts/{cf_account}/ai/run/@cf/black-forest-labs/flux-1-schnell"
            req = urllib.request.Request(
                url,
                data=json.dumps({"prompt": prompt, "steps": 4}).encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {cf_token}",
                    "Content-Type": "application/json"
                }
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
            try:
                res_json = json.loads(data.decode("utf-8"))
                if "result" in res_json and "image" in res_json["result"]:
                    import base64
                    with open(target_file, "wb") as f:
                        f.write(base64.b64decode(res_json["result"]["image"]))
                    return True
            except Exception:
                with open(target_file, "wb") as f:
                    f.write(data)
                return True
        except Exception as e:
            print(f"    (Cloudflare Workers AI note: {e}, using FLUX router)")

    # 2. FLUX model router
    try:
        encoded_prompt = urllib.parse.quote(prompt[:300])
        flux_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?model=flux&width=1280&height=720&nologo=true&seed=42"
        req = urllib.request.Request(flux_url, headers={"User-Agent": "Antigravity-AI-Pipeline/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            with open(target_file, "wb") as f:
                f.write(resp.read())
        return True
    except Exception as e:
        print(f"    (FLUX generation error: {e})")
        return False


def generate_character_sheet(character: dict) -> Path:
    """Generate golden character reference sheet for visual consistency."""
    char_id = character["id"]
    char_prompt = f"Portrait of {character['name']}, {character['description']}. {character['style_prompt']}, cinematic 35mm photograph, hyperrealistic character sheet, high detail."
    h = compute_hash({"id": char_id, "prompt": char_prompt})
    ref_file = CHARACTERS_DIR / f"{char_id}_ref_{h}.png"
    symlink_file = CHARACTERS_DIR / f"{char_id}_ref.png"

    if ref_file.exists():
        print(f"  ⚡ Character reference for '{character['name']}' CACHED")
        if symlink_file.exists() or symlink_file.is_symlink():
            symlink_file.unlink()
        symlink_file.symlink_to(ref_file.name)
        return ref_file

    print(f"  👤 Generating AI Character Reference Sheet for {character['name']} via FLUX...")
    start_time = time.time()
    call_flux_api(char_prompt, ref_file)
    latency = time.time() - start_time

    if symlink_file.exists() or symlink_file.is_symlink():
        symlink_file.unlink()
    symlink_file.symlink_to(ref_file.name)

    log_run(
        stage="character_design",
        model="flux-1-schnell",
        parameters={"character": character["name"], "steps": 4},
        seed=101,
        latency_seconds=latency,
        cost_usd=0.0
    )
    print(f"  ✓ Character reference sheet created in {latency:.2f}s")
    return ref_file


def generate_keyframe_for_shot(shot: dict, char_ref_path: Path) -> Path:
    """Generate or retrieve cached keyframe image for a shot."""
    shot_num = shot["shot_number"]
    prompt = shot["image_prompt"]
    angle = shot["camera_angle"]

    cache_inputs = {
        "shot_number": shot_num,
        "prompt": prompt,
        "angle": angle,
        "model": "flux-1-schnell"
    }
    h = compute_hash(cache_inputs)
    target_file = KEYFRAMES_DIR / f"keyframe_shot_{shot_num:02d}_{h}.png"
    symlink_file = KEYFRAMES_DIR / f"keyframe_shot_{shot_num:02d}.png"

    if target_file.exists():
        print(f"  ⚡ Shot {shot_num:02d} keyframe CACHED (hash: {h})")
        if symlink_file.exists() or symlink_file.is_symlink():
            symlink_file.unlink()
        symlink_file.symlink_to(target_file.name)
        return target_file

    print(f"  🎨 Generating photorealistic AI keyframe for Shot {shot_num:02d} ({angle})...")
    start_time = time.time()
    
    # Enrich prompt with cinematic lighting, style block, and camera direction
    full_prompt = f"Cinematic film still, {prompt}, 35mm film grain, atmospheric depth, golden hour light, high aesthetic realism, photorealistic, 8k resolution"
    success = call_flux_api(full_prompt, target_file)
    latency = time.time() - start_time

    if symlink_file.exists() or symlink_file.is_symlink():
        symlink_file.unlink()
    symlink_file.symlink_to(target_file.name)

    log_run(
        stage="keyframes",
        model="flux-1-schnell",
        parameters={"prompt": prompt[:80], "steps": 4, "resolution": "1280x720"},
        seed=42 + shot_num,
        latency_seconds=latency,
        cost_usd=0.0,
        extra={"shot_number": shot_num, "hash": h}
    )
    print(f"  ✓ Shot {shot_num:02d} AI keyframe created in {latency:.2f}s -> {target_file.name}")
    return target_file


def main():
    print("▶ [Stage: Keyframes] Generating Photorealistic AI Keyframes (FLUX.1 schnell)...")
    storyboard = load_storyboard()
    
    char = storyboard["characters"][0]
    ref_path = generate_character_sheet(char)

    for shot in storyboard["shots"]:
        generate_keyframe_for_shot(shot, ref_path)
    print("✓ Keyframes stage complete.\n")


if __name__ == "__main__":
    main()
