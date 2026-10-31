# Thực hành buổi 3 - Lập trình Python với giao thức CoAP

## 1. Thông tin thực hiện

- **Trần Hữu Nhật** - B23DCCN627 (Bài 1)
- **Trần Đăng Ninh** - B23DCCN634 (Bài 2)
- **Trần Tiến Đạt** - B23DCCN151 (Bài 3)

## 2. Môi trường và thư viện

- Python 3.x (khuyến nghị từ 3.10 trở lên)
- Thư viện `aiocoap`
- Các thư viện có sẵn trong Python: `asyncio`, `json`, `datetime`, `random`
- Giao thức: CoAP trên UDP, cổng 5683

Kiểm tra phiên bản Python và cài thư viện:

```bash
python --version
python -m pip install aiocoap
```

Các chương trình được cấu hình chạy trên cùng một máy bằng địa chỉ `127.0.0.1`. Nếu chạy trên hai máy khác nhau, cần thay địa chỉ trong các file Client thành IP của máy Server, đồng thời chỉnh địa chỉ bind của Server và mở cổng UDP 5683 trên tường lửa.

## 3. Cấu trúc thư mục

```text
CoAP_Lab/
├── bai1/
│   ├── coap_server_bai1.py
│   └── coap_client_bai1.py
├── bai2/
│   ├── sensor_server_bai2.py
│   └── monitor_client_bai2.py
├── bai3/
│   ├── light_server_bai3.py
│   ├── light_controller_bai3.py
│   └── light_monitor_bai3.py
├── requirements.txt
└── README.md
```

## 4. Địa chỉ tài nguyên

| Bài | Địa chỉ URI                                    | Phương thức       |
| --- | ---------------------------------------------- | ----------------- |
| 1   | `coap://127.0.0.1:5683/iot/lab/message`        | GET, POST         |
| 2   | `coap://127.0.0.1:5683/iot/lab/sensor01/data`  | GET               |
| 3   | `coap://127.0.0.1:5683/iot/lab/light01/status` | GET, PUT, Observe |

Trong đề dùng `localhost`; trên máy chạy chương trình, `127.0.0.1` là địa chỉ loopback IPv4 tương ứng. Cả ba Server đều sử dụng cổng UDP 5683, vì vậy chỉ chạy một Server tại một thời điểm.

## 5. Bài 1 - Gửi và nhận thông điệp CoAP

**Nội dung:** Server cung cấp tài nguyên `/iot/lab/message`. Client gửi yêu cầu GET để nhận lời chào và gửi POST kèm họ tên, mã sinh viên và nội dung thông điệp. Server hiển thị thời điểm nhận và phản hồi xác nhận.

Mở hai Terminal tại thư mục gốc của dự án.

Terminal 1:

```bash
python bai1/coap_server_bai1.py
```

Terminal 2:

```bash
python bai1/coap_client_bai1.py
```

Nhập họ tên và mã sinh viên theo hướng dẫn của Client. Chương trình lần lượt gửi GET, POST và hiển thị mã phản hồi cùng payload.

Kết quả đầu ra mong đợi:

```text
Sending GET request...
Response:
Code: 2.05 Content
Payload: Xin chao tu CoAP Server

Sending POST request...
Response:
Code: 2.04 Changed
Payload: Server da nhan thong diep
```

## 6. Bài 2 - Mô phỏng cảm biến nhiệt độ và độ ẩm

**Nội dung:** Server mô phỏng cảm biến `sensor01`, cập nhật nhiệt độ và độ ẩm ngẫu nhiên sau mỗi 3 giây. Client gửi GET định kỳ 3 giây để nhận dữ liệu JSON và kiểm tra ngưỡng cảnh báo.

Terminal 1:

```bash
python bai2/sensor_server_bai2.py
```

Terminal 2:

```bash
python bai2/monitor_client_bai2.py
```

Payload trả về có dạng:

```json
{
  "device_id": "sensor01",
  "temperature": 28.5,
  "humidity": 65.2
}
```

Dữ liệu sử dụng Content-Format `application/json` (50). Nếu nhiệt độ lớn hơn 35°C, Client thông báo `CANH BAO: Nhiet do cao`; nếu độ ẩm nhỏ hơn 40%, Client thông báo `CANH BAO: Do am thap`. Khi không vượt ngưỡng, Client hiển thị `Trang thai: Binh thuong`.

Ví dụ định dạng kết quả hiển thị:

```text
[09:05:12] Received sensor data
Device: sensor01
Temperature: 36.5 C
Humidity: 35.2 %
CANH BAO: Nhiet do cao
CANH BAO: Do am thap
------------------------------
```

Nhấn `Ctrl+C` để dừng chương trình giám sát.

## 7. Bài 3 - Giám sát và điều khiển đèn thông minh

**Nội dung:** Server mô phỏng đèn `light01`, có trạng thái ban đầu `OFF`. Client điều khiển sử dụng GET/PUT; Client giám sát đăng ký Observe để tự động nhận trạng thái mới khi đèn thay đổi.

Mở ba Terminal tại thư mục gốc của dự án.

Terminal 1 - Server:

```bash
python bai3/light_server_bai3.py
```

Terminal 2 - Monitoring Client:

```bash
python bai3/light_monitor_bai3.py
```

Terminal 3 - Controller Client:

```bash
python bai3/light_controller_bai3.py
```

Các lệnh của Controller:

| Lệnh     | Chức năng               |
| -------- | ----------------------- |
| `ON`     | Bật đèn bằng PUT        |
| `OFF`    | Tắt đèn bằng PUT        |
| `STATUS` | Xem trạng thái bằng GET |
| `EXIT`   | Thoát Controller        |

Ví dụ payload điều khiển gửi bằng PUT:

```json
{ "device_id": "light01", "command": "ON" }
```

Payload trạng thái GET/Observe:

```json
{ "device_id": "light01", "status": "ON" }
```

Kết quả đầu ra mong đợi ở Monitoring Client:

```text
Registering CoAP Observe...
Observe registration successful

[10:30:00] Initial State
Device: light01
Status: OFF

[10:30:15] State Updated
Device: light01
Status: ON
```

Monitoring Client không gửi GET liên tục. Sau khi đăng ký Observe, Client nhận thông báo mỗi khi trạng thái thực sự thay đổi. Gửi lại cùng một lệnh ON hoặc OFF sẽ không tạo thông báo trạng thái mới. Có thể mở thêm Monitoring Client để kiểm tra nhiều người cùng theo dõi.

Nhấn `Ctrl+C` để dừng Monitoring Client và Server.

## 8. Kết quả và kiểm tra

- Bài 1: Server xử lý GET, POST và trả lời đúng mã phản hồi `2.05 Content`, `2.04 Changed`.
- Bài 2: Dữ liệu trả về là JSON, cập nhật trên Server sau mỗi 3 giây; Client truy vấn và cảnh báo theo điều kiện nhiệt độ, độ ẩm.
- Bài 3: GET trả về trạng thái hiện tại; PUT thay đổi trạng thái và phản hồi `2.04 Changed`; các Client Observe nhận thông báo khi có thay đổi.
- Trường hợp lỗi: thử tắt Server rồi chạy Client để kiểm tra thông báo lỗi, hoặc gửi lệnh không hợp lệ ở Controller.

Các khối log ở trên là **ví dụ định dạng đầu ra**, không phải log kiểm thử được ghi lại trong lần đóng gói này. Khi chạy thực tế, lưu ảnh Terminal hoặc sao chép log của Server và Client cho từng bài để bổ sung minh chứng vào repository GitHub theo yêu cầu nộp bài.

## 9. Nộp bài

Đưa toàn bộ thư mục `CoAP_Lab` lên GitHub, gồm các file Python và README. Trước khi nộp, kiểm tra lại thông tin sinh viên, chạy từng bài và bổ sung ảnh/log thực tế vào repository.
