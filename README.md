# Đạo Lý Studio (`DL-Studio`)

Tool trong Google Flow tạo video ngắn 9:16 cho kênh đạo lý tiếng Việt. Có hai dạng: **MC Đạo lý** (MC AI nói chuyện trong studio) và **Phim Drama AI** (2–4 nhân vật có thoại). Thoại do Veo 3 tự nói và nhép môi. Watermark và hook được chèn lúc xuất. Phong cách tham khảo `sample/`.

Kiến trúc giống `auto-ns-v3`: Tool dựng bằng mô tả trong ô Create Tool của Flow, kèm script Python để ghép offline.

| Đọc | Để |
|---|---|
| `docs/PRD.md` | hiểu sản phẩm, hai template, luồng bước, tiêu chí đạt |
| `docs/flow-tool/spike-tools.md` | **làm trước tiên:** thử 4 điều chưa biết trên Flow (F‑A…F‑E) |
| `docs/flow-tool/create-tool.md` | dựng Tool: Phần 1 các bước, Phần 2 mô tả dán vào Flow |
| `docs/flow-tool/steps/` | chỉ dẫn từng bước agent (S1…S8), cách ghép prompt (S6‑S7) |
| `docs/topic-bank.md` | kho chủ đề và kịch bản mẫu |

## Ghép offline

```bash
pip3 install -r requirements.txt        # Pillow, để vẽ watermark/hook
python3 scripts/ghep.py <thư-mục-clip> --dry-run
python3 scripts/ghep.py <thư-mục-clip> --watermark "Tên kênh 0900000000" --hook "Câu hook"
```

Thư mục chứa các clip `..._1.mp4 … _N.mp4` và `thoai.txt` (mỗi dòng một clip, dạng `MẸ_CHỒNG: … | CON_DÂU: …`). Script xuất `final.mp4` (1080×1920, -14 LUFS) và `final.srt`. Cần `ffmpeg`/`ffprobe` trong PATH.

`scripts/measure-speech.py <thư-mục>` đo tốc độ nói thực tế của clip; tên file phải chứa số tiếng, ví dụ `fa_28.mp4`.
