from PyQt5.QtWidgets import QMainWindow, QStackedWidget,QLabel,QPushButton,QLineEdit,QWidget
from PyQt5.QtGui import QPixmap


#自訂
from Window.menu.CustomPage.CustomPage import CustomPage
from Window.menu.StatisticsPage.AnalysisPage.SubjectAnalysisPage import SubjectAnalysisPage
from Window.menu.CustomPage.TemsolveMainWindow import TemsolveMainWindow
from Window.menu.StatisticsPage.AnalysisPage.AnalysisPage import AnalysisPage
from Window.menu.EnglishPage.EnglishPage import EnglishPage
from Window.menu.ClubPage.ClubTablePage import ClubTable

from database.DateBase import register_and_login,login_check,find_gpt
from GlobalVar import GlobalVar

class MainWindow(QMainWindow):
    

    def __init__(self):
        super().__init__()
        self.setWindowTitle('介面應用')
        # Stack Widget 用來管理多個頁面
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)
        self.page_index_map={}
        # 第一頁(首頁)---------------------------可用-------------------------------
        #build_MainPage()
        self.MainPage = QLabel(self)
        pixmap1 = QPixmap('Window/image/1.jpg')             # new 一張圖片
        self.MainPage.setPixmap(pixmap1)                   #將pixmap設為QLabel顯示圖片
        self.MainPage.setScaledContents(True)              #自動縮放QPixmap
        self.addStackedWidget_updatePageIndexMap("首頁",self.MainPage)#將QLabel加入stacked_widget 並註冊至self.page_index_map 以利後續查詢
        
        self.MainPage.mousePressEvent = self.showPage("主菜單")    #設定點擊觸發事件(轉跳到stacked_widget[1]//第一頁)
        self.create_buttons_MainPage()                     #建構登入、註冊按鈕

        # 第二頁 (主菜單)------------------可用-------------------------------
        self.MenuPage = QLabel(self)
        pixmap2 = QPixmap('Window/image/2.jpg')  # 替換為你的第二張圖片
        self.MenuPage.setPixmap(pixmap2)
        self.MenuPage.setScaledContents(True)
        self.addStackedWidget_updatePageIndexMap("主菜單",self.MenuPage)
        self.create_buttons_MenuPage()

        # 第三頁 (解題科目菜單)---------------可用-------------------------------
        self.GPTMenuPage = CustomPage(self)
        self.GPTMenuPage.back_button.clicked.connect(lambda _,Page="主菜單":self.showPage(Page))  # 返回按鈕
        self.addStackedWidget_updatePageIndexMap("解題",self.GPTMenuPage)
        
        # 第四頁（讀書會）---------------可用-------------------------------
        self.ClubPage = QLabel(self)
        pixmap4 = QPixmap('Window/image/7.jpg')
        self.ClubPage.setPixmap(pixmap4)
        self.ClubPage.setScaledContents(True)
        self.addStackedWidget_updatePageIndexMap("讀書會",self.ClubPage)
        self.create_buttons_ClubPage()

        # 第五頁 (英文練習頁面)----------------可用-------------------------------
        self.EnglishPage = EnglishPage(self)
        self.EnglishPage.back_button.clicked.connect(lambda _,Page="主菜單":self.showPage(Page))
        self.addStackedWidget_updatePageIndexMap("英文翻譯",self.EnglishPage)



        # 第六頁 (統計頁面)
        self.StatisticsPage = QLabel(self)
        pixmap6 = QPixmap('Window/image/Statistics.jpg')
        self.StatisticsPage.setPixmap(pixmap6)
        self.StatisticsPage.setScaledContents(True)
        self.addStackedWidget_updatePageIndexMap("統計",self.StatisticsPage)
        self.create_buttons_StatisticsPage()




        # 分析頁面
        self.analysis_page = AnalysisPage(self)
        self.analysis_page.back_button.clicked.connect(lambda _,Page="統計":self.showPage(Page))
        self.addStackedWidget_updatePageIndexMap("分析",self.analysis_page)

        # 初始化各個分析頁面
        subject_name=["國文","數學","英文","自然","社會"]
        self.SubjectAnalysisPage_map={}
        for subject in subject_name:
            self.SubjectAnalysisPage_map[subject+"分析"]=SubjectAnalysisPage(subject, self)
            back_btn = QPushButton('', self.SubjectAnalysisPage_map[subject+"分析"])
            back_btn.setGeometry(0, 0, int(self.width() * 0.06),int(self.height() * 0.074))
            back_btn.clicked.connect(lambda _,Page="分析":self.showPage(Page))
            self.addStackedWidget_updatePageIndexMap(subject+"分析",self.SubjectAnalysisPage_map[subject+"分析"])


        
        


        #初始化 {國、數、英、自、社} 解題頁面
        self.INFO_solving_page()
        
        
        


        # 註冊介面
        self.signup_page = QLabel(self)
        pixmapsignup = QPixmap('Window/image/account_sing_up_page.jpg')
        self.signup_page.setPixmap(pixmapsignup)
        self.signup_page.setScaledContents(True)
        self.addStackedWidget_updatePageIndexMap("註冊",self.signup_page)
        self.createSignupPage()
        # 登入介面
        self.signin_page = QLabel(self)
        pixmapsignin = QPixmap('Window/image/account_sing_in_page.jpg')
        self.signin_page.setPixmap(pixmapsignin)
        self.signin_page.setScaledContents(True)  # 這裡你可以自訂頁面的內容
        self.addStackedWidget_updatePageIndexMap("登入",self.signin_page)
        self.createSigninPage()

    # 創建按鈕 (第一頁)
    def create_buttons_MainPage(self): 
        width = self.width()
        height = self.height()
    
        # 設定按鈕大小
        button_width = int(width * 0.39)
        button_height = int(height * 0.12)


        # 登入按鈕 - 放置在右下角偏右的位置
        self.button_signin = QPushButton('Sign-In', self.MainPage)
        self.button_signin.setGeometry(
            int(width * 0.80*2),  # x 座標
            int(height * 0.825*2), # y 座標
            button_width,
            button_height
        )


        # 註冊按鈕 - 放置在右下角偏左的位置
        self.button_signup = QPushButton('Sign-Up', self.MainPage)
        self.button_signup.setGeometry(
            int(width * 1*2),  # x 座標
            int(height * 0.825*2), # y 座標
            button_width,
            button_height
        )
        self.button_signup.clicked.connect(lambda _, Page="註冊": self.showPage(Page))

        
        self.button_signin.clicked.connect(lambda _, Page="登入": self.showPage(Page))

        # 返回按鈕 - 放置在左上角
        self.button_back = QPushButton('Back', self.MainPage)
        self.button_back.setGeometry(
            int(width * 0.02),  # x 座標
            int(height * 0.02), # y 座標
            int(width * 0.1),  # 返回按鈕略小
            int(width * 0.1)
        )
        self.button_back.clicked.connect(lambda _, Page="返回": self.showPage(Page))


    # 創建按鈕 (第二頁)
    def create_buttons_MenuPage(self):

        self.buttons = []
        button_name=["解題","專注偵測","英文翻譯","統計","讀書會"]
        for name in button_name:
            btn = QPushButton(name, self.MenuPage)
            btn.clicked.connect(lambda _, Page=name: self.showPage(Page))
            self.buttons.append(btn)


        # 返回按鈕
        back_btn = QPushButton('', self.MenuPage)
        back_btn.setGeometry(0, 0, int(self.width() * 0.06),
                             int(self.height() * 0.074))
        back_btn.clicked.connect(lambda _,Page="首頁":self.showPage(Page))


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
            btn.setGeometry(int(button_positions[i][0]), int(
                button_positions[i][1]), int(button_width), int(button_height))


    # 創建按鈕 (第四頁)
    def create_buttons_ClubPage(self):
        width = self.width()
        height = self.height()
        button_width = width * 0.6
        button_height = height * 0.5

        #與...聊聊
        #build 與...聊聊
        self.psychological_problem_solving_page = TemsolveMainWindow(self, "與...聊聊")
        self.psychological_problem_solving_page.back_button.clicked.connect(lambda _,Page="讀書會": self.showPage(Page))
        
    
        #讀書會 入口
        self.addStackedWidget_updatePageIndexMap("讀書會圖表",ClubTable(parent=self,backFunction=lambda _,Page="讀書會":self.showPage(Page)))
        self.button_chat_ClubPage = QPushButton('讀書會圖表', self.ClubPage)
        self.button_chat_ClubPage.clicked.connect(lambda _,Page="讀書會圖表": self.showPage(Page))
        self.button_chat_ClubPage.setGeometry(
            int(width * 0.8), int(height), int(button_width), int(button_height))


        #綁定 與...聊聊 入口
        self.addStackedWidget_updatePageIndexMap("與...聊聊",self.psychological_problem_solving_page)
        self.button_chat_ClubPage = QPushButton('與...聊聊', self.ClubPage)
        self.button_chat_ClubPage.clicked.connect(lambda _,Page="與...聊聊": self.showPage(Page))
        self.button_chat_ClubPage.setGeometry(
            int(width * 2), int(height), int(button_width), int(button_height))


        self.ClubPage_back_btn = QPushButton('', self.ClubPage)
        self.ClubPage_back_btn.clicked.connect(lambda _,Page="主菜單":self.showPage(Page))
        self.ClubPage_back_btn.setGeometry(
            0, 0, int(width * 0.06), int(height * 0.074))
        
    
        
        
        
        

    # 創建按鈕 (第六頁)
    def create_buttons_StatisticsPage(self):
        width = self.width()
        height = self.height()
        button_width = width * 0.6
        button_height = height * 0.5


        self.button_study_club_StatisticsPage = QPushButton('', self.StatisticsPage)
        self.button_study_club_StatisticsPage.setGeometry(
            int(width *0.8), int(height ), int(button_width), int(button_height))

        
        self.button_chat_StatisticsPage = QPushButton('分析', self.StatisticsPage)
        self.button_chat_StatisticsPage.setGeometry(
            int(width*2 ), int(height ), int(button_width), int(button_height))
        self.button_chat_StatisticsPage.clicked.connect(lambda _,Page="分析":self.showPage(Page))  # 設置點擊事件

        

        self.StatisticsPage_back_btn = QPushButton('', self.StatisticsPage)
        self.StatisticsPage_back_btn.clicked.connect(lambda _,Page="主菜單":self.showPage(Page))
        self.StatisticsPage_back_btn.setGeometry(
            0, 0, int(width * 0.06), int(height * 0.074))

    
    def show_analysis_page(self, page):
        # 切換到指定的分析頁面
        self.showPage(page)
        self.SubjectAnalysisPage_map[page].update_table()  # 切換到頁面時更新表格

#__________________________________________________________登入及註冊頁面、點擊事件_______________________________________________________
    # 註冊頁面設置
    def createSignupPage(self):
        self.signup_username = QLineEdit(self.signup_page)
        self.signup_username.setPlaceholderText("請輸入用戶名")
        self.signup_username.setGeometry(800, 260, 400, 80)  # 手動設置位置

        self.signup_username.setStyleSheet(
            "background: rgba(255, 255, 255, 0.3); border: none; color: black;font-size: 23px;")

        self.signup_account = QLineEdit(self.signup_page)
        self.signup_account.setPlaceholderText("請輸入帳號")
        self.signup_account.setGeometry(800, 385, 400, 80)
        self.signup_account.setStyleSheet(
            "background: rgba(255, 255, 255, 0.3); border: none; color: black;font-size: 23px;")

        self.signup_password = QLineEdit(self.signup_page)
        self.signup_password.setPlaceholderText("請輸入密碼")
        self.signup_password.setGeometry(800, 510, 400, 80)
        self.signup_password.setStyleSheet(
            "background: rgba(255, 255, 255, 0.3); border: none; color:black;font-size: 23px;")
        self.signup_password.setEchoMode(QLineEdit.Password)

        self.signup_button = QPushButton('註冊', self.signup_page)
        self.signup_button.setGeometry(840, 760, 480, 120)

        self.signup_page_back_btn = QPushButton('', self.signup_page)
        self.signup_page_back_btn.clicked.connect(lambda _,Page="首頁":self.showPage(Page))
        self.signup_page_back_btn.setGeometry(0, 0, 120, 100)

        self.signup_button.clicked.connect(self.handleSignup)

    # 登入頁面設置
    def createSigninPage(self):
        self.signin_acount = QLineEdit(self.signin_page)
        self.signin_acount.setPlaceholderText("請輸入用戶名")
        self.signin_acount.setGeometry(800, 245, 400, 80)
        self.signin_acount.setStyleSheet(
            "background: rgba(255, 255, 255, 0.3); border: none; color:black;font-size: 23px;")

        self.signin_password = QLineEdit(self.signin_page)
        self.signin_password.setPlaceholderText("請輸入密碼")
        self.signin_password.setGeometry(800, 385, 400, 80)
        self.signin_password.setStyleSheet(
            "background: rgba(255, 255, 255, 0.3); border: none; color: black;font-size: 23px;")
        self.signin_password.setEchoMode(QLineEdit.Password)

        self.signin_button = QPushButton('登入', self.signin_page)
        self.signin_button.setGeometry(840, 760, 480, 120)

        self.signin_page_back_btn = QPushButton('', self.signin_page)
        self.signin_page_back_btn.clicked.connect(lambda _,Page="首頁":self.showPage(Page))
        self.signin_page_back_btn.setGeometry(0, 0, 120, 100)

        self.signin_button.clicked.connect(self.handleSignin)

    # 處理註冊按鈕點擊事件
    def handleSignup(self):
        username = self.signup_username.text()
        password = self.signup_password.text()
        msg = username
        pwd = password
        user= register_and_login(username, username, password)
        if user.uID>0:
            print(f"註冊成功！用戶名: {username}")
            GlobalVar.uID = user.uID
            self.showPage("主菜單")
        else:
            print("註冊失敗，可能帳號已存在。")


#
    # 處理登入按鈕點擊事件
    def handleSignin(self):
        account = self.signin_acount.text()
        password = self.signin_password.text()
        msg = account
        pwd = password

    # 使用 login_check 函數來驗證用戶名和密碼
        user = login_check(account, password)
        if user.uID > 0 :
            print("登入成功！用戶名:", user.name, "用戶ID:", user.uID)
            # gpt的資料
            GlobalVar.uID=user.uID
            GlobalVar.gpt_data = find_gpt(user.uID)
            self.showPage("主菜單")
            
        else:
            print("登入失敗，用戶名或密碼錯誤。")
        
    
        





#_____________________________________________________頁面切換_________________________________________________________________________
    #依據頁面名稱string，展示頁面
    def showPage(self,title:str):
        if(self.page_index_map.get(title)!=None):
            self.stacked_widget.setCurrentIndex(self.page_index_map[title])
        else:
            print (f'頁面展示失敗title={title}')


#____________________________________________________頁面註冊__________________________________________________________________________

    #註冊widget頁面，並記錄index-----------------唯一可使用stacked_widget的地方
    def addStackedWidget_updatePageIndexMap(self,name:str,page:QWidget)->int:
        self.stacked_widget.addWidget(page)  # 添加頁面到堆疊
        Index = len(self.page_index_map)  # 獲取當前索引
        self.page_index_map[name] = Index  # 更新頁面索引映射
        print(self.page_index_map)  # 輸出頁面索引映射
        #print(self.stacked_widget.count())  # 輸出當前頁面數量
        return Index  # 返回當前索引

#__________________________________________________________________________建造解題頁面______________________________________________________________
    def INFO_solving_page(self):
        
        suject_names=["國文","數學","英文","自然","社會"]

        for suject in suject_names:
            sujectPage=TemsolveMainWindow(self,suject)                          #建構解題頁面
            self.addStackedWidget_updatePageIndexMap(suject+"解題",sujectPage)  #註冊Page至StackedWidget，並命名為suject+"解題"
            self.GPTMenuPage.button_map[suject].clicked.connect(lambda _,Page=suject+"解題": self.showPage(Page)) #綁定按鈕解題菜單進入解題頁面按鈕
            sujectPage.back_button.clicked.connect(lambda _,Page="解題": self.showPage(Page))                                          #綁定解題頁面返回按鈕
        



