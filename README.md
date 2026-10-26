# Demo mái che thông minh với C4.5

Đây là mô hình mô phỏng để trình bày luồng **dữ liệu cảm biến → cây quyết định C4.5 → lệnh điều khiển**. Chưa kết nối ESP32, cảm biến hay động cơ thật.

## Chạy demo
Yêu cầu Python 3.10 trở lên; không cần cài thư viện ngoài.

```powershell
cd work/smart_canopy_c45
python demo.py
```

Chương trình in số dòng dữ liệu, độ chính xác trên tập kiểm tra, cây đã học và bốn tình huống mẫu. Sau đó có thể nhập tình huống khác.

## Dữ liệu
`data/smart_canopy_demo.csv` được sinh bởi `generate_data.py`. Đây là dữ liệu mô phỏng có nhãn theo quy tắc trong mã, không phải số đo thật hay kết quả khảo sát. Thuộc tính được chia nhóm `THAP/VUA/CAO`, `MAT/NONG`, `CO/KHONG`.

Quy tắc nhãn: có mưa thì đóng nếu mái đang mở, còn mái đã đóng thì giữ nguyên; không mưa và ánh sáng cao thì mở nếu mái đang đóng, còn mái đã mở thì giữ nguyên; tình huống khác giữ nguyên. Đây chỉ là quy tắc giả định cho demo, cần thống nhất lại khi làm mô hình thật.

## Phần C4.5
`src/c45.py` cài cây quyết định rời rạc bằng entropy, Information Gain Ratio và chọn thuộc tính có Gain Ratio cao nhất. Chia tập huấn luyện/kiểm tra cố định để lặp lại kết quả. Bản này chưa bao gồm xử lý giá trị thiếu hay cắt tỉa cây đầy đủ như các triển khai C4.5 hoàn chỉnh.

Đầu ra hiện chỉ là chữ trên màn hình. Nếu nối với cơ cấu thật, công tắc hành trình, dừng khẩn cấp, bảo vệ quá dòng và điều khiển tay phải được xử lý độc lập, ưu tiên hơn dự đoán.

Độ chính xác 100% trong ví dụ này chỉ cho thấy cây đã khớp nhãn do quy tắc mô phỏng tạo ra; không chứng minh hệ thống hoạt động tốt ngoài thực tế.
