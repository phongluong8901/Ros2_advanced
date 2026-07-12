import rclpy  # Nhập thư viện ROS 2 chính cho Python để quản lý vòng đời và giao tiếp
from rclpy.node import Node  # Nhập lớp Node để kế thừa và tạo ra các thành phần ROS 2
from rcl_interfaces.msg import SetParametersResult  # Nhập kiểu dữ liệu chứa kết quả phản hồi (thành công/thất bại) khi thay đổi parameter
from rclpy.parameter import Parameter  # Nhập lớp Parameter để kiểm tra các kiểu dữ liệu của biến tham số (INTEGER, STRING...)


class SimpleParameter(Node):  # Định nghĩa lớp SimpleParameter kế thừa từ lớp Node của ROS 2

    def __init__(self):  # Hàm khởi tạo (constructor) chạy ngay khi đối tượng được tạo từ lớp này
        super().__init__("simple_parameter")  # Gọi hàm khởi tạo lớp cha và đặt tên Node này là "simple_parameter"
        self.declare_parameter("simple_int_param", 28)  # Khai báo một tham số kiểu số nguyên tên là "simple_int_param" với giá trị mặc định là 28
        self.declare_parameter("simple_string_param", "Antonio")  # Khai báo một tham số kiểu chuỗi tên là "simple_string_param" với giá trị mặc định là "Antonio"

        self.add_on_set_parameters_callback(self.paramChangeCallback)  # Đăng ký hàm callback tự động kích hoạt bất khi nào có yêu cầu thay đổi giá trị của parameter từ bên ngoài

    def paramChangeCallback(self, params):  # Định nghĩa hàm callback nhận danh sách các tham số 'params' đang yêu cầu thay đổi giá trị
        result = SetParametersResult()  # Tạo một đối tượng kết quả trống để phản hồi lại trạng thái cho hệ thống

        for param in params:  # Duyệt qua từng tham số nằm trong danh sách yêu cầu thay đổi

            if param.name == "simple_int_param" and param.type_ == Parameter.Type.INTEGER:  # Kiểm tra nếu tên tham số trùng với "simple_int_param" và đúng kiểu dữ liệu số nguyên
                self.get_logger().info("Param simple_int_param changed! New value is %d" % param.value)  # In dòng thông báo log cấp độ INFO kèm giá trị mới ra màn hình console
                result.successful = True  # Đánh dấu trạng thái xử lý thay đổi tham số này là thành công

            if param.name == "simple_string_param" and param.type_ == Parameter.Type.STRING:  # Kiểm tra nếu tên tham số trùng với "simple_string_param" và đúng kiểu dữ liệu chuỗi văn bản
                self.get_logger().info("Param simple_string_param changed! New value is %s" % param.value)  # In dòng thông báo log cấp độ INFO kèm giá trị chuỗi mới ra màn hình console
                result.successful = True  # Đánh dấu trạng thái xử lý thay đổi tham số này là thành công

        return result  # Trả về đối tượng kết quả để hệ thống xác nhận việc cập nhật tham số đã hoàn tất hợp lệ


def main():  # Định nghĩa hàm main - điểm khởi đầu chính của chương trình
    rclpy.init()  # Khởi tạo các cấu hình nền tảng và kết nối của thư viện rclpy
    simple_parameter = SimpleParameter()  # Tạo một thực thể (instance) cụ thể cho Node SimpleParameter
    rclpy.spin(simple_parameter)  # Giữ Node chạy liên tục trong vòng lặp vô hạn để sẵn sàng lắng nghe các sự kiện thay đổi tham số
    simple_parameter.destroy_node()  # Giải phóng tài nguyên và hủy Node sau khi thoát khỏi vòng lặp spin (khi nhấn Ctrl+C)
    rclpy.shutdown()  # Tắt hoàn toàn thư viện rclpy và ngắt kết nối hệ thống với mạng ROS 2


if __name__ == "__main__":  # Kiểm tra xem file script này có đang được thực thi trực tiếp từ dòng lệnh hay không
    main()  # Gọi hàm main để bắt đầu chạy toàn bộ chương trình Node Parameter