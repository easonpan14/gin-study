import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class LineChartWidget(QWidget):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.initUI()

    def initUI(self):
        # 設置主佈局
        layout = QVBoxLayout()
        
        # 初始化Matplotlib Figure並嵌入到PyQt
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        self.setLayout(layout)
        self.plot_data()

    def plot_data(self):
        # 獲取Figure的繪圖區域
        ax = self.figure.add_subplot(111)
        
        # 清除之前的數據（如果有）
        ax.clear()
        
        # 畫折線圖
        for user, values in self.data.items():
            ax.plot(values, label=user)  # 繪製每個使用者的數據
            
        # 加入圖例和標題
        ax.legend()
        ax.set_title("User Line Chart")
        ax.set_xlabel("Index")
        ax.set_ylabel("Value")
        
        # 刷新畫布
        self.canvas.draw()

class MainWindow(QMainWindow):
    def __init__(self, data):
        super().__init__()
        
        # 設置主窗口
        self.setWindowTitle("User Line Chart")
        self.setGeometry(100, 100, 800, 600)
        
        # 初始化 LineChartWidget 並設置為主窗口中心 widget
        line_chart_widget = LineChartWidget(data)
        self.setCentralWidget(line_chart_widget)

def main(data):
    # 啟動 PyQt 應用程序
    app = QApplication(sys.argv)
    main_window = MainWindow(data)
    main_window.show()
    sys.exit(app.exec_())

# 測試數據
data = {
    "user1": [4, 8, 2, 4, 8, 5, 4],
    "user2": [4, 8, 6, 2, 5, 5, 7],
    "user3": [5, 5, 5, 5, 7, 2, 4]
}

# 運行應用
if __name__ == "__main__":
    main(data)
