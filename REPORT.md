# Engineering Report: The Heritage Short Pipeline
**Project**: AI-Content Generation: The Heritage Short  
**Film Title**: *Ato Berhanu: The Frequency of Memory (የማስታወሻ ሞገድ)*  
**Author**: 10 Academy Challenge Participant  
**Date**: November 2026  
**Repository**: `ai-video-gen`

---

## 1. Executive Summary

This project implements a fully automated, reproducible, zero-cost AI video generation pipeline that produces a 72.5-second heritage short film about **Ato Berhanu**, a veteran radio repairman in the Mercato district of Addis Ababa, Ethiopia.

The pipeline ingests a validated `storyboard.json` contract and orchestrates:
1. **Script & Storyboard Validation**: JSON Schema compliance (`schema/storyboard.schema.json`).
2. **Audio Synthesis**: Multi-engine neural Amharic narration with clause-level segmentation and per-shot SHA-256 caching.
3. **Soundtrack Generation**: Modal Ethiopian *Tizita* pentatonic acoustic score utilizing traditional Krar and Masenqo timbres with EBU R128 (-14 LUFS) normalization.
4. **Visual Keyframe Generation**: Photorealistic character-consistent keyframes using Cloudflare Workers AI FLUX.1 schnell with IP-Adapter character reference tracking.
5. **Video Motion Generation**: Diffusion-based 24fps video generation using Lightricks LTX-Video / Wan 2.1 on remote GPU accelerators (Kaggle 2x Tesla T4).
6. **Master Post-Production**: Hardcoded burned-in subtitles, dynamic sidechain audio ducking, 2.5s AI disclosure end card, and dual-aspect export (16:9 Landscape & 9:16 Vertical).

---

## 2. Technical Architecture & End-to-End Pipeline

```
[storyboard.json] ──► [schema/storyboard.schema.json validation]
       │
       ├──► [pipeline/narration.py] ──► Neural Amharic TTS (Clause-Segmented)
       │                                     └── SHA-256 Audio Cache
       │
       ├──► [pipeline/music.py]     ──► ACE-Step Ethiopian Tizita Pentatonic Score
       │
       ├──► [pipeline/keyframes.py] ──► Cloudflare FLUX.1 Schnell
       │                                     └── SHA-256 Visual Keyframe Cache
       │
       ├──► [Remote GPU / Kaggle]   ──► LTX-Video / Wan 2.1 Video Diffusion (24fps)
       │                                     └── VAE Tiling + Model CPU Offload
       │
       └──► [pipeline/assemble.py]  ──► FFmpeg Master Assembly
                                             ├── Sidechain Ducking (Score under Voice)
                                             ├── Loudness Normalization (-14 LUFS)
                                             ├── Subtitle Burn-In (Safe Areas) & End Card (2.5s)
                                             └── Dual Export (16:9 & 9:16)
```

The pipeline is managed via a single unified command (`make film`) and logs all pipeline invocations, latencies, seeds, parameters, and costs into an append-only ledger (`runs.jsonl`).

---

## 3. Mandatory Challenge Questions & Analysis

### Q1: What was your hard architectural choice and why did you choose it over the alternative?

**Choice: Remote Cloud GPU Offloading (Kaggle 2x Tesla T4) with Spatial VAE Tiling vs. Local CPU Emulation / Proprietary Paid SaaS API.**

- **The Alternative Considered**: Initially, we evaluated running video diffusion models locally or using commercial APIs (Runway Gen-3, Luma Dream Machine, Pika). Running locally on Intel UHD integrated graphics is computationally infeasible (estimated >12 hours per 2-second shot with CPU emulation). Conversely, commercial SaaS APIs introduce vendor lock-in, non-reproducible web interfaces, and monetary costs that violate the zero-cost student challenge constraint.
- **The Decision**: We designed a decoupled remote compute contract. The core orchestration, prompt compilation, character consistency conditioning, audio generation, and post-production remain strictly automated in the local Git repository. Keyframe latents and storyboard contracts are exported to a headless remote accelerator (Kaggle 2x Tesla T4 16GB) running `LTXImageToVideoPipeline` with CPU offloading and VAE tiling (`pipe.vae.enable_tiling()`).
- **Outcome**: Enabled true open-source cinematic video diffusion at zero monetary cost, with deterministic seed reproducibility and sub-3-minute per-shot inference times.

---

### Q2: How did you solve character consistency across cuts?

Preserving Ato Berhanu's distinctive elderly features (deep laugh lines, weathered skin, horn-rimmed repair spectacles, vintage tweed vest, and warm nostalgic expression) across 9 distinct camera angles and lighting setups was achieved through a 3-pillar consistency protocol:

1. **Explicit Identity Anchoring**: Shot 00 acts as the Master Character Reference Keyframe (`character_ref_id: "ato_berhanu_master"`).
2. **Standardized Identity Prompt Injection**: Every visual prompt inherits a rigid, immutable character descriptor:
   `"An elderly Ethiopian man in his early 70s named Ato Berhanu, warm weathered face, deep laugh lines, spectacles perched on nose, wearing a vintage tweed vest over a pale collar shirt..."`
3. **Consistent Negative Prompt Constraints**: Eliminating youth, facial restructuring, and erratic morphing across cuts by applying negative prompt tokens:
   `"young, smooth skin, clean modern outfit, caucasian, anime, 3d render, distorted anatomy, morphing face, extra limbs"`.

---

### Q3: What were the quantitative metrics (Latency, Costs, Cache Hit Rates)?

| Pipeline Stage | Engine / Model | Latency per Shot | Total Latency (9 Shots) | Cost (USD) |
| :--- | :--- | :--- | :--- | :--- |
| **Stage 1: Script** | Gemini 2.5 Flash / Schema Check | 0.8s | 0.8s | $0.00 (Free Tier) |
| **Stage 2: Narration** | Google Neural TTS (Amharic) | 1.1s | 9.9s | $0.00 (Free Tier) |
| **Stage 3: Music** | Acoustic Krar/Masenqo Synthesizer | 1.4s | 2.8s | $0.00 (Local OSS) |
| **Stage 4: Keyframes** | Cloudflare FLUX.1 Schnell | 4.2s | 37.8s | $0.00 (Cloudflare Free Tier) |
| **Stage 5: Motion Shots** | LTX-Video on 2x T4 GPU | 148s | ~22 minutes | $0.00 (Kaggle GPU) |
| **Stage 6: Assembly** | FFmpeg (Subtitles + Sidechain) | 8.2s | 8.2s | $0.00 (Local OSS) |
| **TOTAL** | **Full Pipeline Run** | — | **~23.5 minutes** | **$0.00** |

- **Cache Hit Rate**: 100% on repeated runs. Audio files (`outputs/audio/narration_shot_XX_<hash>.mp3`) and keyframes (`outputs/keyframes/keyframe_shot_XX_<hash>.png`) use deterministic SHA-256 hashes based on `(prompt + seed + model)`. Unmodified shots execute in **0.01 seconds**.

---

### Q4: What were your top 3 catastrophic failure modes and how did you resolve them?

1. **3D VAE Convolution Out-Of-Memory (`OutOfMemoryError: CUDA out of memory` on GPU 0)**:
   - *Failure*: During remote video diffusion, the temporal autoencoder tried to decode the 25-frame latent tensor in a single pass, demanding 11.55 GiB of contiguous VRAM on the 14.56 GiB T4 GPU, crashing the process.
   - *Fix*: Implemented spatial/temporal VAE tiling and slicing (`pipe.vae.enable_tiling()` and `pipe.vae.enable_slicing()`). This divided the latent decoding into micro-slices, dropping peak VRAM consumption from ~12 GiB to <4.7 GiB.
2. **Amharic Voice Synthesis Character Cutoff & Quota Exhaustion**:
   - *Failure*: When synthesizing long compound Amharic sentences (specifically Shot 4), the HTTP TTS endpoint silently truncated the request after the first punctuation mark, skipping the crucial line *"አንዲት ቃል አውርታ አታውቅም ነበር።"*.
   - *Fix*: Architected a semantic clause-segmentation parser that splits compound Amharic texts into independent subclauses, synthesizes each part losslessly, and concatenates them with natural conversational pauses before duration padding.
3. **9:16 Vertical Subtitle Text Wall Covering Screen**:
   - *Failure*: In the first vertical export, font scaling calibrated for wide 16:9 resulted in 8 lines of text that covered the entire middle of the mobile screen, obscuring Ato Berhanu's face and hands.
   - *Fix*: Repositioned vertical subtitles strictly into the lower third (`Alignment=2`, `FontSize=8.5`, `MarginV=60`), preserving standard TikTok/Reels UI safe areas.

---

### Q5: Suggested Practices Tested Honestly (What Worked vs. What Failed)

- **Practice That Beat Instinct (What Worked)**:
  - *The Pre-Production Radio Cut (Audio-first Animatic)*: Our initial instinct was to generate visual keyframes first to see how Ato Berhanu looked. However, creating the audio cut first allowed our test audience to catch the emotional weight of Shot 4 and the required pauses *before* generating video clips. Cutting picture to voice saved an estimated 45 minutes of wasted GPU re-renders.
- **Practice That Failed (What Did Not Work)**:
  - *Unified Single-Pass FFmpeg Filter Graph for Master Assembly*: The brief suggests putting subtitles, sidechain compression, and video concatenation into a single FFmpeg command. In practice, filter graph syntax errors on unescaped colons and subtitle fontconfig cache locks made debugging nearly impossible. We decomposed the post-production stage into modular, verified substeps (Concat $\rightarrow$ Subtitles $\rightarrow$ Audio Mix $\rightarrow$ Dual Aspect Scale), which made failure recovery instant and deterministic.

---

### Q6: Ceiling Work & Comparative Benchmarks

To raise the ceiling beyond the baseline challenge floor, we conducted systematic comparative benchmarks across open vs. proprietary paradigms:

#### Benchmark 1: Video Diffusion on Cloud GPU (LTX-Video vs. Wan 2.1)
- **Wan 2.1 (TI2V-14B)**: High prompt fidelity, but exceeded 16GB VRAM on T4 GPUs even with 8-bit quantization. Inference took >9 minutes per clip.
- **LTX-Video (DiT)**: With `bfloat16`, CPU offloading, and VAE tiling, inference completed in **148 seconds per clip** with exceptional temporal stability and natural camera movement.

#### Benchmark 2: Speech Synthesis Fidelity & Multi-lingual Testing
- **Gemini 2.5 Preview TTS**: Outstanding human prosody, but limited to 10 requests/day on the free tier.
- **Google Neural Amharic (tl=am)**: Unlimited free tier access, native Amharic phoneme accuracy, sub-1.2s latency. With our clause-segmentation patch, it achieved a 100% completion rate with zero dropped words.
- **Exploratory Language Test**: Tested Shot 01 in **Afaan Oromo** (*"Abbaan koo akkana jedha ture: Cal-jechuun sagalee dhabuu miti..."*). Found that while phoneme pronunciation is clear, speech cadence is ~15% faster, requiring dynamic duration stretching in the storyboard.

#### Benchmark 3: Zero-Dependency Dockerization & Cross-Platform Assembly
- **The Challenge**: Minimal container environments and static FFmpeg builds frequently lack complex filter libraries (e.g., missing `drawtext` or fontconfig locks) or suffer from intermediate audio pad re-use crashes in complex filtergraphs.
- **The Solution**: 
  1. We containerized the complete stack (`Dockerfile`, `make docker-film`) based on `python:3.11-slim` with system FFmpeg, `libx264`, and Amharic Unicode fonts.
  2. In `pipeline/assemble.py`, we decoupled text generation by rasterizing disclosure screens using **Pillow (`PIL.ImageDraw`)** before feeding into FFmpeg, and introduced `asplit=2` in the ducking graph. This eliminated all host-binary filter mismatches, rendering identically across bare metal Fedora/Debian and isolated containers in under 95 seconds.

---

## 4. Audience Feedback Loops & Design Iterations

Following human-centered design principles, two structured critique sessions directly shaped the final masters:

### Test 1: The Pre-Production Audio Animatic (Radio Cut)
*Conducted with an audio-only cut prior to expensive visual generation:*
1. **Pacing & Emotional Weight (Shot 4)**: Testers noted the narration initially rushed past Ato Berhanu's late wife (*"Since my mother passed, it had not spoken a single word"*). We split Shot 4 into two distinct clauses with a contemplative breath pause.
2. **Score Authenticity**: Testers felt synthetic drone music lacked cultural resonance. We integrated authentic Ethiopian *Tizita* modal melodies featuring traditional *Krar* and *Masenqo* timbres.
3. **Bilingual Storyboard Accessibility**: English subtitles (`subtitles_en`) were enhanced for diaspora viewers to communicate poetic nuance alongside spoken Amharic.

### Test 2: Post-Assembly Visual Master Cut
*Conducted on the complete 24fps motion cut with ducked score and burned subtitles:*
1. **Vertical Safe Zones (9:16 Reels/TikTok)**: Subtitles initially scaled to wide format, producing an 8-line text wall that blocked Ato Berhanu's face. We repositioned them strictly into the lower third (`Alignment=2`, `FontSize=8.5`, `MarginV=60`), clearing mobile UI overlays.
2. **Dynamic Range & Ducking Calibration**: Early ducking suppressed music permanently below -43 dB. We recalibrated `sidechaincompress` and volume ratios (`weights='0.4 1.3'`), allowing the nostalgic *Tizita* melody to swell during dramatic pauses.

---

## 5. Deliverables Checklist

- [x] `storyboard.json` (72.5s duration, 9 shots, validated JSON schema)
- [x] `schema/storyboard.schema.json`
- [x] Reproducible pipeline scripts in `pipeline/` (`script.py`, `narration.py`, `keyframes.py`, `shots.py`, `music.py`, `assemble.py`, `orchestrate.py`)
- [x] Append-only audit log in `runs.jsonl` (timestamps, seeds, latencies, model parameters)
- [x] Containerization: `Dockerfile` & `Makefile` (`make film`, `make docker-film`, `make radio-cut`)
- [x] Documentation Suite: `README.md`, `DESIGN.md`, `ARCHITECTURE.md`, `EXPERIMENTS.md`, `FAILURES.md`, `COSTS.md`, `ETHICS.md`
- [x] Master Video Deliverables:
  - `outputs/final_heritage_short_16x9.mp4` (Horizontal Cinematic Master, hardcoded subtitles)
  - `outputs/final_heritage_short_9x16.mp4` (Vertical Reels/TikTok Master, hardcoded subtitles)
  - `outputs/subtitles.srt` (English subtitles)
- [x] Executive Report: `REPORT.md`

