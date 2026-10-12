# Dựng Tool `DL-Studio` trong Google Flow

**PRD:** `docs/PRD.md` v1.0 · **Chỉ dẫn từng bước:** `docs/flow-tool/steps/` · **Spike:** `docs/flow-tool/spike-tools.md`

Cách làm giống auto-ns-v3: mô tả Tool bằng lời trong ô **Create Tool** của Flow; mỗi lần sửa thì dán một **"Phần 0x — Vá"** vào khung chat của Tool, không tạo Tool mới (Flow có quota tạo Tool/ngày).

> **Trước khi dựng:** chạy xong spike F‑A, F‑B, F‑C. Kết quả của chúng quyết định ba chỗ đánh dấu `[SPIKE]` trong Phần 2: chế độ video T1, chế độ video T2, số người nói mỗi clip.

---

## Phần 0 — Các bản vá (thêm dần, mới nhất ở dưới)

*(chưa có)*

---

## Phần 1 — Các bước làm (~30 phút)

1. Mở https://labs.google/fx/tools/flow, tạo project `Đạo Lý – <tên kênh>`.
2. **Tools → Create Tool**, dán nguyên **khối ở Phần 2** → **Generate**.
3. Kiểm theo bảng Phần 3. Thiếu hoặc sai thì sửa bằng lời trong khung chat của Tool.
4. **Dán các file trong `steps/` vào khung chat của Tool**, mỗi tin nhắn một file, đợi Tool cập nhật xong rồi mới dán tin tiếp. Khối Phần 2 chỉ *nhắc tới* các file này ("the S0 instructions", "the S6‑S7 instructions", "the table in the S4 instructions"); Flow chưa thấy nội dung của chúng, nên trước khi dán, Tool sẽ tự bịa phần đó.
   - **(a) Phần code**, dán trước, theo thứ tự S0 → S4 → S6‑S7. Mở đầu tin nhắn bằng *"Implement the following specification as plain code (not an agent step). Change nothing else:"*, rồi dán **toàn bộ file**:
     - `S0-chia-thoai.md`: quy tắc chia kịch bản thành clip.
     - `S4-khoi-lock.md`: dòng DNA FIXED, bảng SET_LOCK, dàn diễn viên mặc định, bảng POS.
     - `S6-S7-anh-va-clip.md`: công thức prompt ảnh và video, bộ kiểm (a)–(e).
   - **(b) Bước agent**, theo thứ tự S1 → S1s → S2 → S3 → S4 → S4a → S5 → S5b → S8. Mỗi tin nhắn mở đầu bằng *"Replace the instructions of agent step S1 with exactly the following text:"* (đổi S1 thành tên bước tương ứng), rồi dán **chỉ phần nằm trong khối \`\`\` đầu tiên** của file, tức prompt tiếng Anh. Không dán phần giải thích tiếng Việt.
     - S4: khối \`\`\` dưới mục "Prompt dán vào bước S4".
     - S6‑S7 không phải bước agent nên không có mặt ở đây.
   - **(c) Kiểm:** hỏi Tool *"List every agent step and show the first 2 lines of its instructions."* Mỗi bước phải mở đầu đúng như trong file.
5. Màn **Kênh**:
   - Điền tên kênh, watermark, chữ biển, kiểu studio.
   - MC và từng diễn viên: điền Thông tin, rồi chọn "AI tự tạo" hoặc "Tải ảnh lên" (ảnh của bạn hoặc người đã đồng ý).
   - Tạo `STUDIO_IMG`, `HOST_IMG`, `HOST_IN_STUDIO`; tạo lại tới khi ưng (0 credit).
   - Chọn giọng MC bằng popup của Flow.
   - Tạo `CHAR_IMG` cho dàn diễn viên.
6. Chạy thử:
   - **T1 Đạo lý**, chủ đề "Lòng tự trọng", 4 clip.
   - **T2**: dán kịch bản mẫu T2 trong `docs/topic-bank.md`.
   - Nghe từng clip, rồi ghép.

> Không share link Tool: link share **phơi toàn bộ prompt**.

---

## Phần 2 — Mô tả dán vào ô Create Tool

Viết bằng tiếng Anh vì agent dựng Tool làm theo tiếng Anh chính xác hơn. Nhãn giao diện và thoại là tiếng Việt.

```
Build an interactive tool named "DL-Studio – Phim đạo lý" that makes ONE Vietnamese
vertical short video of N clips (8 seconds each) for a moral-lesson ("đạo lý") channel,
in one of two templates:
  T1 "MC Đạo lý": one AI host sits in the channel's studio and talks to the camera.
  T2 "Phim Drama": a short realistic family drama; 2–4 characters speak on screen.
In both, the characters SPEAK the Vietnamese dialogue ON SCREEN with lip-sync (Veo native
audio). No music. The user reviews, edits, regenerates, previews, then joins and exports.
UI text is Vietnamese exactly as written below. 5 screens, with a stepper at the top.

SCREEN 0 – "Kênh" (channel profile; shown first only when no profile exists; reachable
any time from a "Kênh" button in the header; saved in the tool's persistent storage)
- "Tên kênh" (text), "Chữ watermark" (text, e.g. "An Nhiên 0900000000"),
  "Chữ trên biển studio" (text, e.g. "AN NHIÊN PODCAST"),
  "Kiểu studio": chips "Podcast tối ấm" (default) · "Văn phòng sáng" · "Phòng khách" ·
  "Thư phòng gỗ" -> SET_LOCK text from the table in the S4 instructions, with {BIEN} =
  the sign text.
- "MC": a PERSON PANEL (below) with code MC, plus "Xưng hô" (text, default
  "mình – các bạn").
- "Giọng MC": button that calls Flow.media.select() so the host picker shows its voices
  tab; store the picked mediaId and name; show "Giọng MC: <name> · đã gắn".
- "Studio": STUDIO_IMG (Nano Banana Pro, 0 credit, "Tạo lại ảnh"), then HOST_IN_STUDIO
  (references: HOST_IMG + STUDIO_IMG, "Tạo lại ảnh"). Prompts in S6.
- "Dàn diễn viên": a list of PERSON PANELS, prefilled with the default cast of S4
  (MẸ_CHỒNG, CON_DÂU, CHỒNG, BỐ, EM_CHỒNG, CON); "+ Thêm diễn viên", "Xoá".
- Save images as "DL_{kenh}_studio", "DL_{kenh}_host", "DL_{kenh}_host_studio",
  "DL_{kenh}_char_{code}" (and the uploads as "..._upload") in the project.
  Button "Lưu kênh".

PERSON PANEL (the MC and every cast member; same component):
- "Mã" (code, e.g. MẸ_CHỒNG), "Vai" (role), POS (short English recognition phrase).
- "Thông tin": "Giới tính" (Nam/Nữ), "Tuổi" (number), "Ngoại hình" (face, hair, body),
  "Trang phục" (clothes, colours), "Giọng nói" (age, accent, pitch, manner). Prefilled
  from the S4 default cast. CHAR_LOCK and VOICE_LOCK are BUILT from these fields (S6
  "LOCK from fields") and shown in a collapsed editable box "Mô tả gửi AI"; once the user
  edits that box by hand, stop rebuilding it and show "Đã sửa tay · Dựng lại từ thông tin".
- "Ảnh nhân vật": chips "AI tự tạo" (default) · "Tải ảnh lên".
  - "AI tự tạo": the reference image (HOST_IMG for MC, CHAR_IMG_<code> for cast) is
    generated by Nano Banana Pro from CHAR_LOCK (S6), with "Tạo lại ảnh".
  - "Tải ảnh lên": button "Chọn ảnh" -> Flow.media.select() limited to images (the host
    picker lets the user upload from the computer or pick a project image); if the SDK
    also offers a direct file upload, add a file input / drop zone "Kéo thả ảnh vào đây"
    (jpg/png/webp, max 10 MB) that uploads into the project. Store the mediaId as
    UPLOAD_<code> and show a thumbnail with "Đổi ảnh" and "Bỏ ảnh" (back to AI tự tạo).
    Under it a checkbox "Chuẩn hoá ảnh (khuyên dùng)", default ON:
      ON  -> generate the reference image from the upload with the S6 "from upload"
             prompt (same face; clean background, standard framing) with "Tạo lại ảnh";
      OFF -> the upload itself IS the reference image.
    After an upload, if the "Thông tin" fields are still the defaults or empty, run step
    S4a (describe the photo) and fill Ngoại hình, Trang phục, Giới tính, Tuổi from its
    answer; the user can edit. If S4a cannot see images, show "Hãy điền Ngoại hình và
    Trang phục giống ảnh" and require both fields before "Lưu kênh".
    Show once, small, under the button: "Chỉ dùng ảnh của bạn hoặc người đã đồng ý. Không
    dùng ảnh người nổi tiếng hoặc ảnh thật của trẻ em."
    If the host rejects the image (policy), show its message, keep the panel on
    "AI tự tạo" and keep the user's fields.
- Changing the photo or the "Thông tin" of a person marks every image and clip that
  uses that person "Cần tạo lại" (HOST_IN_STUDIO, scene images, clips).

SCREEN 1 – "Thiết lập"
1. "Template": chips "T1 · MC Đạo lý" (default) · "T2 · Phim Drama".
2. T1 only: "Kiểu nội dung": chips "Đạo lý" · "Kể chuyện" · "Kiến thức". With
   "Kiến thức", show a box "Dữ kiện (số liệu, điều luật — tự kiểm tra, ghi nguồn)".
   T2 only: "Nhân vật": checkboxes of the cast (choose 2–4).
3. "Chủ đề": dropdown from the topic bank (headings of docs/topic-bank.md) + "Tự nhập…";
   "Góc nhìn" dropdown filtered by topic + free text (may be empty).
4. "Kịch bản có sẵn (không bắt buộc)": large box. Placeholder for T2:
   "Mỗi dòng một câu: Mẹ chồng: …". When filled, run SPLIT (S0) live and show
   "<total> tiếng · <N> clip · ~<cost> credit" and the S0 warnings.
5. "Phần": number, default 1 (series part).
6. "Khung hình": chips "9:16 dọc" (default) · "16:9 ngang".
7. "Tông": chips "AI tự chọn" · "Căng thẳng – kịch tính" · "Ấm áp – tâm tình" ·
   "Nghiêm khắc – thức tỉnh".
8. "Model video": list the Veo models the SDK offers with their credit cost;
   default [SPIKE F‑D].
Button "Tạo ý tưởng": box empty -> run S1, S2, S3; box filled -> CLIPS = SPLIT(box), run
S1s. Then go to screen 2.

SPLIT: exactly as described in the S0 instructions (dynamic programming, never change a
word; T2 lines "NAME: text", names matched to cast codes ignoring case, accents, spaces
and "_"; max 30 syllables per clip for T1, 26 for T2; T2 max 3 lines and max
[SPIKE F‑B: 2 | 1] speakers per clip).

DATA: CLIPS[i] = array of {who, text}. LINE_i = lines joined as "WHO: text" with " | ".
syllables = number of space-separated words of the texts (names not counted).

SCREEN 2 – "Ý tưởng"
"← Quay lại". Show the BRIEF. Then "Thoại theo clip": one card per clip "Clip i" with one
row per line: a dropdown "Người nói" (T1: only MC; T2: the chosen cast) and a text box;
"+ Thêm câu", "Xoá câu"; a syllable counter per clip (T1: green 26–30, amber < 26,
red > 30; T2: green 16–26, amber < 16, red > 26, plus red if > 3 lines or too many
speakers). Under the list: "+ Thêm clip", "Xoá clip", "Chia lại tự động".
Buttons: "Tạo lại ý tưởng", "Vẽ kịch bản (Story)" (T2: runs S4 then S5; T1: runs S5 only)
then generates the images of S6 and goes to screen 3. 0 credit.

SCREEN 3 – "Storyboard"
"← Quay lại". Top: the lock images: T1 = HOST_IN_STUDIO (from the channel); T2 =
PLACE_IMG (with "Tạo lại ảnh") and the CHAR_IMG of the chosen cast (from the channel).
N cards. Card i:
a. "Thoại": the lines of clip i (same data as screen 2), editable, counter,
   "Lưu thoại" -> runs S5b for this card and marks image and video "Cần tạo lại".
b. "Mô tả cảnh": CẢNH, then "Nhân vật: <WHO>" and "Shots: <SHOTS>". Read-only.
c. Scene image (T2 always; T1 only in mode A2) with "Tạo lại ảnh" (prompt and references
   from S6). Saved as "DL_{slug}_img_{i}".
d. The clip: "Tạo video" / "Tạo lại video" showing the credit cost; inline player after
   generation. Saved as "DL_{slug}_{i}".
   Mode for T1: [SPIKE F‑A: A1 Ingredients = referenceImageMediaIds [HOST_IN_STUDIO] +
   audioReferenceMediaIds [MC voice] | A2 Frames = firstFrameImageMediaId SCENE_IMG_i].
   Mode for T2: [SPIKE F‑B: Frames = firstFrameImageMediaId SCENE_IMG_i].
   durationSeconds 8, the selected aspect ratio and model.
e. Collapsed "Chi tiết kỹ thuật": START, ACTION, EMOTION (editable; editing marks
   "Cần tạo lại") and "Xem prompt gửi đi" (the exact assembled prompt, read-only).
Bottom: "Tạo tất cả video (<k> clip · <cost> credit)" with an inline confirmation; runs the
cards without an up-to-date clip ONE AT A TIME in order using the same function as the
card button; becomes "Dừng (<done>/<k>)"; failures show their reason and the batch goes
on; at the end "Tạo lại các clip lỗi". State updates are functional (never overwrite
other cards). "Ghép & xuất" is enabled when all N cards have an up-to-date clip.

PROMPTS: agents never write final prompts. Build every image and video prompt IN CODE at
click time, exactly as specified in the S6‑S7 instructions: image prompts STUDIO_IMG,
HOST_IMG, HOST_IN_STUDIO, CHAR_IMG, PLACE_IMG, SCENE_IMG_i; the video prompt = 7 blocks
[1] DNA fixed lines, [2] VOICES of the speakers, [3] SHOTS, [4] SET (T1-A1) or START,
[5] ACTION + EMOTION, [6] DIALOGUE, [7] NEGATIVE, joined by "\n\n".
DIALOGUE block [6] = the fixed header sentence from S6‑S7, then one row per line of
CLIPS[i] in order: CODE + " (" + POS(CODE) + "): \"" + text + "\"".
VIDEO CHECKS on the block array before sending (a) clip has ≥ 1 non-empty line; (b) block
[6] has exactly CLIPS[i].length dialogue rows, row k ends with ': "<text_k>"'; (c) no
other block has a row starting with a cast code followed by "(" or ":"; (d) every speaker
is in SCENE_i.WHO (T1: MC); (e) total ≤ 3500 characters. On failure send nothing and show
"Lỗi prompt (a|b|c|d|e)" with details. Never put dialogue text into a RegExp or a
String.replace replacement; compare with ===, endsWith, indexOf.
PARSING: normalize(text) = NFC, zero-width removed, whitespace collapsed, trimmed,
straight " inside a line turned into “ ”. S3 rows "<n> | <beat> | <dialogue> | <count>";
S5/S5b blocks "=== SCENE i ===" with CẢNH, WHO, SHOTS, START, ACTION, EMOTION; ACTION
stops at its first "Hold."; remove from START and ACTION any text equal to a dialogue
text.

SCREEN 4 – "Ghép & xuất"
"← Quay lại". Join the N clips in card order with ffmpeg.wasm, keeping each clip's audio;
trim leading/trailing silence of each clip (keep 0.2 s before and 0.45 s after the
speech); progress "Đang ghép clip <i>/<N> · <p>%" clamped 0–100; a watchdog stops a stuck
join and retries once with concat stream copy; every ffmpeg job runs as one closure on
one instance (clean FS, write, check, exec, read, delete). Preview player.
Then the S8 sheet (titles, hook texts, caption, pinned comment) each with "Sao chép".
"Lớp chữ" panel with live preview on a canvas over the video:
- "Watermark": on by default, text = channel watermark, white ~38% opacity, centred
  horizontally at ~56% of the height, whole video.
- "Hook": on by default, text = first hook from S8 (editable), yellow #FFDE29 with a dark
  red outline and an outer white outline, centred at ~74% of the height, 2 balanced lines
  max, shown 0–1.6 s with a short fade.
- "Phụ đề": off by default; lines ≤ 10 words timed to the voice in each clip.
Fonts: Be Vietnam Pro ExtraBold (load latin, latin-ext and vietnamese ranges and check
them before drawing). "Xuất video" renders 1080×1920 (9:16) or 1920×1080 (16:9) in the
browser (canvas overlays + WebCodecs, ffmpeg.wasm fallback), audio unchanged.
Downloads: "Tải video (MP4)" "<slug>.mp4", "Tải thoại (.txt)" (the N LINE_i, one per
line), "Tải phụ đề (.srt)".
"+ Tập tiếp theo": inline confirmation; keeps channel, template, chosen cast, aspect,
model; Phần + 1; passes the current BRIEF as the previous part to S1; clears story data;
goes to screen 1. "+ Video mới": same but Phần = 1 and no previous part.

RULES:
- Photorealistic cinematic look for every image and clip; real-looking Vietnamese people.
- Faces, clothes and voices come only from the channel profile; copy CHAR_LOCK and
  VOICE_LOCK verbatim into prompts.
- Never put visible text, subtitles or captions inside images or videos, EXCEPT the
  studio sign text in STUDIO_IMG / HOST_IN_STUDIO. Watermark, hook and subtitles are
  drawn only by our own export code.
- No music in any clip. No physical violence, blood, weapons, real names or brands.
- Every agent step calls Flow.generate.text with a short prompt ("Do the task in the
  system instruction now.") and puts its full instructions, with variables filled in, in
  options.systemInstruction (the host rejects prompts longer than about 4000 characters).
- Confirmations are inline boxes with "Đồng ý" / "Huỷ"; never window.confirm, alert or
  prompt (the Flow page blocks them).
- {slug} = short lowercase ASCII slug of the title; {kenh} = slug of the channel name.
- Keep all state so the user can move between screens without losing work; going back
  never deletes anything.
```

---

## Phần 3 — Bảng kiểm sau khi Flow dựng xong

| Kiểm | Đúng khi |
|---|---|
| Màn 0 Kênh | Lưu được; mở lại Tool vẫn còn. Ảnh studio có biển đúng chữ (F‑C). `HOST_IN_STUDIO` giữ mặt MC. Giọng MC ghi "đã gắn". Dàn diễn viên có đủ 6 mã mặc định, mỗi mã có `CHAR_IMG` |
| Ảnh nhân vật | "AI tự tạo": sửa Ngoại hình/Trang phục thì "Mô tả gửi AI" đổi theo, "Tạo lại ảnh" ra người khớp mô tả. "Tải ảnh lên": chọn được ảnh từ máy hoặc project; S4a điền sẵn thông tin; bật "Chuẩn hoá" thì ảnh tham chiếu cùng mặt, nền sạch; tắt thì dùng nguyên ảnh. "Bỏ ảnh" quay về AI tự tạo, không mất thông tin. Đổi ảnh thì các ảnh cảnh và clip liên quan báo "Cần tạo lại" |
| Màn 1 | Đổi T1/T2 thì các ô riêng hiện hoặc ẩn đúng. Dán kịch bản T2 thì hiện "x tiếng · N clip · ~credit" và cảnh báo (tên lạ, chữ số, viết tắt) |
| Chia thoại | Ghép các clip lại đúng bằng kịch bản gốc; T2 không clip nào > 3 dòng |
| Màn 2 | Mỗi câu có dropdown người nói; bộ đếm theo ngưỡng của template |
| Màn 3 | T2: ảnh cảnh có đúng người trong WHO, mặt giống `CHAR_IMG`. "Lưu thoại" → S5b → "Cần tạo lại" |
| Prompt gửi đi | Khối DIALOGUE có đúng số câu của thẻ, đúng thứ tự, đúng tên; ≤ 3500 ký tự |
| Video | T1: đúng chế độ đã chốt sau spike; T2: start frame = ảnh cảnh. Hiện giá credit |
| Màn 4 | Ghép được; watermark và hook hiện đúng chữ, đúng chỗ, đúng thời điểm; xuất 1080×1920; tải MP4, .txt, .srt |
| Series | "+ Tập tiếp theo" giữ kênh và dàn diễn viên, tăng Phần, S1 nối tiếp tập trước |

---

## Phần 4 — Nếu Tool không làm được

| Thiếu | Dự phòng |
|---|---|
| Popup `Flow.media.select()` không cho tải ảnh từ máy | Tải ảnh vào project bằng giao diện Flow trước (kéo thả vào project), rồi "Chọn ảnh" từ project |
| S4a không đọc được ảnh | Người dùng tự điền Ngoại hình và Trang phục; ảnh vẫn dùng làm tham chiếu |
| Flow từ chối ảnh tải lên (ảnh người thật) | Bật "Chuẩn hoá" thử lại; vẫn từ chối thì dùng "AI tự tạo" với mô tả giống ảnh |
| Không lưu được hồ sơ kênh qua lần mở lại | Lưu ảnh trong project (`DL_{kenh}_*`). Màn 0 có ô "Dán hồ sơ (JSON)" và nút "Sao chép hồ sơ (JSON)" để dán lại |
| Không ghép hoặc xuất được | Tải N clip + `thoai.txt`, chạy `python3 scripts/ghep.py <thư mục> --watermark "…" --hook "…"` |
| Chèn chữ hỏng | Xuất bản ghép không chữ, rồi chạy `ghep.py` như trên |
| Chế độ Ingredients không nhận audio ref (T1) | T1 dùng A2 (Frames). Giọng giữ bằng VOICE_LOCK |
| Veo nói lẫn lời giữa các nhân vật (T2) | Đổi SPLIT thành 1 người nói/clip (vá Phần 0x) |
