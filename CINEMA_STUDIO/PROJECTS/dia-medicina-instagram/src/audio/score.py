"""Original score + sound design for "29.10" — synthesised from scratch
(no samples, no third-party music), so the track is fully owned.

120 BPM, D minor, 30 s, structured on the edit:
  0.0  intro drone + reverse swell        → hit 3.0
  3.0  pulse (arrival)                    → breakdown 8.5, silence 9.75
 10.0  full groove (operating room)       → 14.5
 14.5  half-time heartbeat + ECG (slow-mo)→ riser, silence 17.25
 17.5  climax                             → 23.0 final impact
 23.0  outro bells over photos            → fade 30.0

Writes music.wav and sfx.wav (48 kHz stereo float) next to this file's
project in audio/.
"""
from pathlib import Path

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, fftconvolve, sawtooth, sosfilt

SR = 48000
DUR = 30.0
N = int(SR * DUR)
BEAT = 0.5
rng = np.random.default_rng(2910)
OUT = Path(__file__).resolve().parents[2] / "audio"
OUT.mkdir(exist_ok=True)

NOTE = {"G1": 49.00, "A1": 55.00, "Bb1": 58.27, "C2": 65.41, "D2": 73.42, "F2": 87.31,
        "G2": 98.00, "A2": 110.0, "Bb2": 116.54, "C3": 130.81, "Cs3": 138.59, "D3": 146.83,
        "E3": 164.81, "F3": 174.61, "G3": 196.0, "A3": 220.0, "Bb3": 233.08, "C4": 261.63,
        "D4": 293.66, "E4": 329.63, "F4": 349.23, "A4": 440.0, "C5": 523.25, "D5": 587.33,
        "E5": 659.26, "F5": 698.46, "A5": 880.0}


# ── helpers ─────────────────────────────────────────────────────────────
def t_(d):
    return np.arange(int(SR * d)) / SR


def lp(x, f, order=2):
    return sosfilt(butter(order, min(f, SR / 2 - 100), "low", fs=SR, output="sos"), x)


def hp(x, f, order=2):
    return sosfilt(butter(order, f, "high", fs=SR, output="sos"), x)


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], "band", fs=SR, output="sos"), x)


def sweep_lp(x, f0, f1, steps=40):
    """Time-varying low-pass by crossfading blocks (cheap filter sweep)."""
    out = np.zeros_like(x)
    edges = np.linspace(0, len(x), steps + 1).astype(int)
    for i in range(steps):
        f = f0 * (f1 / f0) ** (i / max(steps - 1, 1))
        a, b = edges[i], edges[i + 1]
        pad = min(2048, a)
        out[a:b] = lp(x[a - pad:b], f)[pad:]
    return out


def env(n, a=0.005, d=0.2, curve=4.0):
    t = np.arange(n) / SR
    e = np.exp(-t / d * (curve / 4))
    att = int(a * SR)
    if att:
        e[:att] *= np.linspace(0, 1, att)
    return e


def place(buf, sig, at, gain=1.0, pan=0.0):
    i = int(round(at * SR))
    if i >= N:
        return
    sig = sig[: N - i]
    if sig.ndim == 1:
        l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
        sig = np.stack([sig * l, sig * r], 1) * np.sqrt(2)
    buf[i:i + len(sig)] += sig * gain


def reverb(x, secs=2.2, damp=4000, mix=0.3):
    n = int(SR * secs)
    ir = np.stack([rng.standard_normal(n), rng.standard_normal(n)], 1)
    ir *= np.exp(-np.arange(n) / SR * 6.9 / secs)[:, None]
    ir = np.stack([lp(ir[:, 0], damp), lp(ir[:, 1], damp)], 1)
    ir /= np.sqrt((ir ** 2).sum(0))
    if x.ndim == 1:
        x = np.stack([x, x], 1)
    wet = np.stack([fftconvolve(x[:, c], ir[:, c])[: len(x)] for c in range(2)], 1)
    return x * (1 - mix) + wet * mix


def saw(f, d, detune=0.0):
    t = t_(d)
    return sawtooth(2 * np.pi * f * (1 + detune) * t + rng.uniform(0, 6.28))


# ── instruments ─────────────────────────────────────────────────────────
def kick(d=0.45, f0=150, f1=44):
    t = t_(d)
    f = f1 + (f0 - f1) * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * env(len(t), 0.001, 0.22)
    click = hp(rng.standard_normal(len(t)), 2500) * env(len(t), 0, 0.008)
    knock = np.sin(2 * np.pi * 210 * t) * env(len(t), 0.001, 0.03)
    return np.tanh(1.6 * (body + 0.55 * click + 0.45 * knock))


def snare(d=0.35):
    n = rng.standard_normal(int(SR * d))
    noise = bp(n, 1200, 7000) * env(len(n), 0.001, 0.12)
    tone = np.sin(2 * np.pi * 185 * t_(d)) * env(len(n), 0.001, 0.06)
    return 0.8 * noise + 0.5 * tone


def hat(d=0.08, open_=False):
    n = rng.standard_normal(int(SR * d))
    return hp(n, 7500) * env(len(n), 0, 0.09 if open_ else 0.022)


def tom(f=110, d=0.5):
    t = t_(d)
    f_ = f * (0.75 + 0.25 * np.exp(-t * 18))
    return np.sin(2 * np.pi * np.cumsum(f_) / SR) * env(len(t), 0.001, 0.25)


def bass_note(f, d):
    sub = np.sin(2 * np.pi * f * t_(d))
    grit = lp(saw(f, d) + saw(f, d, 0.004), 1600)
    upper = lp(saw(2 * f, d, 0.003), 2400)
    e = env(int(SR * d), 0.004, d * 0.8)
    return np.tanh(1.6 * (0.5 * sub + 0.55 * grit + 0.3 * upper)) * e


def pad(notes, d, cutoff=(500, 1800), att=0.6):
    x = sum(saw(NOTE[n] * m, d, dt) * g for n in notes for dt in (-0.006, 0.0, 0.007)
            for m, g in ((1, 1.0), (2, 0.6)))
    x = sweep_lp(x / (4.8 * len(notes)), cutoff[0] * 2.2, cutoff[1] * 2.2, steps=24)
    e = np.ones(len(x))
    a, r = int(att * SR), int(min(0.4, d / 3) * SR)
    e[:a] = np.linspace(0, 1, a) ** 2
    e[-r:] *= np.linspace(1, 0, r)
    return x * e


def braam(d=2.6, root="D2"):
    x = sum(saw(NOTE[n], d, dt) for n in (root, "A2", "D3") for dt in (-0.01, 0, 0.012))
    x = sweep_lp(np.tanh(x * 0.6), 300, 3800, steps=20)
    e = env(len(x), 0.02, 0.9)
    return x * e * 0.7


def impact(d=2.5):
    t = t_(d)
    f = 28 + 62 * np.exp(-t * 3.5)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), 0.002, 0.9)
    burst = lp(rng.standard_normal(len(t)), 2500) * env(len(t), 0.001, 0.12)
    return np.tanh(1.3 * (sub + 0.6 * burst))


def riser(d):
    t = t_(d)
    noise = rng.standard_normal(len(t))
    out = np.zeros(len(t))
    edges = np.linspace(0, len(t), 33).astype(int)
    for i in range(32):
        a, b = edges[i], edges[i + 1]
        c = 300 * (12000 / 300) ** (i / 31)
        out[a:b] = bp(noise[max(0, a - 2048):b], c * 0.7, min(c * 1.3, 23000))[-(b - a):]
    f = 110 * 2 ** (3 * (t / d) ** 2)
    tone = lp(sawtooth(2 * np.pi * np.cumsum(f) / SR), 3000) * 0.25
    return (out + tone) * (t / d) ** 2.2


def whoosh(d=0.45):
    t = t_(d)
    noise = rng.standard_normal(len(t))
    out = np.zeros(len(t))
    edges = np.linspace(0, len(t), 17).astype(int)
    for i in range(16):
        a, b = edges[i], edges[i + 1]
        c = 400 + 2600 * np.sin(np.pi * i / 15)
        out[a:b] = bp(noise[max(0, a - 1024):b], c * 0.6, c * 1.6)[-(b - a):]
    return out * np.sin(np.pi * t / d) ** 2


def shutter():
    n = int(SR * 0.09)
    x = hp(rng.standard_normal(n), 2500)
    e = np.zeros(n)
    for at in (0.0, 0.045):
        i = int(at * SR)
        e[i:i + int(0.012 * SR)] = np.exp(-np.arange(int(0.012 * SR)) / SR * 400)
    return x * e


def ecg_beep():
    t = t_(0.11)
    e = np.minimum(1, t / 0.004) * np.minimum(1, (0.11 - t) / 0.02)
    return np.sin(2 * np.pi * 980 * t) * e


def heartbeat():
    x = np.zeros(int(SR * 0.6))
    for at, g in ((0.0, 1.0), (0.22, 0.7)):
        k = kick(0.3, 90, 38) * g
        i = int(at * SR)
        x[i:i + len(k)] += k
    return lp(x, 180)


def pluck(f, d=0.25):
    n = int(SR * d)
    x = saw(f, d) + 0.5 * saw(2 * f, d, 0.002)
    return lp(x, 3800) * env(n, 0.002, 0.11) * 0.5


def bell(f, d=2.4):
    t = t_(d)
    x = (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 3)
         + 0.12 * np.sin(2 * np.pi * 3.01 * f * t) * np.exp(-t * 6))
    return x * env(len(t), 0.003, 0.8)


# ── arrangement ─────────────────────────────────────────────────────────
music = np.zeros((N, 2))
sfx = np.zeros((N, 2))
drums = np.zeros((N, 2))


def mute(buf, a, b, fade=0.03):
    i, j, f = int(a * SR), int(b * SR), int(fade * SR)
    buf[i - f:i] *= np.linspace(1, 0, f)[:, None]
    buf[i:j] = 0


# A — intro drone 0–3
place(music, pad(["D2", "A2", "F3"], 3.2, (250, 1400), att=0.4), 0.0, 0.55)
place(music, bell(NOTE["A5"], 3.0) * 0.3, 0.6, pan=0.4)
place(music, bell(NOTE["D5"], 3.0) * 0.26, 1.6, pan=-0.4)
swell = reverb(impact(1.4), 1.6, mix=0.7)[::-1] * np.linspace(0, 1, int(1.4 * SR))[:, None] ** 2
place(music, swell, 1.6, 0.6)

# chords per section (start, dur, chord, bass root)
B_CH = [(3.0, 2.0, ["D3", "F3", "A3"], "D2"), (5.0, 2.0, ["Bb2", "D3", "F3"], "Bb1"),
        (7.0, 1.5, ["C3", "E3", "G3"], "C2")]
D_CH = [(10.0, 2.0, ["D3", "F3", "A3"], "D2"), (12.0, 2.0, ["Bb2", "D3", "F3"], "Bb1"),
        (14.0, 0.5, ["F3", "A3", "C4"], "F2")]
F_CH = [(17.5, 1.5, ["D3", "F3", "A3"], "D2"), (19.0, 1.5, ["Bb2", "D3", "F3"], "Bb1"),
        (20.5, 1.0, ["G2", "Bb2", "D3"], "G1"), (21.5, 1.5, ["A2", "Cs3", "E3"], "A1")]


def bassline(chords, step, gain):
    for st, d, _, root in chords:
        k = 0
        while k * step < d - 1e-6:
            f = NOTE[root] * (2 if (k % 4 == 3) else 1)
            place(music, bass_note(f, step * 0.95), st + k * step, gain)
            k += 1


def pads(chords, gain, cutoff):
    for st, d, ch, _ in chords:
        place(music, pad(ch, d + 0.05, cutoff, att=0.08), st, gain)


def ostinato(chords, step, gain):
    for st, d, ch, _ in chords:
        f = [NOTE[n] for n in ch]
        pat = [f[0] * 2, f[2] * 2, f[0] * 4, f[1] * 2]
        k = 0
        while k * step < d - 1e-6:
            place(music, pluck(pat[k % 4]), st + k * step, gain, pan=(-0.3, 0.3)[k % 2])
            k += 1


# B — arrival pulse 3–8.5
ostinato(B_CH, BEAT / 2, 0.30)
pads(B_CH, 0.35, (700, 1500))
bassline(B_CH, BEAT / 2, 0.42)
for i in range(11):
    t = 3.0 + i * 0.5
    if i % 2 == 0 or t >= 5.0:
        place(drums, kick(), t, 0.85)
    if t >= 5.0:
        place(drums, hat(), t + 0.25, 0.32, pan=0.3)
    if t >= 7.0 and i % 2 == 1:
        place(drums, reverb(snare(), 1.0, mix=0.25), t, 0.7)

# C — breakdown 8.5–10: filtered pad + riser, silence 9.75
place(music, pad(["Bb2", "D3", "G3"], 1.3, (1500, 300), att=0.02), 8.5, 0.35)
place(music, bass_note(NOTE["G1"], 1.2), 8.5, 0.35)
place(sfx, riser(1.25), 8.5, 0.35)

# D — full groove 10–14.5
ostinato(D_CH, BEAT / 2, 0.34)
pads(D_CH, 0.38, (900, 2400))
bassline(D_CH, BEAT / 2, 0.45)
for i in range(9):
    t = 10.0 + i * 0.5
    place(drums, kick(), t, 0.9)
    place(drums, hat(), t + 0.25, 0.34, pan=0.3)
    if i % 2 == 1:
        place(drums, reverb(snare(), 1.0, mix=0.25), t, 0.8)
for k, f in enumerate((140, 120, 100, 85)):
    place(drums, tom(f), 13.5 + k * 0.125 + 0.5, 0.45, pan=-0.3 + 0.2 * k) if k < 4 else None

# E — slow motion 14.5–17.5: heartbeat + ECG + swelling pad
place(music, pad(["D3", "F3", "A3", "E4"], 3.0, (400, 2600), att=1.2), 14.5, 0.42)
for k in range(3):
    place(drums, heartbeat(), 14.5 + k * 1.0, 0.9)
    place(sfx, ecg_beep(), 14.5 + k * 1.0, 0.22, pan=0.25)
place(sfx, riser(1.4), 15.85, 0.5)

# F — climax 17.5–23
ostinato(F_CH, BEAT / 4, 0.32)
pads(F_CH, 0.42, (1200, 3200))
bassline(F_CH, BEAT / 4, 0.45)
for i in range(22):
    t = 17.5 + i * 0.25
    if i % 2 == 0:
        place(drums, kick(), t, 0.95)
    if i % 4 == 2:
        place(drums, reverb(snare(), 1.2, mix=0.3), t, 0.85)
    place(drums, hat(open_=(i % 4 == 3)), t, 0.28, pan=0.3)
for t in (19.0, 20.5, 21.5):
    place(drums, tom(95), t, 0.5, pan=-0.3)
for k in range(8):  # snare roll into the final hit
    place(drums, snare(), 22.0 + k * 0.0625 + 0.25, 0.2 + 0.05 * k)
for t, root in ((17.5, "D2"), (19.5, "D2"), (20.75, "G1")):
    place(music, reverb(braam(2.2, root), 2.5, mix=0.35), t, 0.55)

# G — final impact + outro 23–30
place(music, reverb(braam(5.5, "D2"), 3.5, mix=0.5), 23.0, 0.6)
arp = ["D4", "A4", "E5", "F5", "A4", "E5", "D5", "A4", "F4", "A4", "D5", "E5"]
for k, n in enumerate(arp):
    place(music, bell(NOTE[n] * 2, 2.6) * 0.45, 23.5 + k * 0.5, pan=(-0.35, 0.35)[k % 2])
place(music, pad(["D3", "A3", "E4", "F4"], 6.5, (900, 500), att=1.5), 23.5, 0.28)

# strategic silences before impacts
for a, b in ((9.75, 10.0), (17.25, 17.5)):
    mute(music, a, b)
    mute(drums, a, b)
    mute(sfx, a, b)

# ── sound design ────────────────────────────────────────────────────────
for t in (3.0, 10.0, 17.5, 23.0):  # impacts on section hits
    place(sfx, reverb(impact(), 2.5, mix=0.4), t, 0.55)
for t in (5.0, 7.0, 8.5, 12.0, 14.5, 19.5, 20.25, 20.75):  # whooshes into cuts
    place(sfx, whoosh(0.4), t - 0.28, 0.16, pan=rng.uniform(-0.5, 0.5))
for t in (19.0, 23.0, 24.0, 25.0):  # photo cuts: shutter
    place(sfx, shutter(), t - 0.02, 0.35)

# master bus for music (drums + music), gentle glue
mix = music + drums
mix = reverb(mix, 1.4, mix=0.12)
fade = np.ones(N)
f0 = int(28.6 * SR)
fade[f0:] = np.linspace(1, 0, N - f0) ** 1.5
mix *= fade[:, None]
sfx *= fade[:, None]


def write(name, x):
    x = x / max(1e-9, np.abs(x).max()) * 0.89
    wavfile.write(OUT / name, SR, x.astype(np.float32))
    print("wrote", OUT / name)


write("music.wav", mix)
write("sfx.wav", sfx)
