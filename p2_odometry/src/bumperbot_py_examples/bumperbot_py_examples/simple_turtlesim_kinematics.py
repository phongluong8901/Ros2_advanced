import rclpy  # Nhập thư viện rclpy cốt lõi để lập trình ROS 2 bằng Python
from rclpy.node import Node  # Nhập lớp Node để tạo và quản lý một Node trong hệ thống ROS 2
from turtlesim.msg import Pose  # Nhập kiểu dữ liệu Pose (chứa tọa độ x, y, góc theta) từ package turtlesim
import math  # Nhập thư viện toán học tiêu chuẩn của Python để dùng các hàm lượng giác sin, cos


class SimpleTurtlesimKinematics(Node):  # Định nghĩa lớp SimpleTurtlesimKinematics kế thừa từ lớp Node của ROS 2
    
    def __init__(self):  # Hàm khởi tạo (Constructor) của lớp khi đối tượng được tạo ra
        super().__init__("simple_turtlesim_kinematics")  # Gọi hàm khởi tạo của lớp cha và đặt tên Node này là 'simple_turtlesim_kinematics'
        self.turtle1_pose_sub_ = self.create_subscription(Pose, "/turtle1/pose", self.turtle1PoseCallback, 10)   # Tạo Subscriber lắng nghe vị trí rùa 1 trên topic '/turtle1/pose' với hàng đợi là 10
        self.turtle2_pose_sub_ = self.create_subscription(Pose, "/turtle2/pose", self.turtle2PoseCallback, 10)  # Tạo Subscriber lắng nghe vị trí rùa 2 trên topic '/turtle2/pose' với hàng đợi là 10

        self.last_turtle1_pose_ = Pose()  # Khởi tạo biến lưu trữ tọa độ mới nhất của rùa 1 (mặc định ban đầu x=0, y=0, theta=0)
        self.last_turtle2_pose_ = Pose()  # Khởi tạo biến lưu trữ tọa độ mới nhất của rùa 2 để phục vụ tính toán toán học

    
    def turtle1PoseCallback(self, pose):  # Hàm callback tự động kích hoạt mỗi khi nhận được dữ liệu vị trí mới từ rùa 1
        self.last_turtle1_pose_ = pose  # Cập nhật và lưu lại dữ liệu vị trí vừa nhận được vào biến thành viên của lớp


    def turtle2PoseCallback(self, pose):  # Hàm callback tự động kích hoạt mỗi khi nhận được dữ liệu vị trí mới từ rùa 2
        self.last_turtle2_pose_ = pose  # Cập nhật và lưu lại dữ liệu vị trí vừa nhận được của rùa 2
        Tx = self.last_turtle2_pose_.x - self.last_turtle1_pose_.x  # Tính khoảng cách chênh lệch vector tịnh tiến theo trục X từ rùa 1 sang rùa 2
        Ty = self.last_turtle2_pose_.y - self.last_turtle1_pose_.y  # Tính khoảng cách chênh lệch vector tịnh tiến theo trục Y từ rùa 1 sang rùa 2
        theta_rad = self.last_turtle2_pose_.theta - self.last_turtle1_pose_.theta  # Tính độ lệch góc hướng (orientation) giữa rùa 2 và rùa 1 theo đơn vị Radian
        theta_deg = 180 * theta_rad / 3.14  # Chuyển đổi độ lệch góc vừa tính được từ đơn vị Radian sang độ (Degree)
        self.get_logger().info("""\n
                      Translation Vector turtle1 -> turtle2\n
                      Tx: %f\n
                      Ty: %f\n
                      Rotation Matrix turtle1 -> turtle2\n 
                      theta (rad): %f\n
                      theta (deg): %f\n
                      |R11   R12|:  |%f %f|\n
                      |R21   R22|   |%f %f|\n""" %  # Định dạng chuỗi văn bản nhiều dòng để chuẩn bị in kết quả động học ra màn hình
                      (  # Truyền danh sách các biến vào chuỗi định dạng %f ở trên theo thứ tự tương ứng:
                        Tx, Ty, theta_rad, theta_deg,  # Truyền vector tịnh tiến Tx, Ty cùng góc quay theo Rad và Độ
                        math.cos(theta_rad), -math.sin(theta_rad),  # Tính toán và truyền phần tử hàng 1 (R11, R12) của ma trận xoay 2D
                        math.sin(theta_rad), math.cos(theta_rad)  # Tính toán và truyền phần tử hàng 2 (R21, R22) của ma trận xoay 2D
                      )  # Kết thúc danh sách các biến truyền vào
                    )  # Kết thúc lệnh in log thông tin ra Terminal
        

def main():  # Hàm khởi chạy chính của toàn bộ chương trình Python
    rclpy.init()  # Khởi tạo hệ thống giao tiếp mạng ROS 2 cho script này

    simple_turtlesim_kinematics = SimpleTurtlesimKinematics()  # Tạo một đối tượng (Instance) từ lớp Node tính toán động học đã định nghĩa ở trên
    rclpy.spin(simple_turtlesim_kinematics)  # Giữ cho Node luôn chạy, liên tục kiểm tra và xử lý các hàm callback khi có dữ liệu mới truyền đến
    
    simple_turtlesim_kinematics.destroy_node()  # Giải phóng bộ nhớ và hủy Node khi người dùng nhấn Ctrl+C để tắt chương trình
    rclpy.shutdown()  # Tắt hoàn toàn hệ thống giao tiếp ROS 2 của tiến trình này


if __name__ == '__main__':  # Kiểm tra nếu file này được chạy trực tiếp từ Terminal chứ không phải được import từ file khác
    main()  # Kích hoạt gọi hàm main để bắt đầu chạy chương trình