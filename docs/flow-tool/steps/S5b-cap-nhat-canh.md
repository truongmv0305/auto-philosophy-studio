# S5b — Cập nhật cảnh khi sửa thoại 1 clip (agent, 0 credit)

**Chạy khi:** bấm "Lưu thoại" trên thẻ i ở màn 3, hoặc thoại thẻ i đổi ở màn 2 khi đã có storyboard.
**Input:** `BRIEF`, `SCENE_i` hiện tại, `LINE_i` mới, `{CAST_POS}`, `{PLACE}`, `{template}` · **Output:** `SCENE_i` mới, cùng định dạng S5
**Sau đó:** thẻ i đánh dấu "Cần tạo lại" cho ảnh và video. Không tự tạo lại.

```
The dialogue of clip {i} changed. Update its scene so the picture matches the new words.
Keep everything that still fits (positions, framing, place, light). Change only what
the new dialogue needs (who is visible, who speaks when, gesture, emotion, shots).

BRIEF:
{BRIEF}
Template: {template}
CAST: {CAST_POS}
PLACE / SET: {PLACE}
CURRENT SCENE:
{SCENE_i}
NEW DIALOGUE OF CLIP {i} ("CODE: text | CODE: text"):
{LINE_i}

Rules: every speaker in the new dialogue must be in WHO; follow the S5 rules of the
template (T1: one shot, one gesture; T2: 1–3 shots with time ranges, no violence).
Do not copy the dialogue into the output.

OUTPUT exactly one block:
=== SCENE {i} ===
CẢNH: ...
WHO: ...
SHOTS: ...
START: ...
ACTION: ... Hold.
EMOTION: ...
```
