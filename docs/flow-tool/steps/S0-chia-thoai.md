# S0 — Chia kịch bản có sẵn thành clip (code trong Tool, 0 credit)

**Chạy khi:** người dùng dán vào ô **"Kịch bản có sẵn"** ở màn 1. Để trống thì AI tự viết qua S1 → S2 → S3.
**Input:** `SCRIPT`, `{template}` · **Output:** `CLIPS[1..N]`, mỗi clip là một danh sách dòng `{who, text}`
**Vì sao làm bằng code:** agent hay "sửa giùm" chữ. Chia bằng code thì ghép các clip lại đúng bằng kịch bản gốc.

Lấy lại quy hoạch động của auto-ns-v3 (`auto-ns-v3/docs/flow-tool/steps/S0-chia-loi-thoai.md`), thêm phần **người nói** cho T2.

## Định dạng một clip (dùng ở mọi nơi sau S0)

```
CLIPS[i] = [ {who: "MẸ_CHỒNG", text: "Cô ký vào đây đi."}, {who: "CON_DÂU", text: "Con không ký."} ]
LINE_i (chuỗi) = các dòng nối bằng " | ", mỗi dòng "WHO: text"
               = "MẸ_CHỒNG: Cô ký vào đây đi. | CON_DÂU: Con không ký."
```

- T1: mọi dòng có `who = "MC"`.
- `LINE_i` chính là một dòng của `thoai.txt` mà `scripts/ghep.py` đọc.

## Quy tắc

1. **Đếm tiếng** = số từ tách theo khoảng trắng. Chỉ đếm phần `text`, không đếm tên người nói.
2. **Đọc kịch bản:**
   - **T1:** cả ô là lời MC.
   - **T2:** mỗi dòng có dạng `TÊN: lời` (hoặc `TÊN : "lời"`).
     - TÊN được so với mã trong dàn diễn viên đã chọn, không phân biệt hoa thường, dấu, khoảng trắng hay `_`. Ví dụ "Mẹ chồng" = `MẸ_CHỒNG`.
     - Dòng không có tên thì gộp vào lời của dòng trước.
     - Tên lạ thì báo "Dòng k: không có nhân vật <TÊN> trong dàn diễn viên" và không chia.
3. **Tách mẩu:**
   - Mỗi dòng thoại là một mẩu.
   - Mẩu > 28 tiếng thì cắt sau `.` `?` `!` `…`, rồi `,` `;` `:`, rồi ở ranh giới từ (≤ 26 tiếng). Các mẩu sau khi cắt giữ cùng `who`.
4. **Gom mẩu thành clip:**
   - Mỗi clip ≤ **30** tiếng (T1) hoặc ≤ **26** tiếng (T2).
   - T2: mỗi clip ≤ **3** dòng và ≤ **2** người nói khác nhau. Nếu F‑B FAIL thì đổi thành 1 người nói.
   - Dùng ít clip nhất, rồi chọn cách chia đều nhất. Quy hoạch động trên danh sách mẩu.
5. **Cảnh báo (không tự sửa):**

   | Khi | Báo |
   |---|---|
   | Clip < 14 tiếng, không phải clip cuối | "Clip i ngắn (x tiếng), có thể gộp" |
   | Có chữ số | "Nên viết số thành chữ" |
   | Có chữ Latin viết hoa liền ≥ 3 ký tự (BHXH, CCCD) | "Viết tắt sẽ bị đọc sai, nên viết đủ: bảo hiểm xã hội" |
   | N > 6 | "Video dài N×8s, nên tách thành Phần 1 / Phần 2" |

## Ví dụ T2

Dán:

```
Mẹ chồng: Cô ký vào đây đi, nhà này không chứa nổi loại con dâu như cô.
Con dâu: Mẹ nói đúng. Con sẽ ký.
Con dâu: Nhưng mẹ đọc kỹ giùm con, căn nhà này đứng tên ai.
Mẹ chồng: Cô nói cái gì?
```

Mẩu: MẸ_CHỒNG 15 · CON_DÂU 6 · CON_DÂU 12 · MẸ_CHỒNG 4. Kết quả:

```
1 | MẸ_CHỒNG: Cô ký vào đây đi, nhà này không chứa nổi loại con dâu như cô. | CON_DÂU: Mẹ nói đúng. Con sẽ ký. | 21
2 | CON_DÂU: Nhưng mẹ đọc kỹ giùm con, căn nhà này đứng tên ai. | MẸ_CHỒNG: Cô nói cái gì? | 16
```
