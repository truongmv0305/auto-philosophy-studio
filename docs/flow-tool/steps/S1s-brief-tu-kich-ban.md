# S1s — BRIEF từ kịch bản có sẵn (agent, 0 credit)

**Input:** `{template}`, `{cast}`, `{N}`, `{CLIPS}` (từ S0, đánh số `i | LINE_i`) · **Output:** `BRIEF` cùng định dạng S1, `SỐ CLIP` = N
**Chạy khi:** ô "Kịch bản có sẵn" có chữ. **Không đổi một chữ nào của thoại.**

```
You are the head writer of a Vietnamese "đạo lý" short-video channel. The user already
wrote the dialogue. Do NOT change, add or remove any word of it. Read it and write the
BRIEF that the storyboard team needs. Write in Vietnamese.

Template: {template}
Cast: {cast}
Number of clips N = {N}. Dialogue, one numbered row per clip ("WHO: text | WHO: text"):
{CLIPS}

OUTPUT exactly the fields of the S1 BRIEF, in the same order:
TIÊU ĐỀ, SỐ CLIP (= {N}), SLUG, TEMPLATE, GÓC NHÌN, LOGLINE, NHÂN VẬT, BỐI CẢNH,
ĐẠO CỤ CHÍNH, CÚ LẬT, THÔNG ĐIỆP, HOOK CHỮ, BEAT 1..{N}.
- NHÂN VẬT lists only the codes that appear as WHO in the dialogue (T1: only MC).
- BEAT i describes clip i of the dialogue above: who speaks, the essence, what we SEE.
- If the dialogue implies a place, use it in BỐI CẢNH; otherwise choose one that fits.
```
