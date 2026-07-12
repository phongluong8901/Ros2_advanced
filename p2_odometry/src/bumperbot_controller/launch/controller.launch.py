from launch import LaunchDescription  # Nhập lớp LaunchDescription để gom nhóm các tiến trình và trả về cấu hình chạy chung
from launch.actions import DeclareLaunchArgument, GroupAction, OpaqueFunction  # Nhập các hành động: Khai báo tham số, Nhóm các node, và Hàm xử lý động OpaqueFunction
from launch_ros.actions import Node  # Nhập lớp Node để thiết lập cấu hình khởi chạy các Node ROS 2 độc lập
from launch.substitutions import LaunchConfiguration  # Nhập công cụ giúp đọc giá trị của các tham số cấu hình (Launch Arguments)
from launch.conditions import UnlessCondition, IfCondition  # Nhập các điều kiện bật/tắt Node: IfCondition (Nếu True) và UnlessCondition (Nếu False)


def noisy_controller(context, *args, **kwargs):  # Hàm Python phụ trợ được gọi bởi OpaqueFunction để tính toán số liệu và trả về Node động
    use_sim_time = LaunchConfiguration("use_sim_time")  # Đọc trạng thái tham số dùng thời gian mô phỏng
    use_python = LaunchConfiguration("use_python")  # Đọc tham số quyết định chạy Node bằng ngôn ngữ Python hay C++
    wheel_radius = float(LaunchConfiguration("wheel_radius").perform(context))  # Thực thi lấy giá trị thực tế của bán kính bánh xe và ép kiểu sang số thực (float)
    wheel_separation = float(LaunchConfiguration("wheel_separation").perform(context))  # Thực thi lấy giá trị khoảng cách 2 bánh xe và ép kiểu sang số thực (float)
    wheel_radius_error = float(LaunchConfiguration("wheel_radius_error").perform(context))  # Lấy giá trị sai số bán kính bánh xe (để tạo nhiễu giả lập thực tế)
    wheel_separation_error = float(LaunchConfiguration("wheel_separation_error").perform(context))  # Lấy giá trị sai số khoảng cách giữa 2 bánh xe

    noisy_controller_py = Node(  # Định nghĩa Node bộ điều khiển nhiễu phiên bản Python
        package="bumperbot_controller",  # Thuộc package 'bumperbot_controller' bạn tự phát triển
        executable="noisy_controller.py",  # Tên file thực thi Python tạo nhiễu odom
        parameters=[  # Truyền các tham số vật lý đã bị cộng thêm sai số vào Node
            {"wheel_radius": wheel_radius + wheel_radius_error,  # Bán kính bánh xe thực tế sau khi bị làm nhiễu
             "wheel_separation": wheel_separation + wheel_separation_error,  # Khoảng cách bánh xe thực tế sau khi bị làm nhiễu
             "use_sim_time": use_sim_time}],  # Trạng thái đồng bộ thời gian giả lập
        condition=IfCondition(use_python),  # Chỉ khởi chạy Node Python này nếu tham số 'use_python' được bật là True
    )  

    noisy_controller_cpp = Node(  # Định nghĩa Node bộ điều khiển nhiễu phiên bản C++ (chạy mượt và nhanh hơn)
        package="bumperbot_controller",  # Thuộc package 'bumperbot_controller'
        executable="noisy_controller",  # Tên file thực thi C++ (không có đuôi .py)
        parameters=[  # Truyền các tham số vật lý đã tính toán nhiễu tương tự như trên
            {"wheel_radius": wheel_radius + wheel_radius_error,  
             "wheel_separation": wheel_separation + wheel_separation_error,  
             "use_sim_time": use_sim_time}],  
        condition=UnlessCondition(use_python),  # Chỉ khởi chạy Node C++ này nếu tham số 'use_python' là False
    )  

    return [  # Trả về danh sách các Node điều khiển nhiễu để hệ thống launch kích hoạt dựa theo điều kiện ngôn ngữ
        noisy_controller_py,  
        noisy_controller_cpp,  
    ]  



def generate_launch_description():  # Hàm chính khởi tạo cấu hình launch file của ROS 2
    
    use_sim_time_arg = DeclareLaunchArgument(  # Tham số 1: Sử dụng thời gian mô phỏng
        "use_sim_time",  # Tên tham số
        default_value="True",  # Mặc định bật True khi chạy trong môi trường giả lập Gazebo
    )  
    use_simple_controller_arg = DeclareLaunchArgument(  # Tham số 2: Chọn bộ điều khiển đơn giản hay bộ điều khiển chuẩn ros2_control
        "use_simple_controller",  
        default_value="True",  # Mặc định sử dụng bộ điều khiển đơn giản 'simple_velocity_controller'
    )  
    use_python_arg = DeclareLaunchArgument(  # Tham số 3: Lựa chọn ngôn ngữ lập trình cho các Node điều khiển tự viết
        "use_python",  
        default_value="False",  # Mặc định chạy phiên bản C++ để tối ưu hiệu năng
    )  
    wheel_radius_arg = DeclareLaunchArgument(  # Tham số 4: Bán kính thiết kế chuẩn của bánh xe robot Bumperbot
        "wheel_radius",  
        default_value="0.033",  # Mặc định là 0.033 m (3.3 cm)
    )  
    wheel_separation_arg = DeclareLaunchArgument(  # Tham số 5: Khoảng cách thiết kế chuẩn giữa 2 bánh xe chủ động
        "wheel_separation",  
        default_value="0.17",  # Mặc định là 0.17 m (17 cm)
    )  
    wheel_radius_error_arg = DeclareLaunchArgument(  # Tham số 6: Độ lệch/Sai số của bán kính bánh xe để thử nghiệm thuật toán
        "wheel_radius_error",  
        default_value="0.005",  # Mặc định giả lập sai số 5 mm
    )  
    wheel_separation_error_arg = DeclareLaunchArgument(  # Tham số 7: Độ lệch/Sai số của khoảng cách 2 bánh xe khi lắp ráp thực tế
        "wheel_separation_error",  
        default_value="0.02",  # Mặc định giả lập sai số 2 cm
    )  
    
    use_sim_time = LaunchConfiguration("use_sim_time")  # Đọc cấu hình biến use_sim_time từ Terminal
    use_simple_controller = LaunchConfiguration("use_simple_controller")  # Đọc cấu hình chọn bộ điều khiển
    use_python = LaunchConfiguration("use_python")  # Đọc cấu hình chọn ngôn ngữ Python/C++
    wheel_radius = LaunchConfiguration("wheel_radius")  # Đọc cấu hình thông số bán kính bánh xe
    wheel_separation = LaunchConfiguration("wheel_separation")  # Đọc cấu hình thông số khoảng cách 2 bánh

    joint_state_broadcaster_spawner = Node(  # Node spawner: Kích hoạt bộ phát trạng thái các khớp (Joint State Broadcaster)
        package="controller_manager",  # Thuộc package quản lý controller trung tâm của ROS 2
        executable="spawner",  # File thực thi spawner dùng để nạp controller vào bộ nhớ
        arguments=[  
            "joint_state_broadcaster",  # Tên bộ điều khiển cần kích hoạt (đọc vị trí encoder bánh xe để phát TF)
            "--controller-manager",  # Cờ chỉ định dịch vụ quản lý khớp
            "/controller_manager",  # Tên topic dịch vụ quản lý controller chính
        ],  
    )  

    wheel_controller_spawner = Node(  # Node spawner: Kích hoạt bộ điều khiển bánh xe nâng cao (thường là Diff Drive Controller chuẩn)
        package="controller_manager",  
        executable="spawner",  
        arguments=["bumperbot_controller",   # Kích hoạt bộ điều khiển mang tên 'bumperbot_controller' đã cấu hình trong file yaml
                   "--controller-manager",   
                   "/controller_manager"  
        ],  
        condition=UnlessCondition(use_simple_controller),  # Chỉ chạy node này nếu 'use_simple_controller' là False (tức là muốn dùng bộ điều khiển phức tạp)
    )  

    simple_controller = GroupAction(  # Nhóm các hành động (GroupAction) sẽ cùng chạy nếu thỏa mãn điều kiện dùng bộ điều khiển đơn giản
        condition=IfCondition(use_simple_controller),  # Điều kiện: Kích hoạt nhóm này khi 'use_simple_controller' là True
        actions=[  
            Node(  # Node con 1 trong nhóm: Kích hoạt bộ điều khiển vận tốc cơ bản
                package="controller_manager",  
                executable="spawner",  
                arguments=["simple_velocity_controller",   # Tên bộ điều khiển đơn giản được cấu hình sẵn để nhận lệnh cmd_vel
                        "--controller-manager",   
                        "/controller_manager"  
                ]  
            ),  
            Node(  # Node con 2 trong nhóm: Khởi chạy node thuật toán chuyển đổi động học bằng Python
                package="bumperbot_controller",  
                executable="simple_controller.py",  # File Python thực hiện tính toán chuyển đổi từ cmd_vel ra tốc độ từng bánh xe
                parameters=[  
                    {"wheel_radius": wheel_radius,  # Nạp thông số bán kính chuẩn
                    "wheel_separation": wheel_separation,  # Nạp thông số khoảng cách chuẩn
                    "use_sim_time": use_sim_time}],  
                condition=IfCondition(use_python),  # Chỉ chạy node thuật toán Python này nếu 'use_python' là True
            ),  
            Node(  # Node con 3 trong nhóm: Khởi chạy node thuật toán chuyển đổi động học bằng C++
                package="bumperbot_controller",  
                executable="simple_controller",  # File thực thi C++ làm nhiệm vụ tương tự node Python phía trên
                parameters=[  
                    {"wheel_radius": wheel_radius,  
                    "wheel_separation": wheel_separation,  
                    "use_sim_time": use_sim_time}],  
                condition=UnlessCondition(use_python),  # Chỉ chạy node thuật toán C++ này nếu 'use_python' là False
            ),  
        ]  
    )  

    noisy_controller_launch = OpaqueFunction(function=noisy_controller)  # Sử dụng OpaqueFunction để gọi hàm 'noisy_controller', cho phép tính toán toán học (cộng sai số) ngay khi đang load cấu hình launch

    return LaunchDescription(  # Trả về danh sách toàn bộ các tham số và tiến trình Node để ROS 2 thực thi
        [  
            use_sim_time_arg,  # Đăng ký tham số thời gian mô phỏng
            use_simple_controller_arg,  # Đăng ký tham số lựa chọn bộ điều khiển
            use_python_arg,  # Đăng ký tham số lựa chọn ngôn ngữ
            wheel_radius_arg,  # Đăng ký tham số bán kính bánh xe
            wheel_separation_arg,  # Đăng ký tham số khoảng cách bánh xe
            wheel_radius_error_arg,  # Đăng ký tham số sai số bán kính
            wheel_separation_error_arg,  # Đăng ký tham số sai số khoảng cách bánh
            joint_state_broadcaster_spawner,  # Khởi chạy node phát trạng thái khớp robot
            wheel_controller_spawner,  # Khởi chạy node nạp bộ điều khiển nâng cao (nếu được chọn)
            simple_controller,  # Khởi chạy nhóm bộ điều khiển đơn giản kèm node thuật toán chuyển đổi động học tương ứng
            noisy_controller_launch,  # Kích hoạt hàm OpaqueFunction để tính toán nhiễu và bật node tạo odom sai số thực tế
        ]  
    )  # Kết thúc tệp launch cấu hình điều khiển cho robot Bumperbot