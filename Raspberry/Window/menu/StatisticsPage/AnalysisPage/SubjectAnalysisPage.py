from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem,QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QHeaderView
from datetime import  date

#自有
from database.DateBase import find_gpt_message
from GlobalVar import GlobalVar

class SubjectAnalysisPage(QWidget):
    def __init__(self, subject, parent=None):
        super().__init__(parent)
        self.subject = subject
        self.setWindowTitle(f'{subject} 分析')
        self.setGeometry(100, 100, 1024, 768)

        # 設定背景圖片路徑
        background_image_path = f'Window/image/{subject}.jpg'

        # 創建背景標籤
        self.background_label = QLabel(self)
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.set_background_image(background_image_path)

        # 設置主佈局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

        # 創建表格
        self.table_widget = QTableWidget(self)
        self.table_widget.setRowCount(5)  # 設置行數
        self.table_widget.setColumnCount(3)  # 設置列數
        self.table_widget.setHorizontalHeaderLabels(['編號', '提問', '日期'])  # 設置標題
        # 填充範例數據
        for row in range(5):
            for col in range(3):
                item = QTableWidgetItem(f'內容 {row+1}-{col+1}')
                item.setFont(QFont("Arial", 14))  # 設置字體大小
                item.setTextAlignment(Qt.AlignCenter)  # 置中對齊
                self.table_widget.setItem(row, col, item)

        # 自動調整列寬和行高，使其填滿表格
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 設置表格樣式
        self.table_widget.setStyleSheet("""
            QTableWidget {
                background-color: #f0f4f8;
                border-radius: 10px;
                padding: 0px;
            }
            QTableWidget::item {
                border-bottom: 1px solid #d0d7de;
                padding: 10px;
            }
            QHeaderView::section {
                background-color: #e9eff5;
                padding: 5px;
                border: none;
                border-bottom: 2px solid #d0d7de;
            }
        """)

        # 創建一個垂直和水平佈局來讓表格居中
        v_layout = QVBoxLayout()
        v_layout.addStretch()  # 添加彈性空間使表格垂直居中
        v_layout.addWidget(self.table_widget)
        v_layout.addStretch()  # 添加彈性空間使表格垂直居中

        h_layout = QHBoxLayout()
        h_layout.addStretch()  # 添加彈性空間使表格水平居中
        h_layout.addLayout(v_layout)
        h_layout.addStretch()  # 添加彈性空間使表格水平居中

        # 把佈局添加到主佈局中
        main_layout.addLayout(h_layout)

        # 根據窗口大小自動調整表格尺寸
        self.adjust_table_size()

    def set_background_image(self, image_path):
        # 加載背景圖片
        background_image = QPixmap(image_path)
        if background_image.isNull():
            print(f"圖片加載失敗：{image_path}")
        else:
            # 設置圖片到 QLabel 並拉伸以適應窗口大小
            self.background_label.setPixmap(background_image)
            self.background_label.setScaledContents(True)

    def resizeEvent(self, event):
        # 調整背景大小以適應窗口調整
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.adjust_table_size()

    def adjust_table_size(self):
        # 根據窗口大小自動調整表格的大小
        width = self.width() * 0.8  # 設置表格寬度為視窗的80%
        height = self.height() * 0.6  # 設置表格高度為視窗的60%
        self.table_widget.setFixedSize(QSize(int(width), int(height)))
    def update_table(self):
        GlobalVar.gpt_data
        filtered_data = [item for item in GlobalVar.gpt_data if item.subject == self.subject]
        self.table_widget.setRowCount(len(filtered_data))  # 根據篩選後的資料設置行數

            # 將篩選後的內容填充到表格中
        for row, gpt_item in enumerate(filtered_data):
                # 查詢 gpt_id 的訊息內容
            messages = find_gpt_message(gpt_item.Gpt_ID)
            
                # 初始化 sender 0 和 sender 1 的訊息
            sender0_message = "無訊息"
            sender1_message = "無訊息"

                # 分類 sender 0 和 sender 1 的訊息
            for msg in messages:
                if msg.sender == 0:
                    sender0_message = msg.message
                elif msg.sender == 1:
                    sender1_message = msg.message

                # 設定表格顯示
            self.table_widget.setItem(row, 0, QTableWidgetItem(sender0_message))  # 第一列顯示 sender 0 的訊息
            self.table_widget.setItem(row, 1, QTableWidgetItem(sender1_message))  # 第二列顯示 sender 1 的訊息

                # 將日期轉換為字串格式
            if isinstance(gpt_item.day, date):
                GlobalVar.date_str = gpt_item.day.strftime("%Y-%m-%d")
            else:
                GlobalVar.date_str = str(gpt_item.day)

            self.table_widget.setItem(row, 2, QTableWidgetItem(GlobalVar.date_str))  # 第三列顯示日期
