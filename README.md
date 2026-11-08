# VocabFlow — bản hoàn thiện thử nghiệm

## Có gì trong phiên bản này?
- Flashcard 2 mặt: click vào thẻ (hoặc Enter/Space) để lật, có hiệu ứng 3D.
- Spaced Repetition 4 mức: Quên / Khó / Nhớ / Dễ.
- Dashboard: từ mới hôm nay, lượt ôn, tổng từ, từ đã vững, streak và biểu đồ 7 ngày.
- Kho từ vựng: tìm kiếm, lọc, thêm, sửa, xóa; đọc phát âm bằng giọng có sẵn trong trình duyệt.
- Kiểm tra nhanh trắc nghiệm hai chiều Anh → Việt và Việt → Anh.
- Reading Lab: dán bài đọc/đoạn trích để tìm từ có ích và lưu câu ngữ cảnh.
- Bài đọc mới: danh sách bài đọc được lấy từ API công khai của News by Levels, có các link Level 1–3.
- Linear Writing: dùng từ trong câu, chuỗi ý tưởng và đoạn ngắn.
- Sao lưu/khôi phục JSON, mục tiêu từ mới mỗi ngày.
- PWA: có thể cài như ứng dụng và mở offline sau khi xuất bản qua HTTPS.

## Chạy thử trên máy
Mở `index.html` bằng Chrome hoặc Edge. Flashcard, từ vựng, thống kê và luyện viết hoạt động offline. Khi mở trực tiếp bằng `file://`, trình duyệt thường chặn tải `reading_feed.json`; lúc đó trang dùng danh sách mẫu được đóng gói sẵn.

Để thử đầy đủ chức năng tự cập nhật, hãy triển khai lên GitHub Pages theo hướng dẫn dưới đây.

## Tích hợp bài đọc tự động miễn phí bằng GitHub Actions

Cách này không yêu cầu API key và không cần máy chủ riêng:
1. Tạo tài khoản GitHub nếu chưa có.
2. Tạo một repository mới, ví dụ `vocabflow`.
3. Tải toàn bộ nội dung thư mục này lên repository, giữ nguyên thư mục `.github/workflows/`.
4. Vào **Settings → Pages**. Chọn **Deploy from a branch**, branch `main`, folder `/ (root)`, rồi Save.
5. Vào **Actions** và bật workflow nếu GitHub yêu cầu.
6. Mở workflow **Update reading feed** → **Run workflow** để chạy lần đầu.
7. Chờ workflow hoàn thành; sau đó mở website GitHub Pages. Hằng ngày workflow được lên lịch lúc 08:17 giờ Việt Nam (01:17 UTC), gọi API, cập nhật `reading_feed.json` và commit dữ liệu mới.

Workflow cũng có thể chạy thủ công từ tab Actions. Nếu không muốn chờ lịch tự động, chọn **Run workflow**. GitHub có thể làm chậm lịch chạy khi hệ thống bận; với repository công khai không có hoạt động trong 60 ngày, lịch tự động có thể bị tắt và cần bật lại trong Actions.

### Tại sao dùng News by Levels?
- News by Levels công bố RSS và API JSON công khai; API tìm kiếm trả về tối đa 20 bài mỗi yêu cầu, không cần tài khoản hay API key. Mỗi bài có các đường dẫn Level 1, 2, 3.
- VOA Learning English công bố RSS cho nhiều chuyên mục; bản tích hợp hiện lấy Science & Technology, Education, Health & Lifestyle và Words and Their Stories. Những bài này liên kết thẳng về bài gốc VOA.
- VocabFlow chỉ lưu tiêu đề, chủ đề, ngày đăng, tóm tắt ngắn trong feed và URL nguồn; không sao chép toàn văn bài báo.
- Script gọi các feed một lần mỗi ngày, có timeout; nếu không có dữ liệu hợp lệ thì giữ lại file feed cũ thay vì ghi đè bằng danh sách rỗng.

## Giới hạn cần biết
- Tự động cập nhật danh sách bài đọc và link đọc, không đồng nghĩa tự động tải hoặc sao chép toàn văn bài đọc. Mở nguồn, chọn đoạn trích rồi dán vào Reading Lab để phân tích từ.
- Các định nghĩa, bản dịch tiếng Việt, IPA và collocations trong kho cần người học bổ sung/kiểm tra. Phiên bản này không gọi AI trả phí.
- Dữ liệu học tập đang nằm trong trình duyệt (localStorage), không tự đồng bộ sang thiết bị khác. Dùng Xuất/Nhập dữ liệu để chuyển bản sao lưu.
- Muốn có tài khoản và đồng bộ nhiều thiết bị, cần thêm backend/auth như Supabase; đó là bước phát triển sau.

## Thêm nguồn bài đọc khác
Mở `update_reading.py`, bổ sung RSS/API hợp pháp vào `VOA_FEEDS` hoặc viết hàm parser riêng, sau đó chuẩn hóa từng bài về cấu trúc:
`title`, `topic`, `summary`, `date_published`, `reading_urls`, `source_name`.
Không scrape/paywall hoặc tái xuất bản nội dung nếu điều khoản nguồn không cho phép. Giữ link nguồn và attribution.


## Lưu ý về quyền riêng tư khi xuất bản
GitHub Pages trên gói Free yêu cầu repository công khai. Website được công khai trên Internet, nhưng tiến độ học và từ vựng cá nhân chỉ nằm trong localStorage của trình duyệt; không đưa file JSON sao lưu hoặc dữ liệu cá nhân lên repository.
