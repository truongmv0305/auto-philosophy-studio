# S4 — Khối lock (agent + hồ sơ kênh, 0 credit)

**Input:** `BRIEF`, `{tone}`, hồ sơ kênh · **Output:** `DNA`, `CHAR_LOCK`, `VOICE_LOCK`, `SET_LOCK`

Có 4 khối lock. **Ba khối lấy cố định từ hồ sơ kênh, agent không viết:**

| Khối | Lấy từ | Agent viết? |
|---|---|---|
| `DNA` FIXED | hằng số trong Tool, bên dưới | không |
| `CHAR_LOCK`, `VOICE_LOCK` | hồ sơ kênh: đoạn mô tả của từng mã diễn viên, chép nguyên văn | không |
| `SET_LOCK` (T1) | hồ sơ kênh: kiểu studio + chữ biển tên | không |
| `DNA` WRITE (T2): PLACE, LIGHT, AMBIENCE | | **có**, theo BỐI CẢNH của BRIEF |

Nhờ vậy mọi tập của kênh có cùng mặt, cùng giọng, cùng studio. Đây là lớp khoá rẻ nhất (auto-ns PRD mục 8).

## DNA — dòng FIXED (hằng số trong Tool)

```
STYLE: photorealistic cinematic vertical video, shot on a full-frame cinema camera, 35mm
  lens, shallow depth of field, natural skin texture, realistic Vietnamese people, modern
  Vietnam. Looks like a high-quality Vietnamese web drama. Not anime, not cartoon, not 3D.
CAMERA: eye level, steady (tripod or slow dolly). Cuts only where the SHOTS say "CUT TO".
  No handheld shake, no drone, no fast zoom, no rotation.
MOTION: natural acting, real-time speed; lips move in sync with the spoken Vietnamese;
  blinking, breathing, small natural gestures. Faces and clothes never change.
AUDIO RULES: only the characters' spoken lines and quiet room tone. NO music. NO score.
  NO singing. NO narrator. NO extra voices. NO sound effects stings.
```

## SET_LOCK (T1) — dựng từ hồ sơ kênh

| Kiểu studio | SET_LOCK (chèn `{BIEN}` = chữ biển tên) |
|---|---|
| Podcast tối ấm (sample 1) | `A cozy podcast studio at night: behind the host a dark wall with a warm glowing neon sign that reads exactly "{BIEN}" with a small microphone icon, vertical wooden slat panels, shelves with books and small plants, a warm table lamp on the left. On the walnut desk: a black podcast microphone on a boom arm in front-left of the host, a white ceramic mug on a cork coaster, a small potted plant in the lower-left corner. Warm amber light, soft key light on the host's face.` |
| Văn phòng sáng (sample 2) | `A bright modern office: behind the host a white wall with large backlit blue 3D letters that read exactly "{BIEN}", light wooden shelves with plants and binders on both sides. On the light-wood desk: an open silver laptop at the right, a white pot with a green plant in the lower-left corner. Soft daylight, clean and professional.` |
| Phòng khách gia đình | `A warm Vietnamese living room: behind the host a wooden shelf with family photos, a small framed calligraphy, a vase of yellow chrysanthemums; a low wooden tea table with a teapot and cups in front. Soft warm afternoon light from a window on the right.` |
| Thư phòng gỗ | `A quiet study with dark wooden bookshelves full of old books, a brass desk lamp, a small bonsai, a cup of green tea on the desk. Low warm light, calm and wise.` |

`HOST_FRAME` (T1, chung mọi clip): `Medium shot from the chest up, the host seated behind the desk in the centre of the frame, looking straight into the camera, the sign fully visible above the head.`

## CHAR_LOCK + VOICE_LOCK — dàn diễn viên mặc định

Màn "Kênh" điền sẵn các đoạn này vào panel người: tách thành các ô Giới tính, Tuổi, Ngoại hình, Trang phục, Giọng nói, rồi dựng lại `CHAR_LOCK`/`VOICE_LOCK` theo `S6-S7-anh-va-clip.md`, mục "LOCK từ thông tin đã điền". Người dùng sửa được từng ô, hoặc tải ảnh lên (S4a điền lại Ngoại hình và Trang phục từ ảnh). Code chép **nguyên văn** đoạn của những mã có trong WHO của clip.

| Mã | CHAR_LOCK | VOICE_LOCK |
|---|---|---|
| `MC` | `MC: Vietnamese woman about 28, oval face, fair skin, long dark-brown wavy hair with a centre part, natural makeup, a white silk V-neck blouse with long sleeves.` | `MC: young Vietnamese woman, native Northern (Hà Nội) accent, warm, clear, friendly mid-pitch voice, calm and sincere like a podcast host, about 4 syllables per second.` |
| `MẸ_CHỒNG` | `MẸ_CHỒNG: Vietnamese woman about 58, round face, short dark hair in a low bun, a navy blouse with a large red-and-orange floral print, a thin gold necklace.` | `MẸ_CHỒNG: Vietnamese woman about 58, Northern accent, sharp, loud, slightly husky voice, speaks fast and bossy.` |
| `CON_DÂU` | `CON_DÂU: Vietnamese woman about 30, slim, long wavy brown hair below the shoulders, a white long-sleeve button shirt tucked into a black pencil skirt.` | `CON_DÂU: Vietnamese woman about 30, Northern accent, clear mid-high voice, controlled and firm, gets cold and calm when angry.` |
| `CHỒNG` | `CHỒNG: Vietnamese man about 33, short black hair with a side part, clean-shaven, a plain blue crew-neck T-shirt and grey trousers.` | `CHỒNG: Vietnamese man about 33, Northern accent, mid-low voice, hesitant, avoids conflict.` |
| `BỐ` | `BỐ: Vietnamese man about 62, short grey hair, thin face with smile lines, a beige collared shirt and dark trousers.` | `BỐ: Vietnamese man about 62, Northern accent, deep, slow, steady voice, few words.` |
| `EM_CHỒNG` | `EM_CHỒNG: Vietnamese woman about 25, shoulder-length straight black hair, light makeup, a pink fitted top and jeans, holds a phone.` | `EM_CHỒNG: young Vietnamese woman about 25, Northern accent, high, mocking, fast voice.` |
| `CON` | `CON: Vietnamese girl about 8, black hair in two low pigtails, a yellow T-shirt and light-blue shorts.` | `CON: Vietnamese girl about 8, Northern accent, small, soft child voice.` |

**POS mặc định** là cụm nhận diện ngắn dùng trong khối DIALOGUE và `{CAST_POS}`, giúp Veo biết ai đang nói:

| Mã | POS |
|---|---|
| `MC` | the host |
| `MẸ_CHỒNG` | the older woman in the floral blouse |
| `CON_DÂU` | the young woman in the white shirt |
| `CHỒNG` | the man in the blue T-shirt |
| `BỐ` | the grey-haired older man |
| `EM_CHỒNG` | the young woman in the pink top |
| `CON` | the little girl |

## Prompt dán vào bước S4 (chỉ cho T2; T1 bỏ qua bước agent này)

```
Write three lines, in English, describing the ONE location of this realistic Vietnamese
family drama. They will be pasted word for word into every image and video prompt, so
every line must be concrete and visual. Never write "same as before".

BRIEF:
{BRIEF}
Tone: {tone}

PLACE: the setting of BỐI CẢNH as a real modern Vietnamese place: 5–7 named objects and
  their positions (e.g. "a beige fabric sofa on the left, a glass coffee table, a dark
  wooden dining table in the foreground, large windows with sheer curtains and a city view
  at the back, framed paintings on a beige wall, a monstera plant"). Include ĐẠO CỤ CHÍNH.
LIGHT: time of day and light source in one line (e.g. "evening: warm ceiling downlights
  and soft daylight fading through the window").
AMBIENCE: 1–2 quiet sounds of the place, identical in every clip (e.g. "faint air
  conditioner hum, distant city traffic").

OUTPUT exactly three lines starting with PLACE:, LIGHT:, AMBIENCE: and nothing else.
```

**Mẫu đã duyệt** (sample 3, phòng khách chung cư):

```
PLACE: a modern Vietnamese apartment living room: a beige fabric sofa at the back left with
  a glass coffee table, a dark wooden dining table in the foreground, floor-to-ceiling
  windows with sheer white curtains and a city view at the back right, framed paintings
  on a beige wall, a large monstera plant, a printed divorce form lying on the table.
LIGHT: evening: warm recessed ceiling lights and soft daylight fading through the window.
AMBIENCE: faint air conditioner hum, distant city traffic.
```
