from PyQt5.QtWidgets import (QMainWindow, QTabWidget, QWidget, QPushButton,
                             QLabel, QListWidget, QListWidgetItem, QComboBox,
                             QVBoxLayout, QHBoxLayout, QMessageBox, QTextEdit)
from core.draw_logic import get_one_card, ten_pull
from core.data_save import load_data, reset_all_data
from core.chart_view import ChartWidget
from ui.draw_anim_dialog import DrawAnimDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5抽卡模拟器大作业")
        self.resize(900,600)
        self.data = load_data()
        self.init_ui()

    def init_ui(self):
        tab = QTabWidget()
        self.tab_draw = QWidget()
        self.tab_collection = QWidget()
        self.tab_stat = QWidget()
        tab.addTab(self.tab_draw, "抽卡页面")
        tab.addTab(self.tab_collection, "卡牌图鉴")
        tab.addTab(self.tab_stat, "数据统计")
        self.setCentralWidget(tab)

        # ========== 抽卡页面 ==========
        draw_layout = QVBoxLayout(self.tab_draw)
        top_bar = QHBoxLayout()
        self.label_remain = QLabel(f"剩余抽卡次数：{self.data['remain_draw']}")
        self.label_streak = QLabel(f"距离上次传说连续抽数：{self.data['legend_streak']}")
        btn_reset = QPushButton("重置全部数据")
        btn_reset.clicked.connect(self.on_reset)
        top_bar.addWidget(self.label_remain)
        top_bar.addWidget(self.label_streak)
        top_bar.addWidget(btn_reset)

        btn_bar = QHBoxLayout()
        self.btn_single = QPushButton("单抽")
        self.btn_ten = QPushButton("十连抽")
        self.btn_single.clicked.connect(self.on_single)
        self.btn_ten.clicked.connect(self.on_ten)
        btn_bar.addWidget(self.btn_single)
        btn_bar.addWidget(self.btn_ten)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)

        draw_layout.addLayout(top_bar)
        draw_layout.addLayout(btn_bar)
        draw_layout.addWidget(QLabel("抽卡结果："))
        draw_layout.addWidget(self.result_text)

        # ========== 图鉴页面 ==========
        coll_layout = QVBoxLayout(self.tab_collection)
        filter_bar = QHBoxLayout()
        self.combo_filter = QComboBox()
        self.combo_filter.addItems(["全部", "普通", "稀有", "史诗", "传说"])
        self.combo_filter.currentTextChanged.connect(self.refresh_collection)
        filter_bar.addWidget(QLabel("筛选品质："))
        filter_bar.addWidget(self.combo_filter)
        self.list_card = QListWidget()
        coll_layout.addLayout(filter_bar)
        coll_layout.addWidget(self.list_card)
        self.refresh_collection()

        # ========== 统计页面 ==========
        stat_layout = QVBoxLayout(self.tab_stat)
        self.chart = ChartWidget()
        self.stat_text = QLabel("统计数据")
        stat_layout.addWidget(self.stat_text)
        stat_layout.addWidget(self.chart)
        self.refresh_stat()

    def update_info_label(self):
        self.label_remain.setText(f"剩余抽卡次数：{self.data['remain_draw']}")
        self.label_streak.setText(f"距离上次传说连续抽数：{self.data['legend_streak']}")

    def on_single(self):
        if self.data["remain_draw"] < 1:
            QMessageBox.warning(self, "提示", "抽卡次数不足！")
            return
        name, qua = get_one_card(self.data)
        anim_win = DrawAnimDialog(name, qua, self)
        anim_win.exec_()

        self.data = load_data()
        self.update_info_label()
        self.refresh_collection()
        self.refresh_stat()
        self.result_text.append(f"【{qua}】{name}")

    def on_ten(self):
        if self.data["remain_draw"] < 10:
            QMessageBox.warning(self, "提示", "抽卡次数不足10次！")
            return
        res = ten_pull(self.data)
        self.result_text.append("=====十连结果=====")
        # 依次播放每张卡动画
        delay = 0
        for name, qua in res:
            QTimer.singleShot(delay, lambda n=name,q=qua: self.show_single_anim(n,q))
            delay += 500
            self.result_text.append(f"【{qua}】{name}")
        self.data = load_data()
        self.update_info_label()
        self.refresh_collection()
        self.refresh_stat()

    def show_single_anim(self, name, qua):
        dialog = DrawAnimDialog(name, qua, self)
        dialog.exec_()

    def on_reset(self):
        reset_all_data()
        self.data = load_data()
        self.result_text.clear()
        self.update_info_label()
        self.refresh_collection()
        self.refresh_stat()
        QMessageBox.information(self, "完成", "数据已重置，恢复1000抽额度")

    def refresh_collection(self):
        self.list_card.clear()
        filter_q = self.combo_filter.currentText()
        all_cards = self.data["collection"]
        for card in all_cards:
            # 匹配品质
            q = ""
            for k, lst in [("普通", ["普通战士A","普通法师B","普通弓手C"]),
                           ("稀有", ["稀有骑士","稀有牧师","稀有盗贼"]),
                           ("史诗", ["史诗龙人","史诗精灵王"]),
                           ("传说", ["创世神","终末魔龙"])]:
                if card in lst:
                    q = k
                    break
            if filter_q != "全部" and q != filter_q:
                continue
            item = QListWidgetItem(f"[{q}] {card}")
            self.list_card.addItem(item)

    def refresh_stat(self):
        cnt = self.data["card_count"]
        total = self.data["total_draw"]
        text = f"总抽卡次数：{total}\n"
        for k, v in cnt.items():
            rate = v / total * 100 if total > 0 else 0
            text += f"{k}：{v}张，实际出货率{rate:.2f}%\n"
        self.stat_text.setText(text)
        self.chart.refresh_chart(cnt)