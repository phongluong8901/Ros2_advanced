import rclpy  # Nhập thư viện ROS 2 chính cho Python để quản lý vòng đời và giao tiếp
from rclpy.node import Node  # Nhập lớp Node để kế thừa và tạo ra các thành phần ROS 2
from std_msgs.msg import String  # Nhập kiểu dữ liệu chuỗi văn bản chuẩn (String) để gửi đi


class SimplePublisher(Node):  # Định nghĩa lớp SimplePublisher kế thừa từ lớp Node của ROS 2

    def __init__(self):  # Hàm khởi tạo (constructor) chạy ngay khi đối tượng được tạo
        super().__init__("simple_publisher")  # Gọi hàm khởi tạo lớp cha và đặt tên Node là "simple_publisher"
        self.pub_ = self.create_publisher(String, "chatter", 10)  # Tạo Publisher gửi kiểu String lên topic "chatter", hàng đợi = 10
        self.counter_ = 0  # Khởi tạo một biến đếm kiểu số nguyên bắt đầu từ giá trị 0
        self.frequency_ = 1.0  # Thiết lập chu kỳ thời gian (hoặc tần suất) hoạt động là 1.0 giây
        self.get_logger().info("Publishing at %d Hz" % self.frequency_)  # In thông báo cấp độ INFO ra console để theo dõi hệ thống

        self.timer_ = self.create_timer(self.frequency_, self.timerCallback)  # Tạo bộ định thời (Timer) gọi hàm timerCallback mỗi 1.0 giây

    def timerCallback(self):  # Định nghĩa hàm callback được tự động gọi mỗi khi Timer gõ nhịp
        msg = String()  # Tạo một đối tượng tin nhắn trống thuộc kiểu dữ liệu String
        msg.data = "Hello ROS 2 - counter: %d" % self.counter_  # Gán chuỗi văn bản kèm số đếm hiện tại vào biến msg.data
        self.pub_.publish(msg)  # Phát (publish) gói tin nhắn chứa dữ liệu này lên topic "chatter"
        self.counter_ += 1  # Tăng giá trị biến đếm lên 1 đơn vị để chuẩn bị cho lần gửi sau


def main():  # Định nghĩa hàm main - điểm khởi đầu chính của chương trình
    rclpy.init()  # Khởi tạo các cấu hình nền tảng và kết nối của thư viện rclpy

    simple_publisher = SimplePublisher()  # Tạo một thực thể (instance) cụ thể cho Node SimplePublisher
    rclpy.spin(simple_publisher)  # Giữ Node chạy liên tục trong vòng lặp vô hạn để xử lý các sự kiện (Timer)

    simple_publisher.destroy_node()  # Giải phóng tài nguyên và hủy Node sau khi thoát khỏi vòng lặp spin (nhấn Ctrl+C)
    rclpy.shutdown()  # Tắt hoàn toàn thư viện rclpy và ngắt kết nối hệ thống ROS 2


if __name__ == "__main__":  # Kiểm tra xem file script này có đang được thực thi trực tiếp hay không
    main()  # Gọi hàm main để bắt đầu chạy toàn bộ chương trình ROS 2