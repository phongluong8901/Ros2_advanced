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

6. ros2 param list
Ý nghĩa: Liệt kê tất cả các Parameter đang có trên hệ thống.

Hành vi hệ thống: ROS 2 sẽ quét toàn bộ các Node đang chạy trong mạng và hiển thị danh sách các tham số được khai báo dưới tên của từng Node đó.

Ví dụ, nếu Node của bạn đang chạy, bạn sẽ thấy đầu ra dạng:

Plaintext
/simple_parameter:
  simple_int_param
  simple_string_param
  use_sim_time
(Lưu ý: use_sim_time là một tham số mặc định hệ thống tự thêm vào tất cả các Node).

7. ros2 param get /simple_paramter simple_int_param
Ý nghĩa: Lấy và hiển thị giá trị hiện tại của một Parameter cụ thể thuộc một Node cụ thể.

Giải thích từng thành phần cấu trúc:

ros2 param get: Lệnh gọi công cụ đọc giá trị tham số (Get Parameter) của ROS 2.

/simple_paramter: Tên của Node đang nắm giữ tham số đó (được viết dưới dạng namespace đầy đủ). (Lưu ý nhỏ: Câu lệnh của bạn đang bị viết nhầm chính tả chữ paramter, đúng ra phải là /simple_parameter tương ứng với tên bạn đặt trong code).

simple_int_param: Tên chính xác của tham số mà bạn muốn kiểm tra giá trị.

8. ros2 param set /simple_paramter simple_string_param "Hi Ros2"
Ý nghĩa: Câu lệnh này dùng để thiết lập hoặc thay đổi (Set) giá trị của một Parameter cụ thể thuộc một Node đang chạy từ xa trực tiếp qua Terminal.

Giải thích chi tiết từng thành phần:

ros2 param set: Lệnh gọi công cụ thay đổi giá trị tham số (Set Parameter) nằm trong bộ tiện ích dòng lệnh của ROS 2.

/simple_paramter: Tên của Node đang nắm giữ tham số cần thay đổi.

⚠️ Lưu ý sửa lỗi chính tả: Giống như câu lệnh trước, chữ /simple_paramter đang bị thiếu chữ e ở cuối. Để lệnh chạy thành công với code bạn đã viết, bạn cần sửa lại chính xác thành /simple_parameter.

simple_string_param: Tên của tham số mà bạn muốn thay đổi giá trị (ở đây là tham số kiểu chuỗi ký tự văn bản).

"Hi Ros2": Giá trị mới mà bạn muốn gán cho tham số đó.

9. ros2 param
Ý nghĩa: Đây là câu lệnh gốc (root command) quản lý Parameter của ROS 2.

Hành vi hệ thống: Khi bạn gõ mỗi cụm này rồi Enter, ROS 2 sẽ không thực hiện tính năng cụ thể nào mà sẽ hiển thị danh sách hướng dẫn sử dụng cùng các câu lệnh con (subcommands) đi kèm như list, get, set, delete, dump, load... để bạn chọn.

10. ros2 run bumperbot_cpp_examples simple_parameter --ros-args -p simple_int_param:=30
Ý nghĩa: Khởi chạy Node simple_parameter (bản C++), đồng thời ép giá trị của tham số simple_int_param thành 30 ngay khi Node vừa được sinh ra (ghi đè lên giá trị mặc định trong code).

Giải thích chi tiết từng thành phần từ trái qua phải:

ros2 run: Lệnh khởi chạy một thực thi/Node trong ROS 2.

bumperbot_cpp_examples: Tên của Package chứa Node C++.

simple_parameter: Tên file thực thi (executable) của Node Parameter.

--ros-args: Cờ báo hiệu (flag) cực kỳ quan trọng. Nó bảo với ROS 2 rằng: "Những tham số đi sau dấu này là dành riêng cho cấu hình nội bộ của ROS 2 (như đổi tên topic, đổi log, truyền tham số), hệ thống hãy xử lý chúng đi chứ đây không phải tham số dòng lệnh thông thường của C++".

-p: Viết tắt của --param. Dòng này báo hiệu bạn chuẩn bị truyền vào một cặp tên-giá trị của Parameter.

simple_int_param:=30: Cú pháp gán giá trị cho tham số.

simple_int_param: Tên tham số bạn muốn tác động.

:=: Cú pháp gán bắt buộc trong dòng lệnh ROS 2 (dấu hai chấm đi liền dấu bằng).

30: Giá trị mới dạng số nguyên mà bạn muốn ép cho tham số này.