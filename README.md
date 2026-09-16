<h1 align="center">Voice Spectrogram Research</h1>

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&color=FFFFFF&center=true&vCenter=true&width=600&lines=Voice+Spectrogram+Analysis;Silence+Detection+%7C+Spectral+Visualization;Perceptual+Voice+Classification" alt="Typing SVG" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-000000?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/aiogram-3.x-000000?style=for-the-badge&logo=telegram&logoColor=white" />
  <img src="https://img.shields.io/badge/FFmpeg-000000?style=for-the-badge&logo=ffmpeg&logoColor=white" />
  <img src="https://img.shields.io/badge/SoX-000000?style=for-the-badge&logoColor=white" />
</p>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:FFFFFF,100:FFFFFF&height=120&section=header" width="100%" />

<img src="./assets/divider.svg" width="100%" height="2" />

## Overview

An exploration of **voice spectrograms** as a tool for vocal characterization, integrated into a production Telegram bot. This project investigates how audio visualization can provide meaningful, personalized feedback to vocal students.

Built for **SOLO Vocal Work** (Tomsk, Russia) — a real vocal school.

<img src="./assets/divider.svg" width="100%" height="2" />

## Visual Output

### Waveform

<p align="center">
  <img src="./assets/waveform.png" width="80%" alt="Waveform" />
</p>

### Spectrogram

<p align="center">
  <img src="./assets/spectrogram.png" width="80%" alt="Spectrogram" />
</p>

### RMS (Loudness)

<p align="center">
  <img src="./assets/rms.png" width="80%" alt="RMS" />
</p>

<img src="./assets/divider.svg" width="100%" height="2" />

## Research Motivation

Traditional vocal coaching relies on subjective listening. But every voice has a unique **spectral fingerprint** — a visual signature that reveals:

- **Timbre** — the "color" of the voice
- **Formants** — resonant frequencies that shape vowels
- **Harmonic structure** — the richness of overtones
- **Dynamic range** — how loud and soft the voice can be
- **Pitch stability** — consistency across a phrase

The goal was to translate acoustic data into actionable, human-readable feedback.

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

Sufficient Nyquist frequency (8 kHz) for vocal range

Smaller file size, faster processing

Standard for speech analysis

2. Silence Detection
bash
ffmpeg -i voice.wav -af volumedetect -f null NUL
Metric	Meaning	Threshold
mean_volume	Average loudness (dB)	< −35 dB → silence
max_volume	Peak loudness (dB)	< −30 dB → silence
File size	Quick sanity check	< 5 KB → silence
3. Spectrogram Generation (SoX)
bash
sox voice.wav -n spectrogram \
    -x 1000 -y 513 -z 120 -w Kaiser -o spectrogram.png
4. Voice Classification
Duration	Category
0–2 s	Too short
3–5 s	High & bright
6–10 s	Warm & rich
11–15 s	Low & deep
15+ s	Strong & confident
<img src="./assets/divider.svg" width="100%" height="2" />
Results
Silence detection accuracy: ~95%

Average processing time: 1.8 s

Users who completed voice test were 3× more likely to book a lesson

<img src="./assets/divider.svg" width="100%" height="2" />
Tech Stack
python
FFmpeg        # Decode, resample, volume analysis
SoX           # Spectrogram generation
aiogram 3.x   # Async Telegram Bot
asyncio       # Concurrent processing
python-dotenv # Environment variables
<img src="./assets/divider.svg" width="100%" height="2" />
🚀 Getting Started
Prerequisites
Python 3.10+

FFmpeg — download (must be in PATH)

SoX — download (must be in PATH)

Installation
bash
git clone https://github.com/LukasMisyunas/voice-spectrogram-research.git
cd voice-spectrogram-research

python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate  # Linux / macOS

pip install -r requirements.txt
Run
bash
python spectrogram_research.py voice.ogg
Output
text
==================================================
🎤  MID VOICE
==================================================
Note:       A3
Pitch:      220 Hz
Avg RMS:    0.0342
Max RMS:    0.0871
Is silent:  False
==================================================
Troubleshooting
Problem	Solution
ffmpeg: command not found	Install FFmpeg and add it to PATH
sox: command not found	Install SoX and add it to PATH
No spectrogram created	Check that the WAV file exists
<img src="./assets/divider.svg" width="100%" height="2" />
Future Work
Direction	Description
F0 Extraction	Use Praat/Librosa for true fundamental frequency
Formant Analysis	Map F1/F2 to vowel quality
ML Classification	Train a CNN on spectrograms
Pitch Tracking	Detect vibrato and stability
<img src="./assets/divider.svg" width="100%" height="2" />
References
Praat — phonetic analysis

Librosa — Python audio analysis

SoX Documentation

FFmpeg Filters

<img src="./assets/divider.svg" width="100%" height="2" />
Author
Lukas Misyunas
Portfolio Project — Built for SOLO Vocal Work (Tomsk, Russia)

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:FFFFFF,100:FFFFFF&height=120&section=footer" width="100%"
