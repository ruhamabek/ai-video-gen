# Design Thinking & Audience Record
**Project**: *Ato Berhanu: The Frequency of Memory (የማስታወሻ ሞገድ)*  
**Author**: 10 Academy Challenge Participant  

---

## 1. Audience & Intent

### Target Audience
- **Primary Persona**: **Yared (26, Software Developer / Diaspora in Berlin)** & **Emebet (68, Mother in Addis Ababa)**.
  - Represents younger urban Ethiopians and diaspora youth seeking tactile connection to elders, alongside elders who lived through the communal radio era in Addis Ababa (Piazza, Mercato).
- **Viewing Context**: 
  - Mobile vertical feeds (Instagram Reels / TikTok 9:16).
  - High-fidelity desktop/TV viewing (YouTube / LinkedIn 16:9).

### Creative Intent
- **What they should feel**: Reverence, warmth, poignant nostalgia (*Tizita*), and gratitude for the patience of craftsmen.
- **What they should understand**: That radio repair was never mere mechanical maintenance; in 20th-century Addis Ababa, it was the fragile lifeline connecting isolated families to national history, distant kin, and communal joy.

---

## 2. Script & Beat Structure
- **Format**: 9 continuous shots over 72.5 seconds (~8 seconds per shot).
- **Core Motif**: The journey from static hiss / cold silence to the harmonic warmth of the *Tizita* pentatonic melody.
- **Pacing**: Contemplative documentary tempo matching native Amharic spoken cadence (~2.0 words per second).

---

## 3. User Test 1: The Radio Cut (Pre-Visuals Prototype)
*Conducted using an audio-only animatic (narration over placeholder drone on black screen) before generating expensive visual assets.*

- **Testers**:
  1. **Dawit K.** (28, Native Amharic speaker & videographer):
     - *Observation*: "The delivery on Shot 4 rushed past the mother's memory. It sounded like an informational sentence rather than grief."
     - *Change*: Split Shot 4 into two distinct semantic clauses with a natural contemplative pause before *'አንዲት ቃል አውርታ አታውቅም ነበር'*.
  2. **Selamawit T.** (24, Diaspora graduate student):
     - *Observation*: "English subtitles are essential for diaspora viewers who understand spoken Amharic partially but miss the poetic nuance of 'የማስታወሻ ሞገድ'."
     - *Change*: Enhanced `subtitles_en` in `storyboard.json` to capture poetic equivalence rather than literal translation.
  3. **Abebe G.** (Student):
     - *Observation*: "The radio shouldn't just play modern music; it has to be classical *Tizita* with Krar and Masenqo timbres, the way ETV and Radio Ethiopia sounded in the 1970s."
     - *Change*: Tuned the acoustic music prompt to specifically invoke the D-pentatonic Tizita mode with bowed masenqo harmonic resonance.

---

## 4. User Test 2: The Near-Final Cut (Post-Assembly Prototype)
*Conducted with the complete 24fps motion cut, ducked score, and burned subtitles.*

- **Testers**:
  1. **Dawit K.** (Student):
     - *Feedback*: "In the 9:16 vertical version, the subtitle text took up half the screen vertically! It covered Ato Berhanu's face and hands."
     - *Resolution*: Repositioned subtitles strictly into the lower third (`Alignment=2`, `FontSize=8.5`, `MarginV=60`), preserving standard mobile safe zones.
  2. **Selamawit T.** (Student):
     - *Feedback*: "The background music was originally so quiet I thought my headphones were unplugged. Music needs to rise when he stops speaking."
     - *Resolution*: Boosted music stem gain by +12 dB and re-calibrated the FFmpeg dynamic ducking (`sidechaincompress`) threshold to let the Tizita melody sing during pauses.
  3. **Yohannes M.** (Student):
     - *Feedback*: "Shot 4 audio abruptly cut off before finishing the sentence in the early draft."
     - *Resolution*: Resolved the Google TTS compound-sentence character truncation bug by implementing clause-based segmentation in `pipeline/narration.py`.

---

## 5. Shot Justification Matrix

| Shot ID | Framing | Purpose / Emotional Reason | Story Beat |
| :--- | :--- | :--- | :--- |
| **Shot 01** | Wide establishing | Introduce the solitary sacred sanctuary of the workshop | Silence as anticipation |
| **Shot 02** | Medium interior | Establish 40 years of artisanal dedication | Lifelong devotion |
| **Shot 03** | Close-up components | Contrast fragile copper wires with monumental human connection | The neighborhood lifeline |
| **Shot 04** | Intimate Medium | Center the family heirloom and personal grief (mother's passing) | The dormant memory |
| **Shot 05** | Extreme Close-Up | Focus on the weathered hands turning the tuner dial | Patient craftsmanship |
| **Shot 06** | Close-up dial | Build tension through analog static and electrical crackle | The search for truth |
| **Shot 07** | Warm Low-Angle | The cathartic breakthrough as the radio springs to life | Epiphany & Tizita |
| **Shot 08** | Medium Close-Up | Capture the transcendent gentle smile of Ato Berhanu | Emotional resolution |
| **Shot 09** | Wide Pull-Out | Final philosophical departure: memory endures beyond matter | Eternal legacy |
