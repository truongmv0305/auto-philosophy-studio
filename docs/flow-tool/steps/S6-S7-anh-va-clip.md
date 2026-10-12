# S6 — Ảnh (Nano Banana Pro) · S7 — Clip có thoại nhép môi

Hai bước sinh media này **không có agent**. Tool **ghép prompt bằng code** ngay lúc bấm nút, từ các khối:
- `DNA`, `SET_LOCK`, `HOST_FRAME`, `CHAR_LOCK`, `VOICE_LOCK` (S4 và hồ sơ kênh);
- `SCENE_i` (S5/S5b);
- **thoại hiện tại của thẻ i** (`CLIPS[i]`).

## Ký hiệu

```
ASPECT      = "9:16 vertical" | "16:9 horizontal"
LOCK(codes) = the CHAR_LOCK paragraphs of those codes, verbatim, joined by a space
VOICE(codes)= the VOICE_LOCK paragraphs of those codes, verbatim, one per line
POS(code)   = the short recognition phrase from the channel cast, e.g.
              "the older woman in the floral blouse"
NO_TEXT_IMG = "No captions, no subtitles, no watermark, no extra text."
```

## S6 — Ảnh

### Ảnh hồ sơ kênh (tạo 1 lần ở màn "Kênh", lưu `DL_{kenh}_...`)

```
STUDIO_IMG = "Photorealistic interior photo, " + ASPECT + ". " + SET_LOCK + " The desk and
  chair are empty: nobody is in the picture. The sign text must be spelled exactly as
  written, with correct Vietnamese diacritics. " + NO_TEXT_IMG

HOST_IN_STUDIO   (reference images: HOST_IMG, STUDIO_IMG)
  = "Photorealistic cinematic frame, " + ASPECT + ". Put the person of the first reference
  image into the studio of the second reference image, keeping the face, hair and clothes
  exactly. " + SET_LOCK + " " + HOST_FRAME + " " + NO_TEXT_IMG
```

### Ảnh tham chiếu người: MC (`HOST_IMG`) và diễn viên (`CHAR_IMG_<code>`)

Mỗi người có một trong ba nguồn ảnh, chọn ở panel người tại màn "Kênh":

| Nguồn | Ảnh tham chiếu | Prompt |
|---|---|---|
| AI tự tạo (mặc định) | sinh bằng Nano Banana Pro | `REF_FROM_TEXT` |
| Tải ảnh lên + Chuẩn hoá (mặc định khi tải) | sinh bằng Nano Banana Pro, tham chiếu `UPLOAD_<code>` | `REF_FROM_UPLOAD` |
| Tải ảnh lên, tắt Chuẩn hoá | chính `UPLOAD_<code>` | không có |

```
FRAMING(code) = code == "MC"
  ? "Medium shot from the waist up, sitting, hands relaxed on a desk edge, looking
     straight at the camera with a gentle smile."
  : "Full body from head to shoes, standing, facing the camera, neutral expression."

REF_FROM_TEXT(code) = "Photorealistic character reference photo, " + ASPECT + ", plain
  light-grey studio background, soft even light. " + LOCK([code]) + " " + FRAMING(code)
  + " Natural skin texture. " + NO_TEXT_IMG

REF_FROM_UPLOAD(code)   (reference image: UPLOAD_<code>)
  = "Photorealistic character reference photo, " + ASPECT + ", plain light-grey studio
  background, soft even light. The SAME person as in the reference photo: keep the face,
  facial features, skin tone, hairstyle and hair colour exactly; do not beautify or change
  age. " + LOCK([code]) + " " + FRAMING(code) + " Natural skin texture. " + NO_TEXT_IMG
```

Vì sao nên bật **Chuẩn hoá**: ảnh tải lên thường có nền rối, người khác lọt khung, ánh sáng xấu hoặc bị cắt nửa người. Những thứ đó lọt vào cảnh và clip. Ảnh chuẩn hoá giữ mặt nhưng có nền sạch, khung chuẩn.

Trang phục: `LOCK` lấy từ ô "Trang phục". Muốn giữ đúng bộ đồ trong ảnh thì để S4a điền ô này từ ảnh. Muốn thay đồ thì sửa ô này; ảnh chuẩn hoá vẫn giữ mặt.

**LOCK từ thông tin đã điền** (code, chỉ dựng lại khi người dùng chưa sửa tay ô "Mô tả gửi AI"):

```
CHAR_LOCK(code) = code + ": Vietnamese " + (Nữ ? "woman" : "man") + " about " + Tuổi + ", "
                  + Ngoại hình + ", " + Trang phục + "."
VOICE_LOCK(code) = code + ": " + Giọng nói + "."
```

Các ô Ngoại hình, Trang phục, Giọng nói ghi bằng tiếng Anh, giống các đoạn mẫu ở S4. Người dùng gõ tiếng Việt thì để nguyên; Nano Banana và Veo vẫn hiểu, nhưng tiếng Anh ổn định hơn.

### Ảnh theo tập

```
PLACE_IMG (T2) = "Photorealistic interior photo, " + ASPECT + ". " + DNA.PLACE + " "
  + DNA.LIGHT + " Nobody is in the picture. " + NO_TEXT_IMG

T1  SCENE_IMG_i (only when T1 runs in mode A2 "Frames"):
    reference = HOST_IN_STUDIO
    = "Photorealistic cinematic frame, " + ASPECT + ". Same woman, same studio, same
      framing as the reference image. " + HOST_FRAME + " Her pose: " + SCENE_i.START
      + " " + NO_TEXT_IMG

T2  SCENE_IMG_i:
    reference = CHAR_IMG of every code in WHO (max 3), then PLACE_IMG
    = "Photorealistic cinematic film still, " + ASPECT + ", 35mm, shallow depth of field. "
      + DNA.PLACE + " " + DNA.LIGHT + " " + LOCK(WHO) + " " + SCENE_i.START + " Emotions: "
      + SCENE_i.EMOTION + ". Each person looks exactly like their reference photo. "
      + NO_TEXT_IMG
```

Ảnh 0 credit. Lưu tên `DL_{slug}_img_{i}`.

## S7 — Prompt video (7 khối, cách nhau một dòng trống, **≤ 3500 ký tự**)

```
[1] DNA: STYLE, CAMERA, MOTION, AUDIO RULES lines, verbatim
[2] "VOICES (keep each voice identical in every clip):\n" + VOICE(speakers of clip i)
[3] "SHOTS: " + SCENE_i.SHOTS + " " + ASPECT + "."
[4] T1-A1: "SET: " + SET_LOCK + " " + HOST_FRAME + " The host looks exactly like the
           reference image."
    T1-A2 / T2: "START: The clip starts exactly on the start frame image and keeps its
           people, their faces, clothes and the place. " + SCENE_i.START
[5] "ACTION: " + SCENE_i.ACTION + " EMOTION: " + SCENE_i.EMOTION
[6] DIALOGUE block (see below)
[7] "NEGATIVE: no on-screen text, no subtitles, no captions, no music, no narrator, no
     extra words, nobody else speaks, no change of faces or clothes, no violence."
```

**Khối [6] DIALOGUE** (dựng từ `CLIPS[i]`, mỗi dòng một câu, đúng thứ tự):

```
DIALOGUE: spoken on screen in Vietnamese with a native Northern accent and accurate
lip-sync, word for word, in this order, each line only once, starting within the first
half second and finishing before the clip ends:
MẸ_CHỒNG (the older woman in the floral blouse, left): "Cô ký vào đây đi, nhà này không chứa nổi loại con dâu như cô."
CON_DÂU (the young woman in the white shirt, right): "Mẹ nói đúng. Con sẽ ký."
```

Mỗi dòng có dạng `CODE (POS(CODE)[, vị trí trái/giữa/phải theo START]): "<text>"`. **T1:** chỉ một dòng `MC (the host): "<text>"`.

**Tham số gọi `Flow.generate.video`:**

| Template | Kiểu | Tham số |
|---|---|---|
| T1 | A1, mặc định nếu F‑A PASS | `referenceImageMediaIds: [HOST_IN_STUDIO]`, `audioReferenceMediaIds: [voice MC]`, `durationSeconds: 8`, `aspectRatio`, `modelDisplayName` |
| T1 | A2 | `firstFrameImageMediaId: SCENE_IMG_i`, không có audio ref |
| T2 | Frames, mặc định | `firstFrameImageMediaId: SCENE_IMG_i` |
| T2 | Ingredients, chỉ khi F‑Bd PASS | `referenceImageMediaIds: [SCENE_IMG_i]`, `audioReferenceMediaIds: [giọng các người nói]` |

Lưu clip tên `DL_{slug}_{i}`.

## Kiểm trước khi gửi video i (code, trên mảng 7 khối, không tìm trong chuỗi đã ghép)

Mỗi `text` đã được chuẩn hoá: NFC, bỏ ký tự ẩn, gộp khoảng trắng, `"` thẳng trong câu đổi thành `“ ”`.

| Mã | Điều kiện |
|---|---|
| (a) | `CLIPS[i]` có ≥ 1 dòng, không dòng nào rỗng |
| (b) | Khối [6] có đúng `CLIPS[i].length` dòng thoại, dòng k kết thúc bằng `: "<text_k>"` |
| (c) | Không khối nào khác chứa dòng bắt đầu bằng một mã diễn viên + `(` hoặc `:` |
| (d) | Mọi `who` trong `CLIPS[i]` có trong `SCENE_i.WHO` (T1: `MC`) |
| (e) | Prompt ghép ≤ 3500 ký tự. Quá thì báo lỗi, không tự cắt |

Lỗi thì hiện "Lỗi prompt (a|b|c|d|e)" kèm số liệu, không gửi, không tốn credit.

**Nếu (e) hay vượt** với T2 có 3 người nói: bỏ CAMERA của khối [1] trước, rồi rút POS về 3–5 từ.

Mỗi thẻ có mục thu gọn **"Xem prompt gửi đi"** hiện nguyên văn prompt.

## Mẫu prompt T2 clip 1 (~2600 ký tự)

```
STYLE: photorealistic cinematic vertical video, shot on a full-frame cinema camera, 35mm lens, shallow depth of field, natural skin texture, realistic Vietnamese people, modern Vietnam. Looks like a high-quality Vietnamese web drama. Not anime, not cartoon, not 3D.
CAMERA: eye level, steady (tripod or slow dolly). Cuts only where the SHOTS say "CUT TO". No handheld shake, no drone, no fast zoom, no rotation.
MOTION: natural acting, real-time speed; lips move in sync with the spoken Vietnamese; blinking, breathing, small natural gestures. Faces and clothes never change.
AUDIO RULES: only the characters' spoken lines and quiet room tone. NO music. NO score. NO singing. NO narrator. NO extra voices. NO sound effects stings.

VOICES (keep each voice identical in every clip):
MẸ_CHỒNG: Vietnamese woman about 58, Northern accent, sharp, loud, slightly husky voice, speaks fast and bossy.
CON_DÂU: Vietnamese woman about 30, Northern accent, clear mid-high voice, controlled and firm, gets cold and calm when angry.

SHOTS: (0–4s) medium-wide, MẸ_CHỒNG slams the form on the dining table, CON_DÂU on the right, CHỒNG on the sofa in the background CUT TO (4–8s) medium close-up CON_DÂU 9:16 vertical.

START: The clip starts exactly on the start frame image and keeps its people, their faces, clothes and the place. MẸ_CHỒNG stands at the dining table on the left, palm flat on a printed form; CON_DÂU stands on the right facing her; CHỒNG sits on the sofa at the back, looking at his phone.

ACTION: MẸ_CHỒNG pushes the form across the table and points at it while speaking; after the cut CON_DÂU looks down at the paper, then lifts her eyes calmly. Hold. EMOTION: MẸ_CHỒNG = contemptuous, CON_DÂU = hurt but composed, CHỒNG = indifferent

DIALOGUE: spoken on screen in Vietnamese with a native Northern accent and accurate lip-sync, word for word, in this order, each line only once, starting within the first half second and finishing before the clip ends:
MẸ_CHỒNG (the older woman in the floral blouse, left): "Cô ký vào đây đi, nhà này không chứa nổi loại con dâu như cô."
CON_DÂU (the young woman in the white shirt, right): "Mẹ nói đúng. Con sẽ ký."

NEGATIVE: no on-screen text, no subtitles, no captions, no music, no narrator, no extra words, nobody else speaks, no change of faces or clothes, no violence.
```
