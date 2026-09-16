"""
Generate waveform, spectrogram, and RMS plots for README.
"""
import os
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
from matplotlib import rcParams

# White-on-dark style (looks good on both themes)
rcParams["figure.facecolor"] = "none"
rcParams["axes.facecolor"] = "none"
rcParams["savefig.facecolor"] = "none"
rcParams["text.color"] = "white"
rcParams["axes.labelcolor"] = "white"
rcParams["xtick.color"] = "white"
rcParams["ytick.color"] = "white"
rcParams["axes.edgecolor"] = "white"


def generate_all(audio_path: str, output_dir: str = "assets"):
    os.makedirs(output_dir, exist_ok=True)

    y, sr = librosa.load(audio_path, sr=22050, mono=True)

    # --- 1. Waveform ---
    plt.figure(figsize=(10, 2.5))
    librosa.display.waveshow(y, sr=sr, color="white")
    plt.title("Waveform", color="white")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/waveform.png", transparent=True, dpi=150)
    plt.close()

    # --- 2. Spectrogram ---
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(D, sr=sr, x_axis="time", y_axis="log", cmap="gray")
    plt.title("Spectrogram", color="white")
    plt.colorbar(format="%+2.0f dB")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/spectrogram.png", transparent=True, dpi=150)
    plt.close()

    # --- 3. RMS ---
    rms = librosa.feature.rms(y=y)[0]
    times = librosa.times_like(rms, sr=sr)
    plt.figure(figsize=(10, 2.5))
    plt.plot(times, rms, color="white")
    plt.title("RMS (Loudness)", color="white")
    plt.xlabel("Time (s)")
    plt.ylabel("RMS")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/rms.png", transparent=True, dpi=150)
    plt.close()

    print(f"Saved 3 plots to {output_dir}/")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python generate_assets.py <audio_file>")
        sys.exit(1)
    generate_all(sys.argv[1])
