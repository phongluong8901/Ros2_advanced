#include <rclcpp/rclcpp.hpp>  // Nhập thư viện client chính của ROS 2 dành cho C++ (quản lý Node, Subscriber...)
#include <std_msgs/msg/string.hpp>  // Nhập kiểu dữ liệu chuỗi văn bản tiêu chuẩn (String) trong hệ thống ROS 2


using std::placeholders::_1;  // Khai báo placeholder _1 để đại diện cho tham số đầu tiên (gói tin nhắn) truyền vào hàm callback khi dùng std::bind

class SimpleSubscriber : public rclcpp::Node  // Định nghĩa lớp SimpleSubscriber kế thừa từ lớp rclcpp::Node của ROS 2
{
public:
  SimpleSubscriber() : Node("simple_subscriber")  // Hàm khởi tạo (constructor): Gọi hàm khởi tạo lớp cha và đặt tên Node là "simple_subscriber"
  {
    sub_ = create_subscription<std_msgs::msg::String>(  // Khởi tạo một Subscriber lắng nghe kiểu dữ liệu gói tin dạng String
        "chatter", 10, std::bind(&SimpleSubscriber::msgCallback, this, _1));  // Đăng ký nghe trên topic "chatter", kích thước hàng đợi = 10, và liên kết sự kiện tới hàm msgCallback với 1 tham số dữ liệu đầu vào (_1)
  }

private:
  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr sub_;  // Khai báo con trỏ thông minh (SharedPtr) để quản lý đối tượng Subscriber lắng nghe kiểu tin nhắn String

  void msgCallback(const std_msgs::msg::String &msg) const  // Định nghĩa hàm callback (hàm hằng - const) tự động kích hoạt để xử lý gói tin tham chiếu 'msg' mỗi khi có tin nhắn mới đổ về
  {
    RCLCPP_INFO_STREAM(this->get_logger(), "I heard: " << msg.data.c_str());  // In dòng log dạng stream cấp độ INFO ra console, trích xuất chuỗi văn bản bằng phương thức .c_str() của C++
  }
};


int main(int argc, char * argv[])  // Hàm main - điểm khởi đầu và thực thi chính của chương trình C++
{
  rclcpp::init(argc, argv);  // Khởi tạo các cấu hình hệ thống, thiết lập lớp nền tảng và phân tích tham số dòng lệnh cho ROS 2
  rclcpp::spin(std::make_shared<SimpleSubscriber>());  // Tạo nhanh một con trỏ thông minh cho Node SimpleSubscriber và đưa vào vòng lặp vô hạn (spin) để lắng nghe và gọi callback xử lý dữ liệu
  rclcpp::shutdown();  // Tắt hoàn toàn môi trường ROS 2 và giải phóng tài nguyên sau khi kết thúc vòng lặp spin (khi bấm Ctrl+C)
  return 0;  // Kết thúc chương trình chính và trả về mã trạng thái thành công 0 cho hệ điều hành
}