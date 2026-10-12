#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ghep cac clip tai tu Flow thanh 1 video dang bai (PRD muc 8, duong B - ghep offline).

Dung:
  python3 scripts/ghep.py <thu-muc-clip>                       # -> final.mp4 (+ final.srt)
  python3 scripts/ghep.py <thu-muc> --watermark "An Nhien 0900000000" --hook "Huong 75% BHXH"
  python3 scripts/ghep.py <thu-muc> --dry-run                  # in thu tu clip, diem cat, lenh ffmpeg
  python3 scripts/ghep.py <thu-muc> --no-trim                  # giu nguyen clip, chi noi + can am

Thu muc chua:
  *.mp4        clip cua Tool, ten co so thu tu o cuoi: DL_me-chong_1.mp4 ... DL_me-chong_4.mp4.
               Sap theo so CUOI CUNG trong ten file.
  thoai.txt    (tuy chon; hoac lời-kể.txt / loi-ke.txt) khoi THOAI cua bang dang bai S8:
               moi dong 1 clip, dung thu tu. Trong 1 dong, nhieu cau thoai cach nhau " | ",
               moi cau co the co ten nguoi noi: "MẸ CHỒNG: Cô ký đi. | CON DÂU: Con ký."
               Co file nay thi xuat them final.srt (bo ten nguoi noi, tru khi --srt-speaker).

Moi clip: tim luc giong bat dau / ket thuc (ffmpeg silencedetect, dung lai measure-speech.py),
cat bot khoang lang thua o dau va duoi, dua ve cung kich thuoc, noi lai, can am -14 LUFS.
Neu co --watermark / --hook: ve chu thanh PNG trong suot (Pillow) roi overlay len video.
Ban ffmpeg pho bien tren macOS (Homebrew) khong co drawtext, nen khong dung drawtext.

Bien moi truong: GHEP_PAD_HEAD (0.20s), GHEP_PAD_TAIL (0.45s), GHEP_LUFS (-14),
R3_NOISE_DB / R3_MIN_SIL (nguong im lang, xem measure-speech.py).
"""
import argparse, glob, importlib.util, json, os, re, subprocess, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAD_HEAD = float(os.environ.get("GHEP_PAD_HEAD", "0.20"))
PAD_TAIL = float(os.environ.get("GHEP_PAD_TAIL", "0.45"))
LUFS = float(os.environ.get("GHEP_LUFS", "-14"))
SRT_MAX_WORDS = 10          # video doc 9:16: dong phu de ngan hon ban ngang
SPEAKER = re.compile(r"^\s*([A-ZÀ-Ỹa-zà-ỹĐđ][\wÀ-Ỹà-ỹĐđ .'-]{0,24}?)\s*:\s+(.+)$")

FONT_CANDIDATES = [
    os.path.join(ROOT, "assets", "fonts", "BeVietnamPro-ExtraBold.ttf"),
    os.path.join(ROOT, "assets", "fonts", "BeVietnamPro-Bold.ttf"),
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]

def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, "scripts", file))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod

ms = _load("measure_speech", "measure-speech.py")      # duration(), silences()

# ---------------------------------------------------------------- thoai

def normalize(s):
    s = unicodedata.normalize("NFC", s)
    s = re.sub(r"[\u200b-\u200d\ufeff]", "", s)
    return re.sub(r"\s+", " ", s).strip()

def segments(line):
    """'A: cau 1 | B: cau 2' -> [('A', 'cau 1'), ('B', 'cau 2')]; khong co ten -> ('', cau)."""
    out = []
    for part in line.split(" | "):
        part = normalize(part).strip('"“”').strip()
        if not part:
            continue
        m = SPEAKER.match(part)
        who, text = (m.group(1).strip(), m.group(2).strip()) if m else ("", part)
        out.append((who, text.strip('"“”').strip()))
    return out

def syllables(line):
    return sum(len(text.split()) for _who, text in segments(line))

# ---------------------------------------------------------------- doc dau vao

def order_key(path):
    nums = re.findall(r"\d+", os.path.splitext(os.path.basename(path))[0])
    return (int(nums[-1]) if nums else 10**9, os.path.basename(path))

def find_clips(folder):
    clips = [f for f in glob.glob(os.path.join(folder, "*.mp4"))
             if not os.path.basename(f).startswith("final")]
    return sorted(clips, key=order_key)

def read_lines(folder):
    for name in ("thoai.txt", "thoại.txt", "lời-kể.txt", "loi-ke.txt"):
        path = os.path.join(folder, name)
        if os.path.exists(path):
            rows = []
            for raw in open(path, encoding="utf-8"):
                s = re.sub(r"^\s*(\d+\s*[.):|]|-|\*)\s*", "", raw.strip())   # bo "1." / "1 |" / "- "
                s = normalize(s)
                if s:
                    rows.append(s)
            return path, rows
    return None, []

def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                          "stream=codec_type,width,height,r_frame_rate", "-of", "json", path],
                         capture_output=True, text=True).stdout
    streams = json.loads(out or "{}").get("streams", [])
    v = next((s for s in streams if s.get("codec_type") == "video"), {})
    return dict(w=v.get("width"), h=v.get("height"), fps=v.get("r_frame_rate", "30/1"),
                has_audio=any(s.get("codec_type") == "audio" for s in streams))

def cut_points(path, trim):
    """(dau cat, cuoi cat, giong bat dau, giong ket thuc, do dai)."""
    dur = ms.duration(path)
    sil = ms.silences(path, dur)
    start = sil[0][1] if sil and sil[0][0] <= 0.05 else 0.0
    end = sil[-1][0] if sil and abs(dur - sil[-1][1]) <= 0.05 else dur
    if end <= start:                        # clip im lang hoan toan
        start, end = 0.0, dur
    if not trim:
        return 0.0, dur, start, end, dur
    return max(0.0, start - PAD_HEAD), min(dur, end + PAD_TAIL), start, end, dur

def target_size(arg, info):
    if arg and arg != "auto":
        w, h = arg.lower().split("x")
        return int(w), int(h)
    w, h = info[0]["w"], info[0]["h"]
    return (1080, 1920) if h > w else (1920, 1080)

# ---------------------------------------------------------------- lop chu (Pillow)

def find_font(path):
    for p in ([path] if path else []) + FONT_CANDIDATES:
        if p and os.path.exists(p):
            return p
    sys.exit("Khong tim thay font co dau tieng Viet. Dat file .ttf vao assets/fonts/ "
             "hoac truyen --font <duong-dan.ttf>.")

def _pil():
    try:
        from PIL import Image, ImageDraw, ImageFont
        return Image, ImageDraw, ImageFont
    except ImportError:
        sys.exit("Can Pillow de ve watermark/hook: pip3 install -r requirements.txt")

def _wrap(draw, font, text, max_w, stroke):
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = f"{cur} {w}".strip()
        if draw.textlength(test, font=font) + 2 * stroke <= max_w or not cur:
            cur = test
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines

def _fit(draw, ImageFont, font_path, text, max_w, size, max_lines, stroke_ratio):
    while size > 14:
        font = ImageFont.truetype(font_path, size)
        stroke = max(2, int(size * stroke_ratio))
        lines = _wrap(draw, font, text, max_w, stroke)
        if len(lines) <= max_lines and all(
                draw.textlength(l, font=font) + 2 * stroke <= max_w for l in lines):
            return font, stroke, lines
        size -= 2
    font = ImageFont.truetype(font_path, size)
    return font, 2, _wrap(draw, font, text, max_w, 2)

def render_watermark(text, W, H, font_path, out, y_ratio=0.56, opacity=0.38):
    """Chu trang mo giua khung (giong 'Viet Ha 0964497135' trong sample)."""
    Image, ImageDraw, ImageFont = _pil()
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    font, _s, lines = _fit(d, ImageFont, font_path, text, int(W * 0.84), int(W * 0.052), 1, 0)
    line = lines[0]
    x = (W - d.textlength(line, font=font)) / 2
    y = int(H * y_ratio)
    a = int(255 * opacity)
    d.text((x + 2, y + 2), line, font=font, fill=(0, 0, 0, int(a * 0.5)))
    d.text((x, y), line, font=font, fill=(255, 255, 255, a))
    img.save(out)

def render_hook(text, W, H, font_path, out, y_ratio=0.74):
    """Sticker hook chu vang, vien do sam + vien trang ngoai (giong sample 2)."""
    Image, ImageDraw, ImageFont = _pil()
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    font, stroke, lines = _fit(d, ImageFont, font_path, text, int(W * 0.86),
                               int(W * 0.085), 2, 0.10)
    if len(lines) == 2:                     # chia 2 dong dai deu nhau, khong de 1-2 chu le
        words = text.split()
        k = min(range(1, len(words)), key=lambda k: max(
            d.textlength(" ".join(words[:k]), font=font),
            d.textlength(" ".join(words[k:]), font=font)))
        lines = [" ".join(words[:k]), " ".join(words[k:])]
    asc, desc = font.getmetrics()
    lh = asc + desc + stroke * 2
    y = int(H * y_ratio) - lh * len(lines) // 2
    for line in lines:
        x = (W - d.textlength(line, font=font)) / 2
        d.text((x, y), line, font=font, fill=(255, 255, 255, 255),
               stroke_width=stroke * 2, stroke_fill=(255, 255, 255, 255))
        d.text((x, y), line, font=font, fill=(255, 222, 41, 255),
               stroke_width=stroke, stroke_fill=(150, 18, 18, 255))
        y += lh
    img.save(out)

# ---------------------------------------------------------------- ffmpeg

def build_cmd(clips, cuts, info, out, size, wm_png=None, hook_png=None, hook_dur=1.6):
    W, H = size
    fps = info[0]["fps"]
    cmd, fc, pairs = ["ffmpeg", "-v", "error", "-y"], [], []
    for c in clips:
        cmd += ["-i", c]
    n_in = len(clips)
    silent = {}
    for i, inf in enumerate(info):          # clip khong co am thanh: chen im lang
        if not inf["has_audio"]:
            silent[i] = n_in; n_in += 1
            cmd += ["-f", "lavfi", "-t", f"{cuts[i][4]:.3f}", "-i", "anullsrc=r=48000:cl=stereo"]
    wm_idx = hook_idx = None
    if wm_png:
        wm_idx = n_in; n_in += 1
        cmd += ["-loop", "1", "-i", wm_png]
    if hook_png:
        hook_idx = n_in; n_in += 1
        cmd += ["-loop", "1", "-t", f"{hook_dur:.2f}", "-i", hook_png]
    for i, (a, b, *_rest) in enumerate(cuts):
        ain = f"{silent.get(i, i)}:a"
        fc.append(f"[{i}:v]trim={a:.3f}:{b:.3f},setpts=PTS-STARTPTS,"
                  f"scale={W}:{H}:force_original_aspect_ratio=decrease,"
                  f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps={fps}[v{i}]")
        fc.append(f"[{ain}]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,"
                  f"aresample=48000,aformat=channel_layouts=stereo[a{i}]")
        pairs.append(f"[v{i}][a{i}]")
    fc.append(f"{''.join(pairs)}concat=n={len(clips)}:v=1:a=1[vc][cat]")
    vlast = "vc"
    if wm_idx is not None:
        fc.append(f"[{wm_idx}:v]format=rgba[wm];[{vlast}][wm]overlay=0:0:shortest=1[vw]")
        vlast = "vw"
    if hook_idx is not None:
        fo = max(0.0, hook_dur - 0.25)
        fc.append(f"[{hook_idx}:v]format=rgba,fade=t=in:st=0:d=0.15:alpha=1,"
                  f"fade=t=out:st={fo:.2f}:d=0.25:alpha=1[hk];"
                  f"[{vlast}][hk]overlay=0:0:eof_action=pass[vh]")
        vlast = "vh"
    fc.append(f"[{vlast}]format=yuv420p[v]")
    fc.append(f"[cat]loudnorm=I={LUFS}:TP=-1.5:LRA=11,aresample=48000[a]")
    cmd += ["-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]",
            "-c:v", "libx264", "-crf", "19", "-preset", "medium",
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out]
    return cmd

def loudness(path):
    p = subprocess.run(["ffmpeg", "-i", path, "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", p.stderr)
    return float(m[-1]) if m else None

# ---------------------------------------------------------------- phu de

def ts(t):
    ms_ = int(round(t * 1000))
    return f"{ms_ // 3600000:02d}:{ms_ // 60000 % 60:02d}:{ms_ // 1000 % 60:02d},{ms_ % 1000:03d}"

def chunks(line):
    """Tach cau dai thanh cac cum <= SRT_MAX_WORDS: cat o dau cau, cau dai thi chia deu,
    uu tien diem cat ngay sau dau phay gan diem chia."""
    out = []
    for sent in re.split(r"(?<=[.!?…])\s+", line):
        words = sent.split()
        while len(words) > SRT_MAX_WORDS:
            parts = -(-len(words) // SRT_MAX_WORDS)
            n = -(-len(words) // parts)
            commas = [k + 1 for k, w in enumerate(words[:SRT_MAX_WORDS]) if w.endswith(",")]
            near = [k for k in commas if abs(k - n) <= 3]
            n = min(near, key=lambda k: abs(k - n)) if near else n
            out.append(" ".join(words[:n])); words = words[n:]
        if words:
            out.append(" ".join(words))
    return out

def write_srt(lines, cuts, path, with_speaker=False):
    cues, offset = [], 0.0
    for line, (a, b, start, end, _dur) in zip(lines, cuts):
        s0, s1 = offset + (start - a), offset + (min(end, b) - a)
        parts = []
        for who, text in segments(line):
            for k, p in enumerate(chunks(text)):
                parts.append(f"{who}: {p}" if with_speaker and who and k == 0 else p)
        total = sum(len(p.split()) for p in parts) or 1
        t = s0
        for p in parts:                     # chia thoi gian theo so tieng
            d = (s1 - s0) * len(p.split()) / total
            cues.append((t, t + d, p)); t += d
        offset += b - a
    with open(path, "w", encoding="utf-8") as f:
        for n, (a, b, text) in enumerate(cues, 1):
            f.write(f"{n}\n{ts(a)} --> {ts(b)}\n{text}\n\n")
    return len(cues)

# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description="Ghep clip Flow thanh final.mp4 (+ final.srt)")
    ap.add_argument("folder")
    ap.add_argument("--out", help="mac dinh <folder>/final.mp4")
    ap.add_argument("--no-trim", action="store_true", help="khong cat khoang lang dau/duoi clip")
    ap.add_argument("--dry-run", action="store_true", help="in ke hoach + lenh ffmpeg, khong ghep")
    ap.add_argument("--size", default="auto", help="WxH dau ra; auto = 1080x1920 (doc) / 1920x1080")
    ap.add_argument("--watermark", help='chu mo giua khung, vd "An Nhiên 0900000000"')
    ap.add_argument("--hook", help='sticker hook o dau video, vd "Hưởng 75% BHXH"')
    ap.add_argument("--hook-dur", type=float, default=1.6, help="so giay hien hook (1.6)")
    ap.add_argument("--font", help="file .ttf co dau tieng Viet (mac dinh: assets/fonts, Arial Bold)")
    ap.add_argument("--srt-speaker", action="store_true", help="giu ten nguoi noi trong .srt")
    a = ap.parse_args()

    clips = find_clips(a.folder)
    if len(clips) < 1:
        sys.exit(f"Khong co file .mp4 nao trong {a.folder}.")
    out = a.out or os.path.join(a.folder, "final.mp4")
    lines_path, lines = read_lines(a.folder)
    if lines and len(lines) != len(clips):
        print(f"!! {os.path.basename(lines_path)} co {len(lines)} dong nhung co {len(clips)} clip "
              f"-> bo qua phu de.")
        lines = []

    info = [probe(c) for c in clips]
    cuts = [cut_points(c, not a.no_trim) for c in clips]
    size = target_size(a.size, info)

    print(f"{'#':>2}  {'clip':<28}{'dai':>7}{'giong (s)':>14}{'cat (s)':>14}{'giu':>8}"
          + ("  tieng" if lines else ""))
    total = 0.0
    for i, (c, (s, e, vs, ve, d)) in enumerate(zip(clips, cuts)):
        total += e - s
        extra = f"  {syllables(lines[i]):>5}" if lines else ""
        note = "" if info[i]["has_audio"] else "  (KHONG CO AM THANH)"
        if info[i]["has_audio"] and d - ve < 0.25:
            note += "  (giong sat cuoi clip: de cut chu)"
        print(f"{i + 1:>2}  {os.path.basename(c)[:27]:<28}{d:>6.2f}s{vs:>8.2f}-{ve:<5.2f}"
              f"{s:>8.2f}-{e:<5.2f}{e - s:>7.2f}s{extra}{note}")
    print(f"Tong: {total:.2f}s · {size[0]}x{size[1]} · can am {LUFS:g} LUFS · "
          f"dem dau {PAD_HEAD}s / duoi {PAD_TAIL}s")

    wm_png = hook_png = None
    if a.watermark or a.hook:
        font = find_font(a.font)
        print(f"Font: {font}")
        base = os.path.splitext(out)[0]
        if a.watermark:
            wm_png = base + "_watermark.png"
            if not a.dry_run:
                render_watermark(normalize(a.watermark), *size, font, wm_png)
        if a.hook:
            hook_png = base + "_hook.png"
            if not a.dry_run:
                render_hook(normalize(a.hook), *size, font, hook_png)

    cmd = build_cmd(clips, cuts, info, out, size, wm_png, hook_png, a.hook_dur)
    if a.dry_run:
        print("\n" + " ".join(f"'{x}'" if " " in x or ";" in x else x for x in cmd))
        return
    subprocess.run(cmd, check=True)
    lu = loudness(out)
    print(f"\nDa ghi {out}: {ms.duration(out):.2f}s · {lu if lu is None else f'{lu:.1f}'} LUFS")
    if lines:
        srt = os.path.splitext(out)[0] + ".srt"
        print(f"Da ghi {srt}: {write_srt(lines, cuts, srt, a.srt_speaker)} cau phu de")
    else:
        print("Khong co thoai.txt -> khong xuat .srt")

if __name__ == "__main__":
    main()
