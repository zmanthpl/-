import cv2
import Solution
SERIAL_PORT = "/dev/ttyUSB1"  # TODO: 填写串口号
# region 主代码
solution = Solution.Solution(SERIAL_PORT)
solution_dict = {  # TODO: 可能要更改对应任务的串口信号
    '0': solution.QR_code_recognition,  # 二维码检测
    '1': solution.Color_Card_Recognition,  # 色卡检测
    '2': solution.target_hit,  # 靶子检测
    '3': solution.trafficlight_detect,  # 红绿灯检测
}
while True:
    sign = solution.read_serial()  # 读取串口
    # print(sign)

    # 判断信号是否合法
    if sign in solution_dict:  # 信号合法
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()  # 捕捉图像
        if not ret:
            print("Error: Failed to capture image.")
            continue  # 确保读取成功后再处理
        solution_dict[sign](frame)  # 调用对应的函数处理图像
        cap.release()

    else:  # 信号非法
        print("Invalid sign")
        continue

