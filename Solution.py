import cv2
import numpy as np
from pyzbar.pyzbar import decode
from USART.communicate import Usart
import Detector
import time

SERIAL_PORT= "/dev/ttyUSB1" 

def show(img):
    return cv2.imshow("img", img)


class Solution:
    RED_LIGHT = 0
    GREEN_LIGHT = 1
    YELLOW_LIGHT = 0
    NO_LIGHT = 0


    def __init__(self,  ser_port: str):
        self.circle_detector = Detector.CircleDetector()
        self.color_detector = Detector.ColorDetector()
        self.uart = Usart(ser_port)
        self.ser_port = ser_port
        self.qr_data = None
        pass

    def QR_code_recognition(self, img):
        """
        二维码识别
        """
        decoded_objects = decode(img)
        if decoded_objects:  # 如果解码成功，且存在二维码
            for obj in decoded_objects:
            # 获取二维码类型
                qr_type = obj.type
            # 获取二维码数据
                self.qr_data = obj.data.decode('utf-8')
                print(f"二维码类型: {qr_type}, 数据: {self.qr_data}")
                self.write_serial1(self.qr_data)
                return self.qr_data


            return None 

    def Color_Card_Recognition(self, _img):
        """
        颜色卡识别
        :param _img: 输入图像
        :return: 颜色卡识别结果
        """
        if self.qr_data is not None:
            parts = self.qr_data.split('+')  # 基于 "+" 拆分字符串
            if len(parts) >= 3:  # 确保有足够的部分
                color_number = parts[2]  # 获取中间的部分作为 color_number
        self.color_detector.set_color(color_number)
        mask,masked_frame,colornumber = self.color_detector.detect(_img)
        self.write_serial2(colornumber)
        return colornumber


 
    

    
    def target_hit(self, _img):
        """
        目标标靶检测
        ----
        本方法会在传入的图像上画出圆形区域和颜色识别区

        :param _img: 图片
        :return: 颜色(str)，位置(tuple)列表，如果没识别到园则返回None
        """
        return_lst = []  # 返回值
        img = _img.copy()
        if self.qr_data is not None:
            parts = self.qr_data.split('+')  # 基于 "+" 拆分字符串
            if len(parts) >= 3:  # 确保有足够的部分
                color_number = parts[1]
        self.color_detector.set_color(color_number)
        mask,masked_frame,colornumber = self.color_detector.detect(img)
        detected_color_number = colornumber
        # self.write_serial2(colornumber)
        point_lst, r_lst = self.circle_detector.detect(masked_frame)  # 使用框选后的帧检测圆形
        if point_lst is None:
            return None
        for point in zip(point_lst):
             self.write_serial3(point[0][0])
             return point[0][0]
        #     return_lst.append((detected_color_number, point))
        # return return_lst
        


    def trafficlight_detect(self, img):
        """
        红绿灯检测
        ----
        :param _img: 输入图像
        :return: 红绿灯检测结果
        
        """


        low_exposure = cv2.convertScaleAbs(img, alpha=1.0, beta=-80)
        # 2. ROI (Region of Interest) 面积处理
        height, width = low_exposure.shape[:2]
        roi = low_exposure[int(height * 0.2):int(height * 0.8), int(width * 0.2):int(width * 0.8)]

        # 3. hsv颜色空间处理
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 100, 100])
        upper_red2 = np.array([180, 255, 255])
        mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask_red = cv2.bitwise_or(mask_red1, mask_red2)

# 绿色
        lower_green = np.array([40, 100, 100])
        upper_green = np.array([80, 255, 255])
        mask_green = cv2.inRange(hsv, lower_green, upper_green)

# 黄色
        lower_yellow = np.array([25, 100, 100])
        upper_yellow = np.array([35, 255, 255])
        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

# 合并掩膜
        mask_combined = cv2.bitwise_or(mask_red, mask_green)
        mask_combined = cv2.bitwise_or(mask_combined, mask_yellow)
        masked_frame = cv2.bitwise_and(roi, roi, mask=mask_combined)

        if cv2.countNonZero(mask_red) > 30:
            self.write_serial4(0)
            return {self.RED_LIGHT}
        elif cv2.countNonZero(mask_green) > 0:
            self.write_serial4(1)
            return {self.GREEN_LIGHT}
        elif cv2.countNonZero(mask_yellow) > 15:
            self.write_serial4(0)
            return {self.YELLOW_LIGHT}
        else:   
            self.write_serial4(0)
            return {self.NO_LIGHT}


       

       

    def read_serial(self):
        """
        读取串口数据
        ----

        """
        # 清除缓冲区
        self.uart.clear()
        # 读取数据
        return self.uart.read()

    def write_serial1(self, data):
                
                """
    写入串口数据
    ----
    :param data: 数据
                """
 
                formatted_data = f"A{data.replace('+', '')}E"
                self.uart.write(formatted_data.encode('utf-8')) 
    def write_serial2(self, data):
         
            """
    写入串口数据
    ----
    :param data: 数据
         """
    
            formatted_data = f"B{data}F"
            self.uart.write(formatted_data.encode('utf-8')) 
            print(self.uart.write(formatted_data.encode('utf-8')))
    def write_serial3(self, data):
         
            """
    写入串口数据
    ----
    :param data: 数据
         """
    
            formatted_data = f"C{data}G"
            self.uart.write(formatted_data.encode('utf-8')) 


           

    def write_serial4(self, data):
         
            """
    写入串口数据
    ----
    :param data: 数据
         """
    
            formatted_data = f"D{data}H"
            self.uart.write(formatted_data.encode('utf-8')) 




