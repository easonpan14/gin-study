from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCalendarWidget, QLabel
from PyQt5.QtGui import QTextCharFormat, QColor, QPixmap
from PyQt5.QtCore import Qt
from database.DateBase import find_focus_time, login_check
from GlobalVar import GlobalVar

class FocusAnalysisPage(QWidget):
    def __init__(self, uID, parent=None):
        super().__init__(parent)
        self.uID = uID
        self.initUI()

    def initUI(self):
        # 設置背景圖
        self.background_label = QLabel(self)
        self.set_background_image("Window/image/幹你媽.jpg")

        # 主佈局設置
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)  # 設置佈局居中
        main_layout.setContentsMargins(0, 0, 0, 0)  # 移除內邊距

        # 日曆部件
        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        self.calendar.setFixedSize(1300, 700)  # 調整日曆尺寸
        self.calendar.clicked.connect(self.display_focus_info)  # 點擊事件
        main_layout.addWidget(self.calendar, alignment=Qt.AlignCenter)

        # 顯示日期專注信息的標籤
        self.info_label = QLabel("請點擊日期以查看專注時間", self)
        self.info_label.setAlignment(Qt.AlignCenter)  # 文字居中對齊
        self.info_label.setStyleSheet("margin: 0px; padding: 0px;")  # 移除邊距和填充
        main_layout.addWidget(self.info_label, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)
        self.update_focus_data()  # 初始化時更新數據

    def set_background_image(self, image_path):
        # 加載背景圖片
        background_image = QPixmap(image_path)
        if background_image.isNull():
            print(f"圖片加載失敗：{image_path}")
        else:
            # 設置圖片到 QLabel 並拉伸以適應窗口大小
            self.background_label.setPixmap(background_image)
            self.background_label.setScaledContents(True)
            self.background_label.lower()  # 將背景圖層設置在底層

    def resizeEvent(self, event):
        # 調整背景大小以適應窗口調整
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)

    def update_focus_data(self):
        if  GlobalVar.uID > 0:
            focus_times = find_focus_time(GlobalVar.uID)
            self.focus_data = {}
            for focus in focus_times:
                date = focus.day
                time_delta = focus.time
                hours = time_delta.total_seconds() / 3600
                self.focus_data[date] = time_delta
            self.apply_calendar_colors()

    def apply_calendar_colors(self):
        """根據 focus_data 字典中的專注時長設置日曆的顏色，從透明到深藍色漸變"""
        for date, time_delta in self.focus_data.items():
            hours = time_delta.total_seconds() / 3600
            format = QTextCharFormat()
            if hours <= 0:
                alpha = 0  # 完全透明
            elif hours >= 12:
                alpha = 255  # 不透明的深藍色
            else:
                # 根據專注時長（0-12小時）計算透明度，25 檔位
                alpha = int((hours / 12) * 255)

            # 設定深藍色（#003366）並應用透明度
            color = QColor(0, 51, 102, alpha)
            format.setBackground(color)

            # 將顏色應用到特定日期
            self.calendar.setDateTextFormat(date, format)

    def display_focus_info(self, date):
        """顯示選中的日期的專注時間"""
        selected_date = date.toPyDate()  # QDate 轉換為 Python 的 date 格式
        time_delta = self.focus_data.get(selected_date)

        if time_delta:
            hours, remainder = divmod(time_delta.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            self.info_label.setText(
                f"{selected_date}: 專注時間 {int(hours)} 小時 {int(minutes)} 分鐘 {int(seconds)} 秒"
            )
        else:
            self.info_label.setText(f"{selected_date}: 沒有專注數據")
