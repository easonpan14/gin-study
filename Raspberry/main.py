#索引值0:封面 1主畫面 2解題 3讀書會 4英文
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHeaderView
from datetime import datetime

# To 金毛
# 解題的部分在「TemsolveMainWindow」這個class，我們把使用者輸入給到「solve_problem」裡面，
# 然後會傳給「gpt_35」，再來會有字串（full_response）把gpt的回覆儲存好 ,
# 然後就把full_response輸出
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QPushButton,
    QStackedWidget,
    QWidget,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
    QSpacerItem,
    QSizePolicy,
    QTextEdit
)
from PyQt5.QtGui import QPixmap,QPalette,  QPainter, QIcon
from PyQt5.QtCore import Qt, QTimer, QRect, QSize
from openai import OpenAI
from gtts import gTTS
import os
import playsound
import pygame
import io
import pymysql
msg=""
pwd=""
gpt_id=0
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="sk-uJ3B62eXV4XouZSH7htWKYzf5QFj1W0WQd4AAn072WQPzptn",
    base_url="https://api.chatanywhere.tech/v1"
)
# 資料庫連接配置(以下都是資料庫跟)
DB_CONFIG = {
    'host': '18.180.122.148',
    'user': 'admin',
    'password': 'LCivpNcrALc6YDK',
    'database': 'my_database',
    'charset': 'utf8mb4',
}
class User:
    def __init__(self, uID:int, name:str):
        self.uID = uID
        self.name = name

# 群組消息類    消息越晚,group_message_ID越大   uID為發送者 gID為群組
class GroupMessage:
    def __init__(self, group_message_ID:int, message:str,Group_ID:int, uID:int):
        self.gmID = group_message_ID                
        self.message = message
        self.Group_ID=Group_ID
        self.uID = uID

class Gpt:
    def __init__(self, Gpt_ID:int, subject:str,day:str, uID:int):
        self.Gpt_ID = Gpt_ID                
        self.subject = subject
        self.day=day
        self.uID = uID

class GptMessage:
    def __init__(self, group_message_ID:int, GPT_ID:int,message:str, sender:bool):
        self.gmID = group_message_ID 
        self.GPT_ID=GPT_ID               
        self.message = message
        self.sender=sender
        
##資料庫資料以上

# 資料庫連接函數
def connect_db():
    try:
        connection = pymysql.connect(**DB_CONFIG)
        return connection
    except pymysql.MySQLError as e:
        print(f"資料庫連接失敗: {e}")
        return None
#將gpt資料插入資料庫
def insert_gpt(subject:str, day:str, uID:int)->int:
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO GPT (subject, day, uID) VALUES (%s, %s, %s)"
            cursor.execute(sql, (subject, day, uID))
            connection.commit()
            print("插入成功")
            return  cursor.lastrowid
    except Exception as e:
        print(f"插入失敗: {e}")
        connection.rollback()
        return -1
    finally:
        connection.close()
def insert_gpt_message(gpt_id:int, message:str, sender:bool):
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO GPT_MESSAGE (GPT_ID, message, sender) 
                VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (gpt_id, message, sender))
            connection.commit()
            print("消息插入成功")
    except Exception as e:
        print(f"插入失败: {e}")
        connection.rollback()
    finally:
        connection.close()

# 用戶註冊函數
def register_and_login(name: str, account: str, password: str) -> bool:
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            # 檢查賬號是否已存在
            sql = 'SELECT uID FROM User WHERE account = %s'
            cursor.execute(sql, (account,))
            result = cursor.fetchone()
            if result:
                print("註冊失敗，帳號已存在。")
                return False

            # 插入新用戶數據
            sql = "INSERT INTO User (name, account, password) VALUES (%s, %s, %s)"
            cursor.execute(sql, (name, account, password))  # 直接插入明文密碼
            connection.commit()
            print("註冊成功！")
            return True
    except Exception as e:
        print(f"註冊失敗: {e}")
        connection.rollback()
        return False
    finally:
        connection.close()

# 用戶登入檢查函數
def login_check(account: str, password: str) -> User:
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT uID, name, password FROM User WHERE account = %s'
            cursor.execute(sql, (account,))
            result = cursor.fetchone()
            if result and result[2] == password:  # 比對密碼
                # 創建一個 User 對象，並返回
                return User(result[0], result[1])
            else:
                return None
    except Exception as e:
        print(f"資料庫操作失敗: {e}")
        return None
    finally:
        connection.close()
        
def get_all_gpt_ids() -> list[int]:
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            # 查詢 GPT 資料表中的所有 GPT_ID
            sql = "SELECT GPT_ID FROM GPT"
            cursor.execute(sql)
            results = cursor.fetchall()
            # 將所有 GPT_ID 存入列表
            gpt_ids = [row[0] for row in results]
            return gpt_ids
    except Exception as e:
        print(f"查詢失敗: {e}")
        return []
    finally:
        connection.close()

# 自訂第三頁的視窗
class CustomPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Solving Interface')
        self.setGeometry(100, 100, 1024, 768)

        width = self.width()
        height = self.height()
        # 創建背景標籤
        self.background_label = QLabel(self)
        self.background_label.setGeometry(0, 0, self.width(), self.height())

        # 呼叫設定背景圖片函數
        self.set_background_image('image/3.jpg')

        # 創建按鈕
        self.create_buttons()

        # 創建返回按鈕
        self.back_button = QPushButton('', self)
        self.back_button.setGeometry(0, 0,int(width*0.0625), int(height*0.0807265))
        #self.back_button.setStyleSheet('background-color: transparent; font-size: 18px;')

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

        #self.button1.setStyleSheet('background-color: transparent;')
        #self.button2.setStyleSheet('background-color: transparent;')
        #self.button3.setStyleSheet('background-color: transparent;')
        #self.button4.setStyleSheet('background-color: transparent;')
        #self.button5.setStyleSheet('background-color: transparent;')

    def create_buttons(self):
        self.button1 = QPushButton('國文', self)
        self.button2 = QPushButton('英文', self)
        self.button3 = QPushButton('數學', self)
        self.button4 = QPushButton('自然', self)
        self.button5 = QPushButton('社會', self)

class EnglishPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 設定佈局
        self.setWindowTitle('English Practice')
        self.setGeometry(100, 100, 1024, 768)
        width = self.width()
        height = self.height()
        
        # 加載背景圖片
        self.background_label = QLabel(self)
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.set_background_image('image/5.jpg')

        # 創建輸入框
        self.input_field = QLineEdit(self)
        self.input_field.setGeometry(int(width*0.078125), int(height*0.282542), int(width*0.3125), int(height*0.2018163))
        self.input_field.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0);  /* 設置完全透明 */
            border: none;  /* 移除邊框 */
            color: black;  /* 設置文字顏色 */
            font-size: 24px;
            padding: 10px;
        """)
        self.input_field.setPlaceholderText("輸入英文")

        # 創建透明播放按鈕
        self.play_button = QPushButton('', self)
        self.play_button.setGeometry(int(width*0.423), int(height*0.676084), int(width*0.041666), int(height*0.0807265))
        self.play_button.clicked.connect(self.play_audio)

        # 創建翻譯按鈕
        self.translate_button = QPushButton('翻譯成中文', self)
        self.translate_button.setGeometry(int(width*0.423), int(height*0.776084), int(width*0.1), int(height*0.05))
        self.translate_button.clicked.connect(self.translate_text)

        # 顯示翻譯結果的標籤
        self.translation_label = QLabel(self)
        self.translation_label.setGeometry(1000, int(height*0.282542), int(width*0.1), int(height*0.05))
        self.translation_label.setStyleSheet("""
            color: black;
            font-size: 24px;
        """)

        # 創建返回按鈕
        self.back_button = QPushButton('', self)
        self.back_button.setGeometry(0, 0, int(width*0.0625), int(height*0.0807265))

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
        self.background_label.setGeometry(0, 0, width, height)
        self.input_field.setGeometry(int(width*0.078125), int(height*0.282542), int(width*0.3125), int(height*0.2018163))
        self.play_button.setGeometry(int(width*0.423), int(height*0.676084), int(width*0.041666), int(height*0.0807265))
        self.translate_button.setGeometry(int(width*0.375), int(height*0.676084), 80,80)
        self.back_button.setGeometry(0, 0, int(width*0.0625), int(height*0.0807265))
        self.translation_label.setGeometry(1080, 350, int(width*0.1), int(height*0.05))
    def play_audio(self):
        # 撥放音頻的功能
        text = self.input_field.text()
        if text:
            language = 'en'
            tts = gTTS(text=text, lang=language, slow=False)
            audio_fp = io.BytesIO()
            tts.write_to_fp(audio_fp)
            audio_fp.seek(0)
            pygame.mixer.init()
            pygame.mixer.music.load(audio_fp, 'mp3')
            pygame.mixer.music.play()

            # 防止程序退出，等待播放完成
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

    def translate_text(self):
        # 翻譯功能
        text = self.input_field.text()
        if text:
            translator = Translator(from_lang="english", to_lang="chinese")
            translation = translator.translate(text)
            self.translation_label.setText(f"{translation}")
        else:
            self.translation_label.setText("請輸入英文文本")
            
#分析葉面  
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
        self.set_background_image('image/8.png')

        # 設置佈局來防止其他部件影響背景
        self.setLayout(QVBoxLayout())
        # 創建返回按鈕 這她媽沒用阿 耖你媽
        self.back_button = QPushButton('', self)
        self.back_button.setGeometry(0, 0, int(width*0.0625), int(height*0.0807265))
        #分析國文
        self.chinese_button = QPushButton('國文', self)
        self.chinese_button.setGeometry(500, 600, 120, 60)  # 設定按鈕的位置和大小
        self.chinese_button.clicked.connect(self.go_to_chinese_analysis_page)  # 設定點擊事件
        #分析英文
        self.example_button = QPushButton('英文', self)
        self.example_button.setGeometry(700, 1200, 120, 60)  # 設定按鈕的位置和大小
        #分析數學
        self.example_button = QPushButton('數學', self)
        self.example_button.setGeometry(900, 1200, 120, 60)  # 設定按鈕的位置和大小
        #分析自然
        self.example_button = QPushButton('自然', self)
        self.example_button.setGeometry(1100, 1200, 120, 60)  # 設定按鈕的位置和大小
        #分析社會
        self.example_button = QPushButton('社會', self)
        self.example_button.setGeometry(1300, 1200, 120, 60)  # 設定按鈕的位置和大小

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
    def go_to_chinese_analysis_page(self):
        # 確保父窗口存在並且有 show_chinese_analysis_page 方法
        if self.main_window and hasattr(self.main_window, 'show_chinese_analysis_page'):
            self.main_window.show_chinese_analysis_page()  # 通知主視窗進行頁面切換
        else:
            print("父窗口沒有方法 show_chinese_analysis_page")
#美編國文分析葉面啦幹您娘
class ChineseAnalysisPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('國文分析')
        self.setGeometry(100, 100, 1024, 768)

        # 創建背景標籤
        self.background_label = QLabel(self)
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.set_background_image('image/9.png')

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

class TemsolveMainWindow(QWidget):
    def __init__(self,  parent=None, objects=""):
        super().__init__(parent)
        self.parent=parent
        # 設定主視窗
        self.setWindowTitle("Chat Window Example")
        self.setAttribute(Qt.WA_TranslucentBackground, True)  # 設置整體透明
        self.showFullScreen()  # 設置為全螢幕
        
        # 設定背景圖片
        if(objects=="chinese"):
            self.background_image_path = 'image/chinese.jpg'
        elif(objects=="math"):
            self.background_image_path = 'image/math.jpg'
        elif(objects=="science"):
            self.background_image_path = 'image/science.jpg'
        elif(objects=="english"):
            self.background_image_path = 'image/english.jpg'
        else:
            self.background_image_path = 'image/social.jpg'


        # 主佈局
        main_layout = QVBoxLayout(self)
        
        # 上方返回按鈕 (透明)
        top_layout = QHBoxLayout()
        self.back_button = QPushButton("")
        self.back_button.setFixedSize(50, 50)
        self.back_button.setStyleSheet("background-color: rgba(, 0, 0, 1);")
        top_layout.addWidget(self.back_button)
        top_layout.setAlignment(Qt.AlignLeft)
        main_layout.addLayout(top_layout)
        

        # 添加獨立的滾動區域
        self.scroll_area = self.create_scroll_area()
        main_layout.addWidget(self.scroll_area)

        # 底部輸入區域
        input_layout = QHBoxLayout()
        
        # 相機按鈕 (透明)
        camera_button = QPushButton("相機")
        camera_button.setFixedSize(50, 50)
        camera_button.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        input_layout.addWidget(camera_button)

        # 輸入框 (多行輸入)
        self.input_field = QTextEdit()
        self.input_field.setFixedHeight(50)
        self.input_field.setStyleSheet("""
            border-radius: 25px;
            padding-left: 10px;
            background-color: rgba(200, 200, 200, 0.5);
        """)
        self.input_field.setPlaceholderText("Type a message...")
        self.input_field.setMaximumHeight(100)  # 設置最大高度
        self.input_field.textChanged.connect(self.adjust_input_height)  # 根據文字調整高度
        input_layout.addWidget(self.input_field)
    
        # 傳送按鈕 (透明)   
        send_button = QPushButton("傳送")
        send_button.setFixedSize(50, 50)
        send_button.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        #send_button.clicked.connect(self.add_message(objects))
        send_button.clicked.connect(lambda: self.add_message(self,objects))
        input_layout.addWidget(send_button)

        main_layout.addLayout(input_layout)

    def paintEvent(self, event):
        # 使用 QPainter 繪製背景圖片
        painter = QPainter(self)
        pixmap = QPixmap(self.background_image_path)
        painter.drawPixmap(self.rect(), pixmap)

    def create_scroll_area(self):
        # 建立滾動區域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("background-color: rgba(0, 0, 0, 0);")  # 透明背景

        # 聊天內容Widget
        self.chat_content = QWidget()
        self.chat_content.setStyleSheet("background-color: rgba(0, 0, 0, 0);")  # 透明背景
        self.chat_layout = QVBoxLayout(self.chat_content)
        self.chat_layout.setContentsMargins(10, 10, 10, 10)
        self.chat_layout.setSpacing(10)

        # 添加頂部空白區域
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.chat_layout.addItem(spacer)
        
        scroll_area.setWidget(self.chat_content)
        return scroll_area

    def adjust_input_height(self):
        # 根據輸入文字的高度動態調整輸入框的高度
        document_height = int(self.input_field.document().size().height())
        self.input_field.setFixedHeight(min(document_height + 10, 100))  # 調整最大高度到 150
            # 確保文字可以換行顯示
    def add_message(self,objects, response):
        # 取得輸入的文字並清空輸入框
        message = self.input_field.toPlainText()
        #把使用者輸入的問題傳進對話框
        
        current_date = datetime.now()
        date_str = current_date.strftime("%Y-%m-%d")
        current_user = login_check(msg, pwd)  # 假設這是你登入的地方
        global gpt_id
        gpt_id = insert_gpt("國文", date_str, current_user.uID)
        insert_gpt_message(gpt_id, message, True)  
        self.input_field.clear()

        if message:
            # 用戶訊息顯示（靠右）
            user_message_layout = QHBoxLayout()
            user_message_layout.setAlignment(Qt.AlignRight)  # 對齊到右側

            # 頭貼部分
            user_avatar = QLabel()
            user_avatar.setPixmap(self.create_circle_avatar("image/0.jpg"))  # 用戶頭貼
            user_avatar.setFixedSize(50, 50)  # 設定頭貼大小
            user_avatar.setScaledContents(True)  # 圖片自動縮放

            # 設定用戶的輸入框
            user_message_label = QLabel(message)
            user_message_label.setStyleSheet("""
                background-color: #dcf8c6; 
                border-radius: 20px; 
                padding: 10px; 
                word-wrap: break-word;
                max-width: 300px;  /* 限制最大寬度 */
            """)
            user_message_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
            user_message_label.setWordWrap(True)  # 啟用自動換行

            user_message_layout.addWidget(user_message_label)  # 用戶訊息在頭貼右側
            user_message_layout.addWidget(user_avatar)  # 頭貼放在右邊
            self.chat_layout.addLayout(user_message_layout)

            # 對方的回答顯示（靠左）
            response_message_layout = QHBoxLayout()
            response_message_layout.setAlignment(Qt.AlignLeft)  # 對齊到左側
            
            # 頭貼部分
            bot_avatar = QLabel()
            bot_avatar.setPixmap(self.create_circle_avatar("image/0.jpg"))  # 機器人頭貼
            bot_avatar.setFixedSize(50, 50)  # 設定頭貼大小
            bot_avatar.setScaledContents(True)  # 圖片自動縮放
            response=self.solve_problem(message,objects)

            current_date = datetime.now()
            date_str = current_date.strftime("%Y-%m-%d")
            current_user = login_check(msg, pwd)  # 假設這是你登入的地方
            gpt_id = insert_gpt("國文", date_str, current_user.uID)
            insert_gpt_message(gpt_id, response, False)  
            # 設定對方的回答
            
            
            response_message_label = QLabel( response)
            response_message_label.setStyleSheet("""
                background-color: #f1f0f0; 
                border-radius: 20px; 
                padding: 10px; 
                word-wrap: break-word; 
                max-width: 300px;  /* 限制最大寬度 */
            """)
            response_message_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
            response_message_label.setWordWrap(True)  # 啟用自動換行

            response_message_layout.addWidget(bot_avatar)  # 頭貼放在左邊
            response_message_layout.addWidget(response_message_label)  # 機器人回答在頭貼右側
            self.chat_layout.addLayout(response_message_layout)

            # 滾動條位置設定
            QTimer.singleShot(10, lambda: self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum()))



    def gpt_35_api_stream(self, messages: list): #GPT 輸出
        try:
            stream = client.chat.completions.create(
                model='gpt-3.5-turbo',
                messages=messages,
                stream=True,
            )
            full_response = ""
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_response  += chunk.choices[0].delta.content #輸出
            return full_response  
        except Exception as e:
            self.answer_label.setText(f"發生錯誤: {e}")

    def solve_problem(self, question,objects):
        if question:
            # 構造發送給 GPT 的訊息
            if(objects=="chinese"):
                messages = [{'role': 'user', 'content': f'你是個國小和國中的國文老師，麻煩用繁體中文幫她解決問題，問題是「{question}」'}]
            elif(objects=="math"):
                messages = [{'role': 'user', 'content': f'你是個國小和國中的數學老師，麻煩用繁體中文幫她解決問題，問題是「{question}」'}]
            elif(objects=="science"):
                messages = [{'role': 'user', 'content': f'你是個國小和國中的自然老師，麻煩用繁體中文幫她解決問題，問題是「{question}」'}]
            elif(objects=="english"):
                messages = [{'role': 'user', 'content': f'你是個國小和國中的英文老師，麻煩用繁體中文幫她解決問題，問題是「{question}」'}]
            else:
                messages = [{'role': 'user', 'content': f'你是個國小和國中的社會老師，麻煩用繁體中文幫她解決問題，問題是「{question}」'}]
            print(messages)
            
            # 調用 GPT API 生成解答
            response = self.gpt_35_api_stream(messages)
            return response


    def create_circle_avatar(self, image_path):
        # 生成圓形頭貼
        pixmap = QPixmap(image_path)
        size = min(pixmap.width(), pixmap.height())
        pixmap = pixmap.scaled(size, size)
        mask = pixmap.createMaskFromColor(Qt.transparent)
        pixmap.setMask(mask)
        return pixmap
        

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('介面應用')

        # Stack Widget 用來管理多個頁面
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)
        
        # 第一頁
        self.page1 = QLabel(self)
        pixmap1 = QPixmap('image/1.jpg')  # 替換為你的第一張圖片
        self.page1.setPixmap(pixmap1)
        self.page1.setScaledContents(True)
        self.stacked_widget.addWidget(self.page1)
        self.page1.mousePressEvent = self.changePage  # 滑鼠點一下進去大類別頁面
        self.create_buttons_page1()

        # 第二頁 (選大類別頁面)
        self.page2 = QLabel(self)
        pixmap2 = QPixmap('image/2.jpg')  # 替換為你的第二張圖片
        self.page2.setPixmap(pixmap2)
        self.page2.setScaledContents(True)
        self.stacked_widget.addWidget(self.page2)
        self.create_buttons_page2()

        # 第三頁 (自訂頁面)
        self.page3 = CustomPage(self)
        self.page3.back_button.clicked.connect(self.goBackToSecondPage)  # 返回按鈕
        self.stacked_widget.addWidget(self.page3)

        # 第四頁（讀書會與聊聊）
        self.page4 = QLabel(self)
        pixmap4 = QPixmap('image/7.jpg')
        self.page4.setPixmap(pixmap4)
        self.page4.setScaledContents(True)
        self.stacked_widget.addWidget(self.page4)
        self.button_chat_page4 = None  # 確保不重複創建按鈕
        self.button_study_club_page4 = None
        self.page4_back_btn = None

        # 第五頁 (英文練習頁面)
        self.page5 = EnglishPage(self)
        self.page5.back_button.clicked.connect(self.goBackToSecondPage)
        self.stacked_widget.addWidget(self.page5)


        

        # 第六頁 (統計頁面)
        self.page6 = QLabel(self)
        pixmap6 = QPixmap('image/Statistics.jpg')
        self.page6.setPixmap(pixmap6)
        self.page6.setScaledContents(True)
        self.stacked_widget.addWidget(self.page6)
        self.button_chat_page6 = None
        self.button_study_club_page6 = None
        self.page6_back_btn = None

        #分析葉面
        self.analysis_page = AnalysisPage(self)
        self.stacked_widget.addWidget(self.analysis_page)
        
         # 替換 QLabel 為新的 ChineseAnalysisPage
        self.chinese_analysis_page = ChineseAnalysisPage(self)
        self.stacked_widget.addWidget(self.chinese_analysis_page)

        
        
        # 國文解題頁面
        self.chinese_problem_solving_page = TemsolveMainWindow(self,"chinese")
        self.stacked_widget.addWidget(self.chinese_problem_solving_page)
        self.page3.button1.clicked.connect(self.showProblemSolvingPage_chinese)
        self.chinese_problem_solving_page.back_button.clicked.connect(self.go_back)

        self.math_problem_solving_page = TemsolveMainWindow(self,"math")
        self.stacked_widget.addWidget(self.math_problem_solving_page)
        self.page3.button3.clicked.connect(self.showProblemSolvingPage_math)
        self.math_problem_solving_page.back_button.clicked.connect(self.go_back)

        self.english_problem_solving_page = TemsolveMainWindow(self,"english")
        self.stacked_widget.addWidget(self.english_problem_solving_page)
        self.page3.button2.clicked.connect(self.showProblemSolvingPage_english)
        self.english_problem_solving_page.back_button.clicked.connect(self.go_back)
        
        self.science_problem_solving_page = TemsolveMainWindow(self,"science")
        self.stacked_widget.addWidget(self.science_problem_solving_page)
        self.page3.button4.clicked.connect(self.showProblemSolvingPage_science)
        self.science_problem_solving_page.back_button.clicked.connect(self.go_back)

        self.social_problem_solving_page = TemsolveMainWindow(self,"social")
        self.stacked_widget.addWidget(self.social_problem_solving_page)
        self.page3.button5.clicked.connect(self.showProblemSolvingPage_social)
        self.social_problem_solving_page.back_button.clicked.connect(self.go_back)

        #註冊介面
        self.signup_page = QLabel(self)
        pixmapsignup = QPixmap('image/account_sing_up_page.jpg')
        self.signup_page.setPixmap(pixmapsignup)
        self.signup_page.setScaledContents(True)
        self.stacked_widget.addWidget(self.signup_page)
        self.createSignupPage()
        #登入介面
        self.signin_page = QLabel(self)
        pixmapsignin = QPixmap('image/account_sing_in_page.jpg')
        self.signin_page.setPixmap(pixmapsignin)
        self.signin_page.setScaledContents(True) # 這裡你可以自訂頁面的內容
        self.stacked_widget.addWidget(self.signin_page)
        self.createSigninPage()

    # 創建按鈕 (第一頁)
    def create_buttons_page1(self):
        width = self.width()
        height = self.height()
        button_width = int(width * 0.130208)
        button_height = int(height * 0.0605)
        
        self.button_chat = QPushButton('sign-up', self.page1)
        self.button_chat.setGeometry(int(width * 0.71354166), int(height * 0.79717457114), int(button_width), int(button_height))
        self.button_chat.clicked.connect(self.showSignupPage)

        self.button_study_club = QPushButton('sign-in', self.page1)
        self.button_study_club.setGeometry(int(width * 0.5625), int(height * 0.79717457114), int(button_width), int(button_height))
        self.button_study_club.clicked.connect(self.showSigninPage)

    # 創建按鈕 (第二頁)
    def create_buttons_page2(self):
        button_positions = [(0.2, 0.3), (0.4, 0.3), (0.7, 0.3), (0.25, 0.6), (0.55, 0.6)]
        self.buttons = []

        for i, pos in enumerate(button_positions):
            btn = QPushButton('', self.page2)
            btn.clicked.connect(lambda checked, idx=i + 1: self.showPage(idx))
            self.buttons.append(btn)

        # 返回按鈕
        back_btn = QPushButton('', self.page2)
        back_btn.setGeometry(0, 0, int(self.width() * 0.06), int(self.height() * 0.074))
        back_btn.clicked.connect(self.goBackToFirstPage)

    def resizeEvent(self, event):
        QMainWindow.resizeEvent(self, event)

        # 調整第二頁按鈕
        width = self.width()
        height = self.height()
        button_width = width * 0.2
        button_height = height * 0.2
        button_positions = [(width * 0.13, height * 0.25), (width * 0.4, height * 0.25), (width * 0.67, height * 0.25),
                            (width * 0.25, height * 0.6), (width * 0.55, height * 0.6)]

        for i, btn in enumerate(self.buttons):
            btn.setGeometry(int(button_positions[i][0]), int(button_positions[i][1]), int(button_width), int(button_height))

        # 調整第四頁與第六頁的按鈕
        self.create_buttons_page4()
        self.create_buttons_page6()

    # 創建按鈕 (第四頁)
    def create_buttons_page4(self):
        width = self.width()
        height = self.height()
        button_width = width * 0.234
        button_height = height * 0.231

        if not self.button_chat_page4:
            self.button_chat_page4 = QPushButton('', self.page4)
        self.button_chat_page4.setGeometry(int(width * 0.6), int(height * 0.509), int(button_width), int(button_height))

        if not self.button_study_club_page4:
            self.button_study_club_page4 = QPushButton('', self.page4)
        self.button_study_club_page4.setGeometry(int(width * 0.156), int(height * 0.509), int(button_width), int(button_height))

        if not self.page4_back_btn:
            self.page4_back_btn = QPushButton('', self.page4)
            self.page4_back_btn.clicked.connect(self.goBackToSecondPage)
        self.page4_back_btn.setGeometry(0, 0, int(width * 0.06), int(height * 0.074))

    # 創建按鈕 (第六頁)
    def create_buttons_page6(self):
        width = self.width()
        height = self.height()
        button_width = width * 0.234
        button_height = height * 0.231

        if not self.button_chat_page6:
            self.button_chat_page6 = QPushButton('', self.page6)
            self.button_chat_page6.setGeometry(int(width * 0.6), int(height * 0.509), int(button_width), int(button_height))
            self.button_chat_page6.clicked.connect(self.goToAnalysisPage)  # 設置點擊事件

        if not self.button_study_club_page6:
            self.button_study_club_page6 = QPushButton('', self.page6)
        self.button_study_club_page6.setGeometry(int(width * 0.156), int(height * 0.509), int(button_width), int(button_height))

        if not self.page6_back_btn:
            self.page6_back_btn = QPushButton('', self.page6)
            self.page6_back_btn.clicked.connect(self.goBackToSecondPage)
        self.page6_back_btn.setGeometry(0, 0, int(width * 0.06), int(height * 0.074))
    def goToAnalysisPage(self):
        # 切換到分析頁面
        self.stacked_widget.setCurrentWidget(self.analysis_page)
    
    def createSignupPage(self):
        self.signup_username = QLineEdit(self.signup_page)
        self.signup_username.setPlaceholderText("請輸入用戶名")
        self.signup_username.setGeometry(800, 260, 400, 80)  # 手動設置位置

        self.signup_username.setStyleSheet("background: rgba(255, 255, 255, 0.3); border: none; color: black;font-size: 23px;")

        self.signup_account= QLineEdit(self.signup_page)
        self.signup_account.setPlaceholderText("請輸入帳號")
        self.signup_account.setGeometry(800, 385, 400,80) 
        self.signup_account.setStyleSheet("background: rgba(255, 255, 255, 0.3); border: none; color: black;font-size: 23px;")

        self.signup_password = QLineEdit(self.signup_page)
        self.signup_password.setPlaceholderText("請輸入密碼")
        self.signup_password.setGeometry(800, 510, 400,80) 
        self.signup_password.setStyleSheet("background: rgba(255, 255, 255, 0.3); border: none; color:black;font-size: 23px;")
        self.signup_password.setEchoMode(QLineEdit.Password)

        self.signup_button = QPushButton('註冊', self.signup_page)
        self.signup_button.setGeometry(840, 760, 480, 120)

        self.signup_page_back_btn = QPushButton('', self.signup_page)
        self.signup_page_back_btn.clicked.connect(self.goBackToFirstPage)
        self.signup_page_back_btn.setGeometry(0, 0, 120, 100)

        self.signup_button.clicked.connect(self.handleSignup)

    # 登入頁面設置
    def createSigninPage(self):
        self.signin_acount = QLineEdit(self.signin_page)
        self.signin_acount.setPlaceholderText("請輸入用戶名")
        self.signin_acount.setGeometry(800, 245, 400, 80) 
        self.signin_acount.setStyleSheet("background: rgba(255, 255, 255, 0.3); border: none; color:black;font-size: 23px;")

        self.signin_password = QLineEdit(self.signin_page)
        self.signin_password.setPlaceholderText("請輸入密碼")
        self.signin_password.setGeometry(800, 385, 400,80)
        self.signin_password.setStyleSheet("background: rgba(255, 255, 255, 0.3); border: none; color: black;font-size: 23px;")
        self.signin_password.setEchoMode(QLineEdit.Password)

        self.signin_button = QPushButton('登入', self.signin_page)
        self.signin_button.setGeometry(840, 760, 480, 120)

        self.signin_page_back_btn = QPushButton('', self.signin_page)
        self.signin_page_back_btn.clicked.connect(self.goBackToFirstPage)
        self.signin_page_back_btn.setGeometry(0, 0, 120, 100)

        self.signin_button.clicked.connect(self.handleSignin)

    # 處理註冊按鈕點擊事件
    def handleSignup(self):
        global msg, pwd  # 告訴 Python 修改的是全局變量
        username = self.signup_username.text()
        password = self.signup_password.text()
        msg=username
        pwd=password
        if register_and_login(username, username, password):
            print(f"註冊成功！用戶名: {username}")
        else:
            print("註冊失敗，可能帳號已存在。")

    # 處理登入按鈕點擊事件
    def handleSignin(self):
        global msg, pwd  # 告訴 Python 修改的是全局變量
        account = self.signin_acount.text()
        password = self.signin_password.text()
        msg=account
        pwd=password

    # 使用 login_check 函數來驗證用戶名和密碼
        user = login_check(account, password)
        if user:
            print("登入成功！用戶名:", user.name, "用戶ID:", user.uID)
        else:
            print("登入失敗，用戶名或密碼錯誤。")

    def showPage(self, button_id):
        if button_id == 1:
            self.stacked_widget.setCurrentIndex(2)
        elif button_id == 5:
            self.stacked_widget.setCurrentIndex(3)
        elif button_id == 3:
            self.stacked_widget.setCurrentIndex(4)
        elif button_id == 4:
            self.stacked_widget.setCurrentIndex(5)

    def goBackToFirstPage(self):
        self.stacked_widget.setCurrentIndex(0)

    def goBackToSecondPage(self):
        self.stacked_widget.setCurrentIndex(1)

    def changePage(self, event):
        self.stacked_widget.setCurrentIndex(1)

    def showProblemSolvingPage_chinese(self):
        self.stacked_widget.setCurrentWidget(self.chinese_problem_solving_page)
    def showProblemSolvingPage_math(self):
        self.stacked_widget.setCurrentWidget(self.math_problem_solving_page)
    def showProblemSolvingPage_english(self):
        self.stacked_widget.setCurrentWidget(self.english_problem_solving_page)
    def showProblemSolvingPage_social(self):
        self.stacked_widget.setCurrentWidget(self.social_problem_solving_page)
    def showProblemSolvingPage_science(self):
        self.stacked_widget.setCurrentWidget(self.science_problem_solving_page)

    def go_back(self):
        # 返回到上一個頁面
        #print("FFFFFFFFFFFFFFFFFFF")
        self.stacked_widget.setCurrentWidget(self.page3)

    def showSignupPage(self):
        self.stacked_widget.setCurrentWidget(self.signup_page)

    # 顯示 Sign-in 頁面
    def showSigninPage(self):
        self.stacked_widget.setCurrentWidget(self.signin_page)

    def show_chinese_analysis_page(self):
        self.stacked_widget.setCurrentWidget(self.chinese_analysis_page)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.showMaximized()  # 最大化顯示
    sys.exit(app.exec_())
