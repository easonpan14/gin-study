
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import timedelta,datetime
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
        self.date_range = 7  # 默認日期範圍為7天
        self.display_mode="daily"
        self.initUI()

    def initUI(self):
        # 設置主佈局
        layout = QVBoxLayout()

        # 添加返回按鈕
        self.back_button = QPushButton("返回")
        self.back_button.clicked.connect(self.backFunction)
        layout.addWidget(self.back_button)

        # 添加時間範圍和顯示模式的按鈕
        self.add_buttons(layout)

        # 初始化Matplotlib Figure並嵌入到PyQt
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

        # 繪製初始圖表
        self.update_data()

    def add_buttons(self, layout):
        # 添加日期範圍按鈕
        range_buttons = {
            "最近7天": 7,
            "最近14天": 14,
            "最近30天": 30
        }

        for text, days in range_buttons.items():
            button = QPushButton(text)
            button.clicked.connect(lambda _, d=days: self.set_date_range(d))
            layout.addWidget(button)

        # 添加顯示模式按鈕
        self.mode_button_daily = QPushButton("每日數據")
        self.mode_button_daily.clicked.connect(lambda: self.set_display_mode('daily'))
        layout.addWidget(self.mode_button_daily)

        self.mode_button_cumulative = QPushButton("累積數據")
        self.mode_button_cumulative.clicked.connect(lambda: self.set_display_mode('cumulative'))
        layout.addWidget(self.mode_button_cumulative)

    def set_date_range(self, days):
        self.date_range = days
        self.plot_data()

    def set_display_mode(self, mode):
        self.display_mode = mode
        self.plot_data()

    def plot_data(self):
        self.get_Data_In_Range()

        # 清除所有內容，包括子圖和刻度
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # 繪製折線圖
        for user, times in self.data.items():
            time_in_seconds = []
            dates = []
            total_seconds = 0

            for day, time in times:
                today = datetime.today().date()

                if self.display_mode == "daily":
                    total_seconds = 0

                # 判斷日期範圍
                if day < today - timedelta(days=self.date_range) or day > today:
                    continue

                # 轉換時間格式
                if isinstance(time, str):  # 'HH:MM:SS' 格式
                    h, m, s = map(int, time.split(':'))
                    total_seconds += h * 3600 + m * 60 + s
                elif isinstance(time, timedelta):
                    total_seconds += int(time.total_seconds())
                else:
                    total_seconds += 0

                time_in_seconds.append(total_seconds)
                dates.append(day)

            ax.plot(dates, time_in_seconds, marker='o', label=user)

        # 設置標題與標籤
        ax.set_title("用戶專注時間圖表")
        ax.set_xlabel("日期")
        ax.set_ylabel("時間 (HH:MM:SS)")

        # 格式化 Y 軸時間
        def format_seconds(x, _):
            hours = int(x // 3600)
            minutes = int((x % 3600) // 60)
            seconds = int(x % 60)
            return f"{hours:02}:{minutes:02}:{seconds:02}"

        ax.yaxis.set_major_formatter(plt.FuncFormatter(format_seconds))

        # 調整 X 軸和 Y 軸刻度數量
        ax.xaxis.set_major_locator(plt.MaxNLocator(6))  # X 軸最多 6 個主要刻度
        ax.xaxis.set_minor_locator(plt.MaxNLocator(12))  # X 軸次要刻度

        ax.yaxis.set_major_locator(plt.MaxNLocator(5))  # Y 軸最多 5 個主要刻度

        # 添加圖例和網格
        ax.legend()
        ax.grid()

        # 刷新畫布
        self.canvas.draw()




    def update_data(self):
        # 根據群組ID獲取用戶的專注時間數據
        user_ids = get_members_by_group_id(self.group_id)  # 獲取群組中的所有用戶ID
        print(user_ids)
        self.get_Data(user_ids)

    def get_Data_In_Range(self):
        self.data = {}
        today = datetime.today().date()
            


        # 設定最小和最大日期
        min_date = today - timedelta(days=30)
        max_date =  today
        # 生成包含所有日期的範圍
        full_date_range = [(min_date + timedelta(days=i)) for i in range((max_date - min_date).days + 1)]

        # 填充每個用戶的專注時間數據，缺失的日期設為 0
        for ID, focus_times in self.all_focus_times.items():
            time_dict = {ft.day: ft.time for ft in focus_times}  # 用字典來快速查找日期對應的時間
            filled_times = []

            for date in full_date_range:
                time = time_dict.get(date, "00:00:00")  # 若缺失則填充 '00:00:00'
                filled_times.append((date, time))

            name = get_name_by_uid(ID)
            self.data[name] = filled_times


    def get_Data(self, uID: list[int]):
        

        # 初始化所有用戶的時間數據
        self.all_focus_times = {}

        # 收集所有用戶的專注時間數據
        for ID in uID:
            focus_times = find_focus_time(ID)
            focus_times = sorted(focus_times, key=lambda x: x.day)  # 根據日期排序
            self.all_focus_times[ID] = focus_times


        

        self.plot_data()

