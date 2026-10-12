# S3 — Căn chỉnh số tiếng (agent, 0 credit, **luôn chạy** khi AI viết thoại)

**Input:** `DRAFT` (N dòng từ S2), `{template}` · **Output:** `FINAL` (N dòng) → `CLIPS[1..N]`
**Kiểm lại bằng code** sau bước này: Tool tự đếm lại tiếng mỗi clip và tô màu bộ đếm ở màn 2. Không tin số agent ghi.

```
You are a strict Vietnamese script editor. Check and fix the rows below. Keep the same
number of rows, the same order, the same speakers and the same meaning.

Template: {template}
DRAFT:
{DRAFT}

For EACH row:
1. Count syllables yourself: split the text of every line on spaces and count the pieces.
   Do not count the CODE before ":". Ignore the count written in the draft.
2. Target: T1 26–30 (last row 22–27) · T2 16–26 (last row 12–24). Rewrite lines outside the target while
   keeping their speaker, meaning and the concrete detail.
3. T2: at most 3 lines and at most 2 different speakers per row. Move or merge lines if not.
4. Row 1: its first sentence must be ≤ 12 syllables.
5. Replace digits with Vietnamese words, write abbreviations out, remove quotes, English
   words and emoji.
6. Each line ends with . ? or ! . Recount after every rewrite.

OUTPUT N rows, nothing else:
<i> | <BEAT> | <CODE: text | CODE: text> | <recounted syllables>
Then one last line: TỔNG: <sum>
```

**Parse (code):** chỉ lấy dòng `<số> | <beat> | <thoại> | <số>`. Bỏ dòng `TỔNG`. Tách thoại theo ` | ` rồi theo `CODE:` đầu dòng thành `{who, text}`. `who` không có trong NHÂN VẬT thì đánh dấu đỏ ở màn 2.
