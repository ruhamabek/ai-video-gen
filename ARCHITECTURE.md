# Architecture & Pipeline Design

## 1. System Overview
The pipeline functions as a programmatic film studio turning `storyboard.json` into a complete, rendered 60–90 second film in both vertical (9:16) and horizontal (16:9) formats.

```
┌─────────────────┐
│ storyboard.json │ <── (Validated against schema/storyboard.schema.json)
└────────┬────────┘
         │
         ├──> [1. Keyframes Stage]  ──> outputs/keyframes/{shot_id}.png (FLUX / Cloudflare AI)
         │                                (Conditioned on outputs/characters/ref_sheet.png)
         ├──> [2. Video Stage]      ──> outputs/shots/{shot_id}.mp4 (Wan 2.2 / Ken Burns fallback)
         ├──> [3. Narration Stage]  ──> outputs/audio/narration_{shot_id}.mp3 (Gemini 3.8 Flash TTS)
         ├──> [4. Music Stage]      ──> outputs/audio/score_{cue_id}.mp3 (ACE-Step 1.5)
         │
         └──> [5. Assembly Stage]   ──> outputs/final_vertical.mp4 & outputs/final_horizontal.mp4
                                        (FFmpeg: ducking, subtitles, -14 LUFS normalisation, end card)
```

---

## 2. The Contract: `storyboard.json`
- Every stage is decoupled: stages only read from `storyboard.json` and local cached assets.
- `schema/storyboard.schema.json` is validated at the entrypoint of every stage execution.
- Prompts, seeds, durations, camera instructions, narration lines, and music cues are explicitly stated in the contract, never hard-coded in Python scripts.

---

## 3. Incremental Caching & Invalidation
To preserve GPU quotas and allow instant live edits during demonstrations:
- **Hash-Keyed Cache**: Each generated asset is indexed by a SHA-256 hash of its inputs:
  $$\text{Cache Key} = \text{SHA256}(\text{Prompt} + \text{Seed} + \text{Model} + \text{Duration} + \text{Reference Image Hash})$$
- When `storyboard.json` is modified:
  - Unchanged shots produce matching cache hashes and are skipped immediately.
  - Only modified shots (e.g. edited narration or changed prompt) trigger new model calls.
- Every model call writes an entry to `runs.jsonl`.

---

## 4. Failure Handling & Fallback Hierarchy
1. **API Quota / Network Blocker**:
   - Automatic exponential backoff retry (up to 3 attempts).
   - If an API quota is exhausted, the pipeline logs the failure in `runs.jsonl` and prompts the user or swaps to local fallback.
2. **Video Generation Fallback**:
   - If GPU capacity (Kaggle/Colab) or queue limits halt Wan 2.2 video generation, the assembly pipeline falls back to high-resolution keyframes animated with the **Ken Burns effect** (`zoompan` in FFmpeg). The film remains 100% complete, scored, and subtitled.
3. **Audio Normalisation**:
   - Audio tracks are dynamically ducked using FFmpeg's `sidechaincompress` filter and normalized to -14 LUFS via `loudnorm` to prevent clipping or uneven dialogue levels.
