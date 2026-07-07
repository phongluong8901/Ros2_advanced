# 1
Quy Trình Biên Dịch Và Kiểm Tra Node ROS 2
🖥️ Terminal 1 (t1): Biên dịch Workspace
Sử dụng terminal này để quét và xây dựng lại không gian làm việc sau khi thay đổi mã nguồn.

Bash
cd bumperbot_ws/
colcon build
cd bumperbot_ws/: Di chuyển vào thư mục gốc của workspace ROS 2 tên là bumperbot_ws.

colcon build: Công cụ biên dịch chuẩn của ROS 2. Hệ thống sẽ quét qua toàn bộ các package nằm trong thư mục src/, xử lý mã nguồn (C++/Python) và tạo ra các thư mục quản lý: build/, install/, log/.

💡 Lưu ý: Riêng với Python, lệnh này không biên dịch ra file nhị phân mà đóng vai trò đăng ký các script vào hệ thống để bộ chạy của ROS 2 có thể tìm thấy và gọi thực thi.

🚀 Terminal 2 (t2): Chạy Node Publisher
Mở một terminal mới để khởi chạy Node vừa được đăng ký.

Bash
cd bumperbot_ws/
. install/setup.bash
ros2 run bumperbot_py_examples simple_publisher
. install/setup.bash (hoặc source install/setup.bash): Dòng này cực kỳ quan trọng. Nó giúp cập nhật các biến môi trường của riêng terminal này, giúp hệ thống định vị được các package vừa tạo trong thư mục install/.

ros2 run bumperbot_py_examples simple_publisher: Lệnh kích hoạt Node chạy thực tế.

bumperbot_py_examples: Tên của package chứa mã nguồn.

simple_publisher: Tên của executable (file thực thi/script) mà bạn đã cấu hình trong file setup.py.

🔍 Terminal 3 (t3): Kiểm tra trạng thái Topic (Debugging)
Mở terminal thứ ba độc lập để tiến hành "soi" xem dữ liệu từ Node ở Terminal 2 đang truyền nhận ra sao trên hệ thống.

1. Liệt kê các topic hiện có
Bash
ros2 topic list
Mục đích: Liệt kê tất cả các topic đang hoạt động trong mạng ROS 2 hiện tại. Khi chạy lệnh này, bạn sẽ nhìn thấy topic /chatter xuất hiện trong danh sách.

2. Xem dữ liệu truyền theo thời gian thực
Bash
ros2 topic echo /chatter
Mục đích: Hứng và in trực tiếp dữ liệu đang được đẩy lên topic /chatter ra màn hình. Bạn sẽ thấy dòng chữ data: "Hello ROS 2 - counter: X" nhảy liên tục sau mỗi giây.

3. Xem thông tin cấu trúc chi tiết
Bash
ros2 topic info /chatter --verbose
Mục đích: Xem thông tin chi tiết nâng cao về topic /chatter. Lệnh này hiển thị cụ thể: kiểu dữ liệu (std_msgs/msg/String), danh sách Node đang Publish (gửi), danh sách Node đang Subscribe (nhận) và cấu hình chất lượng dịch vụ (QoS).

4. Đo tần suất gửi tin nhắn
Bash
ros2 topic hz /chatter
Mục đích: Đo tần suất gửi tin nhắn thực tế của topic /chatter. Vì trong mã nguồn chúng ta cài đặt self.frequency_ = 1.0 (chu kỳ 1 giây một lần), nên kết quả tính toán trả về từ lệnh này sẽ xấp xỉ 1.0 Hz (tương đương 1 tin nhắn / giây).

5. ros2 topic pub /chatter std_msgs/msg/String "data: 'Hello ROS 2'"
Ý nghĩa: Đây là câu lệnh hoàn chỉnh dùng để phát một tin nhắn thủ công từ Terminal lên một topic.

Giải thích từng thành phần cấu trúc:

ros2 topic pub: Lệnh gọi công cụ phát dữ liệu (Publish) của hệ thống ROS 2.

/chatter: Tên của Topic mà bạn muốn gửi dữ liệu vào.

std_msgs/msg/String: Kiểu dữ liệu chính xác của Topic này (gói tin String nằm trong package std_msgs).

"data: 'Hello ROS 2'": Nội dung của gói tin cần truyền đi, được viết dưới định dạng cú pháp YAML. Vì cấu trúc của gói tin String chứa một trường tên là data, ta gán nội dung mong muốn vào trường này.