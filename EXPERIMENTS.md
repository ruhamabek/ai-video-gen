# Experimentation & Iteration Log

This log tracks hypothesis-driven iterations across prompt engineering, audio models, character consistency, and video generation.

---

### Experiment 01: Amharic Narration Pacing & Prosody
- **Date**: 2026-11-25
- **Hypothesis**: Plain text without punctuation in Gemini 3.8 Flash TTS will cause rushed delivery across sentence boundaries in Amharic. Adding natural pauses (`...`, `፦`, commas) and a style prompt (*"Calm, warm, unhurried elder voice"*) will achieve ~2 words/second.
- **Change**: Updated `storyboard.json` narration text with punctuation markers and explicit voice styling tags.
- **Result**: Measured narration duration matched the 8.0-second scene window accurately without awkward syllable clipping. Confirmed during radio cut testing.

---

### Experiment 02: Single Golden Reference for Character Consistency
- **Date**: 2026-11-25
- **Hypothesis**: Conditioning FLUX keyframes on a fixed descriptive style block and a single approved reference image of Ato Berhanu will prevent face drifting between close-ups and wide shots.
- **Change**: Locked character description in `storyboard.json` to fixed facial features, round wire spectacles, and brown wool cardigan.
- **Result**: In progress.

---

*(Additional experiments 03–10 will be logged as keyframe generation, Wan 2.2 runs, ACE-Step audio batches, and FFmpeg ducking are performed).*
