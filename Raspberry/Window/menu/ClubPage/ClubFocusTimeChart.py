import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTableWidget, QTableWidgetItem
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import timedelta
import matplotlib.pyplot as plt

# 設置 Matplotlib 字體為支持中文的字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 微軟正黑體
plt.rcParams['axes.unicode_minus'] = False  # 使負號顯示正常

# 自訂
from database.DateBase import find_focus_time, get_name_by_uid, get_members_by_group_id  # 假設這些函數已經正確實現

class ClubChartPage(QWidget):
    def __init__(self, group_id, parent=None, backFunction=None):
        super().__init__(parent)
        self.backFunction = backFunction
        self.group_id = group_id  # 這裡可以傳入群組ID來獲取對應數據
        self.data = {}
        self.initUI()

    def initUI(self):
        # 設置主佈局
        layout = QVBoxLayout()

        # 添加返回按鈕
        self.back_button = QPushButton("返回")
        self.back_button.clicked.connect(self.backFunction)
        layout.addWidget(self.back_button)

        # 初始化Matplotlib Figure並嵌入到PyQt
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

        # 繪製初始圖表
        self.update_data()

    def plot_data(self):
        ax = self.figure.add_subplot(111)
        ax.clear()

        



        # 繪製折線圖
        for user, times in self.data.items():
            time_in_seconds = []
            dates = []
            for day, time in times:
                if isinstance(time, str):  # 如果是字符串格式，例如 'HH:MM:SS'
                    h, m, s = map(int, time.split(':'))
                    total_seconds = h * 3600 + m * 60 + s
                elif isinstance(time, timedelta):  # 如果是 timedelta 格式
                    total_seconds = int(time.total_seconds())
                else:
                    total_seconds = 0
            
                time_in_seconds.append(total_seconds)
                dates.append(day)

            ax.plot(dates, time_in_seconds, marker='o', label=user)

        ax.set_title("用戶專注時間圖表")
        ax.set_xlabel("日期")
        ax.set_ylabel("時間 (HH:MM:SS)")

        def format_seconds(x, _):
            hours = int(x // 3600)
            minutes = int((x % 3600) // 60)
            seconds = int(x % 60)
            return f"{hours:02}:{minutes:02}:{seconds:02}"

        ax.yaxis.set_major_formatter(plt.FuncFormatter(format_seconds))
        ax.legend()
        ax.grid()

        self.canvas.draw()

    def update_data(self):
        # 根據群組ID獲取用戶的專注時間數據
        user_ids = get_members_by_group_id(self.group_id)  # 獲取群組中的所有用戶ID
        print(user_ids)
        self.get_Data(user_ids)

    def get_Data(self, uID: list[int]):
        self.data = {}

        # 初始化所有用戶的時間數據
        all_focus_times = {}

        # 收集所有用戶的專注時間數據
        for ID in uID:
            focus_times = find_focus_time(ID)
            focus_times = sorted(focus_times, key=lambda x: x.day)  # 根據日期排序
            all_focus_times[ID] = focus_times

        # 找出所有數據中的最小和最大日期
        all_dates = [ft.day for times in all_focus_times.values() for ft in times]
        min_date, max_date = min(all_dates), max(all_dates)

        # 生成包含所有日期的範圍
        full_date_range = [(min_date + timedelta(days=i)) for i in range((max_date - min_date).days + 1)]

        # 填充每個用戶的專注時間數據，缺失的日期設為 0
        for ID, focus_times in all_focus_times.items():
            time_dict = {ft.day: ft.time for ft in focus_times}  # 用字典來快速查找日期對應的時間
            filled_times = []

            for date in full_date_range:
                time = time_dict.get(date, "00:00:00")  # 若缺失則填充 '00:00:00'
                filled_times.append((date, time))

            name = get_name_by_uid(ID)
            self.data[name] = filled_times

        self.plot_data()
