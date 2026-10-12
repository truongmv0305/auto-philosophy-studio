# assets/

| Thư mục / file | Dùng cho | Ghi chú |
|---|---|---|
| `fonts/BeVietnamPro-ExtraBold.ttf` | `scripts/ghep.py` vẽ watermark và hook | Tải từ Google Fonts (OFL). Không có file này thì `ghep.py` dùng Arial Bold của hệ thống |
| `channel/<kenh>/studio.png`, `host.png`, `host_studio.png` | Bản lưu ảnh hồ sơ kênh tải từ Flow | Để dựng lại kênh khi đổi project hoặc tài khoản |
| `channel/<kenh>/char_<MÃ>.png` | Ảnh tham chiếu dàn diễn viên | Một ảnh mỗi mã, toàn thân, nền xám |
| `channel/<kenh>/upload_<MÃ>.jpg` | Ảnh gốc bạn tải lên cho MC/diễn viên (tuỳ chọn) | Chỉ ảnh của bạn hoặc người đã đồng ý. Nên rõ mặt, nhìn thẳng, ánh sáng đều, một người trong khung |
| `channel/<kenh>/profile.json` | Bản sao hồ sơ kênh (nút "Sao chép hồ sơ (JSON)" ở màn 0) | Tên, watermark, biển, kiểu studio, CHAR_LOCK, VOICE_LOCK, POS |

**Không** đưa vào repo ảnh, logo, tên hay SĐT của kênh khác. Thư mục `sample/` chỉ để tham khảo phong cách.

Dàn diễn viên mặc định (mã, CHAR_LOCK, VOICE_LOCK) nằm ở `docs/flow-tool/steps/S4-khoi-lock.md`.
