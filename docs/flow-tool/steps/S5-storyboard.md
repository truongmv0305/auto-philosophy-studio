# S5 — Storyboard (agent, 0 credit)

**Input:**
- `BRIEF`
- `{CLIPS}`: N dòng `i | LINE_i`
- `{CAST_POS}`: mã diễn viên kèm một cụm nhận diện ngắn lấy từ CHAR_LOCK, ví dụ `MẸ_CHỒNG = older woman in a floral blouse`
- `DNA.PLACE` (T2) hoặc `SET_LOCK` (T1)
- `{aspect}`

**Output:** `SCENE_1..N`. Mỗi cảnh gồm: CẢNH, WHO, SHOTS, ACTION, EMOTION.

Như auto-ns: S5 **không chép thoại, không viết prompt đầy đủ**. Code ghép prompt lúc bấm nút (`S6-S7-anh-va-clip.md`).

```
You are the director of a realistic Vietnamese short drama / podcast video. For each of the
N clips below (8 seconds each), design what the camera shows. Do not copy the dialogue
into your output and do not write full prompts.

BRIEF:
{BRIEF}
CLIPS (N = {N}; clip i is spoken exactly as written, "CODE: text | CODE: text"):
{CLIPS}
CAST (code = how to recognise them): {CAST_POS}
PLACE / SET: {PLACE}
Aspect ratio: {aspect}

TEMPLATE T1 (only MC):
- Every clip is the same framing (medium shot, host centred behind the desk, sign visible).
- SHOTS has ONE shot: "medium shot, static" or "medium shot, very slow push-in".
- Vary only the gesture: choose a different one for each clip from: resting chin on one
  hand and listening, raising one index finger, opening both hands to explain, a small
  warm smile with hands folded on the desk, tilting the head with a knowing look, a hand
  on the chest. The gesture must fit the line.
TEMPLATE T2:
- WHO = every character visible in the clip (all speakers must be visible).
- SHOTS: 1–3 shots that together last 8 seconds, separated by " CUT TO ". Start the clip
  with a shot that shows the speakers together; then cut to a close-up of whoever speaks
  the key line, and/or the reaction of the listener. Give each shot a time range.
  Example: "(0–3s) medium-wide, the three standing around the dining table CUT TO (3–6s)
  close-up MẸ_CHỒNG pointing at the camera CUT TO (6–8s) close-up CON_DÂU, shocked".
- Positions stay consistent across clips (who stands left / right).
- Big but non-violent acting: pointing, slamming a palm on the table, throwing papers on
  the table, arms crossed, turning away, tears in the eyes. Never hitting, pushing,
  weapons or blood.
- A document or object that is read on screen is shown at an angle; never a close-up of
  text.

OUTPUT, for i = 1..N, exactly this block and nothing else:
=== SCENE i ===
CẢNH: <one short Vietnamese sentence shown to the user on the card>
WHO: <codes of visible characters, comma-separated>
SHOTS: <English, as described above, one line>
START: <English, 2–3 sentences: the very first frame of the clip — who stands where, pose,
  facial expression, where the main prop is. This becomes the start image.>
ACTION: <English, 1–2 sentences: what bodies do during the clip, in time order, matching
  who speaks when. End with "Hold.">
EMOTION: <CODE = emotion for each visible character, e.g. "MẸ_CHỒNG = furious, CON_DÂU =
  hurt but calm">
```

**Parse (code):** mỗi trường lấy từ sau nhãn tới nhãn kế tiếp, hoặc tới dòng `===`, hoặc tới hết. Dòng gãy thì nối bằng dấu cách. ACTION dừng ở `Hold.` đầu tiên. Xoá khỏi START/ACTION mọi đoạn trùng với một dòng thoại (giống auto-ns Phần 0k).

## Mẫu (sample 3, clip 2)

```
=== SCENE 2 ===
CẢNH: Mẹ chồng chỉ thẳng mặt con dâu, chồng đứng sau lưng mẹ, con dâu sững người.
WHO: MẸ_CHỒNG, CON_DÂU, CHỒNG
SHOTS: (0–4s) medium shot, MẸ_CHỒNG in front with CHỒNG behind her shoulder, CON_DÂU's back
  on the right edge CUT TO (4–8s) close-up MẸ_CHỒNG pointing straight at the camera
START: In the living room, MẸ_CHỒNG stands in the centre-left, right index finger raised
  toward CON_DÂU at the right edge; CHỒNG stands just behind MẸ_CHỒNG's left shoulder,
  looking smug. The divorce form lies on the dining table in the foreground.
ACTION: MẸ_CHỒNG jabs her finger forward as she speaks; CHỒNG nods slightly; after the
  cut she leans toward the camera, frowning. Hold.
EMOTION: MẸ_CHỒNG = furious and contemptuous, CHỒNG = smug, CON_DÂU = stunned
```
