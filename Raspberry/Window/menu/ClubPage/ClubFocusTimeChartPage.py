import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime, timedelta
import matplotlib.pyplot as plt  
# 設置 Matplotlib 字體為支持中文的字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 微軟正黑體
plt.rcParams['axes.unicode_minus'] = False  # 使負號顯示正常

# 自訂
from database.DateBase import find_focus_time, get_name_by_uid

class ClubChartPage(QWidget):
    def __init__(self, parent=None, backFunction=None):
        super().__init__(parent)
        self.backFunction = backFunction
        self.data = {}  # 初始化數據
        self.initUI()

    def initUI(self):
        # 設置主佈局
        layout = QVBoxLayout()

        # 添加返回按鈕
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.backFunction)
        layout.addWidget(self.back_button)

        # 初始化Matplotlib Figure並嵌入到PyQt
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # 添加更新按鈕
        self.update_button = QPushButton("抓取資料")
        self.update_button.clicked.connect(self.update_data)
        layout.addWidget(self.update_button)

        self.setLayout(layout)

        # 繪製初始圖表
        self.update_data()

    def plot_data(self):
        # 獲取Figure的繪圖區域
        ax = self.figure.add_subplot(111)

        # 清除之前的數據（如果有）
        ax.clear()

        # 繪製折線圖
        for user, times in self.data.items():
            time_in_seconds = []
            dates = []  # 儲存日期的列表
            for day, time in times:
                if isinstance(time, str):  # 如果是字符串格式，例如 'HH:MM:SS'
                    h, m, s = map(int, time.split(':'))
                    total_seconds = h * 3600 + m * 60 + s
                elif isinstance(time, timedelta):  # 如果是 timedelta 格式
                    total_seconds = int(time.total_seconds())
                else:
                    # 處理未知類型的情況
                    total_seconds = 0
            
                time_in_seconds.append(total_seconds)
                dates.append(day)

            # 繪製圖表，X 軸為日期
            ax.plot(dates, time_in_seconds, marker='o', label=user)  # 繪製每個使用者的數據

        # 設置標題和標籤
        ax.set_title("User Focus Time Chart")
        ax.set_xlabel("Date")
        ax.set_ylabel("Time (HH:MM:SS)")

        # 格式化Y軸顯示為HH:MM:SS
        def format_seconds(x, _):
            hours = int(x // 3600)
            minutes = int((x % 3600) // 60)
            seconds = int(x % 60)
            return f"{hours:02}:{minutes:02}:{seconds:02}"

        ax.yaxis.set_major_formatter(plt.FuncFormatter(format_seconds))
        ax.legend()
        ax.grid()

        # 刷新畫布
        self.canvas.draw()

    def update_data(self):
        # 假設這裡是從數據庫中抓取的數據
        user_ids = [1, 2, 3]  # 假設有三個用戶的ID
        self.get_Data(user_ids)

    def get_Data(self, uID: list[int]):
        self.data = {}  # 清空數據
        for ID in uID:
            focus_times = find_focus_time(ID)
            # 不再需要轉換為字符串，因為 x.day 已經是日期對象
            focus_times = sorted(focus_times, key=lambda x: x.day)

            time_list = []
            for ft in focus_times:
                time_list.append((ft.day, ft.time))  # 假設 time 是 'HH:MM:SS' 格式的字符串

            name = get_name_by_uid(ID)
            self.data[name] = time_list

        # 繪製更新後的圖表
        self.plot_data()