from PyQt5.QtWidgets import QWidget, QLabel, QPushButton
from PyQt5.QtGui import QPixmap


class CustomPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Solving Interface')
        self.setGeometry(100, 100, 1024, 768)

        width = self.width()
        height = self.height()
        # 創建背景標籤
        self.background_label = QLabel(self)
        self.background_label.setGeometry(0, 0, self.width(), self.height())

        # 呼叫設定背景圖片函數
        self.set_background_image('Window/image/3.jpg')

        # 創建按鈕
        self.create_buttons()

        # 創建返回按鈕
        self.back_button = QPushButton('', self)
        self.back_button.setGeometry(
            0, 0, int(width*0.0625), int(height*0.0807265))
        # self.back_button.setStyleSheet('background-color: transparent; font-size: 18px;')

    def set_background_image(self, image_path):
        # 載入圖片
        background_image = QPixmap(image_path)
        if background_image.isNull():
            print(f"圖片未加載成功，請確認路徑：{image_path}")
        else:
            # 將背景圖片設定給 QLabel
            self.background_label.setPixmap(background_image)
            self.background_label.setScaledContents(True)

    def resizeEvent(self, event):
        # 重新設定背景圖片大小
        self.background_label.setGeometry(0, 0, self.width(), self.height())

        width = self.width()
        height = self.height()
        button_width = int(width * 0.15)
        button_height = int(height * 0.25)

        self.button1.setGeometry(
            int(width * 0.425), int(height * 0.26), button_width, button_height)  # 國文
        self.button2.setGeometry(
            int(width * 0.675), int(height * 0.26), button_width, button_height)  # 英文
        self.button3.setGeometry(
            int(width * 0.18), int(height * 0.61), button_width, button_height)  # 數學
        self.button4.setGeometry(
            int(width * 0.425), int(height * 0.61), button_width, button_height)  # 自然
        self.button5.setGeometry(
            int(width * 0.675), int(height * 0.61), button_width, button_height)  # 社會

        # self.button1.setStyleSheet('background-color: transparent;')
        # self.button2.setStyleSheet('background-color: transparent;')
        # self.button3.setStyleSheet('background-color: transparent;')
        # self.button4.setStyleSheet('background-color: transparent;')
        # self.button5.setStyleSheet('background-color: transparent;')

    def create_buttons(self):
        self.button1 = QPushButton('國文', self)
        self.button2 = QPushButton('英文', self)
        self.button3 = QPushButton('數學', self)
        self.button4 = QPushButton('自然', self)
        self.button5 = QPushButton('社會', self)
        self.button_map={"國文":self.button1,"英文":self.button2,"數學":self.button3,"自然":self.button4,"社會":self.button5}