# S8 — Bảng đăng bài (agent, 0 credit) · Ghép & xuất

**Input:** `BRIEF`, `{kenh}`, thoại cuối cùng của N thẻ (`LINE_i`), `{phan}` · **Output:** mục 1–4 của `PUBLISH_SHEET`
**Chạy khi:** mở màn "Ghép & xuất". Luôn lấy thoại trên thẻ, vì thoại có thể đã bị sửa.
**Khối THOAI do code ghép**, không qua agent: N dòng `LINE_i`, giống file `thoai.txt` của `scripts/ghep.py`.

```
Write the publishing sheet for this finished Vietnamese "đạo lý" video of the channel
"{kenh}". Write in Vietnamese.

BRIEF:
{BRIEF}
Part: {phan}
FINAL DIALOGUE (one row per clip):
{LINES}

OUTPUT these sections, in this order, nothing else:

## 1. Tiêu đề
3 title options, ≤ 70 characters each, emotional but honest (no fake news, no real
names). If the story continues, end with "(Phần {phan})".

## 2. Chữ hook
3 options for the yellow sticker shown in the first 1.5 seconds, ≤ 7 words each. The first
one = HOOK CHỮ of the BRIEF.

## 3. Caption
2–3 sentences that end with a question to the viewer (to get comments), then 6–10
hashtags without diacritics (#daoly #giadinh #mechongnangdau ...).

## 4. Bình luận ghim
One short comment the channel pins: asks the viewer's opinion or announces the next part.
```

## Ghép & xuất (màn 4)

**Trong Tool:**
1. Ghép N clip bằng ffmpeg.wasm theo thứ tự thẻ, giữ tiếng từng clip. Cắt khoảng lặng thừa đầu và cuối clip: giữ 0.2s ở đầu, 0.45s ở cuối.
2. Lớp chữ vẽ bằng canvas, font Be Vietnam Pro ExtraBold, có đủ bảng chữ tiếng Việt (như auto-ns Phần 0n/0p):
   - **Watermark:** chữ watermark của kênh, trắng mờ ~38%, giữa khung, ở ~56% chiều cao, suốt video.
   - **Hook:** chữ hook đã chọn, vàng `#FFDE29`, viền đỏ sẫm, thêm viền trắng ngoài. Nằm ở ~74% chiều cao, hiện 0–1.6s, có fade.
   - **Phụ đề** (tuỳ chọn, mặc định tắt vì sample không có): dòng ≤ 10 từ, khớp giọng như auto-ns Phần 0i.
3. Xuất 1080×1920. Nút tải: MP4 (`<slug>.mp4`), thoại `.txt` (khối THOAI), phụ đề `.srt`. Mỗi mục S8 có nút "Sao chép".

**Nếu Tool không ghép được:** tải N clip và file thoại `.txt` về một thư mục, rồi chạy:

```bash
python3 scripts/ghep.py ~/Videos/dl/me-chong --dry-run
python3 scripts/ghep.py ~/Videos/dl/me-chong --watermark "An Nhiên 0900000000" --hook "Mẹ chồng ép ký đơn ly hôn"
```

Kết quả: `final.mp4` (1080×1920, -14 LUFS, có watermark và hook) và `final.srt`. Cần Pillow: `pip3 install -r requirements.txt`.

## Kiểm trước khi đăng

- [ ] Mỗi clip nói đủ thoại, đúng người, không cụt chữ cuối
- [ ] Không có nhạc, giọng lạ, chữ lạ do Veo sinh ra
- [ ] Mặt và quần áo mỗi nhân vật giống nhau ở mọi clip
- [ ] Giọng mỗi nhân vật giống nhau ở mọi clip
- [ ] Watermark và hook đúng chính tả
- [ ] Không có bạo lực, không tên người thật
