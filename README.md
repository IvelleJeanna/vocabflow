# VocabFlow — phiên bản nâng cấp bộ từ vựng

## Có gì mới?

Phiên bản này mở rộng Kho từ vựng thành hệ thống quản lý bộ học, đồng thời giữ lại các tính năng hiện có (Flashcard, SRS, Quiz, Reading Lab, bài đọc, Linear Writing, sao lưu/khôi phục và PWA).

- Có sẵn các khung bộ: Global Success 12 (Unit 1–10), THPT lớp 10–12, IELTS, TOEIC, Academic English.
- Có bộ CEFR A1, A2, B1, B2, C1, C2 và các bộ theo chủ đề.
- Mỗi mục từ có thể được gán vào nhiều bộ cùng lúc.
- Phân loại theo dạng: từ vựng, collocation, phrasal verb, idiom, phrase/expression, word family, academic phrase.
- Thêm mục từ với CEFR, nguồn học, Unit, chủ đề, IPA, nghĩa, collocations, họ từ, ví dụ và ghi chú.
- Tạo bộ cá nhân, lọc kho theo bộ/cấp độ/dạng/trạng thái học.
- Học flashcard theo từng bộ; làm quiz trên toàn kho hoặc một bộ.
- Nhập hàng loạt bằng TSV: Từ → Nghĩa → CEFR → Dạng → Chủ đề → Ví dụ → Collocations. Có nút tải tệp mẫu ngay trong ứng dụng.
- Tự động nâng cấp dữ liệu localStorage phiên bản cũ: từ đã lưu, lịch sử ôn tập, bài đọc và bài viết được giữ nguyên; trường phân loại mới được bổ sung mặc định.

## Lưu ý về nội dung từ vựng

Các bộ Global Success 12, THPT, IELTS, CEFR và chủ đề được tạo sẵn dưới dạng **khung phân loại**, không phải danh sách từ vựng đầy đủ đã được xác minh. Một số mục mẫu cũ trong VocabFlow được gắn nhãn B2 để minh họa; CEFR có thể thay đổi theo ngữ cảnh và nguồn. Khi bổ sung bộ sách/đề thi, hãy đối chiếu với tài liệu gốc. Không nên tự động coi mọi từ trong một chủ đề là cùng cấp độ.

## Cập nhật website GitHub Pages đang có

1. Tải và giải nén `VocabFlow_Upgrade_Package.zip`.
2. Mở thư mục `vocabflow_package` vừa giải nén.
3. Sao chép **toàn bộ nội dung bên trong** thư mục này, bao gồm thư mục ẩn `.github`, vào thư mục repository `vocabflow` trên máy tính. Không đặt thêm một lớp thư mục `vocabflow_package` trong repository.
4. Khi Windows hỏi có ghi đè các tệp trùng tên không, chọn **Replace the files in the destination**. Đây là cập nhật mã nguồn, không phải xóa dữ liệu học trong trình duyệt.
5. Mở GitHub Desktop. Repository `vocabflow` sẽ hiển thị các thay đổi. Kiểm tra danh sách tệp, nhập Summary: `Upgrade vocabulary collections and filters`, chọn **Commit to main**, sau đó **Push origin**.
6. Mở website GitHub Pages và tải lại mạnh bằng `Ctrl + F5`. Nếu giao diện cũ còn xuất hiện, đóng tab website rồi mở lại; service worker đã được tăng phiên bản cache để trình duyệt tải bản mới.

## Quan trọng: sao lưu trước khi cập nhật

Trước khi thay mã nguồn, mở website hiện tại → bấm **Xuất dữ liệu** ở góc trên để tải bản JSON sao lưu. Bản nâng cấp dùng cùng khóa lưu trữ `vocabflow_v1`, có cơ chế bổ sung trường mới và giữ dữ liệu học đang có. Dù vậy, hãy luôn giữ file JSON dự phòng. Không đưa file backup cá nhân lên repository công khai.

## Sử dụng sau cập nhật

- Vào **Kho từ vựng & bộ học** để duyệt các bộ có sẵn.
- Chọn **Mở bộ** để lọc các mục từ thuộc bộ; chọn **Học bộ** để tạo phiên flashcard riêng.
- Chọn **Tạo bộ** để lập bộ riêng.
- Chọn **Thêm mục từ** để thêm một mục; đánh dấu những bộ mà mục từ đó thuộc về.
- Chọn **Nhập danh sách hàng loạt** để dán TSV và gán cả loạt từ vào một bộ.
- Trong **Kiểm tra nhanh**, chọn bộ muốn làm quiz.

## Chạy thử trên máy

Mở `index.html` bằng Chrome hoặc Edge. Học từ, flashcard, kho từ, bộ học và quiz có thể chạy cục bộ. Một số chức năng lấy dữ liệu bài đọc cần được chạy qua HTTPS/GitHub Pages.

## Những giới hạn hiện tại

- Dữ liệu vẫn lưu trong localStorage của từng trình duyệt/thiết bị; chưa có tài khoản hoặc đồng bộ đám mây.
- Các bộ từ chưa tự tải hàng nghìn mục từ từ sách hoặc nguồn thương mại. Bạn có thể nhập danh sách do mình có quyền sử dụng.
- CEFR cần được xác định dựa trên từ điển/danh mục đáng tin cậy; nhãn mẫu chỉ để khởi đầu và không thay thế kiểm chứng.
- Bài đọc tự động vẫn chỉ hiển thị dữ liệu/link nguồn, không tải hay sao chép toàn văn bài báo.

## Cấu trúc gói

```text
vocabflow_package/
  index.html
  reading_feed.json
  update_reading.py
  sw.js
  manifest.webmanifest
  icon.svg
  README.md
  .github/workflows/update-reading.yml
```
