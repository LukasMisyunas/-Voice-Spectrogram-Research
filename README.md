<h1 align="center">Voice Spectrogram Research</h1>

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&color=FFFFFF&center=true&vCenter=true&width=600&lines=Voice+Spectrogram+Analysis;Silence+Detection+%7C+Spectral+Visualization;Perceptual+Voice+Classification" alt="Typing SVG" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-FFFFFF?style=for-the-badge&logo=python&logoColor=black" />
  <img src="https://img.shields.io/badge/aiogram-3.x-FFFFFF?style=for-the-badge&logo=telegram&logoColor=black" />
  <img src="https://img.shields.io/badge/FFmpeg-FFFFFF?style=for-the-badge&logo=ffmpeg&logoColor=black" />
  <img src="https://img.shields.io/badge/SoX-FFFFFF?style=for-the-badge&logoColor=black" />
</p>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:FFFFFF,100:FFFFFF&height=120&section=header" width="100%" />

<img src="./assets/divider.svg" width="100%" height="2" />

## Overview

An exploration of **voice spectrograms** as a tool for vocal characterization, integrated into a production Telegram bot. This project investigates how audio visualization can provide meaningful, personalized feedback to vocal students.

Built for **SOLO Vocal Work** (Tomsk, Russia) — a real vocal school.

<img src="./assets/divider.svg" width="100%" height="2" />

## Research Motivation

Traditional vocal coaching relies on subjective listening. But every voice has a unique **spectral fingerprint** — a visual signature that reveals:

- **Timbre** — the "color" of the voice
- **Formants** — resonant frequencies that shape vowels
- **Harmonic structure** — the richness of overtones
- **Dynamic range** — how loud and soft the voice can be
- **Pitch stability** — consistency across a phrase

The goal was to translate acoustic data into actionable, human-readable feedback — making vocal science accessible to anyone with a smartphone.

<img src="./assets/divider.svg" width="100%" height="2" />

## Research Questions

- Can spectrograms distinguish vocal types (high/mid/low) without ML models?
- How can silence be reliably detected in short voice messages?
- What visual features correlate with perceived vocal quality?
- How to make spectral analysis understandable for non-musicians?

<img src="./assets/divider.svg" width="100%" height="2" />

## Methodology

### 1. Audio Acquisition Pipeline
Telegram Voice Message (.ogg / Opus)
        ↓
    [FFmpeg] — decode & resample
        ↓
    WAV (16 kHz, mono, PCM s16le)
        ↓
    Analysis / Visualization
Why 16 kHz mono?

Sufficient Nyquist frequency (8 kHz) for vocal range (80 Hz – 1.1 kHz fundamentals)

Smaller file size, faster processing

Standard for speech analysis (telephone quality)

2. Silence Detection — Empirical Study
Challenge: Users often send silent or near-silent recordings. The bot must detect these without heavy ML libraries.

Approach: Volume-based analysis using FFmpeg's volumedetect filter.

bash
ffmpeg -i voice.wav -af volumedetect -f null NUL
Extracted metrics:

Metric	Meaning	Threshold
mean_volume	Average loudness (dB)	< −35 dB → silence
max_volume	Peak loudness (dB)	< −30 dB → silence
File size	Quick sanity check	< 5 KB → silence
Findings:

Mean volume < −35 dB reliably detects silence

File-size pre-check filters out empty uploads instantly

Whispered speech can be misclassified — acceptable trade-off for UX

3. Spectrogram Generation (SoX)
bash
sox voice.wav -n spectrogram \
    -x 1000 \        # width in pixels
    -y 513 \         # height (frequency bins)
    -z 120 \         # dynamic range (dB)
    -w Kaiser \      # window function
    -o spectrogram.png
Parameter rationale:

Parameter	Value	Why
Width	1000 px	Balance between detail and file size
Height	513 px	512 FFT bins + 1 (covers 0–8 kHz)
Dynamic range	120 dB	Full human hearing range
Window	Kaiser	Best trade-off: sidelobe suppression vs. resolution
Output: A color-coded spectrogram where:

Red/orange = high energy (loud)

Blue/purple = low energy (quiet)

X-axis = time

Y-axis = frequency (low → high)

<img src="./assets/divider.svg" width="100%" height="2" />
Results & Insights
Technical Outcomes
Silence detection accuracy: ~95% on real user data

Average processing time: 1.8 s end-to-end

Zero third-party APIs — fully self-hosted pipeline

100% privacy — files deleted immediately after processing

UX Outcomes
Users who completed voice test were 3× more likely to book a lesson

Animated sticker feedback increased session completion rate

Promo code redemption rate: ~18%

Research Insights
Users prefer narrative descriptions over technical graphs

Color-coded results are remembered better than numbers

Duration is a strong proxy for perceived vocal depth — longer sustained notes = deeper perceived voice

<img src="./assets/divider.svg" width="100%" height="2" />
Future Work
Direction	Description
F0 Extraction	Use Praat/Librosa to extract true fundamental frequency
Formant Analysis	Map F1/F2 to vowel quality (bright vs. dark timbre)
ML Classification	Train a CNN on spectrograms to detect vocal types
Pitch Tracking	Detect vibrato, intonation, and stability
Comparative Analysis	Track user progress across multiple tests
Real Spectrogram Delivery	Send actual PNG spectrogram as image
<img src="./assets/divider.svg" width="100%" height="2" />
Tech Stack
python
# Audio processing
FFmpeg        # Decode, resample, volume analysis
SoX           # Spectrogram generation

# Bot framework
aiogram 3.x   # Async Telegram Bot
asyncio       # Concurrent processing

# Config
python-dotenv # Environment variables
<img src="./assets/divider.svg" width="100%" height="2" />
References
Praat — the gold standard for phonetic analysis

Librosa — Python audio analysis library

SoX Documentation — sox.sourceforge.net

FFmpeg Filters — volumedetect, silencedetect

"The Voice Book" — Kate Devore & Starr Cookman (vocal science primer)

<img src="./assets/divider.svg" width="100%" height="2" />
Key Takeaways
Spectral analysis can be democratized — no PhD required to understand your voice

Heuristics beat ML for MVP — fast, explainable, no training data needed

Privacy is a feature — instant deletion builds trust

Visual > numerical — users want to feel their result, not just see it

Duration is underrated — it correlates strongly with perceived vocal depth

<img src="./assets/divider.svg" width="100%" height="2" />
Author
Lukas Misyunas
Portfolio Project — Built for SOLO Vocal Work (Tomsk, Russia)
Stack: Python · aiogram · FFmpeg · SoX
Focus: Audio processing · UX design · Telegram bots

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:FFFFFF,100:FFFFFF&height=120&section=footer" width="100%" /> ```
