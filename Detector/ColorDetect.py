import cv2
import numpy as np
try:
    from Detect import Detect
except ModuleNotFoundError:
    from.Detect import Detect


import cv2
import numpy as np

# 定义颜色阈值字典
COLOR_DICT = {
    1: {'name': 'R', 'low_h': 0, 'high_h': 10, 'low_s': 100, 'high_s': 255, 'low_v': 100, 'high_v': 255},  # 红色
    2: {'name': 'G', 'low_h': 40, 'high_h': 80, 'low_s': 100, 'high_s': 255, 'low_v': 100, 'high_v': 255},  # 绿色
    3: {'name': 'B', 'low_h': 100, 'high_h': 140, 'low_s': 100, 'high_s': 255, 'low_v': 100, 'high_v': 255}   # 蓝色
}

class ColorDetector(Detect):
    def __init__(self) -> None:
        """初始化"""
        self.current_color = None
    
    def set_color(self, color_number: int):
        """设置当前颜色"""
        if color_number in COLOR_DICT:
            self.current_color = color_number
         
    def detect(self, img: cv2.typing.MatLike):
        """检测图像中的颜色，返回二值化图像"""
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
     
        
        # 获取当前颜色的阈值
        thresholds = COLOR_DICT[self.current_color]
        low = np.array([thresholds['low_h'], thresholds['low_s'], thresholds['low_v']])
        high = np.array([thresholds['high_h'], thresholds['high_s'], thresholds['high_v']])
        
        mask = cv2.inRange(hsv, low, high)
        kernel = np.ones((5, 5), np.uint8)  # 5x5内核，可以根据需要调整

        # 腐蚀和膨胀操作
        mask = cv2.dilate(mask, kernel, iterations=3)
        # mask = cv2.erode(mask, kernel, iterations=1)

      
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
                largest_contour = max(contours, key=cv2.contourArea)
                if cv2.contourArea(largest_contour) > 0:  # 检查是否有有效的轮廓
                    masked_frame = cv2.bitwise_and(img, img, mask=mask)
                    return mask, masked_frame, self.current_color
                    
                    
# 如果没有找到轮廓或没有有效轮廓，返回一个空的掩码和默认颜色
        return np.zeros_like(mask),np.zeros_like(img), None  # 返回一个有效的默认值而不是 None

        
     
    
    # def draw_rectangle(self, frame: cv2.typing.MatLike):
    #     """在原始图像上绘制矩形框并检测颜色"""
    #     mask = self.detect(frame) 
    #     contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
    #     if contours:
    #         largest_contour = max(contours, key=cv2.contourArea)
    #         if cv2.contourArea(largest_contour) > 0:  # 检查是否有有效的轮廓
    #             x, y, w, h = cv2.boundingRect(largest_contour)
    #             color_name = COLOR_DICT[self.current_color]['name']

    #             cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    #             cv2.putText(frame, f"Detected Color: {color_name}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    #     return frame, mask

if __name__ == "__main__":
    cap = cv2.VideoCapture(1)
    detector = ColorDetector()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 调用检测和绘制
        mask, masked_frame, colornumber = detector.detect(frame)

        cv2.imshow("mask", mask)
        cv2.imshow("frame", frame)

        if colornumber is not None:
            print(colornumber)
        else:
            print("None")
        

        if cv2.waitKey(0) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
