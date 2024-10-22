#第一頁 封面 第二頁選大類別 第三頁 解題 第四頁專注 第五頁 英文 第六頁統計 第七頁 讀書會
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QStackedWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QRect

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('介面應用')

        # Stack Widget for managing multiple pages
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        # First page (first image)
        self.page1 = QLabel(self)
        pixmap1 = QPixmap('1.png')  # 替換為你的第一張圖片
        self.page1.setPixmap(pixmap1)
        self.page1.setScaledContents(True)
        self.stacked_widget.addWidget(self.page1)

        # Second page (second image with hidden buttons)
        self.page2 = QLabel(self)
        pixmap2 = QPixmap('2.png')  # 替換為你的第二張圖片
        self.page2.setPixmap(pixmap2)
        self.page2.setScaledContents(True)
        self.stacked_widget.addWidget(self.page2)

        width = 1920
        height = 1080
        button_width = width * 0.2
        button_height = height * 0.2

        # Create 5 buttons on second page
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
            btn.setStyleSheet('background-color: transparent;')  # 使按鈕透明
            btn.clicked.connect(lambda checked, idx=i+1: self.showPage(idx))

        # Add back button on top left corner (returns to first page)
        back_btn = QPushButton('', self.page2)
        back_btn.setGeometry(QRect(0, 0, 150, 100))  # 左上角返回按鈕
        back_btn.setStyleSheet('background-color: transparent;')  # 透明按鈕
        back_btn.clicked.connect(self.goBackToFirstPage)

        # Third page
        self.page3 = QLabel(self)
        pixmap3 = QPixmap('3.jpg')  # 替換為你的第三張圖片
        self.page3.setPixmap(pixmap3)
        self.page3.setScaledContents(True)
        self.stacked_widget.addWidget(self.page3)

        back_btn_page3 = QPushButton('',s elf.page3)
        back_btn_page3.setGeometry(QRect(0, 0, 150, 100))  # 左上角返回按鈕
        back_btn_page3.setStyleSheet('background-color: transparent;')  # 透明按鈕
        back_btn_page3.clicked.connect(self.goBackToSecondPage)
        # Fourth page
        self.page4 = QLabel(self)
        pixmap4 = QPixmap('3.jpg')  # 替換為你的第四張圖片
        self.page4.setPixmap(pixmap4)
        self.page4.setScaledContents(True)
        self.stacked_widget.addWidget(self.page4)

        back_btn_page4 = QPushButton('', self.page4)
        back_btn_page4.setGeometry(QRect(0, 0, 150, 100))  # 左上角返回按鈕
        back_btn_page4.setStyleSheet('background-color: transparent;')  # 透明按鈕
        back_btn_page4.clicked.connect(self.goBackToSecondPage)
        # Fifth page
        self.page5 = QLabel(self)
        pixmap5 = QPixmap('3.jpg')  # 替換為你的第五張圖片
        self.page5.setPixmap(pixmap5)
        self.page5.setScaledContents(True)
        self.stacked_widget.addWidget(self.page5)

        back_btn_page5 = QPushButton('', self.page5)
        back_btn_page5.setGeometry(QRect(0, 0, 150, 100))  # 左上角返回按鈕
        back_btn_page5.setStyleSheet('background-color: transparent;')  # 透明按鈕
        back_btn_page5.clicked.connect(self.goBackToSecondPage)
        # Sixth page
        self.page6 = QLabel(self)
        pixmap6 = QPixmap('3.jpg')  # 替換為你的第六張圖片
        self.page6.setPixmap(pixmap6)
        self.page6.setScaledContents(True)
        self.stacked_widget.addWidget(self.page6)

        back_btn_page6 = QPushButton('', self.page6)
        back_btn_page6.setGeometry(QRect(0, 0, 150, 100))  # 左上角返回按鈕
        back_btn_page6.setStyleSheet('background-color: transparent;')  # 透明按鈕
        back_btn_page6.clicked.connect(self.goBackToSecondPage)
        # Seventh page
        self.page7 = QLabel(self)
        pixmap7 = QPixmap('3.jpg')  # 替換為你的第七張圖片
        self.page7.setPixmap(pixmap7)
        self.page7.setScaledContents(True)
        self.stacked_widget.addWidget(self.page7)

        back_btn_page7 = QPushButton('', self.page7)
        back_btn_page7.setGeometry(QRect(0, 0, 150, 100))  # 左上角返回按鈕
        back_btn_page7.setStyleSheet('background-color: transparent;')  # 透明按鈕
        back_btn_page7.clicked.connect(self.goBackToSecondPage)
        # Connect the click event to change pages (from page1 to page2)
        self.page1.mousePressEvent = self.changePage

    def changePage(self, event):
        # Change to the second page
        self.stacked_widget.setCurrentIndex(1)

    def showPage(self, button_id):
        # 根據按鈕ID跳轉到對應的頁面
        if button_id == 1:
            self.stacked_widget.setCurrentIndex(2)  # 第三頁
        elif button_id == 2:
            self.stacked_widget.setCurrentIndex(3)  # 第四頁
        elif button_id == 3:
            self.stacked_widget.setCurrentIndex(4)  # 第五頁
        elif button_id == 4:
            self.stacked_widget.setCurrentIndex(5)  # 第六頁
        elif button_id == 5:
            self.stacked_widget.setCurrentIndex(6)  # 第七頁

    def goBackToFirstPage(self):
        # Go back to the first page when the top left button is clicked
        self.stacked_widget.setCurrentIndex(0)
    def goBackToSecondPage(self):
        # Go back to the second page when the top left button on the third page is clicked
        self.stacked_widget.setCurrentIndex(1)
    def goBackToThirdPage(self):
        # Go back to the second page when the top left button on the third page is clicked
        self.stacked_widget.setCurrentIndex(2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.showMaximized()  # 窗口最大化顯示
    sys.exit(app.exec_())
