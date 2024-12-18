
import sys
sys.path.append("/ProgramData/Anaconda3/Lib/site-packages")

print("add sys path /ProgramData/Anaconda3/Lib/site-packages")
import serial
class Usart(serial.Serial):
    """
    串口通信类
    ----
    * 继承了serial.Serial类，实现了使用包头包尾接受数据的方法
    * 发送数据的时候可以指定包头包尾
    """

    def __init__(self, port, baudrate=9600, timeout=None):
        super().__init__(port=port, baudrate=baudrate, timeout=timeout)

    def read(self):
        """
        读取数据
        ----
        :return: 数据
        """
        data = super().read()
        print(data)
        return data.decode('utf-8')

 

    def write(self, data):
            """
    发送数据
    ----
    :param data: 数据
    """
            super().write(data)

    def clear(self):
        """
        清除缓存区
        """
        super().reset_input_buffer()
        super().reset_output_buffer()
