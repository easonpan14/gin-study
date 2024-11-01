from PyQt5.QtWidgets import QWidget,QLabel,QPushButton,QLineEdit
from PyQt5.QtGui import QPixmap
from gtts import gTTS
from translate import Translator 
import io
import pygame

class EnglishPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 設定佈局
        self.setWindowTitle('English Practice')
        self.setGeometry(100, 100, 1024, 768)
        width = 800
        height = 480

        # 加載背景圖片
        self.background_label = QLabel(self)
        self.background_label.setGeometry(0, 0, 800, 480)
        self.set_background_image('Window/image/5.jpg')

        # 創建輸入框
        self.input_field = QLineEdit(self)
        self.input_field.setGeometry(int(
            width*0.078125), int(height*0.282542), int(width*0.3125), int(height*0.2018163))
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
        self.play_button.setGeometry(int(
            width*0.423), int(height*0.676084), int(width*0.041666), int(height*0.0807265))
        self.play_button.clicked.connect(self.play_audio)

        # 創建翻譯按鈕
        self.translate_button = QPushButton('翻譯成中文', self)
        self.translate_button.setGeometry(
            int(width*0.423), int(height*0.776084), int(width*0.1), int(height*0.05))
        self.translate_button.clicked.connect(self.translate_text)

        # 顯示翻譯結果的標籤
        self.translation_label = QLabel(self)
        self.translation_label.setGeometry(
            1000, int(height*0.282542), int(width*0.1), int(height*0.05))
        self.translation_label.setStyleSheet("""
            color: black;
            font-size: 24px;
        """)

        # 創建返回按鈕
        self.back_button = QPushButton('', self)
        self.back_button.setGeometry(
            0, 0, int(width*0.0625), int(height*0.0807265))

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
        width = 800
        height = 480
        self.background_label.setGeometry(0, 0, width, height)
        self.input_field.setGeometry(int(
            width*0.078125), int(height*0.282542), int(width*0.3125), int(height*0.2018163))
        self.play_button.setGeometry(int(
            width*0.423), int(height*0.676084), int(width*0.041666), int(height*0.0807265))
        self.translate_button.setGeometry(
            int(width*0.375), int(height*0.676084), 80, 80)
        self.back_button.setGeometry(
            0, 0, int(width*0.0625), int(height*0.0807265))
        self.translation_label.setGeometry(
            1080, 350, int(width*0.1), int(height*0.05))

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
