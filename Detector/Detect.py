import cv2
import numpy as np

class Detect:
    """
    主识别器
    ----
    * 包含图像处理与识别的基本功能
    """

    def __init__(self, image=None):
        self.image = image
    
    def sharpen(self):
        """锐化图像"""
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])
        self.image = cv2.filter2D(self.image, -1, kernel)

    def select_region(self, start_point, end_point):
        """选取图像区域"""
        return self.image[start_point[1]:end_point[1], start_point[0]:end_point[0]]

    def adjust_exposure(self, alpha, beta):
        """调整曝光度
        alpha: 亮度增益因子
        beta: 亮度偏移
        """
        self.image = cv2.convertScaleAbs(self.image, alpha=alpha, beta=beta)

    def get_processed_image(self):
        """返回处理后的图像"""
        return self.image


