# 📻 The Frequency of Memory (የማስታወሻ ሞገድ)
### An Automated, Zero-Cost AI Heritage Short Film Pipeline

> *"Over forty years in this small room, he repaired more than just broken radios. He reconnected the hopes, longings, and distant news of an entire neighborhood."*

[![Pipeline Status](https://img.shields.io/badge/Pipeline-Verified%20Passing-brightgreen.svg)]()
[![Video Walkthrough](https://img.shields.io/badge/Video-Walkthrough-1AB7EA?logo=vimeo&logoColor=white)](https://vimeo.com/1250348776?share=copy&fl=sv&fe=ci)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Cost: $0.00](https://img.shields.io/badge/Direct%20Cost-$0.00%20(100%25%20Free)-success.svg)]()
[![Aspect Ratios: 16:9 & 9:16](https://img.shields.io/badge/Formats-16%3A9%20%26%209%3A16-orange.svg)]()

---

## 🎬 1. Executive Summary

**The Frequency of Memory** is an automated 72.5-second heritage short film produced entirely through a reproducible, code-driven multi-model generative AI pipeline. It tells the story of **Ato Berhanu**, an elderly master artisan in the historic Mercato district of Addis Ababa, Ethiopia, who repairs vintage vacuum tube radios, tuning past static noise to find the warm, comforting frequency of family memory (*Tizita*).

Built for the **10 Academy AI-Content Generation Challenge ("The Heritage Short")**.

- **Total Film Duration**: 72.5 seconds (9 distinct narrative shots, ~8.0s each).
- **Narration Language**: Authentic Amharic voiceover with hardcoded, burned-in English subtitles.
- **Soundtrack**: Classical modal Ethiopian *Tizita* pentatonic score with traditional Krar and Masenqo timbres, dynamically ducked under speech.
- **Dual Deliverables**:
  - **Horizontal Cinematic Master (16:9)**: [`outputs/final_heritage_short_16x9.mp4`](outputs/final_heritage_short_16x9.mp4) (Cinema / YouTube / Desktop).
  - **Vertical Social Master (9:16)**: [`outputs/final_heritage_short_9x16.mp4`](outputs/final_heritage_short_9x16.mp4) (TikTok / Instagram Reels / YouTube Shorts).
- **AI Transparency**: Dedicated 2.5s end card complying with the EU AI Act (Art. 52) and FTC disclosure standards.
- **Zero-Cost Constraint**: **$0.00 spent** using free tiers accessible from Ethiopia.

---

## 2. Quick Start & One-Command Execution

A stranger can clone this repository, run one command, and regenerate the entire film from its storyboard contract.

### Prerequisites
- Python 3.10+
- `ffmpeg` 6.x or 7.x (or static build in `~/.local/bin`)
- Free API keys:
  - **Google AI Studio**: Free Gemini API Key.
  - **Cloudflare Workers AI**: Free Cloudflare API Token & Account ID.
  - **Kaggle**: Phone-verified account for remote 2x Tesla T4 GPU compute.

### Setup & Run
```bash
# 1. Clone the repository
git clone https://github.com/ruhamabek/ai-video-gen.git
cd ai-video-gen

# 2. Configure credentials
cp .env.example .env
# Edit .env with your GEMINI_API_KEY, CLOUDFLARE_API_TOKEN, and CLOUDFLARE_ACCOUNT_ID

# 3. Run the complete pipeline
make film
# (Or python -m pipeline.orchestrate)
```

### Selective 1-Shot Re-run Architecture (Smart Caching)
Each stage implements content-addressed caching via SHA-256 hashes of its inputs `(prompt + seed + model)`.
- If you edit a single line or camera direction for **Shot 05** in `storyboard.json`, running `make film` will **only regenerate Shot 05**, completing in **under 20 seconds** instead of re-rendering all 9 shots.

---

## 🏗️ 3. Pipeline Architecture & Data Contracts

The pipeline is organized around `storyboard.json` as a single, immutable contract between all 6 stages. The contract is strictly validated against `schema/storyboard.schema.json` prior to execution.

```
                  ┌──────────────────────┐
                  │   storyboard.json    │
                  └──────────┬───────────┘
                             │ Validated by schema/storyboard.schema.json
     ┌───────────────────────┼───────────────────────────┐
     │                       │                           │
┌────▼─────────────┐   ┌─────▼──────────────┐   ┌────────▼─────────────┐
│ 1. Script & TTS  │   │ 2. Visuals         │   │ 3. Soundtrack        │
│ pipeline/        │   │ pipeline/          │   │ pipeline/            │
│ narration.py     │   │ keyframes.py       │   │ music.py             │
│                  │   │                    │   │                      │
│ - Semantic       │   │ - FLUX.1 Schnell   │   │ - Ethiopian Tizita   │
│   clause-split   │   │ - Char Consistency │   │   pentatonic score   │
│ - Amharic TTS    │   │ - Negative prompts │   │ - Tape warmth & eq   │
│ - SHA-256 Cache  │   │ - SHA-256 Cache    │   │ - SHA-256 Cache      │
└────┬─────────────┘   └─────┬──────────────┘   └────────┬─────────────┘
     │                       │                           │
     │                 ┌─────▼──────────────┐            │
     │                 │ 4. Remote GPU      │            │
     │                 │ wan2_video_        │            │
     │                 │ generator.ipynb    │            │
     │                 │                    │            │
     │                 │ - 2x Tesla T4      │            │
     │                 │ - VAE Tiling (OOM) │            │
     │                 │ - 24fps motion     │            │
     │                 └─────┬──────────────┘            │
     │                       │                           │
     └───────────────────────┼───────────────────────────┘
                             │
                  ┌──────────▼───────────┐
                  │ 5. Master Assembly   │
                  │ pipeline/assemble.py │
                  │                      │
                  │ - Sidechain ducking  │
                  │ - -14 LUFS loudness  │
                  │ - Burned subtitles   │
                  │ - 2.5s AI End Card   │
                  │ - Dual 16:9 & 9:16   │
                  └──────────────────────┘
```

---

## 🛠️ 4. The Multi-Model Zero-Cost Stack

| Stage | Model / Tool | Role in Pipeline | Hosting / Provider | Cost |
| :--- | :--- | :--- | :--- | :---: |
| **Stage 1: Script** | Gemini 2.5 Flash | Script drafting & schema verification | Google AI Studio | $0.00 |
| **Stage 2: Voiceover** | Google Neural TTS | Natural Amharic narration with clause splitting | Google Speech Endpoint | $0.00 |
| **Stage 3: Music** | Classical *Tizita* | Acoustic Krar & Masenqo Ethiopian score | Public Domain / Archive | $0.00 |
| **Stage 4: Keyframes**| FLUX.1 schnell | Photorealistic character-consistent keyframes | Cloudflare Workers AI | $0.00 |
| **Stage 5: Video Diffusion**| LTX-Video / Wan 2.1 | 24fps motion clips with VAE tiling | Kaggle 2x Tesla T4 GPU | $0.00 |
| **Stage 6: Assembly** | FFmpeg 7.x Static | Ducking, loudness normalization, subtitle burn-in | Local CPU | $0.00 |
| **TOTAL** | | | | **$0.00** |

---

## 📁 5. Repository Layout

```text
├── README.md                      # Comprehensive guide, architecture & quick start
├── REPORT.md                      # Executive Engineering Report (Assignment 1 answers)
├── ARCHITECTURE.md                # Component contracts, caching strategy, and offloading
├── DESIGN.md                      # Audience personas, creative intent, and User Tests 1 & 2
├── EXPERIMENTS.md                 # 10 logged experiments (hypothesis -> change -> result)
├── FAILURES.md                    # Blocker post-mortems (GPU OOM, character limits, codec locks)
├── COSTS.md                       # Quantitative latency, GPU accounting, and list prices
├── ETHICS.md                      # Likeness consent, licenses, and AI labeling transparency
├── Makefile                       # Unified targets (`make film`, `make clean`, `make test`)
├── storyboard.json                # Single source of truth (72.5s, 9 shots, prompts, audio cues)
├── runs.jsonl                     # Append-only run ledger (model, seed, latency, cost)
├── wan2_video_generator.ipynb     # Verified Kaggle notebook with VAE tiling OOM fixes
├── schema/
│   └── storyboard.schema.json     # JSON Schema validation contract
├── pipeline/
│   ├── common.py                  # SHA-256 caching, schema validation, logger
│   ├── script.py                  # Storyboard compilation & validation
│   ├── narration.py               # Clause-segmented neural Amharic TTS
│   ├── keyframes.py               # Cloudflare FLUX image generator
│   ├── shots.py                   # Local video motion assembler
│   ├── music.py                   # Acoustic Tizita score generator
│   ├── assemble.py                # FFmpeg master ducking, subtitles, and dual exports
│   └── orchestrate.py             # End-to-end pipeline runner
└── outputs/
    ├── final_heritage_short_16x9.mp4  # 🎬 Horizontal Cinematic Master (72.5s)
    ├── final_heritage_short_9x16.mp4  # 📱 Vertical Social Media Master (72.5s)
    ├── subtitles.srt                  # Formatted English subtitles
    ├── full_video_track.mp4           # Raw assembled video track with end card
    └── audio/                         # Master ducked soundtrack and shot audio
```

---

## 🔬 6. Key Engineering Breakthroughs & Failure Recoveries

1. **Overcoming 12GB 3D VAE Out-of-Memory (`OutOfMemoryError: CUDA out of memory`)**:
   - *Problem*: Video diffusion autoencoders attempt to decode temporal 3D tensors in a single pass, exhausting 11.55 GiB on 15GB T4 GPUs.
   - *Solution*: Enabled spatial and temporal micro-tiling (`pipe.vae.enable_tiling()` & `pipe.vae.enable_slicing()`), reducing peak VRAM consumption from ~12 GiB down to 4.7 GiB.
2. **Amharic Compound Sentence Truncation**:
   - *Problem*: The TTS endpoint silently truncated compound Amharic lines on Shot 4 (*"አንዲት ቃል አውርታ አታውቅም ነበር።"* was skipped).
   - *Solution*: Built a semantic clause-segmentation parser in `pipeline/narration.py` that splits compound clauses across Amharic punctuation (`።` and `፦`), generates each part losslessly, and concatenates them with conversational pauses before padding.
3. **9:16 Vertical Subtitle Legibility & Safe-Area Alignment**:
   - *Problem*: Scaling subtitles from 16:9 to vertical 9:16 caused narrow width wrapping, resulting in an 8-line text wall that obscured Ato Berhanu's face.
   - *Solution*: Calibrated dedicated mobile subtitle parameters (`Alignment=2`, `FontSize=8.5`, `MarginV=60`), anchoring subtitles in the lower third to respect Instagram Reels and TikTok UI overlays.
4. **Dynamic Sidechain Compression Tuning**:
   - *Problem*: Early audio mixes either had inaudible music (-43 dB) or drowned out the narrator.
   - *Solution*: Designed an FFmpeg sidechain compression filter graph (`sidechaincompress=threshold=0.04:ratio=4:attack=120:release=1000`) paired with EBU R128 (-14 LUFS) normalization, ensuring the acoustic Tizita melody is clearly audible during pauses and cleanly ducks when the narrator speaks.

---

## 📜 7. License & Ethics

- **Code**: Released under the [MIT License](LICENSE).
- **Models**: FLUX.1 schnell (Apache 2.0 / Free Cloudflare Tier), LTX-Video / Wan 2.1 (Open-Weight Apache 2.0).
- **Ethics & Provenance**: Ato Berhanu is an original synthetic composite character representing traditional Ethiopian craftsmanship. All outputs include mandatory AI disclosure end cards in compliance with international transparency directives. See [ETHICS.md](ETHICS.md) for full records.
