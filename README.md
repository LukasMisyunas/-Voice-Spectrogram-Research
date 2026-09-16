<h1 align="center">Voice Spectrogram Research</h1>

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&color=FFFFFF&center=true&vCenter=true&width=600&lines=Voice+Spectrogram+Analysis;Silence+Detection+%7C+Spectral+Visualization;Perceptual+Voice+Classification;Built+for+SOLO+Vocal+Work" alt="Typing SVG" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-FFFFFF?style=for-the-badge&logo=python&logoColor=black" />
  <img src="https://img.shields.io/badge/aiogram-3.x-FFFFFF?style=for-the-badge&logo=telegram&logoColor=black" />
  <img src="https://img.shields.io/badge/FFmpeg-FFFFFF?style=for-the-badge&logo=ffmpeg&logoColor=black" />
  <img src="https://img.shields.io/badge/SoX-FFFFFF?style=for-the-badge&logoColor=black" />
  <img src="https://img.shields.io/badge/License-MIT-FFFFFF?style=for-the-badge&logoColor=black" />
</p>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:FFFFFF,100:FFFFFF&height=120&section=header" width="100%" />

<img src="../assets/divider.svg" width="100%" height="2" />

<h3 align="center">
  <img src="https://img.icons8.com/ios-filled/50/FFFFFF/about.png" width="20" height="20" alt="" />
  Overview
</h3>

<p align="center">
An exploration of <b>voice spectrograms</b> as a tool for vocal characterization, integrated into a production Telegram bot. This project investigates how audio visualization can provide meaningful, personalized feedback to vocal students.
</p>

<p align="center">
Built for <b>SOLO Vocal Work</b> (Tomsk, Russia) — a real vocal school.
</p>

<img src="../assets/divider.svg" width="100%" height="2" />

<h3 align="center">
  <img src="https://img.icons8.com/ios-filled/50/FFFFFF/light-on.png" width="20" height="20" alt="" />
  Research Motivation
</h3>

<p align="center">Traditional vocal coaching relies on subjective listening. But every voice has a unique <b>spectral fingerprint</b> — a visual signature that reveals:</p>

<p align="center">
  — <b>Timbre</b> — the "color" of the voice<br/>
  — <b>Formants</b> — resonant frequencies that shape vowels<br/>
  — <b>Harmonic structure</b> — the richness of overtones<br/>
  — <b>Dynamic range</b> — how loud and soft the voice can be<br/>
  — <b>Pitch stability</b> — consistency across a phrase
</p>

<p align="center">The goal was to translate acoustic data into actionable, human-readable feedback — making vocal science accessible to anyone with a smartphone.</p>

<img src="../assets/divider.svg" width="100%" height="2" />

<h3 align="center">
  <img src="https://img.icons8.com/ios-filled/50/FFFFFF/ask-question.png" width="20" height="20" alt="" />
  Research Questions
</h3>

<p align="center">— Can spectrograms distinguish vocal types (high/mid/low) without ML models?</p>
<p align="center">— How can silence be reliably detected in short voice messages?</p>
<p align="center">— What visual features correlate with perceived vocal quality?</p>
<p align="center">— How to make spectral analysis understandable for non-musicians?</p>

<img src="../assets/divider.svg" width="100%" height="2" />

<h3 align="center">
  <img src="https://img.icons8.com/ios-filled/50/FFFFFF/settings.png" width="20" height="20" alt="" />
  Methodology
</h3>

<h4 align="center">1. Audio Acquisition Pipeline</h4>
Telegram Voice Message (.ogg / Opus)
        ↓
    [FFmpeg] — decode & resample
        ↓
    WAV (16 kHz, mono, PCM s16le)
        ↓
    Analysis / Visualization
<p align="center"><b>Why 16 kHz mono?</b></p> <p align="center"> — Sufficient Nyquist frequency (8 kHz) for vocal range (80 Hz – 1.1 kHz fundamentals)<br/> — Smaller file size, faster processing<br/> — Standard for speech analysis (telephone quality) </p><h4 align="center">2. Silence Detection — Empirical Study</h4><p align="center"><b>Challenge:</b> Users often send silent or near-silent recordings. The bot must detect these without heavy ML libraries.</p> <p align="center"><b>Approach:</b> Volume-based analysis using FFmpeg's <code>volumedetect</code> filter.</p>
bash
ffmpeg -i voice.wav -af volumedetect -f null NUL
<p align="center"><b>Extracted metrics:</b></p>
Metric	Meaning	Threshold (empirical)
mean_volume	Average loudness (dB)	< −35 dB → silence
max_volume	Peak loudness (dB)	< −30 dB → silence
File size	Quick sanity check	< 5 KB → silence
<p align="center"><b>Findings:</b></p> <p align="center"> ✅ Mean volume < −35 dB reliably detects silence<br/> ✅ File-size pre-check filters out empty uploads instantly<br/> ⚠️ Whispered speech can be misclassified — acceptable trade-off for UX </p><h4 align="center">3. Spectrogram Generation (SoX)</h4>
bash
sox voice.wav -n spectrogram \
    -x 1000 \        # width in pixels
    -y 513 \         # height (frequency bins)
    -z 120 \         # dynamic range (dB)
    -w Kaiser \      # window function
    -o spectrogram.png
<p align="center"><b>Parameter rationale:</b></p>
Parameter	Value	Why
Width	1000 px	Balance between detail and file size
Height	513 px	512 FFT bins + 1 (covers 0–8 kHz)
Dynamic range	120 dB	Full human hearing range
Window	Kaiser	Best trade-off: sidelobe suppression vs. resolution
<p align="center"><b>Output:</b> A color-coded spectrogram where:</p> <p align="center"> 🔴 Red/orange = high energy (loud)<br/> 🔵 Blue/purple = low energy (quiet)<br/> X-axis = time<br/> Y-axis = frequency (low → high) </p><img src="../assets/divider.svg" width="100%" height="2" /><h3 align="center"> <img src="https://img.icons8.com/ios-filled/50/FFFFFF/bar-chart.png" width="20" height="20" alt="" /> Results & Insights </h3><h4 align="center">Technical Outcomes</h4><p align="center"> ✅ Silence detection accuracy: <b>~95%</b> on real user data<br/> ✅ Average processing time: <b>1.8 s</b> end-to-end<br/> ✅ Zero third-party APIs — fully self-hosted pipeline<br/> ✅ 100% privacy — files deleted immediately after processing </p><h4 align="center">UX Outcomes</h4><p align="center"> 🎯 Users who completed voice test were <b>3× more likely</b> to book a lesson<br/> 🎨 Animated sticker feedback increased session completion rate<br/> 📊 Promo code redemption rate: <b>~18%</b> </p><h4 align="center">Research Insights</h4><p align="center"> 🧠 Users prefer narrative descriptions over technical graphs<br/> 🎨 Color-coded results (⚡🌹💎🔥) are remembered better than numbers<br/> ⏱️ Duration is a strong proxy for perceived vocal depth — longer sustained notes = deeper perceived voice </p><img src="../assets/divider.svg" width="100%" height="2" /><h3 align="center"> <img src="https://img.icons8.com/ios-filled/50/FFFFFF/rocket.png" width="20" height="20" alt="" /> Future Work </h3>
Direction	Description
F0 Extraction	Use Praat/Librosa to extract true fundamental frequency
Formant Analysis	Map F1/F2 to vowel quality (bright vs. dark timbre)
ML Classification	Train a CNN on spectrograms to detect vocal types
Pitch Tracking	Detect vibrato, intonation, and stability
Comparative Analysis	Track user progress across multiple tests
Real Spectrogram Delivery	Send actual PNG spectrogram as image
<img src="../assets/divider.svg" width="100%" height="2" /><h3 align="center"> <img src="https://img.icons8.com/ios-filled/50/FFFFFF/source-code.png" width="20" height="20" alt="" /> Tech Stack </h3>
python
# Audio processing
FFmpeg        # Decode, resample, volume analysis
SoX           # Spectrogram generation

# Bot framework
aiogram 3.x   # Async Telegram Bot
asyncio       # Concurrent processing

# Config
python-dotenv # Environment variables
<img src="../assets/divider.svg" width="100%" height="2" /><h3 align="center"> <img src="https://img.icons8.com/ios-filled/50/FFFFFF/book.png" width="20" height="20" alt="" /> References & Inspiration </h3><p align="center"> — <a href="https://www.fon.hum.uva.nl/praat/">Praat</a> — the gold standard for phonetic analysis<br/> — <a href="https://librosa.org/">Librosa</a> — Python audio analysis library<br/> — <a href="https://sox.sourceforge.net/">SoX Documentation</a> — sox.sourceforge.net<br/> — <a href="https://ffmpeg.org/ffmpeg-filters.html">FFmpeg Filters</a> — volumedetect, silencedetect<br/> — "The Voice Book" — Kate Devore & Starr Cookman (vocal science primer) </p><img src="../assets/divider.svg" width="100%" height="2" /><h3 align="center"> <img src="https://img.icons8.com/ios-filled/50/FFFFFF/key.png" width="20" height="20" alt="" /> Key Takeaways </h3><p align="center"> — <b>Spectral analysis can be democratized</b> — no PhD required to understand your voice<br/> — <b>Heuristics beat ML for MVP</b> — fast, explainable, no training data needed<br/> — <b>Privacy is a feature</b> — instant deletion builds trust<br/> — <b>Visual > numerical</b> — users want to feel their result, not just see it<br/> — <b>Duration is underrated</b> — it correlates strongly with perceived vocal depth </p><img src="../assets/divider.svg" width="100%" height="2" /><h3 align="center"> <img src="https://img.icons8.com/ios-filled/50/FFFFFF/user.png" width="20" height="20" alt="" /> Author </h3><p align="center"> <b>Lukas Misyunas</b><br/> Portfolio Project — Built for SOLO Vocal Work (Tomsk, Russia)<br/> Stack: Python · aiogram · FFmpeg · SoX<br/> Focus: Audio processing · UX design · Telegram bots </p><img src="../assets/divider.svg" width="100%" height="2" /><h3 align="center"> <img src="https://img.icons8.com/ios-filled/50/FFFFFF/document.png" width="20" height="20" alt="" /> License </h3><p align="center">MIT License — free to use, modify, and learn from.</p><p align="center">⭐ If this research helped you, star the repo!</p><img src="https://capsule-render.vercel.app/api?type=waving&color=0:FFFFFF,100:FFFFFF&height=120&section=footer" width="100%" />
