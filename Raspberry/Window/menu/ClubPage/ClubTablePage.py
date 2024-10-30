import sys
from PyQt5.QtWidgets import QLabel,QGridLayout, QVBoxLayout, QWidget, QPushButton,QInputDialog,QSpacerItem,QSizePolicy,QMessageBox
from PyQt5.QtCore import Qt


from Window.menu.ClubPage.ClubFocusTimeChart import ClubChartPage
from GlobalVar import GlobalVar
from database.DateBase import get_groups_by_uid,get_Group_Name,create_group,join_group,get_name_by_uid  # 假設這些函數已經定義好


class ClubTable(QWidget):
    def __init__(self, parent=None,backFunction=None):
        super().__init__(parent)
        self.backFunction=backFunction
        self.initUI()
        self.page_index_map={}
        
    def showEvent(self, a0):
        super().showEvent(a0)
        self.getGroup()

    def initUI(self):
        layout = QVBoxLayout()
        # 創建backButton
        self.backButton=QPushButton("back",self)
        self.backButton.clicked.connect(self.backFunction)
        layout.addWidget(self.backButton,alignment=Qt.AlignTop)

        # 創建新增群组按钮
        self.newGroupButton = QPushButton("新增群组", self)
        self.newGroupButton.clicked.connect(self.showInputDialog)
        layout.addWidget(self.newGroupButton, alignment=Qt.AlignTop)


        # 用 QWidget 包裹 QGridLayout 表格
        self.table_widget = QWidget(self)
        self.table = QGridLayout(self.table_widget)
        layout.addWidget(self.table_widget)


        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)

        self.setLayout(layout)

    def show_chart(self, group_id):
        # 創建 ClubChartPage 實例並替換當前頁面
        self.chart_page = ClubChartPage(group_id, backFunction=self.show_table)
        self.chart_page.setParent(self)  # 設置父級為 ClubTable
        self.layout().replaceWidget(self.table_widget, self.chart_page)  # 使用table_widget替換內容
        self.chart_page.show()  # 顯示圖表頁面
        self.table_widget.hide()  # 隱藏表格頁面
        self.backButton.hide()  # 隱藏表格頁面
        self.newGroupButton.hide()  # 隱藏表格頁面

    def show_table(self):
        self.layout().replaceWidget(self.chart_page, self.table_widget)  # 替換回表格
        self.table_widget.show()  # 顯示表格界面
        self.backButton.show()  # 顯示表格界面
        self.newGroupButton.show()  # 顯示表格界面
        self.chart_page.hide()  # 隱藏表格頁面

    def getGroup(self): # 假設有幾個群組
        group_ids = get_groups_by_uid(GlobalVar.uID)  # 假設有這些群組ID
        print(group_ids)

        for i, group_id in enumerate(group_ids):
            group_label = QLabel(get_Group_Name(group_id))
            group_label.setAlignment(Qt.AlignCenter)  # 設置文字居中
            self.table.addWidget(group_label,i, 0 )

            # 創建按鈕並連接到顯示圖表的函數
            button = QPushButton("顯示圖表")
            button.clicked.connect(lambda _, gid=group_id: self.show_chart(gid))
            self.table.addWidget(button,i, 1 )
            button = QPushButton("邀請加入群組", self)
            button.clicked.connect(lambda _,gid=group_id:self.showInputDialog_For_pull_in_group(gid))
            self.table.addWidget(button,i, 2 )





    def showInputDialog(self):
        # 彈出輸入對話框
        text, ok = QInputDialog.getText(self, '輸入群組名稱', '請輸入群組名稱：')
        if ok and text:  # 檢查用戶是否點擊了 OK，並且輸入不為空
            self.new_Group(text)  # 創建新群組


    def new_Group(self,Name):
        if create_group(Name,GlobalVar.uID):
            QMessageBox.information(self, "成功", f"群組 '{Name}' 建立成功。")
            self.getGroup()  # 刷新組列表
        else:
            QMessageBox.warning(self, "失敗", f"群組 '{Name}' 建立失敗，請再試一次。")

    def showInputDialog_For_pull_in_group(self,Group_ID):
        # 彈出輸入對話框
        text, ok = QInputDialog.getText(self,'將新同伴加入讀書會!!!', '輸入想邀請的使用者ID：')
        if ok and text:  # 檢查用戶是否點擊了 OK，並且輸入不為空
            self.pull_in_group(Group_ID,text)  # 創建新群組

    def pull_in_group(self,Group_ID,uID):
        if join_group(Group_ID,uID)==1:
            QMessageBox.information(self, "成功", f"邀請 '{get_name_by_uid(uID)}' 成功。")
            self.getGroup()  # 刷新組列表
        else:
            QMessageBox.warning(self, "失敗", f"邀請 '{get_name_by_uid(uID)}' 失敗，請再試一次。")

    


        

