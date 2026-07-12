import rclpy  # Nhập thư viện ROS 2 chính cho Python để quản lý vòng đời và giao tiếp
from rclpy.node import Node  # Nhập lớp Node để kế thừa và tạo ra các thành phần ROS 2
from std_msgs.msg import String  # Nhập kiểu dữ liệu chuỗi văn bản chuẩn (String) để nhận gói tin dữ liệu


class SimpleSubscriber(Node):  # Định nghĩa lớp SimpleSubscriber kế thừa từ lớp Node của ROS 2

    def __init__(self):  # Hàm khởi tạo (constructor) chạy ngay khi đối tượng được tạo từ lớp này
        super().__init__("simple_subscriber")  # Gọi hàm khởi tạo lớp cha và đặt tên Node này là "simple_subscriber"
        self.sub_ = self.create_subscription(String, "chatter", self.msgCallback, 10)  # Tạo Subscriber lắng nghe kiểu String trên topic "chatter", gọi hàm msgCallback khi có tin và hàng đợi = 10
        self.sub_  # Dòng này dùng để giữ tham chiếu đến đối tượng subscription (tránh bị bộ gom rác Python hiểu nhầm và xóa đi)

    def msgCallback(self, msg):  # Định nghĩa hàm callback, tự động chạy và nhận tham số 'msg' mỗi khi có tin nhắn mới truyền tới topic
        self.get_logger().info("I heard: %s" % msg.data)  # Trích xuất chuỗi từ trường dữ liệu '.data' của tin nhắn và in log ra màn hình console


def main():  # Định nghĩa hàm main - điểm khởi đầu chính của chương trình
    rclpy.init()  # Khởi tạo các cấu hình nền tảng và kết nối của thư viện rclpy

    simple_publisher = SimpleSubscriber()  # Tạo một thực thể (instance) cụ thể cho Node SimpleSubscriber (tên biến đang đặt tạm là simple_publisher)
    rclpy.spin(simple_publisher)  # Giữ Node chạy liên tục trong vòng lặp vô hạn để sẵn sàng đón nhận và xử lý tin nhắn từ topic

    simple_publisher.destroy_node()  # Giải phóng tài nguyên và hủy Node sau khi thoát khỏi vòng lặp spin (khi nhấn Ctrl+C)
    rclpy.shutdown()  # Tắt hoàn toàn thư viện rclpy và ngắt kết nối hệ thống với mạng ROS 2


if __name__ == '__main__':  # Kiểm tra xem file script này có đang được thực thi trực tiếp từ dòng lệnh hay không
    main()  # Gọi hàm main để bắt đầu chạy toàn bộ chương trình Node Subscriber