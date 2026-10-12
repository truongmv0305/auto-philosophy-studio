#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Do khach quan spike R-3: mot clip Veo/Omni thuc su chua bao nhieu tieng?

Dung: python3 scripts/measure-speech.py <thu-muc-clip>
Ten file phai chua so tieng da dat vao prompt, vd: r3_20.mp4, r3_24.mp4...

Script KHONG danh gia phat am (viec do can tai nguoi). No do:
  - luc giong doc bat dau / ket thuc
  - thoi gian phat am thuc
  - so tieng/giay THUC TE
  - khoang lang dau va duoi clip
va canh bao khi giong bi noi don hoac chay sat me clip (dau hieu cut chu).
"""
import re, subprocess, sys, os, glob

NOISE_DB = os.environ.get("R3_NOISE_DB", "-35")   # nguong coi la im lang
MIN_SIL  = os.environ.get("R3_MIN_SIL", "0.20")   # do dai im lang toi thieu

def duration(path):
    out = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
                          "-of","default=nw=1:nk=1", path],
                         capture_output=True, text=True).stdout.strip()
    return float(out)

def silences(path, dur):
    """Tra ve list cac doan im lang [(start, end), ...].

    ffmpeg phat silence_end ca o EOF, nen doan cuoi thuong da duoc ghep du.
    Neu file ket thuc giua mot doan im lang ma khong co silence_end, ta tu
    dong dong doan do lai o cuoi file.
    """
    p = subprocess.run(["ffmpeg","-i",path,"-af",
                        f"silencedetect=noise={NOISE_DB}dB:d={MIN_SIL}",
                        "-f","null","-"], capture_output=True, text=True)
    log = p.stderr
    starts = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", log)]
    ends   = [float(x) for x in re.findall(r"silence_end: (-?[\d.]+)", log)]
    if len(ends) < len(starts):
        ends = ends + [dur]
    return list(zip(starts, ends))

def analyse(path, declared):
    dur = duration(path)
    sil = silences(path, dur)
    # Giong bat dau: neu doan im lang dau tien khoi dau ~0 thi giong bat dau o
    # cuoi doan do; nguoc lai giong vao ngay tu giay 0.
    speech_start = sil[0][1] if sil and sil[0][0] <= 0.05 else 0.0
    # Giong ket thuc: neu doan im lang cuoi keo den het clip thi giong ket thuc
    # o dau doan do; nguoc lai giong chay den het clip.
    speech_end = sil[-1][0] if sil and abs(dur - sil[-1][1]) <= 0.05 else dur
    if speech_end <= speech_start:          # clip im lang hoan toan
        speech_start, speech_end = 0.0, dur
    speech = max(speech_end - speech_start, 0.001)
    rate = declared / speech
    lead, trail = speech_start, dur - speech_end
    flags = []
    if trail < 0.40: flags.append("CUT-OFF-RISK (duoi clip <0.4s lang)")
    if rate > 4.2:   flags.append(f"NOI DON ({rate:.2f} tieng/s > 4.2)")
    if rate < 2.8:   flags.append(f"DOC QUA CHAM ({rate:.2f} tieng/s < 2.8)")
    if trail > 1.60: flags.append("THUA CHO (duoi clip >1.6s lang - nen them tieng)")
    return dict(file=os.path.basename(path), declared=declared, dur=dur,
                lead=lead, speech=speech, trail=trail, rate=rate, flags=flags)

def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    files = sorted(glob.glob(os.path.join(sys.argv[1], "*.mp4")) +
                   glob.glob(os.path.join(sys.argv[1], "*.wav")) +
                   glob.glob(os.path.join(sys.argv[1], "*.m4a")))
    if not files:
        sys.exit(f"Khong thay file .mp4/.wav/.m4a nao trong {sys.argv[1]}")
    rows = []
    for f in files:
        base = os.path.basename(f)
        # So tieng = so sau dau gach duoi, vd r3_24.mp4 -> 24. Tranh bat nham
        # so "3" trong tien to "r3_".
        m = re.search(r"_(\d+)", base) or re.search(r"(\d+)(?!.*\d)", base)
        if not m:
            print(f"BO QUA {f} (ten file khong co so tieng)"); continue
        rows.append(analyse(f, int(m.group(1))))

    print(f"\nnguong im lang: {NOISE_DB} dB | im lang toi thieu: {MIN_SIL}s\n")
    print(f"{'file':<16}{'tieng':>6}{'clip':>8}{'lang dau':>10}{'phat am':>9}{'lang duoi':>11}{'tieng/s':>9}")
    print("-"*72)
    for r in rows:
        print(f"{r['file']:<16}{r['declared']:>6}{r['dur']:>7.2f}s{r['lead']:>9.2f}s"
              f"{r['speech']:>8.2f}s{r['trail']:>10.2f}s{r['rate']:>9.2f}")
    print()
    for r in rows:
        for fl in r["flags"]:
            print(f"  [{r['declared']} tieng] {fl}")

    good = [r for r in rows if not r["flags"]]
    print("\n=== KET LUAN ===")
    if good:
        lo, hi = min(r["declared"] for r in good), max(r["declared"] for r in good)
        print(f"Budget do duoc: {lo}-{hi} tieng/clip")
        print(f"So sanh PRD 6.2 (22-26): "
              + ("KHOP - khong can sua" if lo >= 22 and hi <= 26 + 2
                 else "LECH - phai cap nhat muc 6.2 va bang 6.4 cua PRD"))
    else:
        print("Khong co muc tieng nao dat. Xem canh bao o tren; rat co the phai")
        print("recalibrate toan bo muc 6 cua PRD (xem fallback cua R-3).")

if __name__ == "__main__":
    main()
