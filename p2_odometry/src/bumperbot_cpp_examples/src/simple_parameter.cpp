#include <rclcpp/rclcpp.hpp>  // Nhập thư viện client chính của ROS 2 dành cho C++ (quản lý Node, Parameter...)
#include <rcl_interfaces/msg/set_parameters_result.hpp>  // Nhập kiểu dữ liệu chứa kết quả phản hồi (thành công/thất bại) khi thay đổi parameter

#include <vector>  // Nhập thư viện vector của C++ để quản lý danh sách mảng động
#include <string>  // Nhập thư viện string của C++ để làm việc với chuỗi ký tự văn bản
#include <memory>  // Nhập thư viện memory của C++ để sử dụng các công cụ quản lý bộ nhớ như SharedPtr


using std::placeholders::_1;  // Khai báo placeholder _1 để đại diện cho tham số đầu tiên (danh sách parameters) truyền vào hàm callback khi dùng std::bind

class SimpleParameter : public rclcpp::Node  // Định nghĩa lớp SimpleParameter kế thừa từ lớp rclcpp::Node của ROS 2
{
public:
    SimpleParameter() : Node("simple_parameter")  // Hàm khởi tạo (constructor): Gọi hàm khởi tạo lớp cha và đặt tên Node là "simple_parameter"
    {
        declare_parameter<int>("simple_int_param", 28);  // Khai báo một tham số kiểu số nguyên (<int>) tên là "simple_int_param" với giá trị mặc định là 28
        declare_parameter<std::string>("simple_string_param", "Antonio");  // Khai báo một tham số kiểu chuỗi (<std::string>) tên là "simple_string_param" với giá trị mặc định là "Antonio"
        param_callback_handle_ = add_on_set_parameters_callback(std::bind(&SimpleParameter::paramChangeCallback, this, _1));  // Đăng ký hàm callback thay đổi parameter và lưu lại handle quản lý để tránh callback bị hủy
    }

private:
    OnSetParametersCallbackHandle::SharedPtr param_callback_handle_;  // Khai báo biến con trỏ thông minh để quản lý vòng đời của handle liên kết callback parameter

    rcl_interfaces::msg::SetParametersResult paramChangeCallback(const std::vector<rclcpp::Parameter> &parameters)  // Định nghĩa hàm callback nhận danh sách hằng tham chiếu chứa các tham số yêu cầu thay đổi
    {
        rcl_interfaces::msg::SetParametersResult result;  // Tạo một đối tượng kết quả trống để lưu trạng thái phản hồi (mặc định result.successful là false)
        for(const auto& param : parameters)  // Duyệt qua từng tham số nằm trong danh sách yêu cầu thay đổi bằng vòng lặp range-based for
        {
            if(param.get_name() == "simple_int_param" && param.get_type() == rclcpp::ParameterType::PARAMETER_INTEGER)  // Kiểm tra tên tham số có phải "simple_int_param" và đúng kiểu dữ liệu số nguyên không
            {
                RCLCPP_INFO_STREAM(get_logger(), "Param simple_int_param changed! New value is " << param.as_int());  // In dòng log dạng stream cấp độ INFO kèm giá trị mới được ép sang kiểu int bằng .as_int()
                result.successful = true;  // Đánh dấu trạng thái xử lý thay đổi tham số này là thành công
            }
            if(param.get_name() == "simple_string_param" && param.get_type() == rclcpp::ParameterType::PARAMETER_STRING)  // Kiểm tra tên tham số có phải "simple_string_param" và đúng kiểu dữ liệu chuỗi không
            {
                RCLCPP_INFO_STREAM(get_logger(), "Param simple_string_param changed! New value is " << param.as_string());  // In dòng log dạng stream cấp độ INFO kèm giá trị chuỗi mới bằng phương thức .as_string()
                result.successful = true;  // Đánh dấu trạng thái xử lý thay đổi tham số này là thành công
            }
        }
        
        return result;  // Trả về đối tượng kết quả để hệ thống xác nhận chấp nhận việc cập nhật tham số mới
    }
};


int main(int argc, char* argv[])  // Hàm main - điểm khởi đầu và thực thi chính của chương trình C++
{
  rclcpp::init(argc, argv);  // Khởi tạo các cấu hình hệ thống, thiết lập lớp nền tảng và phân tích tham số dòng lệnh cho ROS 2
  auto node = std::make_shared<SimpleParameter>();  // Tạo một con trỏ thông minh chứa thực thể (instance) của Node SimpleParameter
  rclcpp::spin(node);  // Đưa Node vào vòng lặp vô hạn (spin) để giữ Node luôn sống và sẵn sàng xử lý các yêu cầu thay đổi tham số
  rclcpp::shutdown();  // Tắt hoàn toàn môi trường ROS 2 và giải phóng tài nguyên sau khi kết thúc vòng lặp spin (khi bấm Ctrl+C)
  return 0;  // Kết thúc chương trình chính và trả về mã trạng thái thành công 0 cho hệ điều hành
}