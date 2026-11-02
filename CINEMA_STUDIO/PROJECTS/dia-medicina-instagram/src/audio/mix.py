"""Build the production-sound bed from the original clips (same cuts/speeds as
the picture) and mix it with the score and SFX. Output: audio/mix.wav,
loudness-normalised for Instagram/web (-14 LUFS integrated, -1 dBTP).
"""
import subprocess
import sys
from pathlib import Path

import numpy as np
from scipy.io import wavfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "edit"))
from edl import SEGMENTS, timeline  # noqa: E402

PROJ = Path(__file__).resolve().parents[2]
AUD = PROJ / "audio"
WORK = PROJ / "renders" / "work"
SR = 48000
N = SR * 30

# integrated loudness of each clip's own audio (measured with ebur128)
LUFS = {"IMG_7123": -37.8, "IMG_7126": -35.7, "IMG_7128": -31.9, "IMG_7129": -37.9,
        "IMG_7136": -33.5, "IMG_7154": -23.4, "IMG_7155": -31.2, "IMG_7164": -27.5,
        "IMG_7167": -27.2, "IMG_7168": -19.2, "IMG_7172": -28.8}


def seg_audio(seg):
    """Original sound for one segment at the picture's speed, levelled to ~-26 LUFS."""
    n = round(seg["dur"] * SR)
    if seg["src"].startswith("foto"):
        return np.zeros((n, 2))
    a, b = seg["a"], seg["b"]
    speed = (b - a) / seg["dur"]  # >1 faster, <1 slower
    gain = min(-26 - LUFS[seg["src"]], 9)
    out = WORK / f"amb_{seg['id']}.wav"
    subprocess.run([
        "ffmpeg", "-v", "error", "-y", "-ss", str(a), "-t", str(b - a),
        "-i", str(PROJ / "footage" / "raw" / f"{seg['src']}.mov"),
        "-af", f"atempo={speed:.5f},highpass=f=110,volume={gain}dB,"
               f"afade=t=in:d=0.02,afade=t=out:st={seg['dur'] - 0.03}:d=0.03",
        "-ar", str(SR), "-ac", "2", "-c:a", "pcm_f32le", str(out)], check=True)
    _, x = wavfile.read(out)
    x = x[:n]
    return np.pad(x, ((0, n - len(x)), (0, 0)))


def automation(points):
    """Piecewise-linear gain curve in dB → linear, points = [(t, dB), ...]."""
    t = np.arange(N) / SR
    ts, db = zip(*points)
    return 10 ** (np.interp(t, ts, db) / 20)


def main():
    tl, total = timeline()
    amb = np.zeros((N, 2))
    for t0, seg in tl:
        x = seg_audio(seg)
        i = round(t0 * SR)
        amb[i:i + len(x)] += x[: N - i]

    _, music = wavfile.read(AUD / "music.wav")
    _, sfx = wavfile.read(AUD / "sfx.wav")

    # production sound sits under the score, comes forward in the quiet moments
    amb_gain = automation([
        (0, -9), (2.8, -9), (3.0, -14), (8.4, -14), (8.6, -6), (9.7, -6), (9.75, -40),
        (10.0, -40), (10.05, -13), (14.4, -13), (14.6, -5), (17.2, -5), (17.25, -40),
        (17.5, -40), (17.55, -15), (22.9, -15), (23.0, -40), (30, -40)])
    amb *= amb_gain[:, None]

    mix = music * 0.82 + sfx * 0.55 + amb
    mix = np.nan_to_num(mix)
    raw = AUD / "mix_raw.wav"
    wavfile.write(raw, SR, (mix / np.abs(mix).max() * 0.7).astype(np.float32))
    wavfile.write(AUD / "production_sound.wav", SR, amb.astype(np.float32))

    # two-pass loudness normalisation to -14 LUFS / -1 dBTP
    meas = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(raw), "-af",
         "loudnorm=I=-14:TP=-1.0:LRA=11:print_format=json", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    import json
    j = json.loads(meas[meas.rindex("{"):meas.rindex("}") + 1])
    subprocess.run([
        "ffmpeg", "-v", "error", "-y", "-i", str(raw), "-af",
        f"loudnorm=I=-14:TP=-1.0:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:"
        f"measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:"
        f"offset={j['target_offset']}:linear=true,aresample=48000",
        "-c:a", "pcm_s24le", str(AUD / "mix.wav")], check=True)
    print("mix:", AUD / "mix.wav", "| input", j["input_i"], "LUFS")


if __name__ == "__main__":
    main()
