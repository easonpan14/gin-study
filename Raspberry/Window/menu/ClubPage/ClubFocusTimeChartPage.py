import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class ClubChartPage(QWidget):
    def __init__(self, parent=None,backFunction=None):
        super().__init__(parent)
        # 初始測試數據
        self.data = {
            "user1": [4, 8, 2, 4, 8, 5, 4],
            "user2": [4, 8, 6, 2, 5, 5, 7],
            "user3": [5, 5, 5, 5, 7, 2, 4]
        }
        self.backFunvtion=backFunction
        self.initUI()

    def initUI(self):
        # 設置主佈局
        layout = QVBoxLayout()

        # 添加返回按鈕
        self.update_button = QPushButton("Back")
        self.update_button.clicked.connect(self.backFunvtion)
        layout.addWidget(self.update_button)

        # 初始化Matplotlib Figure並嵌入到PyQt
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        # 添加更新按鈕
        self.update_button = QPushButton("Update Data")
        self.update_button.clicked.connect(self.update_data)
        layout.addWidget(self.update_button)

        
        
        self.setLayout(layout)
        self.plot_data()

    def plot_data(self):
        # 獲取Figure的繪圖區域
        ax = self.figure.add_subplot(111)
        
        # 清除之前的數據（如果有）
        ax.clear()
        
        # 畫折線圖
        for user, values in self.data.items():
            ax.plot(values, label=user)  # 繪製每個使用者的數據
            
        # 加入圖例和標題
        ax.legend()
        ax.set_title("User Line Chart")
        ax.set_xlabel("Index")
        ax.set_ylabel("Value")
        
        # 刷新畫布
        self.canvas.draw()

    def update_data(self):
        # 隨機更新數據
        for user in self.data:
            self.data[user] = [random.randint(1, 10) for _ in range(7)]
        
        # 重新繪製圖表
        self.plot_data()





