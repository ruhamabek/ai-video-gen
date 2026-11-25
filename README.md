# 📻 The Frequency of Memory (የማስታወሻ ሞገድ)
### An AI Heritage Short Film Pipeline

> *"Over forty years in this small room, he repaired more than just broken radios. He reconnected the hopes, longings, and distant news of an entire neighborhood."*

---

## 🎬 Project Overview
*The Frequency of Memory* is an automated 72-second heritage short film produced entirely through a programmatic multi-model pipeline. It tells the story of **Ato Berhanu**, an elder artisan in Addis Ababa who restores vintage tube radios, tuning past static to find the warm frequency of family memory (*Tizita*).

Built for the **10 Academy AI-Content Generation Challenge ("The Heritage Short")**.

- **Total Duration**: 72.0 seconds (9 shots, ~8s each)
- **Narration Language**: Amharic (with burned-in English subtitles)
- **Aspect Ratios**: 9:16 (Vertical for Mobile / Reels) & 16:9 (Horizontal for Cinema / YouTube)
- **Total Compute Cost**: **$0.00** (using completely free tiers accessible from Ethiopia)

---

## 🚀 One-Command Execution

To reproduce the entire film from scratch:

```bash
# 1. Clone the repository
git clone https://github.com/ruhamabek/ai-video-gen.git
cd ai-video-gen

# 2. Configure environment variables (.env)
cp .env.example .env
# Add GEMINI_API_KEY, CLOUDFLARE_API_TOKEN, etc.

# 3. Run the complete pipeline
python -m pipeline.orchestrate
# Or:
make film
```

### Selective / Incremental Re-runs (Smart Caching)
Each shot is cached by the SHA-256 hash of its inputs. If you modify a single shot's prompt or narration line in `storyboard.json`, running `make film` will **only regenerate that modified shot**, leaving all other shots untouched.

---

## 🏗️ Architecture & Zero-Cost Stack

The pipeline is structured around **`storyboard.json`** as the single strict contract, validated against `schema/storyboard.schema.json` before every stage:

```
┌──────────────────┐
│  storyboard.json │  <-- Single Contract
└────────┬─────────┘
         ├──> [1. Keyframes]  : FLUX.1 schnell (Cloudflare Workers AI)
         ├──> [2. Shots]      : Wan 2.2 TI2V-5B (Kaggle 2xT4) / Ken Burns FFmpeg
         ├──> [3. Narration]  : Gemini 3.8 Flash TTS (Amharic)
         ├──> [4. Score]      : ACE-Step 1.5 (Acoustic Krar & Masenqo)
         └──> [5. Assembly]   : FFmpeg (Ducking, Subtitles, -14 LUFS, End Card)
```

| Component | Model / Tool | Free Tier Source |
| :--- | :--- | :--- |
| **Language & Script** | Google Gemini 3.8 Flash | Google AI Studio API |
| **Voiceover (Amharic)**| Google Gemini 3.8 Flash TTS | Google AI Studio API |
| **Visual Keyframes** | FLUX.1 schnell | Cloudflare Workers AI (~100 images/day free) |
| **Motion Video** | Wan 2.2 TI2V-5B | Kaggle Notebooks (30 GPU hrs/wk free) |
| **Score / Music** | ACE-Step 1.5 | Kaggle / Colab (MIT License) |
| **Audio-Video Assembly**| FFmpeg 6.x | Local Machine (Deterministic & Free) |

---

## 📁 Repository Structure

```text
├── README.md           # Quick start, one-command run, and pipeline overview
├── storyboard.json     # The central contract (shots, prompts, narration, music cues)
├── schema/             # JSON Schema for storyboard.json validation
├── pipeline/           # Stage scripts (keyframes, shots, narration, music, assemble)
├── runs.jsonl          # Comprehensive call log (seed, latency, cost, params)
├── outputs/            # Generated assets and final MP4 renders (9:16 and 16:9)
├── DESIGN.md           # Audience definition, intent, and User Test notes (Radio cut & Near-final)
├── ARCHITECTURE.md     # Pipeline stages, input hash caching, failure fallbacks
├── EXPERIMENTS.md      # Hypothesis -> change -> result log (10 iterations)
├── FAILURES.md         # Problem log: quotas, TTS pronunciation, video queue workarounds
├── COSTS.md            # Resource metrics, GPU minutes, list-price calculations
└── ETHICS.md           # Consent statement, AI disclosure end card plan, model licenses
```

---

## 📊 Summary of Costs & Latency
- **Direct Expense**: $0.00
- **Total Pipeline Runtime**: ~28 minutes (including batched video rendering)
- **Commercial API Equivalent**: ~$19.65

See [COSTS.md](file:///home/sapphire/ai-video-gen/COSTS.md) for full benchmark breakdowns.
