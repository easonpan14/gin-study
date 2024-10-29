from PyQt5.QtWidgets import QWidget,QLabel,QPushButton,QVBoxLayout
from PyQt5.QtGui import QPixmap
# 分析葉面


class AnalysisPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent  # 保存父窗口的引用
        self.setWindowTitle('Analysis Page')
        self.setGeometry(100, 100, 1024, 768)
        width = self.width()
        height = self.height()

        # 創建背景標籤
        self.background_label = QLabel(self)
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.set_background_image('Window/image/8.png')

        # 設置佈局來防止其他部件影響背景
        self.setLayout(QVBoxLayout())

        # 創建返回按鈕
        self.back_button = QPushButton('', self)
        self.back_button.setGeometry(
            0, 0, int(width * 0.0625), int(height * 0.0807265))



        # 分析國文
        self.chinese_button = QPushButton('國文', self)
        self.chinese_button.setGeometry(500, 600, 120, 60)  # 設定按鈕的位置和大小
        self.chinese_button.clicked.connect(
            lambda: self.show_analysis_page("國文分析"))  # 設定點擊事件

        # 分析英文
        self.english_button = QPushButton('英文', self)
        self.english_button.setGeometry(700, 600, 120, 60)  # 設定按鈕的位置和大小
        self.english_button.clicked.connect(
            lambda: self.show_analysis_page(("英文分析"))  # 設定點擊事件
        )
        # 分析數學
        self.math_button = QPushButton('數學', self)
        self.math_button.setGeometry(900, 600, 120, 60)  # 設定按鈕的位置和大小
        self.math_button.clicked.connect(
            lambda: self.show_analysis_page("數學分析"))  # 設定點擊事件

        # 分析自然
        self.science_button = QPushButton('自然', self)
        self.science_button.setGeometry(1100, 600, 120, 60)  # 設定按鈕的位置和大小
        self.science_button.clicked.connect(
            lambda: self.show_analysis_page("自然分析"))  # 設定點擊事件

        # 分析社會
        self.social_button = QPushButton('社會', self)
        self.social_button.setGeometry(1300, 600, 120, 60)  # 設定按鈕的位置和大小
        self.social_button.clicked.connect(
            lambda: self.show_analysis_page("社會分析"))  # 設定點擊事件
        

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

    def show_analysis_page(self, page):
        # 切換到指定的分析頁面
        if self.main_window:
            self.main_window.show_analysis_page(page)
        else:
            print("主視窗未正確設置")