import os  # Nhập thư viện os hệ thống để xử lý đường dẫn tệp tin và môi trường
from os import pathsep  # Nhập ký tự phân tách đường dẫn hệ thống (Dấu ':' trên Ubuntu) để nối chuỗi PATH
from pathlib import Path  # Nhập thư viện Path giúp thao tác, xử lý đường dẫn thư mục chuẩn OOP
from ament_index_python.packages import get_package_share_directory  # Nhập hàm lấy đường dẫn thư mục cài đặt 'share' của Package

from launch import LaunchDescription  # Nhập lớp LaunchDescription để gom nhóm các tiến trình và trả về cấu hình chạy chung
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable  # Nhập các hành động: Khai báo tham số, Gộp file launch khác, Thiết lập biến môi trường
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution, PythonExpression  # Nhập các công cụ thay thế động: Chạy lệnh, Đọc tham số, Nối đường dẫn, Chạy biểu thức Python
from launch.launch_description_sources import PythonLaunchDescriptionSource  # Nhập lớp định nghĩa nguồn nạp file launch từ một file Python khác

from launch_ros.actions import Node  # Nhập lớp Node để thiết lập cấu hình khởi chạy các Node ROS 2 độc lập
from launch_ros.parameter_descriptions import ParameterValue  # Nhập lớp định nghĩa kiểu dữ liệu cho Parameter của hệ thống ROS 2


def generate_launch_description():  # Hàm khởi tạo bắt buộc, hệ thống ROS 2 sẽ gọi hàm này để thực thi kịch bản launch
    bumperbot_description = get_package_share_directory("bumperbot_description")  # Tìm và lưu đường dẫn tuyệt đối đến thư mục cài đặt của package robot

    model_arg = DeclareLaunchArgument(  # Khai báo tham số đầu vào đặt tên là 'model' để người dùng có thể tùy biến file thiết kế từ Terminal
        name="model", default_value=os.path.join(  # Định nghĩa giá trị mặc định nếu người dùng không truyền tham số này vào...
                bumperbot_description, "urdf", "bumperbot.urdf.xacro"  # ...chính là đường dẫn trỏ thẳng đến file cấu trúc xacro của robot
            ),  # Kết thúc định nghĩa giá trị mặc định cho xacro
        description="Absolute path to robot urdf file"  # Dòng văn bản mô tả tác dụng của tham số 'model' này
    )  

    world_name_arg = DeclareLaunchArgument(name="world_name", default_value="empty")  # Khai báo tham số 'world_name' để chọn bản đồ giả lập, mặc định là map trống 'empty'

    world_path = PathJoinSubstitution([  # Sử dụng bộ nối đường dẫn thông minh (an toàn khi chạy đa nền tảng) cho file bản đồ (.world)
            bumperbot_description,  # Đi qua thư mục gốc của package
            "worlds",  # Vào tiếp thư mục 'worlds'
            PythonExpression(expression=["'", LaunchConfiguration("world_name"), "'", " + '.world'"])  # Sử dụng biểu thức Python để tự động cộng chuỗi đuôi tệp thành '<tên_bản_đồ>.world'
        ]  
    )  

    model_path = str(Path(bumperbot_description).parent.resolve())  # Lấy đường dẫn cha của package (thường là thư mục install/share) để Gazebo tìm kiếm các tài nguyên đi kèm
    model_path += pathsep + os.path.join(get_package_share_directory("bumperbot_description"), 'models')  # Nối thêm đường dẫn vào thư mục chứa các file thiết kế 3D 'models' bằng dấu phân tách hệ thống

    gazebo_resource_path = SetEnvironmentVariable(  # Thực hiện thiết lập một biến môi trường tạm thời cho phiên làm việc này
        "GZ_SIM_RESOURCE_PATH",  # Tên biến môi trường của Gazebo Sim (để nó biết chỗ tìm kiếm mesh 3D và map)
        model_path  # Gán giá trị bằng chuỗi đường dẫn tổng hợp 'model_path' vừa tạo ở bước trên
        )  

    ros_distro = os.environ["ROS_DISTRO"]  # Đọc biến hệ thống để kiểm tra phiên bản ROS 2 hiện tại bạn đang sử dụng (ví dụ: humble, jazzy)
    is_ignition = "True" if ros_distro == "humble" else "False"  # Nếu đang chạy bản 'humble' thì bật cờ Ignition=True, các bản mới hơn sẽ dùng Gazebo Sim đời mới (=False)

    robot_description = ParameterValue(Command([  # Sử dụng công cụ Command để thực thi lệnh biên dịch xacro ngay khi file launch chạy
            "xacro ",  # Gọi chương trình biên dịch xacro
            LaunchConfiguration("model"),  # Truyền đường dẫn file cấu trúc xacro lấy từ tham số 'model'
            " is_ignition:=",  # Truyền thêm tham số cấu hình vào trong file xacro
            is_ignition  # Gán giá trị biến 'is_ignition' (True/False) đã tính toán ở trên cho file xacro hiểu
        ]),  # Kết thúc chuỗi câu lệnh biên dịch
        value_type=str  # Chuyển đổi toàn bộ kết quả đầu ra của lệnh biên dịch thành một chuỗi văn bản (string) XML cấu trúc robot
    )  

    robot_state_publisher_node = Node(  # Cấu hình Node 1: robot_state_publisher
        package="robot_state_publisher",  # Thuộc package 'robot_state_publisher' tiêu chuẩn của ROS 2
        executable="robot_state_publisher",  # Tên file thực thi chính của Node
        parameters=[{"robot_description": robot_description,  # Nạp chuỗi dữ liệu cấu trúc robot vừa biên dịch vào bộ nhớ tham số
                     "use_sim_time": True}]  # Ép Node này phải đồng bộ và sử dụng thời gian của bộ giả lập (Simulation Time) thay vì thời gian thực của máy tính
    )  

    gazebo = IncludeLaunchDescription(  # Nạp và khởi chạy một file kịch bản launch có sẵn từ một package khác
                PythonLaunchDescriptionSource([os.path.join(  # Định nghĩa nguồn tệp tin cần nạp
                    get_package_share_directory("ros_gz_sim"), "launch"), "/gz_sim.launch.py"]),  # Tìm và nạp file launch gốc của Gazebo Sim ('gz_sim.launch.py' từ package 'ros_gz_sim')
                launch_arguments={  # Thiết lập các tham số điều khiển khi mở trình giả lập Gazebo
                    "gz_args": PythonExpression(["'", world_path, " -v 4 -r'"])  # Nạp đường dẫn map, thiết lập mức độ log chi tiết là 4 (-v 4) và tự động chạy mô phỏng ngay khi bật (-r)
                }.items()  # Chuyển đổi dict tham số thành dạng list tuple để truyền vào hành động nạp
             )  

    gz_spawn_entity = Node(  # Cấu hình Node 2: Tạo và thả robot vào thế giới ảo
        package="ros_gz_sim",  # Sử dụng package tiện ích 'ros_gz_sim'
        executable="create",  # Gọi file thực thi 'create' có chức năng sinh thực thể trong không gian 3D
        output="screen",  # Đẩy toàn bộ thông tin log của quá trình thả robot trực tiếp ra màn hình Terminal hiện tại
        arguments=["-topic", "robot_description",  # Lấy dữ liệu cấu trúc robot từ topic '/robot_description' mà Node 1 đang phát ra
                   "-name", "bumperbot"],  # Đặt tên định danh cho thực thể robot khi xuất hiện trong thế giới Gazebo là 'bumperbot'
    )  

    gz_ros2_bridge = Node(  # Cấu hình Node 3: Tạo cầu nối dữ liệu (Bridge) giữa mạng Gazebo và mạng ROS 2
        package="ros_gz_bridge",  # Thuộc package 'ros_gz_bridge'
        executable="parameter_bridge",  # Gọi file thực thi thiết lập cầu nối dữ liệu theo tham số cấu hình
        arguments=[  # Định nghĩa danh sách các luồng dữ liệu cần thông suốt giữa 2 môi trường:
            "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock",  # Cầu nối truyền thời gian giả lập góc (Clock) từ Gazebo sang ROS 2
            "/imu@sensor_msgs/msg/Imu[gz.msgs.IMU",  # Cầu nối truyền dữ liệu cảm biến quán tính (IMU) từ Gazebo sang ROS 2
            "/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan"  # Cầu nối truyền dữ liệu mảng quét tia Laser (LiDAR) từ Gazebo sang ROS 2
        ],  
        remappings=[  # Ánh xạ/Đổi tên lại các topic hệ thống cho gọn gàng hoặc đúng kiến trúc thiết kế
            ('/imu', '/imu/out'),  # Đổi tên topic mặc định từ '/imu' thành '/imu/out' để khớp với các bộ lọc dữ liệu khác của bạn
        ]  
    )  

    return LaunchDescription([  # Trả về toàn bộ danh sách tập hợp các cấu hình để ROS 2 tiến hành khởi chạy đồng loạt
        model_arg,  # Kích hoạt tham số cấu hình tệp robot xacro
        world_name_arg,  # Kích hoạt tham số lựa chọn bản đồ giả lập
        gazebo_resource_path,  # Đăng ký biến môi trường tìm kiếm tài nguyên cho Gazebo
        robot_state_publisher_node,  # Khởi chạy bộ phát trạng thái và tính toán hệ tọa độ robot
        gazebo,  # Mở trình giả lập đồ họa Gazebo Sim cùng bản đồ đã chọn
        gz_spawn_entity,  # Thực hiện lệnh thả robot vào vị trí trong không gian giả lập
        gz_ros2_bridge  # Khởi động cầu nối để truyền nhận dữ liệu cảm biến (IMU, LiDAR, Clock) thông suốt giữa ROS 2 và Gazebo
    ])  # Kết thúc kịch bản cấu hình launch file cho robot Bumperbot