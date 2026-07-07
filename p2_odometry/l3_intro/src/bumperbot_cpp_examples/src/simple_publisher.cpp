#include <rclcpp/rclcpp.hpp>  // Nhập thư viện client chính của ROS 2 dành cho C++ (quản lý Node, Timer, Publisher...)
#include <std_msgs/msg/string.hpp>  // Nhập kiểu dữ liệu chuỗi văn bản tiêu chuẩn (String) trong hệ thống ROS 2

#include <chrono>  // Thư viện chuẩn của C++ dùng để xử lý và đo lường các khoảng thời gian


using namespace std::chrono_literals;  // Cho phép sử dụng các hậu tố thời gian như "1s" (1 giây), "100ms" một cách ngắn gọn

class SimplePublisher : public rclcpp::Node  // Định nghĩa lớp SimplePublisher kế thừa từ lớp rclcpp::Node của ROS 2
{
public:
  SimplePublisher() : Node("simple_publisher"), counter_(0)  // Hàm khởi tạo: Đặt tên Node là "simple_publisher" và gán biến đếm counter_ xuất phát từ 0
  {
    pub_ = create_publisher<std_msgs::msg::String>("chatter", 10);  // Tạo Publisher gửi kiểu String lên topic "chatter" với kích thước hàng đợi là 10
    timer_ = create_wall_timer(1s, std::bind(&SimplePublisher::timerCallback, this));  // Tạo bộ định thời (Timer) chạy mỗi 1 giây, liên kết để gọi hàm timerCallback
    RCLCPP_INFO(get_logger(), "Publishing at 1 Hz");  // In thông báo log cấp độ INFO ra màn hình console để giám sát trạng thái Node
  }

  void timerCallback()  // Định nghĩa hàm callback được tự động kích hoạt mỗi khi Timer "gõ nhịp" (mỗi giây một lần)
  {
    auto message = std_msgs::msg::String();  // Tạo một đối tượng tin nhắn trống thuộc kiểu dữ liệu String của ROS 2
    message.data = "Hello ROS 2 - counter:" + std::to_string(counter_++);  // Ghép chuỗi văn bản với biến đếm (được ép kiểu sang string), sau đó tăng counter_ lên 1
    pub_->publish(message);  // Phát (publish) gói tin nhắn chứa chuỗi dữ liệu này lên topic "chatter"
  }

private:
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr pub_;  // Khai báo con trỏ thông minh (SharedPtr) để quản lý đối tượng Publisher
  rclcpp::TimerBase::SharedPtr timer_;  // Khai báo con trỏ thông minh để quản lý bộ định thời Timer
  unsigned int counter_;  // Khai báo biến đếm không âm (unsigned int) để đếm số lượng tin nhắn đã phát đi
};


int main(int argc, char* argv[])  // Hàm main - điểm khởi đầu và thực thi chính của chương trình C++
{
  rclcpp::init(argc, argv);  // Khởi tạo các cấu hình nền tảng, phân tích các tham số dòng lệnh truyền vào cho ROS 2
  auto node = std::make_shared<SimplePublisher>();  // Tạo một con trỏ thông minh chứa thực thể (instance) của Node SimplePublisher
  rclcpp::spin(node);  // Đưa Node vào vòng lặp vô hạn để giữ Node luôn chạy và sẵn sàng xử lý các sự kiện thời gian (Timer)
  rclcpp::shutdown();  // Tắt hoàn toàn môi trường ROS 2 và giải phóng các tài nguyên hệ thống sau khi thoát spin (nhấn Ctrl+C)
  return 0;  // Kết thúc chương trình chính và trả về mã thành công 0 cho hệ điều hành
}