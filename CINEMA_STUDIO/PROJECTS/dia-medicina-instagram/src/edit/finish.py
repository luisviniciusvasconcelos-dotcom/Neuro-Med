"""Final pass: graded picture + light flashes on the musical hits + grain +
vignette + typography layer (Remotion, alpha) + mixed audio → deliverables.

Outputs
  renders/dia-medicina_16x9_4K_master_vNN.mp4   (3840x2160 H.264 high bitrate)
  renders/dia-medicina_16x9_1080p_vNN.mp4       (1920x1080 H.264, Instagram)
"""
import subprocess
import sys
from pathlib import Path

PROJ = Path(__file__).resolve().parents[2]
WORK = PROJ / "renders" / "work"
VER = sys.argv[1] if len(sys.argv) > 1 else "v01"

HITS = (3.0, 10.0, 17.5)  # exposure flash on the score's impacts
flash = "+".join(f"0.16*gte(t,{h})*exp(-(t-{h})*16)" for h in HITS)

graph = (
    f"[0:v]eq=brightness='{flash}':eval=frame,"
    "vignette=angle=0.42,"
    "noise=c0s=5:c0f=t+u:c1s=2:c1f=t+u:c2s=2:c2f=t+u[pic];"
    "[1:v]format=yuva444p10le[type];"
    "[pic][type]overlay=format=auto:shortest=1,format=yuv420p[v4k];"
    "[v4k]split[a][b];"
    "[b]scale=1920:1080:flags=lanczos[v1080];"
    # AAC overshoots a little: keep ~0.5 dB of true-peak headroom below -1 dBTP
    "[2:a]volume=-1dB,alimiter=limit=0.75:level=false:attack=1:release=50,asplit[a1][a2]"
)
master = PROJ / "renders" / f"dia-medicina_16x9_4K_master_{VER}.mp4"
insta = PROJ / "renders" / f"dia-medicina_16x9_1080p_{VER}.mp4"
common = ["-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
          "-r", "24", "-movflags", "+faststart"]
cmd = [
    "ffmpeg", "-v", "error", "-stats", "-y",
    "-i", str(WORK / "picture.mp4"),
    "-i", str(PROJ / "src" / "remotion" / "out" / "type.mov"),
    "-i", str(PROJ / "audio" / "mix.wav"),
    "-filter_complex", graph,
    "-map", "[a]", "-map", "[a1]",
    "-c:v", "libx264", "-preset", "slow", "-crf", "13", "-profile:v", "high",
    "-c:a", "aac", "-b:a", "320k", "-ar", "48000", *common, "-t", "30", str(master),
    "-map", "[v1080]", "-map", "[a2]",
    "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-profile:v", "high",
    "-maxrate", "25M", "-bufsize", "50M",
    "-c:a", "aac", "-b:a", "256k", "-ar", "48000", *common, "-t", "30", str(insta),
]
subprocess.run(cmd, check=True)
print(master)
print(insta)
