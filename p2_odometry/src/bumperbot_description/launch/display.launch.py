import os  # Nhập thư viện os tiêu chuẩn của Python để làm việc với đường dẫn hệ thống tệp tin
from ament_index_python.packages import get_package_share_directory  # Nhập hàm để tìm đường dẫn tuyệt đối đến thư mục 'share' của một package ROS 2

from launch import LaunchDescription  # Nhập lớp LaunchDescription để gom nhóm toàn bộ cấu hình chạy hệ thống và trả về cho ROS 2
from launch.actions import DeclareLaunchArgument  # Nhập lớp dùng để khai báo các tham số đầu vào (Arguments) khi chạy file Launch từ Terminal
from launch.substitutions import Command, LaunchConfiguration  # Nhập các công cụ thay thế: Command (chạy lệnh hệ thống), LaunchConfiguration (đọc biến tham số Launch)

from launch_ros.actions import Node  # Nhập lớp Node để định nghĩa cấu hình khởi chạy cho một Node ROS 2 cụ thể
from launch_ros.parameter_descriptions import ParameterValue  # Nhập lớp dùng để đóng gói và định nghĩa kiểu dữ liệu cho một biến Parameter trong ROS 2


def generate_launch_description():  # Định nghĩa hàm bắt buộc, ROS 2 sẽ luôn tìm và gọi hàm này để đọc cấu hình file Launch
    bumperbot_description_dir = get_package_share_directory("bumperbot_description")  # Tìm và lưu đường dẫn tuyệt đối đến thư mục cài đặt của package "bumperbot_description"

    model_arg = DeclareLaunchArgument(name="model", default_value=os.path.join(  # Khai báo một tham số Launch tên là "model", có giá trị mặc định là đường dẫn...
                                        bumperbot_description_dir, "urdf", "bumperbot.urdf.xacro"  # ...nối thẳng tới file thiết kế robot dạng xacro: "bumperbot_description/urdf/bumperbot.urdf.xacro"
                                        ),  # Kết thúc thiết lập giá trị mặc định cho tham số
                                      description="Absolute path to robot urdf file")  # Dòng mô tả ý nghĩa của tham số này để người dùng đọc khi tra cứu lệnh trợ giúp

    robot_description = ParameterValue(Command(["xacro ", LaunchConfiguration("model")]),  # Tạo giá trị parameter bằng cách chạy lệnh terminal "xacro <đường_dẫn_file_model>" để biên dịch file xacro sang URDF thuần
                                       value_type=str)  # Định nghĩa kiểu dữ liệu trả về của nội dung cấu trúc robot sau khi biên dịch là một chuỗi văn bản (string)

    robot_state_publisher_node = Node(  # Cấu hình khởi chạy Node thứ nhất: robot_state_publisher
        package="robot_state_publisher",  # Node này thuộc về package tiêu chuẩn tên là "robot_state_publisher"
        executable="robot_state_publisher",  # Tên file thực thi (executable) của Node cần gọi chạy
        parameters=[{"robot_description": robot_description}]  # Nạp parameter "robot_description" chứa toàn bộ cấu trúc xương/vỏ robot đã biên dịch ở trên vào Node này
    )  # Node này có nhiệm vụ đọc cấu trúc URDF và tính toán phát ra hệ tọa độ các liên kết (TF) của robot

    joint_state_publisher_gui_node = Node(  # Cấu hình khởi chạy Node thứ hai: joint_state_publisher_gui
        package="joint_state_publisher_gui",  # Node này thuộc về package đồ họa tên là "joint_state_publisher_gui"
        executable="joint_state_publisher_gui"  # Tên file thực thi của Node cần gọi chạy (Sẽ hiển thị bảng thanh trượt Slider trên màn hình để bạn kéo xoay/dịch chuyển các khớp robot)
    )  

    rviz_node = Node(  # Cấu hình khởi chạy Node thứ ba: rviz2 (Giao diện hiển thị 3D)
        package="rviz2",  # Node thuộc package hiển thị đồ họa 3D cốt lõi "rviz2"
        executable="rviz2",  # Tên file thực thi chính để mở phần mềm RViz 2
        name="rviz2",  # Đặt tên định danh cho Node này khi hoạt động trong mạng ROS 2 là "rviz2"
        output="screen",  # Đẩy toàn bộ dữ liệu Log, thông báo lỗi của RViz trực tiếp ra màn hình Terminal hiện tại để tiện theo dõi
        arguments=["-d", os.path.join(bumperbot_description_dir, "rviz", "display.rviz")],  # Truyền tham số "-d" đi kèm đường dẫn cấu hình để RViz tự động load đúng giao diện camera/trục tọa độ bạn đã lưu trước đó
    )  

    return LaunchDescription([  # Trả về đối tượng LaunchDescription chứa danh sách tất cả các thành phần đã thiết lập ở trên
        model_arg,  # Đăng ký tham số đầu vào "model" vào trình quản lý Launch
        joint_state_publisher_gui_node,  # Kích hoạt chạy giao diện trượt điều khiển khớp
        robot_state_publisher_node,  # Kích hoạt chạy Node tính toán xuất tọa độ TF robot
        rviz_node  # Kích hoạt mở phần mềm mô phỏng đồ họa RViz 2
    ])  # Kết thúc hàm, ROS 2 sẽ chạy đồng thời cả 3 Node này chỉ với duy nhất một câu lệnh gọi file launch