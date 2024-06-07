# Ứng dụng quản lý đơn hàng

Ứng dụng quản lý đơn hàng là một ứng dụng web được xây dựng bằng Python và sử dụng thư viện Streamlit để tạo giao diện người dùng. Ứng dụng này kết nối với cơ sở dữ liệu Larkbase để lấy thông tin khách hàng và sản phẩm, cho phép người dùng tạo và quản lý các đơn hàng.

## Tính năng

- Lấy danh sách khách hàng và sản phẩm từ Larkbase
- Thêm mới khách hàng hoặc chọn khách hàng từ danh sách
- Thêm sản phẩm vào đơn hàng
- Tính tổng tiền đơn hàng
- Nhập thông tin tiền cọc, phí công thợ, phí vận chuyển, phụ thu và ghi chú đơn hàng
- Lưu đơn hàng và gửi thông tin đến webhook

## Yêu cầu hệ thống

- Python 3.6 trở lên
- Các thư viện được liệt kê trong file `requirements.txt`

## Cài đặt

1. Clone repository về máy tính của bạn:

   ```
   git clone https://github.com/your-username/order-management-app.git
   ```

2. Di chuyển vào thư mục dự án:

   ```
   cd order-management-app
   ```

3. Tạo và kích hoạt môi trường ảo (virtual environment):

   ```
   python -m venv venv
   source venv/bin/activate
   ```

4. Cài đặt các thư viện cần thiết:

   ```
   pip install -r requirements.txt
   ```

5. Cấu hình các biến môi trường:

   - Tạo file `.env` trong thư mục gốc của dự án. (HOẶC .streamlit/secrets.toml)
   - Thêm các biến môi trường cần thiết vào file `.env`, bao gồm:
     - `LARK_APP_ID`: ID của ứng dụng Lark
     - `LARK_APP_SECRET`: Secret của ứng dụng Lark
     - `LARK_APP_TOKEN`: Token của ứng dụng Lark
     - `TABLE_CUSTOMER_ID`: ID của bảng khách hàng trong Larkbase
     - `TABLE_PRODUCT_ID`: ID của bảng sản phẩm trong Larkbase

6. Chạy ứng dụng:

   ```
   streamlit run mainv4.py
   ```

## Sử dụng

1. Truy cập vào địa chỉ `http://localhost:8501` trên trình duyệt web để mở ứng dụng. (HOẶC HỆ THỐNG TỰ NHẢY VỀ TRÌNH DUYỆT BẠN CHẠY)

2. Chọn khách hàng từ danh sách hoặc thêm mới khách hàng.

3. Thêm sản phẩm vào đơn hàng bằng cách chọn sản phẩm từ danh sách và nhập số lượng.

4. Nhập thông tin tiền cọc, phí công thợ, phí vận chuyển, phụ thu và ghi chú đơn hàng.

5. Nhấn nút "Lưu đơn hàng" để lưu thông tin đơn hàng và gửi đến webhook.

## Tác giả

- thượng - work@nguyenngothuong.com

## Giấy phép

Dự án này được cấp phép theo [Giấy phép MIT](LICENSE).