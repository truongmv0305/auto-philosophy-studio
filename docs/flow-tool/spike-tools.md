# Spike F‑A…F‑E — Kiểm Flow cho `DL-Studio` (Đạo Lý Studio)

**PRD:** `docs/PRD.md` mục 10. **Thứ tự:** F‑C (0 cr) → F‑A → F‑B → F‑D → F‑E (0 cr, máy local).
**Ngân sách:** ~120 credit. Mỗi clip `veo-3.1-lite` 8s = 10 cr; Fast/Quality ghi lại giá thật.
**Ghi kết quả:** tạo `docs/spikes/F-<x>.md` theo mẫu cuối file, rồi báo lại để cập nhật PRD và `create-tool.md`.

Các spike chạy **bằng tay trong Flow** (tạo ảnh, tạo video), chưa cần dựng Tool. Mục đích là chốt 4 điều mà auto-ns-v3 chưa từng thử, vì auto-ns chỉ có người kể giấu mặt và tranh 2D:

1. Veo có **nhép môi tiếng Việt** đúng nhân vật trên hình không, giọng có giữ qua các clip không?
2. Một clip có **2 người nói** và **cắt shot** ("CUT TO") được không?
3. Nano Banana Pro có vẽ **biển tên kênh** (chữ có dấu) đúng không?
4. Model nào đủ tốt cho thoại nhép môi với giá chấp nhận được?

Tạo tất cả trong **một project** `Đạo Lý – spike`. Tải clip về `spikes-out/<x>/` để đo bằng `scripts/ghep.py`.

---

## F‑C — Ảnh MC, studio có biển tên, dàn diễn viên (0 credit)

Nano Banana Pro, 9:16. Dùng prompt mẫu ở `docs/flow-tool/steps/S6-S7-anh-va-clip.md`, mục "Ảnh hồ sơ kênh".

| Câu | Ghi |
|---|---|
| F‑Ca | `STUDIO_IMG` có biển neon "AN NHIÊN PODCAST" (thử thêm "Việt Hà PODCAST") đúng chữ, đúng dấu không? Thử 3 lần, ghi số lần đúng |
| F‑Cb | `HOST_IMG`: ảnh người thật, nửa người, ngồi bàn có micro podcast, khung giống sample 1. Có bị "da nhựa", méo tay không? |
| F‑Cc | `HOST_IN_STUDIO`: ghép MC vào studio bằng 2 ảnh tham chiếu (`HOST_IMG` + `STUDIO_IMG`). Mặt MC còn giống không? |
| F‑Cd | Dàn drama 3 người (mẹ chồng ~58, con dâu ~30, chồng ~32): `CHAR_IMG` từng người. Rồi `SCENE_IMG` 3 người trong phòng khách chung cư như sample 3. Mặt cả ba có giữ không? |
| F‑Ce | Chữ trên giấy tờ ("ĐƠN XIN LY HÔN") vẽ đúng không? Nếu sai thì để S5 tránh cận chữ |
| F‑Cf | **Ảnh tải lên:** dùng ảnh chân dung của bạn (hoặc người đã đồng ý). Flow có nhận làm ảnh tham chiếu không, hay chặn vì là người thật? `REF_FROM_UPLOAD` (S6) có giữ được mặt không? Rồi ghép vào studio (`HOST_IN_STUDIO`) và một `SCENE_IMG`: mặt còn giống ảnh gốc không? |
| F‑Cg | **Trong một Tool thử nhỏ:** `Flow.media.select()` có cho tải ảnh từ máy không, hay chỉ chọn ảnh có sẵn trong project? SDK có hàm tải file trực tiếp không? `Flow.generate.text` có nhận ảnh đính kèm để chạy S4a không? |

**PASS:** biển tên đúng ≥ 2/3 lần; mặt MC/diễn viên giữ khi ghép cảnh. **FAIL F‑Cf (bị chặn):** chỉ để "AI tự tạo"; nút tải ảnh vẫn giữ nhưng báo trước là có thể bị từ chối. **FAIL biển tên:** đặt biển tên làm logo PNG chèn lúc xuất, prompt ảnh ghi "a blank glowing neon sign".

## F‑A — Template MC: "Thành phần" vs "Ảnh đầu" (~50 cr)

Lời thoại MC (28 tiếng, giọng Bắc):

```
Có một điều phải ngoài bốn mươi tuổi tôi mới hiểu. Người thương mình thật lòng sẽ không bắt mình phải chọn giữa họ và lòng tự trọng.
```

Tạo cùng lời trên theo 2 cách, mỗi cách 2 clip liên tiếp (lời clip 2 tự viết, cũng ~28 tiếng):

- **A1 — Thành phần (Ingredients):** ảnh tham chiếu `HOST_IN_STUDIO` (+ `STUDIO_IMG` nếu cho thêm), cộng giọng nữ preset (`Sulafat` hoặc `Vindemiatrix`). Prompt video theo khối T1 ở S6‑S7.
- **A2 — Ảnh đầu (Frames):** start frame = `HOST_IN_STUDIO`, không gắn giọng, giọng tả bằng chữ (VOICE_LOCK).

| Câu | Ghi |
|---|---|
| F‑Aa | Nhép môi: miệng MC khớp lời không? Đọc đủ, đúng nguyên văn, không thêm chữ? |
| F‑Ab | Giọng 2 clip của A1 có giống nhau không? Của A2? (nghe nối tiếp bằng `ghep.py`) |
| F‑Ac | A1 bố cục có giống studio không, biển tên có bị méo khi chuyển động? Mặt MC có trôi? |
| F‑Ad | A2 khung có giữ đúng start frame không? |
| F‑Ae | Có nhạc nền, phụ đề hay chữ lạ do Veo tự thêm không? |
| F‑Af | Ngôn ngữ cử chỉ: chống cằm, giơ ngón tay, cười như sample 1/2 có ra theo ACTION không? |
| Credit | trước / sau, từng clip |

**PASS A1:** a, b, c đạt ⇒ T1 mặc định "Thành phần". **FAIL A1 nhưng PASS A2:** T1 dùng "Ảnh đầu"; giọng tả bằng chữ; nếu giọng trôi, giữ cùng một start frame cho mọi clip (sample 1 làm vậy).

## F‑B — Template Drama: 2 người nói + cắt shot trong 1 clip (~40 cr)

Start frame: `SCENE_IMG` 3 người từ F‑Cd. Thoại (21 tiếng):

```
MẸ CHỒNG: "Cô ký vào đây đi, nhà này không chứa nổi loại con dâu như cô."
CON DÂU: "Mẹ nói đúng, con sẽ ký. Nhưng căn nhà này là tên con."
```

Tạo 4 biến thể (mỗi biến thể 1 clip):

| Biến thể | Cách |
|---|---|
| B1 | Ảnh đầu, 1 shot, VOICE_LOCK 2 người |
| B2 | Ảnh đầu, 3 shot: "Shot 1 (0–3s) wide… CUT TO Shot 2 (3–6s) close-up MẸ CHỒNG… CUT TO Shot 3 (6–8s) close-up CON DÂU" |
| B3 | Thành phần: ảnh 3 nhân vật + PLACE, **2 audio ref** (1 giọng nữ già, 1 giọng nữ trẻ) nếu Flow cho chọn 2 |
| B4 | Như B2 nhưng thoại chia theo thời điểm: "(0–3s) MẸ CHỒNG: …", "(4–8s) CON DÂU: …" |

| Câu | Ghi |
|---|---|
| F‑Ba | Câu nào do ai nói: có đúng người, đúng miệng không? Có người thứ ba tự mở miệng không? |
| F‑Bb | Hai giọng có khác nhau rõ (già/trẻ) không? |
| F‑Bc | B2/B4 có cắt shot thật không? Mặt sau khi cắt còn đúng người không? |
| F‑Bd | B3: Flow có nhận 2 audio ref không? Giọng gán đúng người không? |
| F‑Be | Cảm xúc: giận, chỉ tay, đập bàn có ra như sample 3 không? Có bị Veo từ chối vì "bạo lực" không? |

**PASS:** a + b đạt ở ít nhất một biến thể ⇒ biến thể đó thành mặc định T2. **FAIL a:** giới hạn **1 người nói / clip** (người kia chỉ phản ứng), S2 viết thoại theo luật đó.

## F‑D — Model cho clip có thoại (~30 cr)

Chạy lại lời của F‑A bằng `veo-3.1-fast` và `veo-3.1` (Quality) nếu tài khoản có; so với Lite.

| Câu | Ghi |
|---|---|
| F‑Da | Credit mỗi clip từng model |
| F‑Db | Nhép môi và phát âm tiếng Việt: model nào rõ hơn? |
| F‑Dc | Thời lượng có chọn được ngoài 8s không? |

**Kết luận:** chọn model mặc định cho T1 và T2 (có thể khác nhau).

## F‑E — Ghép + watermark + hook trên máy (0 credit)

Dùng clip của F‑A (và F‑B) trong `spikes-out/fa/`:

```bash
python3 scripts/ghep.py spikes-out/fa --watermark "An Nhiên 0900000000" --hook "Hưởng 75% BHXH"
```

| Câu | Ghi |
|---|---|
| F‑Ea | Chữ tiếng Việt có dấu đúng, watermark mờ đúng vị trí (giữa, ~60% chiều cao)? |
| F‑Eb | Sticker hook hiện 0–1.5s, chữ vàng viền đỏ như sample 2? |
| F‑Ec | Mối nối giữa clip có bị hụt chữ không (cột "giọng (s)")? |

---

## Mẫu `docs/spikes/F-<x>.md`

```markdown
# Spike F‑<x> — <câu hỏi>

**Ngày chạy:** YYYY-MM-DD · **Tài khoản:** Google AI Pro/Ultra · **Credit:** trước ___ / sau ___

## Kết quả
| Câu | Trả lời | Bằng chứng (ảnh chụp, tên file) |
|---|---|---|

## Kết luận: PASS / FAIL
Việc phải sửa ở PRD / docs/flow-tool:
```
