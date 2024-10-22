import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QStackedWidget, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QRect

# 自訂第三頁的視窗
class CustomPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Solving Interface')
        self.setGeometry(100, 100, 1024, 768)

        # 創建背景標籤
        self.background_label = QLabel(self)
        self.background_label.setGeometry(0, 0, self.width(), self.height())

        # 呼叫設定背景圖片函數
        self.set_background_image('image/3.jpg')

        # 創建按鈕
        self.create_buttons()

        # 創建返回按鈕
        self.back_button = QPushButton('', self)
        self.back_button.setGeometry(0, 0, 150, 100)
        self.back_button.setStyleSheet('background-color: transparent; font-size: 18px;')

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

        self.button1.setGeometry(int(width * 0.425), int(height * 0.26), button_width, button_height)  # 國文
        self.button2.setGeometry(int(width * 0.675), int(height * 0.26), button_width, button_height)  # 英文
        self.button3.setGeometry(int(width * 0.18), int(height * 0.61), button_width, button_height)  # 數學
        self.button4.setGeometry(int(width * 0.425), int(height * 0.61), button_width, button_height)  # 自然
        self.button5.setGeometry(int(width * 0.675), int(height * 0.61), button_width, button_height)  # 社會

        self.button1.setStyleSheet('background-color: transparent;')
        self.button2.setStyleSheet('background-color: transparent;')
        self.button3.setStyleSheet('background-color: transparent;')
        self.button4.setStyleSheet('background-color: transparent;')
        self.button5.setStyleSheet('background-color: transparent;')

    def create_buttons(self):
        self.button1 = QPushButton(' ', self)
        self.button2 = QPushButton(' ', self)
        self.button3 = QPushButton(' ', self)
        self.button4 = QPushButton(' ', self)
        self.button5 = QPushButton(' ', self)

        self.button1.clicked.connect(lambda: self.on_button_click('國文'))
        self.button2.clicked.connect(lambda: self.on_button_click('英文'))
        self.button3.clicked.connect(lambda: self.on_button_click('數學'))
        self.button4.clicked.connect(lambda: self.on_button_click('自然'))
        self.button5.clicked.connect(lambda: self.on_button_click('社會'))

    def on_button_click(self, button_name):
        print(f"{button_name} 按鈕被點擊！")


# 主視窗類別
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('介面應用')

        # Stack Widget 用來管理多個頁面
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        # 第一頁
        self.page1 = QLabel(self)
        pixmap1 = QPixmap('image/1.png')  # 替換為你的第一張圖片
        self.page1.setPixmap(pixmap1)
        self.page1.setScaledContents(True)
        self.stacked_widget.addWidget(self.page1)

        # 第二頁 (選大類別頁面)
        self.page2 = QLabel(self)
        pixmap2 = QPixmap('image/2.png')  # 替換為你的第二張圖片
        self.page2.setPixmap(pixmap2)
        self.page2.setScaledContents(True)
        self.stacked_widget.addWidget(self.page2)

        # 創建並添加按鈕至第二頁
        width = 1920
        height = 1080
        button_width = width * 0.2
        button_height = height * 0.2

        button_positions = [
            (width * 0.1, height * 0.2),  # 按鈕 1
            (width * 0.4, height * 0.2),  # 按鈕 2
            (width * 0.7, height * 0.2),  # 按鈕 3
            (width * 0.25, height * 0.6),  # 按鈕 4
            (width * 0.55, height * 0.6)   # 按鈕 5
        ]

        for i, pos in enumerate(button_positions):
            btn = QPushButton('', self.page2)
            btn.setGeometry(QRect(int(pos[0]), int(pos[1]), int(button_width), int(button_height)))  # 調整按鈕的位置和大小
            btn.setStyleSheet('background-color: transparent;')
            btn.clicked.connect(lambda checked, idx=i+1: self.showPage(idx))

        # 回到第一頁的返回按鈕
        back_btn = QPushButton('', self.page2)
        back_btn.setGeometry(QRect(0, 0, 150, 100))
        back_btn.setStyleSheet('background-color: transparent;')
        back_btn.clicked.connect(self.goBackToFirstPage)

        # 第三頁 (自訂頁面)
        self.page3 = CustomPage(self)
        self.page3.back_button.clicked.connect(self.goBackToSecondPage)  # 將返回按鈕連接到返回第二頁
        self.stacked_widget.addWidget(self.page3)

        # 頁面間的切換
        self.page1.mousePressEvent = self.changePage

    def changePage(self, event):
        self.stacked_widget.setCurrentIndex(1)

    def showPage(self, button_id):
        if button_id == 1:
            self.stacked_widget.setCurrentIndex(2)  # 自訂頁面
        # 可在這裡擴充其他按鈕的頁面切換邏輯

    def goBackToFirstPage(self):
        self.stacked_widget.setCurrentIndex(0)

    def goBackToSecondPage(self):
        self.stacked_widget.setCurrentIndex(1)  # 返回第二頁


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.showMaximized()  # 最大化顯示
    sys.exit(app.exec_())
