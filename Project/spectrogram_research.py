"""
Voice Spectrogram Research
==========================
An exploration of voice spectrograms as a tool for vocal characterization.

This script:
1. Accepts an audio file (OGG/WAV).
2. Converts it to WAV via FFmpeg.
3. Analyzes it via Librosa (RMS + pyin pitch detection).
4. Generates a spectrogram via SoX.
5. Outputs a perceptual voice classification.

Author: Lukas Misyunas
"""

import os
import subprocess
import logging
from pathlib import Path

import numpy as np
import librosa


# ==================== LOGGING ====================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# ==================== HELPERS ====================

def freq_to_note(freq: float) -> str:
    """
    Convert a frequency (Hz) to a musical note name.

    Example:
        440.0 -> "A4"
        261.6 -> "C4"

    Returns "—" if the frequency is invalid.
    """
    if freq <= 0:
        return "—"

    A4 = 440.0
    semitones = 12 * np.log2(freq / A4)
    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    note_index = int(round(semitones)) % 12
    octave = 4 + (int(round(semitones)) + 9) // 12
    return f"{note_names[note_index]}{octave}"


# ==================== AUDIO ANALYSIS ====================

def analyze_voice(file_path: str) -> dict:
    """
    Analyze an audio file and return acoustic features.

    Pipeline:
        OGG -> FFmpeg -> WAV (16 kHz, mono)
        WAV -> Librosa -> RMS + pyin pitch

    Returns a dict with:
        - is_silent  (bool)
        - avg_rms    (float)  — average loudness
        - max_rms    (float)  — peak loudness
        - avg_pitch  (float)  — average fundamental frequency (Hz)
        - note       (str)    — closest musical note
    """
    # Convert OGG -> WAV (librosa does not read Telegram OGG reliably)
    wav_path = str(file_path).replace(".ogg", ".wav")
    try:
        subprocess.run(
            ["ffmpeg", "-i", str(file_path), "-ar", "22050", "-ac", "1", wav_path, "-y"],
            capture_output=True,
            timeout=15
        )
        if os.path.exists(wav_path):
            file_path = wav_path
    except Exception as e:
        logger.error(f"Conversion error: {e}")

    try:
        # Load audio at 22050 Hz, mono
        y, sr = librosa.load(str(file_path), sr=22050, mono=True)

        # --- Loudness (RMS) ---
        rms = librosa.feature.rms(y=y)[0]
        avg_rms = float(np.mean(rms))
        max_rms = float(np.max(rms))

        # --- Silence detection ---
        SILENCE_THRESHOLD = 0.01
        is_silent = max_rms < SILENCE_THRESHOLD

        # --- Pitch detection via pyin (fundamental frequency, not harmonics) ---
        f0, voiced_flag, voiced_probs = librosa.pyin(
            y,
            fmin=librosa.note_to_hz("C2"),   # 65 Hz  — low male voice
            fmax=librosa.note_to_hz("C6"),   # 1046 Hz — high female voice
            sr=sr
        )

        # Keep only voiced frames
        pitch_values = f0[~np.isnan(f0)]

        # Filter outliers (real human voice: 65–1000 Hz)
        pitch_values = pitch_values[(pitch_values > 65) & (pitch_values < 1000)]

        avg_pitch = float(np.mean(pitch_values)) if len(pitch_values) > 0 else 0.0
        note = freq_to_note(avg_pitch) if avg_pitch > 0 else "—"

        # Remove temporary WAV
        if wav_path != str(file_path) and os.path.exists(wav_path):
            try:
                os.remove(wav_path)
            except Exception:
                pass

        return {
            "is_silent": is_silent,
            "avg_rms": avg_rms,
            "max_rms": max_rms,
            "avg_pitch": avg_pitch,
            "note": note,
        }

    except Exception as e:
        logger.error(f"Audio analysis error: {e}")
        return {
            "is_silent": True,
            "avg_rms": 0.0,
            "max_rms": 0.0,
            "avg_pitch": 0.0,
            "note": "—",
        }


# ==================== VOICE CLASSIFICATION ====================

def get_voice_result(analysis: dict, duration: int) -> dict:
    """
    Classify voice type based on acoustic analysis and duration.

    Returns a dict with:
        - emoji (str)
        - title (str)
        - text  (str)
    """
    # Case 1: silence
    if analysis["is_silent"] or analysis["max_rms"] < 0.01:
        return {
            "emoji": "🔇",
            "title": "SILENCE",
            "text": "No sound detected. Try speaking louder or checking your microphone."
        }

    # Case 2: too short
    if duration <= 2:
        return {
            "emoji": "📢",
            "title": "TOO SHORT",
            "text": "Recording is too short. Try 5–15 seconds."
        }

    pitch = analysis["avg_pitch"]

    # Case 3: pitch undefined
    if pitch <= 0:
        return {
            "emoji": "🎵",
            "title": "UNDEFINED",
            "text": "Could not detect pitch. Try singing louder or reducing background noise."
        }

    # Case 4: low voice
    if pitch < 150:
        return {
            "emoji": "🎸",
            "title": "LOW VOICE",
            "text": f"Your voice sounds deep and powerful. "
                    f"Note: {analysis['note']} ({int(pitch)} Hz)."
        }

    # Case 5: mid voice
    elif pitch < 250:
        return {
            "emoji": "🎤",
            "title": "MID VOICE",
            "text": f"Your voice sounds warm and velvety. "
                    f"Note: {analysis['note']} ({int(pitch)} Hz)."
        }

    # Case 6: high voice
    else:
        return {
            "emoji": "🎼",
            "title": "HIGH VOICE",
            "text": f"Your voice sounds bright and ringing. "
                    f"Note: {analysis['note']} ({int(pitch)} Hz)."
        }


# ==================== SPECTROGRAM GENERATION ====================

def generate_spectrogram(wav_path: str, output_path: str = "spectrogram.png") -> str:
    """
    Generate a spectrogram image from a WAV file using SoX.

    Parameters:
        wav_path     — path to the input WAV file
        output_path  — path to save the spectrogram PNG

    SoX parameters:
        -x 1000   — width in pixels
        -y 513    — height (frequency bins)
        -z 120    — dynamic range (dB)
        -w Kaiser — window function

    Returns the path to the generated image.
    """
    try:
        subprocess.run(
            [
                "sox", wav_path, "-n", "spectrogram",
                "-x", "1000",
                "-y", "513",
                "-z", "120",
                "-w", "Kaiser",
                "-o", output_path
            ],
            capture_output=True,
            timeout=15
        )
        if os.path.exists(output_path):
            logger.info(f"Spectrogram saved: {output_path}")
            return output_path
        else:
            logger.error("Spectrogram was not created.")
            return ""
    except Exception as e:
        logger.error(f"Spectrogram generation error: {e}")
        return ""


# ==================== MAIN ====================

def main(audio_file: str):
    """
    Run the full pipeline on a single audio file.

    Pipeline:
        1. Analyze voice (RMS + pitch)
        2. Classify voice type
        3. Generate spectrogram
        4. Print results
    """
    if not os.path.exists(audio_file):
        logger.error(f"File not found: {audio_file}")
        return

    logger.info(f"Processing: {audio_file}")

    # 1. Analysis
    analysis = analyze_voice(audio_file)
    logger.info(f"Analysis: {analysis}")

    # 2. Classification (duration is unknown here — pass 10 as a placeholder)
    duration = 10
    result = get_voice_result(analysis, duration)

    # 3. Spectrogram
    wav_path = str(audio_file).replace(".ogg", ".wav")
    if not os.path.exists(wav_path):
        wav_path = audio_file  # fallback if already WAV
    generate_spectrogram(wav_path, "spectrogram.png")

    # 4. Output
    print("\n" + "=" * 50)
    print(f"{result['emoji']}  {result['title']}")
    print("=" * 50)
    print(f"Note:       {analysis['note']}")
    print(f"Pitch:      {int(analysis['avg_pitch'])} Hz")
    print(f"Avg RMS:    {analysis['avg_rms']:.4f}")
    print(f"Max RMS:    {analysis['max_rms']:.4f}")
    print(f"Is silent:  {analysis['is_silent']}")
    print("=" * 50)
    print(f"\n{result['text']}\n")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python spectrogram_research.py <audio_file>")
        sys.exit(1)

    main(sys.argv[1])
