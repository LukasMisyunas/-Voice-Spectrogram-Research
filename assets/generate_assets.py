"""
Generate waveform, spectrogram, and RMS plots for README.

Usage:
    python generate_assets.py voice.ogg

Output:
    assets/waveform.png
    assets/spectrogram.png
    assets/rms.png
"""

import os
import sys
import subprocess

import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
from matplotlib import rcParams


# ==================== STYLE ====================

# Transparent background + white lines (looks good on both themes)
rcParams["figure.facecolor"] = "none"
rcParams["axes.facecolor"] = "none"
rcParams["savefig.facecolor"] = "none"
rcParams["text.color"] = "white"
rcParams["axes.labelcolor"] = "white"
rcParams["xtick.color"] = "white"
rcParams["ytick.color"] = "white"
rcParams["axes.edgecolor"] = "white"
rcParams["axes.spines.top"] = False
rcParams["axes.spines.right"] = False


# ==================== HELPERS ====================

def convert_to_wav(audio_path: str) -> str:
    """
    Convert any audio file to WAV (22050 Hz, mono) via FFmpeg.
    Returns the path to the WAV file.
    """
    wav_path = os.path.splitext(audio_path)[0] + ".wav"
    if audio_path.endswith(".wav"):
        return audio_path

    try:
        subprocess.run(
            ["ffmpeg", "-i", audio_path, "-ar", "22050", "-ac", "1", wav_path, "-y"],
            capture_output=True,
            timeout=15
        )
        return wav_path
    except Exception as e:
        print(f"FFmpeg error: {e}")
        return audio_path


# ==================== GENERATORS ====================

def generate_waveform(y, sr, output_path: str):
    """Generate a waveform plot."""
    plt.figure(figsize=(10, 2.5))
    librosa.display.waveshow(y, sr=sr, color="white")
    plt.title("Waveform", color="white", fontsize=14)
    plt.xlabel("Time (s)", color="white")
    plt.ylabel("Amplitude", color="white")
    plt.tight_layout()
    plt.savefig(output_path, transparent=True, dpi=150)
    plt.close()
    print(f"Saved: {output_path}")


def generate_spectrogram(y, sr, output_path: str):
    """Generate a spectrogram plot."""
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)

    plt.figure(figsize=(10, 4))
    librosa.display.specshow(D, sr=sr, x_axis="time", y_axis="log", cmap="gray")
    plt.title("Spectrogram", color="white", fontsize=14)
    plt.xlabel("Time (s)", color="white")
    plt.ylabel("Frequency (Hz)", color="white")

    cbar = plt.colorbar(format="%+2.0f dB")
    cbar.ax.yaxis.set_tick_params(color="white")
    plt.setp(plt.getp(cbar.ax.axes, "yticklabels"), color="white")

    plt.tight_layout()
    plt.savefig(output_path, transparent=True, dpi=150)
    plt.close()
    print(f"Saved: {output_path}")


def generate_rms(y, sr, output_path: str):
    """Generate an RMS (loudness) plot."""
    rms = librosa.feature.rms(y=y)[0]
    times = librosa.times_like(rms, sr=sr)

    plt.figure(figsize=(10, 2.5))
    plt.plot(times, rms, color="white", linewidth=1.5)
    plt.fill_between(times, rms, color="white", alpha=0.15)
    plt.title("RMS (Loudness)", color="white", fontsize=14)
    plt.xlabel("Time (s)", color="white")
    plt.ylabel("RMS", color="white")
    plt.tight_layout()
    plt.savefig(output_path, transparent=True, dpi=150)
    plt.close()
    print(f"Saved: {output_path}")


# ==================== MAIN ====================

def main(audio_path: str, output_dir: str = "assets"):
    if not os.path.exists(audio_path):
        print(f"File not found: {audio_path}")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    # Convert to WAV if needed
    wav_path = convert_to_wav(audio_path)

    # Load audio
    print(f"Loading: {wav_path}")
    y, sr = librosa.load(wav_path, sr=22050, mono=True)

    # Generate all three plots
    generate_waveform(y, sr, f"{output_dir}/waveform.png")
    generate_spectrogram(y, sr, f"{output_dir}/spectrogram.png")
    generate_rms(y, sr, f"{output_dir}/rms.png")

    print(f"\nAll plots saved to {output_dir}/")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_assets.py <audio_file>")
        sys.exit(1)

    main(sys.argv[1])
