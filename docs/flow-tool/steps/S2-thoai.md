# S2 — Viết thoại theo clip (agent, 0 credit)

**Input:** `BRIEF`, `{kenh_xung_ho}` (T1: MC xưng gì, gọi khán giả là gì) · **Output:** `DRAFT` (N dòng)
**Sau bước này luôn chạy S3.**

```
Write the spoken Vietnamese for each clip of the BRIEF below. Every word you write will
be SPOKEN ON SCREEN by a character with lip-sync in an 8-second clip, so it must sound
like real, natural Northern Vietnamese speech.

BRIEF:
{BRIEF}
Host form of address (T1): {kenh_xung_ho}

RULES FOR BOTH TEMPLATES
- One row per clip, in BEAT order, exactly N rows.
- Each spoken line is "CODE: text". CODE is one of the codes in NHÂN VẬT. T1: always "MC".
- Several lines in one clip are joined with " | ".
- Budget per clip (count syllables = words separated by spaces, do not count the CODE):
    T1: 26–30 syllables, one line or two lines of the MC.
    T2: 16–26 syllables (drama needs pauses for reactions), at most 3 lines and at most
        2 different speakers in one clip.
- First clip: the first sentence is ≤ 12 syllables and grabs attention.
- Last clip: T1 22–27 syllables, T2 12–24.
- Write numbers as Vietnamese words ("ba trăm triệu", not "300 triệu"). Write
  abbreviations out ("bảo hiểm xã hội", not "BHXH"). No English, no emoji, no quotes
  inside the text.
- Every line ends with . ? or ! and does not continue into the next clip.
- Spoken style: short sentences, natural particles (à, đấy, mà, chứ, nhé), how people
  really talk; no literary phrasing, no proverbs copied word for word.
T1
- The MC talks TO the viewer ({kenh_xung_ho}), warm and sincere, like a podcast.
- Last clip ends with a gentle call ("Nếu thấy đúng, hãy theo dõi kênh để nghe tiếp nhé.")
  only if it fits in the budget.
T2
- Sharp, emotional, but no swearing beyond "cái loại", "đồ", "hỗn". No threats of violence.
- Each speaker sounds like their age and role (mẹ chồng: "cô", "nhà này"; con dâu: "con",
  "mẹ"; chồng: "anh", "em", "mẹ").
- The reveal (CÚ LẬT) is said in ONE clear sentence that anyone understands.

OUTPUT N rows, nothing else:
<i> | <BEAT name> | <CODE: text | CODE: text> | <syllable count>
```
