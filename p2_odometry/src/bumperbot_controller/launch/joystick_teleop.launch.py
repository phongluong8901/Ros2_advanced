import os  # Nhập thư viện os của hệ thống để xử lý các thao tác liên quan đến đường dẫn tệp tin

from ament_index_python.packages import get_package_share_directory  # Nhập hàm tiện ích để tìm đường dẫn cài đặt 'share' của một Package ROS 2

from launch import LaunchDescription  # Nhập lớp LaunchDescription để gom nhóm các tiến trình và trả về cấu hình chạy chung
from launch.actions import DeclareLaunchArgument  # Nhập lớp hành động dùng để khai báo các tham số đầu vào (Arguments) từ Terminal
from launch.substitutions import LaunchConfiguration  # Nhập công cụ giúp đọc giá trị nạp từ các tham số cấu hình (Launch Arguments)
from launch.actions import IncludeLaunchDescription  # Nhập lớp hành động cho phép gọi và nhúng một file launch từ package khác vào file này
from launch_ros.actions import Node  # Nhập lớp Node để định nghĩa cấu hình khởi chạy một Node ROS 2 độc lập


def generate_launch_description():  # Hàm khởi tạo bắt buộc, hệ thống ROS 2 sẽ thực thi nội dung kịch bản bên trong hàm này
    
    bumperbot_controller_pkg = get_package_share_directory('bumperbot_controller')  # Lấy và lưu đường dẫn tuyệt đối đến thư mục cài đặt của package 'bumperbot_controller'

    use_sim_time_arg = DeclareLaunchArgument(name="use_sim_time", default_value="True",  # Khai báo tham số đầu vào 'use_sim_time' với giá trị mặc định là True để chạy đồng bộ giả lập
                                             description="Use simulated time"  # Dòng mô tả ngắn gọn chức năng của tham số này khi người dùng tra cứu lệnh
    )  

    joy_teleop = Node(  # Cấu hình Node 1: joy_teleop (Dịch tín hiệu nút bấm/analog của tay cầm thành lệnh vận tốc geometry_msgs/Twist)
        package="joy_teleop",  # Thuộc package tiêu chuẩn 'joy_teleop' của ROS 2 chuyên dùng cho tay cầm điều khiển
        executable="joy_teleop",  # Tên file thực thi chính để chạy node dịch mã điều khiển này
        parameters=[os.path.join(get_package_share_directory("bumperbot_controller"), "config", "joy_teleop.yaml"),  # Nạp file cấu hình ánh xạ nút bấm (ví dụ: gán cần gạt analog cho trục linear/angular)
                    {"use_sim_time": LaunchConfiguration("use_sim_time")}],  # Đồng bộ thời gian của hệ thống theo tham số 'use_sim_time' đã khai báo ở trên
    )  

    joy_node = Node(  # Cấu hình Node 2: joy_node (Node driver trực tiếp đọc dữ liệu phần cứng tay cầm từ cổng USB hệ điều hành)
        package="joy",  # Thuộc package driver thiết bị ngoại vi 'joy' cốt lõi
        executable="joy_node",  # Tên file thực thi chính để đọc joystick/gamepad và phát ra topic '/joy'
        name="joystick",  # Đặt tên định danh cho node này trong mạng ROS 2 là 'joystick' thay vì tên mặc định
        parameters=[os.path.join(get_package_share_directory("bumperbot_controller"), "config", "joy_config.yaml"),  # Nạp file cấu hình driver (định dạng thiết bị, độ nhạy, vùng chết analog - deadzone)
                    {"use_sim_time": LaunchConfiguration("use_sim_time")}]  # Thiết lập đồng bộ thời gian giả lập cho driver nhận diện chính xác tần số gửi tin nhắn
    )  
    
    twist_mux_launch = IncludeLaunchDescription(  # Cấu hình nạp file launch từ bên ngoài: Tích hợp bộ gom và phân cấp ưu tiên nguồn lệnh vận tốc (Twist Mux)
        os.path.join(  # Định nghĩa đường dẫn chi tiết nối đến file launch của Twist Mux
            get_package_share_directory("twist_mux"),  # Tìm thư mục cài đặt gốc của bộ công cụ 'twist_mux'
            "launch",  # Vào thư mục chứa kịch bản khởi chạy 'launch'
            "twist_mux_launch.py"  # Tên file launch gốc cần nhúng vào kịch bản hiện tại
        ),  
        launch_arguments={  # Truyền các tham số cấu hình riêng cho bộ Twist Mux hoạt động theo ý muốn:
            "cmd_vel_out": "bumperbot_controller/cmd_vel_unstamped",  # Chỉ định tên topic đầu ra sau khi đã trộn và phân cấp ưu tiên (gửi tới bộ điều khiển robot)
            "config_locks": os.path.join(bumperbot_controller_pkg, "config", "twist_mux_locks.yaml"),  # Đường dẫn file cấu hình các điều kiện khóa kênh điều khiển (E-stop, ưu tiên tuyệt đối)
            "config_topics": os.path.join(bumperbot_controller_pkg, "config", "twist_mux_topics.yaml"),  # Đường dẫn file cấu hình danh sách các topic đầu vào (Keyboard, Joystick, Autonomous) và độ ưu tiên của chúng
            "config_joy": os.path.join(bumperbot_controller_pkg, "config", "twist_mux_joy.yaml"),  # Đường dẫn file cấu hình các nút bấm kích hoạt nhanh (cho phép hoặc chặn lệnh từ tay cầm)
            "use_sim_time": LaunchConfiguration("use_sim_time"),  # Chuyển tiếp trạng thái biến thời gian mô phỏng vào file launch của bộ trộn
        }.items(),  # Chuyển đổi cấu trúc dict tham số thành danh sách các cặp item để ROS 2 xử lý nạp argument
    )  

    twist_relay_node = Node(  # Cấu hình Node 3: twist_relay (Làm nhiệm vụ trung chuyển, chuyển đổi hoặc đổi tên topic trung gian nếu cần thiết)
        package="bumperbot_controller",  # Thuộc package bộ điều khiển robot 'bumperbot_controller' của bạn
        executable="twist_relay",  # Tên file thực thi làm nhiệm vụ relay dữ liệu vận tốc
        name="twist_relay",  # Đặt tên đăng ký của node trong mạng hệ thống là 'twist_relay'
        parameters=[{"use_sim_time": LaunchConfiguration("use_sim_time")}]  # Đồng bộ thời gian mô phỏng để đồng nhất nhãn thời gian timestamp khi đẩy tin nhắn đi
    )  

    return LaunchDescription(  # Trả về tập hợp danh sách các cấu hình tham số và tiến trình Node để hệ thống ROS 2 tiến hành khởi chạy đồng loạt
        [  
            use_sim_time_arg,  # Đăng ký tham số thời gian mô phỏng lên hệ thống launch chung
            joy_teleop,  # Kích hoạt tiến trình dịch mã nút bấm tay cầm thành vận tốc hình học
            joy_node,  # Khởi động bộ driver kết nối trực tiếp với phần cứng tay cầm USB
            twist_mux_launch,  # Bật bộ trộn và phân cấp ưu tiên các luồng điều khiển vận tốc (Tránh việc robot phân vân khi nhận cả lệnh tự động lẫn lệnh tay cầm)
            twist_relay_node,  # Khởi chạy node trung chuyển tin nhắn vận tốc để đưa dữ liệu về đúng định dạng mong muốn của robot
        ]  
    )  # Kết thúc kịch bản cấu hình điều khiển robot bằng tay cầm tích hợp bộ trộn vận tốc cho Bumperbot