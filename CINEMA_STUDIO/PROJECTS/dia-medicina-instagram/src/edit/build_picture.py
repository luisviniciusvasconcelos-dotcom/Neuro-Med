"""Render each EDL segment (cut, speed, grade, layout, push-in) to a 4K
intermediate, then concatenate into the graded picture track.

usage: python3 build_picture.py [segment_id ...]
"""
import subprocess
import sys
from pathlib import Path

from edl import BASE_GRADE, FPS, H, PRE, SEGMENTS, W

PROJ = Path(__file__).resolve().parents[2]
RAW = PROJ / "footage" / "raw"
PHOTOS = PROJ / "footage" / "photos"
WORK = PROJ / "renders" / "work"
WORK.mkdir(parents=True, exist_ok=True)


def src_path(name):
    return PHOTOS / f"{name}.jpg" if name.startswith("foto") else RAW / f"{name}.mov"


def layout_chain(layout):
    cover = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"
    if layout == "fill":
        return f"[g]{cover}[l]"
    # portrait: sharp frame over a blurred, darkened copy of itself
    x = "(W-w)/2" if layout == "portrait" else "W*0.665-w/2"
    return (
        f"[g]split[bg][fg];"
        f"[bg]{cover},gblur=sigma=70,eq=brightness=-0.11:saturation=0.75[bgb];"
        f"[fg]scale=-2:{H}[fgs];"
        f"[bgb][fgs]overlay=x='{x}':y=0[l]"
    )


def build(seg):
    name, dur = seg["src"], seg["dur"]
    frames = round(dur * FPS)
    out = WORK / f"{seg['id']}.mp4"
    photo = name.startswith("foto")
    cmd = ["ffmpeg", "-v", "error", "-y"]
    if photo:
        cmd += ["-loop", "1", "-framerate", str(FPS), "-t", f"{dur + 0.5}", "-i", str(src_path(name))]
        timing = "setpts=PTS-STARTPTS"
    else:
        a, b = seg["a"], seg["b"]
        cmd += ["-ss", f"{a}", "-t", f"{b - a + 0.25}", "-i", str(src_path(name))]
        f = dur / (b - a)
        timing = f"setpts=(PTS-STARTPTS)*{f:.5f}"
        if seg.get("interp"):
            timing += f",minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1"
        else:
            timing += f",fps={FPS}"

    z = seg.get("zoom", 0)
    zoom = (
        f"scale=w='2*trunc({W}*(1+{z}*t/{dur})/2)':h=-2:eval=frame:flags=lanczos,"
        f"crop={W}:{H}"
    )
    fades = []
    if seg.get("fade_in"):
        fades.append(f"fade=t=in:st=0:d={seg['fade_in']}")
    if seg.get("fade_out"):
        fades.append(f"fade=t=out:st={dur - seg['fade_out']}:d={seg['fade_out']}")
    tail = ",".join([zoom, *fades, "format=yuv420p"])

    graph = (
        f"[0:v]{timing},{PRE.get(name, 'null')},{BASE_GRADE}[g];"
        f"{layout_chain(seg.get('layout', 'fill'))};"
        f"[l]{tail}[v]"
    )
    cmd += [
        "-filter_complex", graph, "-map", "[v]", "-frames:v", str(frames), "-an",
        "-c:v", "libx264", "-preset", "medium", "-crf", "13",
        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
        "-r", str(FPS), str(out),
    ]
    subprocess.run(cmd, check=True)
    n = subprocess.run(
        ["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v",
         "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(out)],
        capture_output=True, text=True, check=True).stdout.strip()
    assert int(n) == frames, f"{seg['id']}: {n} frames, expected {frames}"
    print(f"{seg['id']} ok  {frames} frames", flush=True)
    return out


def concat():
    lst = WORK / "concat.txt"
    lst.write_text("".join(f"file '{WORK / (s['id'] + '.mp4')}'\n" for s in SEGMENTS))
    out = WORK / "picture.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
                    "-c", "copy", str(out)], check=True)
    print("picture:", out)


if __name__ == "__main__":
    wanted = set(sys.argv[1:])
    for s in SEGMENTS:
        if not wanted or s["id"] in wanted:
            build(s)
    if not wanted:
        concat()
