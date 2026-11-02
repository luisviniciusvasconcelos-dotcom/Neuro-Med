"""Edit decision list — "29.10 · Um dia de medicina" (16:9, 24 fps, 30 s).

Times are seconds on the output timeline; cuts land on the 120 BPM grid of the
original score (beat = 0.5 s). Source in/out points come from the analysis of
every clip (see brief/proposta.md).
"""

FPS = 24
W, H = 3840, 2160
BPM = 120

# Light, shared look applied after each clip's own correction.
BASE_GRADE = (
    "curves=master='0/0.025 0.22/0.18 0.5/0.5 0.8/0.83 1/0.965',"
    "colorbalance=rs=-0.04:bs=0.05:gs=0.01:rh=0.04:gh=0.01:bh=-0.04,"
    "eq=saturation=1.06"
)

# Per-source correction (exposure / white balance) before the shared look.
PRE = {
    "IMG_7123": "eq=saturation=0.95",
    "IMG_7126": "colortemperature=temperature=6200",
    "IMG_7128": "eq=saturation=0.95",
    "IMG_7129": "colortemperature=temperature=6200",
    "IMG_7136": "colortemperature=temperature=6300,eq=gamma=1.05",
    "IMG_7154": "colortemperature=temperature=6300",
    "IMG_7155": "colortemperature=temperature=5600,eq=gamma=1.06",
    "IMG_7164": "eq=gamma=1.25:brightness=0.02",
    "IMG_7167": "null",
    "IMG_7168": "eq=gamma=0.98",
    "IMG_7172": "curves=master='0/0 0.7/0.66 1/0.9'",
    "foto1": "eq=saturation=0.97",
    "foto2": "colortemperature=temperature=6800,eq=saturation=0.92",
    "foto3": "eq=saturation=0.95",
    "foto4": "colortemperature=temperature=6300",
}

# id, source, src_in, src_out (None for photos), out_dur, options
#   zoom: push-in amount over the segment (0.04 = 4 %)
#   layout: "fill" (cover 16:9), "portrait" (sharp centre over blurred self),
#           "portrait_right" (portrait shifted right, room for type on the left)
#   interp: motion-interpolate slow motion
SEGMENTS = [
    # ── Abertura ───────────────────────────────────────────── 0.0 – 3.0
    dict(id="s01", src="IMG_7123", a=0.00, b=3.00, dur=3.00, zoom=0.05, fade_in=0.35),
    # ── Chegada ────────────────────────────────────────────── 3.0 – 10.0
    dict(id="s02", src="IMG_7126", a=0.05, b=2.05, dur=2.00, zoom=0.03),
    dict(id="s03", src="IMG_7128", a=0.70, b=2.70, dur=2.00, layout="portrait", zoom=0.03),
    dict(id="s04", src="IMG_7129", a=0.00, b=1.79, dur=1.50, zoom=0.06),
    dict(id="s05", src="IMG_7136", a=0.00, b=1.50, dur=1.50, zoom=0.03),
    # ── Centro cirúrgico ───────────────────────────────────── 10.0 – 17.5
    dict(id="s06", src="IMG_7154", a=1.00, b=2.00, dur=1.00, zoom=0.02),
    dict(id="s07", src="IMG_7154", a=2.00, b=2.50, dur=1.00, zoom=0.04, interp=True),
    dict(id="s08", src="IMG_7155", a=1.40, b=3.90, dur=2.50, zoom=0.05),
    dict(id="s09", src="IMG_7164", a=1.00, b=2.50, dur=3.00, zoom=0.06, interp=True),
    # ── Clímax (flashes curtos) ────────────────────────────── 17.5 – 23.0
    dict(id="s10", src="IMG_7167", a=0.00, b=1.00, dur=1.00, layout="portrait", zoom=0.03),
    dict(id="s11", src="IMG_7167", a=2.50, b=3.00, dur=0.50, layout="portrait", zoom=0.03),
    dict(id="s12", src="foto3", dur=0.50, layout="portrait", zoom=0.06),
    dict(id="s13", src="IMG_7168", a=0.40, b=1.15, dur=0.75, zoom=0.03),
    dict(id="s14", src="IMG_7168", a=4.00, b=4.50, dur=0.50, zoom=0.03),
    dict(id="s15", src="IMG_7172", a=0.00, b=2.25, dur=2.25, zoom=0.05),
    # ── Encerramento ───────────────────────────────────────── 23.0 – 30.0
    dict(id="s16", src="foto4", dur=1.00, zoom=0.04),
    dict(id="s17", src="foto2", dur=1.00, zoom=0.04),
    dict(id="s18", src="foto1", dur=5.00, layout="portrait_right", zoom=0.035, fade_out=1.2),
]

# Real capture times (file metadata) shown on screen, keyed by output time.
TIMESTAMPS = [
    (0.6, "12:21"), (3.0, "12:22"), (5.0, "12:53"), (7.0, "12:56"), (8.5, "13:14"),
    (10.0, "15:00"), (12.0, "15:03"), (14.5, "15:10"), (17.5, "17:11"),
    (19.5, "17:17"), (20.75, "17:28"),
]
TIMESTAMPS_END = 23.0  # timestamps hide when the photo epilogue starts


def timeline():
    t = 0.0
    out = []
    for s in SEGMENTS:
        out.append((t, s))
        t += s["dur"]
    return out, t


if __name__ == "__main__":
    tl, total = timeline()
    for t, s in tl:
        print(f"{t:6.2f}  {s['id']}  {s['src']:9s}  {s['dur']:.2f}s")
    print("total", total)
