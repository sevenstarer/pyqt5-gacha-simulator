import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QWidget, QVBoxLayout

plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

class ChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = plt.figure(figsize=(6,4))
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def refresh_chart(self, count_data):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        names = list(count_data.keys())
        nums = list(count_data.values())
        ax.bar(names, nums, color=["gray", "blue", "purple", "gold"])
        ax.set_title("各品质卡牌获取数量统计")
        self.canvas.draw()