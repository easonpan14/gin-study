#索引值0:封面 1主畫面 2解題 3讀書會 4英文
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QStackedWidget, QWidget,QLineEdit,QVBoxLayout,QHBoxLayout
from PyQt5.QtGui import QPixmap,QPalette, QColor
from PyQt5.QtCore import Qt, QRect
from openai import OpenAI

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="sk-uJ3B62eXV4XouZSH7htWKYzf5QFj1W0WQd4AAn072WQPzptn",
    base_url="https://api.chatanywhere.tech/v1"
)

class ProblemSolvingPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('國文解題')

        # 設定佈局
        layout = QVBoxLayout()

        # 創建顯示解答區域
        self.answer_label = QLabel("解答會顯示在這裡", self)
        self.answer_label.setStyleSheet('font-size: 18px; color: black;')
        layout.addWidget(self.answer_label)

        # 創建輸入框
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("請輸入國文問題")
        self.input_field.setStyleSheet('font-size: 18px; padding: 10px;')
        layout.addWidget(self.input_field)
        
        # 創建模擬 GPT 回答的按鈕
        self.solve_button = QPushButton('解題', self)
        self.solve_button.setStyleSheet('font-size: 18px; padding: 10px;')
        self.solve_button.clicked.connect(self.solve_problem)
        layout.addWidget(self.solve_button)

        self.setLayout(layout)

    def gpt_35_api_stream(self, messages: list):
        try:
            stream = client.chat.completions.create(
                model='gpt-3.5-turbo',
                messages=messages,
                stream=True,
            )
            
            full_response = ""
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_response  += chunk.choices[0].delta.content

            self.answer_label.setText(full_response )

        except Exception as e:
            self.answer_label.setText(f"發生錯誤: {e}")

    def solve_problem(self):
        # 取得輸入的問題
        question = self.input_field.text()

        if question:
            # 清空標籤並顯示等待訊息
            self.answer_label.setText(f"正在為「{question}」生成解答...")
            
            # 構造發送給 GPT 的訊息
            messages = [{'role': 'user', 'content': f'你是個國文老師，麻煩用繁體中文幫她解決問題，問題是「{question}」'}]
            
            # 調用 GPT API 生成解答
            self.gpt_35_api_stream(messages)

        else:
            self.answer_label.setText("請輸入一個問題。")

    

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
        self.back_button.setGeometry(0, 0, 120, 80)
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


class EnglishPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 設定佈局
        self.setWindowTitle('English Practice')
        self.setGeometry(100, 100, 1024, 768)

         # 加載背景圖片
        self.background_label = QLabel(self)
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.set_background_image('image/5.jpg')  # Adjust the path based on where the file is saved
        #創建輸入框
        self.input_field = QLineEdit(self)
        self.input_field.setGeometry( 200,500 , 100, 200)
        self.input_field.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0);  /* 設置完全透明 */
            border: none;  /* 移除邊框 */
            color: black;  /* 設置文字顏色 */
            font-size: 24px;
            padding: 10px;
        """)
        # 創建透明撥放按鈕
        self.play_button = QPushButton('', self)
        self.input_field.setPlaceholderText("輸入英文")
        self.play_button.setGeometry(400,400, 80, 80)  # Adjust the size and position
        self.play_button.setStyleSheet('background-color: transparent; border: none;')
        self.play_button.clicked.connect(self.play_audio)

    def set_background_image(self, image_path):
        # 加載圖片並設置為背景
        background_image = QPixmap(image_path)
        if background_image.isNull():
            print(f"圖片加載失敗：{image_path}")
        else:
            self.background_label.setPixmap(background_image)
            self.background_label.setScaledContents(True)

    def resizeEvent(self, event):
         # 在窗口調整大小時，重新調整背景圖片大小
        width = self.width()
        height = self.height()
        print(width,height)
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.input_field.setGeometry(150,280 , 100, 200)
        self.play_button.setGeometry(810,670, 80, 80)
        self.play_button.setStyleSheet('background-color: transparent; border: none;')
        self.input_field.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0);  /* 設置完全透明 */
            border: none;  /* 移除邊框 */
            color: black;  /* 設置文字顏色 */
            font-size: 24px;
            padding: 10px;
        """)

    def play_audio(self):
         # 撥放音頻的功能（目前是占位符）
        print(f"Playing audio for text: {self.input_field.text()}")

 
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

        # 第四頁（讀書會與聊聊）
        self.page4 = QLabel(self)
        pixmap4 = QPixmap('image/7.jpg')  #
        self.page4.setPixmap(pixmap4)
        self.page4.setScaledContents(True)
        self.stacked_widget.addWidget(self.page4)

        # 添加第四頁的按鈕
        self.add_buttons_to_page4()

        #第五頁 (英文練習頁面)
        self.page5 = EnglishPage(self)  # 使用新建的 EnglishPage 類別
        self.stacked_widget.addWidget(self.page5)

        self.problem_solving_page = ProblemSolvingPage(self)
        self.stacked_widget.addWidget(self.problem_solving_page)
        self.page3.button1.clicked.connect(self.showProblemSolvingPage)
        # 頁面間的切換
        self.page1.mousePressEvent = self.changePage

    def showProblemSolvingPage(self):
        self.stacked_widget.setCurrentWidget(self.problem_solving_page)

    def add_buttons_to_page4(self):
        # 第四頁的按鈕
        width = 1920
        height = 1080
        button_width = width*0.234
        button_height = height*0.231

        self.button_chat = QPushButton('', self.page4)
        self.button_chat.setGeometry(int(width*0.6), int(height*0.509), int(button_width), int(button_height))  # 讀書會按鈕右側
        self.button_chat.setStyleSheet('background-color: transparent;')

        self.button_study_club = QPushButton('', self.page4)
        self.button_study_club.setGeometry(int(width*0.156), int(height*0.509), int(button_width), int(button_height))  # 左側按鈕
        self.button_study_club.setStyleSheet('background-color: transparent;')

        # 第四頁的返回按鈕
        self.page4_back_btn = QPushButton('', self.page4)
        self.page4_back_btn.setGeometry(0, 0, int(width*0.06), int(height*0.074))
        self.page4_back_btn.setStyleSheet('background-color: transparent;')
        self.page4_back_btn.clicked.connect(self.goBackToSecondPage)

    def changePage(self, event):
        self.stacked_widget.setCurrentIndex(1)

    def showPage(self, button_id):
        if button_id == 1:
            self.stacked_widget.setCurrentIndex(2)
        elif button_id == 5:
            self.stacked_widget.setCurrentIndex(3)
        elif button_id == 3:
            self.stacked_widget.setCurrentIndex(4)   # 自訂頁面
            
    def goBackToFirstPage(self):
        self.stacked_widget.setCurrentIndex(0)

    def goBackToSecondPage(self):
        self.stacked_widget.setCurrentIndex(1)  # 返回第二頁


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.showMaximized()  # 最大化顯示
    sys.exit(app.exec_())
