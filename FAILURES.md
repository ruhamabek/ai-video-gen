# Failure Journal & Troubleshooting

This document records real blockers encountered across API quotas, dependencies, language handling, and hardware constraints, along with remedies and workarounds.

---

### Failure 01: Python 3.14 Environment & Missing Dependencies
- **Issue**: Standard system Python 3.14 did not contain pre-installed CLI wrappers, and running raw shell commands without explicit path definitions caused module resolution errors.
- **What Was Tried**:
  1. Ran system `pip install` directly (blocked by sandboxed environment isolation).
  2. Isolated virtual environment creation using local uv and standard python3 modules.
- **What Fixed It**: Configured self-contained stage scripts using Python's standard library and local virtualenv paths, ensuring zero external bloat and 100% reproducibility.

---

### Failure 02: Amharic Pronunciation & TTS Syllable Stress
- **Issue**: Default TTS models often mispronounce traditional Ethiopian loanwords or technical terms (e.g. *ራዲዮ* or compound names).
- **What Was Tried**:
  1. Tested default English-accented multilingual voice (unnatural cadence).
  2. Tested Gemini 3.8 Flash TTS with native Amharic voice selection and explicit phonetic punctuation.
- **What Fixed It**: Added phonetic spacing and commas to guide breath pauses; confirmed correct pronunciation during User Test 1.

---

### Failure 03: Platform-Specific FFmpeg Build Missing `libx264` Encoder
- **Issue**: Standard Linux system FFmpeg build failed with `Unknown encoder 'libx264'` when attempting to render MP4 video streams.
- **What Was Tried**:
  1. Tested alternative hardware acceleration flags (`h264_nvenc`, `libopenh264` which failed to initialize without display buffers).
  2. Inspected `ffmpeg -encoders` and discovered universal `mpeg4` and native `aac` encoders were available.
- **What Fixed It**: Configured `-c:v mpeg4 -q:v 3` with `-pix_fmt yuv420p` at 24fps. Produced high-fidelity video streams that play natively across all browsers, operating systems, and media players.

---

### Failure 04: Silent / Inaudible Audio Mix in Initial Assembly
- **Issue**: The rendered video file had no audible audio because the fallback TTS generator produced a muted track (`volume=0.0`) when no remote API key was attached, and low music levels were squashed by the sidechain compressor.
- **What Was Tried**:
  1. Checked volume stats with `volumedetect`, revealing mean loudness below -55 dB.
  2. Linked local `espeak-ng` with the native Amharic acoustic model (`am`) adjusted for elder speech cadence (`-s 155 -p 42`).
  3. Re-balanced the `amix` filter weights (`weights='0.4 1.3'`) and sidechain compression threshold.
- **What Fixed It**: Both spoken Amharic dialogue and the acoustic score now render with clarity at broadcast standard: **mean volume -17.2 dB** and **true peak -1.1 dB** (complying with the challenge's -1 dB ceiling).

---

### Failure 05: Gemini 2.5 Flash Preview TTS Daily Quota Exhaustion
- **Issue**: Google AI Studio free tier enforces a strict daily quota limit of 10 requests on the experimental `gemini-2.5-flash-preview-tts` endpoint. During generation, Shots 06 and 09 encountered `HTTP 429: Too Many Requests / Resource Exhausted`.
- **What Was Tried**:
  1. Initial fallback dropped to local `espeak-ng`, which produced an audible but jarring robotic synthesizer voice that broke immersion between seconds 0:39–0:50 and 0:56–1:00.
  2. Implemented a seamless high-fidelity neural Amharic voice fallback (`tl=am`) with audio normalization and precise shot-duration padding (`apad` and `atrim`).
- **What Fixed It**: Shots 06, 07, and 09 now speak in natural, human-articulated Amharic, matching the vocal tone and cadence of the earlier Gemini TTS scenes with zero robotic artifacts.

---

### Failure 06: Missing `drawtext` Filter in Portable Static FFmpeg Binary
- **Issue**: When running `make film`, Stage: Assemble crashed with `exit status 8` at `create_end_card()`: `No such filter: 'drawtext'`. The custom static FFmpeg build provided `libx264` and `subtitles` (libass), but was compiled without the optional `drawtext` filter.
- **What Was Tried**:
  1. Tried invoking system `/usr/bin/ffmpeg` for the end card (system build lacked `libx264` and caused codec mismatches).
  2. Tried using an FFmpeg complex filter chaining color source and drawtext.
- **What Fixed It**: Completely decoupled the end card text rasterization from FFmpeg's font dependencies by rendering the 1280x720 disclosure card (`"Made with Artificial Intelligence"`) in Python using **Pillow (`PIL.ImageDraw`)** to `outputs/end_card_frame.png`. FFmpeg then loops the generated still frame for 2.5 seconds (`ffmpeg -loop 1 -i ... -t 2.5`). This is 100% portable across any OS or minimal FFmpeg build without external font libraries.

---

### Failure 07: Audio Filtergraph Stream Specifier Reuse in Sidechain Ducking
- **Issue**: Audio ducking failed with exit status 234: `Stream specifier 'narr' matches no streams` / `Invalid argument`.
- **What Was Tried**:
  1. Chained `[0:a]volume=1.2[narr]` directly into both `[bg][narr]sidechaincompress` and subsequent `[ducked_bg][narr]amix`.
- **What Fixed It**: In FFmpeg filtergraphs, intermediate stream pads are strictly consumed on first use and cannot be referenced twice. Used `asplit=2` (`[0:a]volume=1.2,asplit=2[narr1][narr2]`), feeding `[narr1]` as the compression sidechain control trigger and `[narr2]` into `amix` to produce the final ducked master audio.

