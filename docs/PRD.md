# PRD — Đạo Lý Studio (`DL-Studio`) v1.0

**Ngày:** 2026‑10‑08 · **Dựa trên:** auto-ns-v3 (Nhân Sinh Auto, PRD v3.1) · **Trạng thái:** chờ spike F‑A…F‑E (`docs/flow-tool/spike-tools.md`)

Tool trong Google Flow tạo video ngắn 9:16 cho **kênh đạo lý** tiếng Việt, gồm hai dạng:

- **T1 — MC Đạo lý:** một MC AI cố định ngồi trong studio có biển tên kênh, nhìn camera nói chuyện đạo lý, chuyện đời, kiến thức (sample 1, 2).
- **T2 — Phim Drama AI:** 2–4 nhân vật cãi nhau, lật thế, chốt bài học (sample 3).

Cả hai dạng: ảnh người thật kiểu điện ảnh, **thoại tiếng Việt do Veo 3 tự nói và nhép môi**, không nhạc nền, watermark kênh, sticker hook ở đầu video.

---

## 1. Phân tích sample (`sample/`)

| | Sample 1 | Sample 2 | Sample 3 |
|---|---|---|---|
| Dạng | T1, podcast: biển neon "Việt Hà PODCAST", micro, cốc, cây, đèn ấm | T1, văn phòng: logo "EFY", laptop, tủ sách sáng | T2: phòng khách chung cư, mẹ chồng (~58, áo hoa), con dâu (~30, sơ mi trắng), chồng (~32, áo phông xanh) |
| Khung | 720×1280, 30fps | như sample 1 | như sample 1 |
| Dài | 34.3s | 30.1s | 30.8s |
| Clip | 4–5 clip, cùng một khung, chỉ đổi tư thế: chống cằm, cười, đưa tay | Cắt ở 7.9 / 14.7 / 22.7s, tức 4 clip 8s | Clip ở 0–7.5 / 7.5–14.8 / 14.8–22.8 / 22.8–30.8s. **Trong clip có cắt shot**: toàn → cận → đặc tả chỉ tay |
| Âm thanh | Giọng nữ Bắc, nhép môi, không nhạc | như sample 1 | Nhiều giọng, có quát, không nhạc |
| Chữ trên hình | Watermark "Việt Hà 0964497135" mờ ở giữa | Watermark và sticker hook vàng "Hưởng 75% BHXH" 0–1.5s | Watermark. Chữ "ĐƠN XIN LY HÔN" nằm trong ảnh |

Nhãn ✦ ở góc phải dưới là dấu của Veo, giữ nguyên.

## 2. Mục tiêu và phạm vi v1

**Đầu vào:**
- Hồ sơ kênh, tạo một lần.
- Template: T1 hoặc T2.
- Chủ đề lấy từ `docs/topic-bank.md`, hoặc tự gõ, hoặc dán kịch bản có sẵn.

**Đầu ra:**
- MP4 9:16, 30–40s, 4–5 clip 8s.
- File thoại `.txt` và phụ đề `.srt`.
- Bảng đăng bài S8: tiêu đề, caption, hashtag, chữ hook, bình luận ghim, gợi ý tập sau.

**Ngoài phạm vi v1:**
- Tự đăng bài.
- TTS riêng hoặc lip-sync ngoài.
- Nhạc nền.
- Video dài hơn 60s. Muốn dài hơn thì làm series "Phần 1, 2, 3".

## 3. Kiến trúc

Giống auto-ns-v3 v3.1:

- **Flow Tool** dựng bằng mô tả trong ô Create Tool (`docs/flow-tool/create-tool.md`). Mọi thứ chạy bằng tài khoản Flow của người dùng: không cần API key, không tự động hoá trình duyệt.
- **Bước agent:** `Flow.generate.text(prompt ngắn, { systemInstruction: chỉ dẫn đầy đủ })`, 0 credit. Chỉ dẫn của từng bước nằm trong `docs/flow-tool/steps/`.
- **Ảnh:** Nano Banana Pro, 0 credit trên gói Pro.
- **Video:** `Flow.generate.video`, có hai chế độ:
  - Frames: `firstFrameImageMediaId`.
  - Ingredients: `referenceImageMediaIds` + `audioReferenceMediaIds`.
- **Prompt ảnh và video ghép bằng code**, agent không tự viết prompt cuối. Prompt video ≤ 3500 ký tự (lỗi `hk`).
- **Ghép:**
  - Trong Tool: ffmpeg.wasm, chữ vẽ bằng canvas.
  - Dự phòng: `scripts/ghep.py` chạy trên máy.

**Lưu ý kế thừa từ auto-ns-v3**, xem `auto-ns-v3/docs/flow-tool/create-tool.md`:

| Lưu ý | Ở đâu |
|---|---|
| `systemInstruction` cho prompt dài (lỗi `Jj`) | dòng 44‑62 |
| Prompt video ngắn | Phần 0d |
| Batch cập nhật state theo kiểu hàm | Phần 0e |
| Giọng chỉ gắn được qua `mediaId` từ `Flow.media.select()` | Phần 0l/0m |
| Ghép một closure, có watchdog | Phần 0o/0q |
| Chèn chữ bằng canvas, nạp đủ bảng chữ tiếng Việt | Phần 0n/0p |
| Hỏi xác nhận ngay trong trang (không `window.confirm`) | — |
| Không đưa lời thoại vào RegExp | — |

## 4. Hồ sơ kênh

Tạo ở màn "Kênh", lưu trong state của Tool. Media lưu trong project Flow với tiền tố `DL_{kenh}_`.

| Trường | Ví dụ | Dùng ở |
|---|---|---|
| Tên kênh | `An Nhiên` | S1, S8, watermark |
| Chữ watermark | `An Nhiên 0900000000` | lúc xuất |
| Chữ biển studio | `AN NHIÊN PODCAST` | `STUDIO_IMG` |
| Kiểu studio | Podcast tối ấm / Văn phòng sáng / Phòng khách / Thư phòng gỗ | S4, `STUDIO_IMG` |
| MC | thông tin (giới tính, tuổi, ngoại hình, trang phục, giọng) + ảnh: **tải lên hoặc AI tự tạo** → `HOST_IMG`, rồi `HOST_IN_STUDIO` | T1 |
| Giọng MC | preset Flow, lấy `mediaId` qua `Flow.media.select()` | T1, chế độ Ingredients |
| Dàn diễn viên | 3–6 người cố định: mã, vai, thông tin như MC, ảnh **tải lên hoặc AI tự tạo** → `CHAR_IMG` | T2 |
| Xưng hô | MC xưng "mình/em/chị", gọi khán giả "các bạn/cả nhà" | S2 |

Dàn diễn viên cố định giúp khán giả nhận ra nhân vật qua nhiều tập, như các kênh drama thật.

**Ảnh nhân vật: tải lên hoặc AI tự tạo.** MC và từng diễn viên dùng chung một panel:

| Lựa chọn | Ảnh tham chiếu | Mô tả chữ (CHAR_LOCK) |
|---|---|---|
| AI tự tạo (mặc định) | Nano Banana Pro sinh từ thông tin đã điền | dựng từ các ô thông tin |
| Tải ảnh lên + Chuẩn hoá (mặc định khi tải) | Nano Banana Pro sinh lại từ ảnh tải lên: giữ mặt, nền sạch, khung chuẩn | S4a đọc ảnh và điền Ngoại hình, Trang phục; người dùng sửa được |
| Tải ảnh lên, tắt Chuẩn hoá | chính ảnh tải lên | như trên |

- Ảnh tải lên đi qua `Flow.media.select()`: popup của Flow cho tải từ máy hoặc chọn ảnh trong project. Nếu SDK có hàm tải file trực tiếp thì Tool có thêm ô kéo thả.
- Chỉ dùng ảnh của chính người dùng hoặc người đã đồng ý. Không dùng ảnh người nổi tiếng, không dùng ảnh thật của trẻ em. Flow có thể từ chối ảnh người thật; khi đó quay về "AI tự tạo" và giữ nguyên thông tin đã điền.
- Đổi ảnh hoặc thông tin của một người thì mọi ảnh cảnh và clip có người đó báo "Cần tạo lại".

**Dàn mặc định**, để bắt đầu nhanh (`assets/README.md`):

| Mã | Vai | Tuổi |
|---|---|---|
| `MC` | MC nữ | ~30 |
| `MẸ_CHỒNG` | mẹ chồng | ~58 |
| `CON_DÂU` | con dâu | ~30 |
| `CHỒNG` | chồng, con trai | ~33 |
| `BỐ` | bố, ông | ~62 |
| `EM_CHỒNG` | em chồng, cô em | ~25 |
| `CON` | cháu | ~8 |

## 5. Template T1 — MC Đạo lý

- **4 clip** (32s), hoặc 5 clip (40s).
- **Nhịp:**
  1. **HOOK.** Câu đầu ≤ 12 tiếng, có con số, nghịch lý hoặc câu hỏi.
  2. **CHUYỆN:** một chuyện cụ thể ("Có một bà mẹ…").
  3. **LẬT:** điều người ta hay hiểu sai.
  4. **ĐÚC KẾT + KÊU GỌI:** câu chốt tự viết, rồi "Theo dõi để nghe…".
- **Hình:** cùng một khung (MC trong studio). Mỗi clip một **cử chỉ** khác nhau, chọn từ danh sách cố định: chống cằm nghe, giơ một ngón tay, hai tay mở ra giải thích, cười nhẹ, nghiêng đầu, đặt tay lên ngực. Camera đứng yên hoặc đẩy vào rất chậm.
- **Tạo clip, mặc định chờ F‑A:**
  - **A1 — Ingredients:** `referenceImageMediaIds = [HOST_IN_STUDIO]`, `audioReferenceMediaIds = [giọng MC]`.
  - **A2 — Frames (dự phòng):** start frame `HOST_POSE_i` (ảnh MC trong studio ở tư thế i), giọng tả bằng VOICE_LOCK.
- **Kiểu nội dung (`{format}`):** Đạo lý (tâm tình) · Kể chuyện (MC kể chuyện có thật) · Kiến thức (luật, BHXH, lương hưu, thừa kế, như sample 2).
  - Kiểu Kiến thức phải dùng số liệu **người dùng dán vào**. Agent không tự bịa số luật.

## 6. Template T2 — Phim Drama

- **4 clip** (32s), hoặc 5 clip. Một bối cảnh, 2–4 nhân vật lấy từ dàn diễn viên.
- **Nhịp:**
  1. **NỔ:** câu thoại gắt ngay giây đầu, xung đột rõ. Ví dụ: mẹ chồng ném tờ đơn.
  2. **ÉP:** bên mạnh dồn, bên yếu nhẫn nhịn.
  3. **LẬT:** bên yếu đưa ra sự thật hoặc bằng chứng ("Căn nhà này đứng tên con").
  4. **CHỐT:** người sai cứng họng, nói câu đạo lý; hoặc cliffhanger "Còn tiếp phần 2".
- **Thoại mỗi clip:** 2–3 câu, tổng 16–26 tiếng (kịch cần khoảng lặng cho phản ứng). Mỗi câu ghi người nói: `MẸ_CHỒNG: "…"`.
  - Nếu F‑B FAIL thì mỗi clip **chỉ 1 người nói**, người kia chỉ phản ứng.
- **Hình mỗi clip:** 2–3 shot nối bằng "CUT TO". Ví dụ: toàn cảnh 3 người → cận người nói → cận phản ứng. Như vậy giống sample 3 mà vẫn chỉ tốn 1 clip.
- **Tạo clip, mặc định chờ F‑B:** chế độ Frames, start frame `SCENE_IMG_i`. Ảnh này tạo bằng Nano Banana Pro, tham chiếu các `CHAR_IMG` của người có mặt và `PLACE_IMG`.
  - Giọng tả bằng VOICE_LOCK của từng người, lặp nguyên văn ở mọi clip.
- **Giới hạn nội dung:**
  - Không đánh nhau, không máu, không đồ vật sát thương. Cãi vã chỉ bằng lời, chỉ tay, đập bàn.
  - Không trẻ em bị bạo hành.
  - Không nhắc tên người thật, thương hiệu thật.

## 7. Luồng bước

| Bước | Việc | Loại | File |
|---|---|---|---|
| S0 | Chia thoại dán sẵn thành clip theo số tiếng, giữ nguyên chữ | code | `steps/S0-chia-thoai.md` |
| S1 | Chốt đề: BRIEF | agent | `steps/S1-chot-de.md` |
| S1s | Có kịch bản sẵn: dựng ngược BRIEF | agent | `steps/S1s-brief-tu-kich-ban.md` |
| S2 | Viết thoại theo clip | agent | `steps/S2-thoai.md` |
| S3 | Căn chỉnh số tiếng (luôn chạy khi AI viết) | agent | `steps/S3-can-chinh.md` |
| S4 | Khối lock: DNA, CHAR_LOCK, VOICE_LOCK, SET_LOCK | agent | `steps/S4-khoi-lock.md` |
| S4a | Mô tả ảnh nhân vật tải lên → điền thông tin (màn Kênh) | agent | `steps/S4a-mo-ta-anh.md` |
| S5 | Storyboard: WHO, SHOTS, ACTION, EMOTION mỗi clip | agent | `steps/S5-storyboard.md` |
| S5b | Sửa thoại 1 clip → cập nhật cảnh của clip đó | agent | `steps/S5b-cap-nhat-canh.md` |
| S6 / S7 | Ghép prompt ảnh và video bằng code, kiểm prompt, gọi Flow | code | `steps/S6-S7-anh-va-clip.md` |
| S8 | Bảng đăng bài | agent | `steps/S8-bang-dang-bai.md` |

**Budget thoại**, chờ F‑A/F‑B đo lại:

| Loại clip | Tiếng / clip 8s | Ghi chú |
|---|---|---|
| T1, một người nói | 26–30 | như auto-ns |
| T2 | 16–26 | đổi người nói tốn ~0.4s, chừa chỗ cho phản ứng |
| Clip đầu | | câu đầu ≤ 12 tiếng |
| Clip cuối | T1 22–27 · T2 12–24 | chừa khoảng lặng |

## 8. Màn hình Tool

| Màn | Nội dung |
|---|---|
| 0 · Kênh | Hồ sơ kênh: tên, watermark, biển studio, MC và giọng, dàn diễn viên. Mỗi ảnh có nút "Tạo lại ảnh". Mở lại Tool thì giữ nguyên |
| 1 · Thiết lập | Template T1/T2, kiểu nội dung (T1) hoặc nhân vật tham gia (T2), chủ đề, góc nhìn, ô "Kịch bản có sẵn", số tập/phần, khung hình, model, tông |
| 2 · Ý tưởng | BRIEF. Các ô thoại theo clip, mỗi ô có bộ đếm tiếng. T2 hiện từng dòng `NGƯỜI NÓI: lời`, đổi người nói bằng dropdown. Nút "Tạo lại ý tưởng", "Vẽ kịch bản" |
| 3 · Storyboard | Ảnh lock (CHAR, PLACE/STUDIO). N thẻ, mỗi thẻ có: thoại, mô tả cảnh, ảnh cảnh, clip, "Xem prompt gửi đi". "Tạo tất cả video" |
| 4 · Ghép & xuất | Ghép, xem trước. Chèn watermark, sticker hook (chữ lấy từ S8, sửa được), phụ đề tuỳ chọn. Tải MP4, `.txt`, `.srt`. Bảng S8 có nút "Sao chép". Nút "+ Tập tiếp theo" giữ kênh và dàn diễn viên, tăng số phần |

## 9. Rủi ro

| Rủi ro | Giảm |
|---|---|
| Veo đọc sai tiếng Việt hoặc thêm chữ | Bỏ số, viết bằng chữ. Câu ngắn. Prompt có "word for word". Kiểm mỗi clip bằng tai, tạo lại clip lỗi |
| Giọng nhân vật trôi giữa các clip | T1: Ingredients + audio ref. T2: VOICE_LOCK nguyên văn. Đo ở F‑A/F‑B |
| Nhân vật nói lời của người khác | Mỗi dòng thoại ghi tên + vị trí trong khung ("the woman in the white shirt on the right"). Nếu vẫn sai: 1 người nói/clip |
| Biển tên méo chữ | F‑C. Fail thì biển trống, chèn logo lúc xuất |
| Bị từ chối do cãi vã căng thẳng | Không bạo lực vật lý. Dùng từ "argues firmly", "points" |
| Ảnh tải lên là người thật không đồng ý, hoặc bị Flow chặn | Cảnh báo ngay dưới nút tải. Bị chặn thì quay về AI tự tạo |
| Mô tả chữ lệch với ảnh tải lên → nhân vật trôi | S4a mô tả từ ảnh; bật Chuẩn hoá |
| Sao chép kênh khác | Không dùng tên, SĐT, logo của sample. Mọi chữ lấy từ hồ sơ kênh của người dùng |
| Lộ prompt khi share Tool | Như auto-ns L4: không share link Tool bản đầy đủ |

## 10. Lộ trình

1. **Phase 0 — Spike F‑A…F‑E** (`docs/flow-tool/spike-tools.md`). Kết quả ghi vào `docs/spikes/`, rồi sửa mục 5–7.
2. **Phase 1 — T1 MC.** Dựng Tool theo `create-tool.md` Phần 2 với màn 0–4, chỉ bật T1. Chạy 3 tập.
3. **Phase 2 — T2 Drama.** Gửi patch "Phần 0a — Thêm T2". Chạy 3 tập, so với sample 3.
4. **Phase 3 — Kênh và series.** Topic bank, "+ Tập tiếp theo", lịch đăng (S8).

## 11. Tiêu chí đạt (mỗi video)

- **Định dạng:** 9:16, 30–40s, 1080×1920 sau xuất, -14 LUFS. Kiểm bằng `ffprobe` và `ghep.py`.
- **Đồng nhất:** mặt và trang phục mọi nhân vật không đổi giữa các clip; giọng mỗi nhân vật không đổi.
- **Thoại:** nghe được, đúng nguyên văn ô thoại, đúng người nói, không cụt chữ cuối clip.
- **Sạch:** không nhạc, không chữ hay phụ đề lạ do Veo sinh ra.
- **Chữ của Tool:** watermark và hook đúng chữ, đúng dấu, đúng thời điểm.
- **Chi phí:** ≤ 50 credit mỗi video với `veo-3.1-lite` (5 clip, không tính tạo lại).
