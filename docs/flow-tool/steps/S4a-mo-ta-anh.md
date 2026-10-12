# S4a — Mô tả ảnh tải lên (agent, 0 credit)

**Chạy khi:** người dùng tải ảnh MC hoặc diễn viên lên ở màn "Kênh", trong khi các ô "Thông tin" vẫn là mặc định hoặc đang trống.
**Input:** ảnh `UPLOAD_<code>` (gửi kèm `Flow.generate.text` nếu SDK nhận ảnh), `{vai}` · **Output:** 4 trường để điền vào panel người
**Chưa biết:** `Flow.generate.text` có nhận ảnh không. Spike F‑Cg sẽ trả lời. Không nhận thì bỏ bước này; người dùng tự điền Ngoại hình và Trang phục.

Lý do cần bước này: prompt ảnh cảnh và prompt video chép `CHAR_LOCK` nguyên văn. Nếu mô tả bằng chữ khác với ảnh (ảnh tóc ngắn, chữ ghi tóc dài), Nano Banana và Veo sẽ kéo nhân vật lệch khỏi ảnh. Vì vậy mô tả phải lấy từ chính ảnh.

```
Describe the person in the attached photo so that an image model can keep them
consistent. Write in English. Describe only what is visible; do not guess identity,
name, nationality, profession, or anything private. Role in the story: {vai}.

OUTPUT exactly these 4 lines, nothing else:
GIỚI TÍNH: <Nam | Nữ>
TUỔI: <one number, apparent age>
NGOẠI HÌNH: <face shape, skin tone, hair length, style and colour, notable features such
  as glasses or a beard; 1 sentence, max 30 words>
TRANG PHỤC: <visible clothes with colours and patterns, accessories; 1 sentence, max 25
  words>
```

**Parse (code):** lấy 4 dòng theo nhãn rồi điền vào ô tương ứng. Ô "Giọng nói" không đổi, vì giọng không đoán được từ ảnh. Người dùng chọn giọng hoặc sửa mô tả giọng.
