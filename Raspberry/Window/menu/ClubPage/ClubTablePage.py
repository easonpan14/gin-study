import sys
from PyQt5.QtWidgets import QLabel,QGridLayout, QVBoxLayout, QWidget, QPushButton,QSpacerItem,QSizePolicy
from PyQt5.QtCore import Qt



from Window.menu.ClubPage.ClubFocusTimeChart import ClubChartPage
from GlobalVar import GlobalVar
from database.DateBase import get_groups_by_uid,get_Group_Name,create_group  # 假設這些函數已經定義好


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


        # 用 QWidget 包裹 QGridLayout 表格
        self.table_widget = QWidget(self)
        self.table = QGridLayout(self.table_widget)
        layout.addWidget(self.table_widget)


        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)

        self.setLayout(layout)

    def show_chart(self, group_id):
        # 创建 ClubChartPage 实例并替换当前页面
        self.chart_page = ClubChartPage(group_id, backFunction=self.show_table)
        self.chart_page.setParent(self)  # 设置父级为 ClubTable
        self.layout().replaceWidget(self.table_widget, self.chart_page)  # 使用table_widget替换内容
        self.chart_page.show()  # 显示图表页面
        self.table_widget.hide()  # 隐藏表格页面
        self.backButton.hide()  # 隐藏表格页面

    def show_table(self):
        self.layout().replaceWidget(self.chart_page, self.table_widget)  # 替换回表格
        self.table_widget.show()  # 显示表格界面
        self.backButton.show()  # 隐藏表格页面
        self.chart_page.hide()  # 隐藏表格页面

    def getGroup(self): # 假設有幾個群組
        group_ids = get_groups_by_uid(GlobalVar.uID)  # 假設有這些群組ID
        

        for i, group_id in enumerate(group_ids):
            group_label = QLabel(get_Group_Name(group_id))
            group_label.setAlignment(Qt.AlignCenter)  # 設置文字居中
            self.table.addWidget(group_label,i, 0 )

            # 創建按鈕並連接到顯示圖表的函數
            button = QPushButton("顯示圖表")
            button.clicked.connect(lambda _, gid=group_id: self.show_chart(gid))
            self.table.addWidget(button,i, 1 )
    #def new_Group(self,Name):
        #if create_group(Name,GlobalVar.uID):
            #
        #else :

        
        

