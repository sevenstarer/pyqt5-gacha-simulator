from PyQt5.QtWidgets import (QDialog, QLabel, QVBoxLayout, QGraphicsOpacityEffect)
from PyQt5.QtCore import Qt, QPropertyAnimation, QTimer, QPoint
from PyQt5.QtGui import QFont, QColor, QLinearGradient, QBrush, QPainter
import random
from PyQt5.QtGui import QPixmap

class DrawAnimDialog(QDialog):
    def __init__(self, card_name, quality, parent=None):
        super().__init__(parent)
        self.card_name = card_name
        self.quality = quality
        self.setWindowTitle("召唤结果")
        self.setFixedSize(500, 600)
        self.setModal(True)
        self.setAutoFillBackground(False)
        self.bg_pix = QPixmap("assets/summon_bg.jpg")
        print("图片加载状态：", self.bg_pix.isNull())
        print("图片宽高：", self.bg_pix.width(), self.bg_pix.height())

        if not self.bg_pix.isNull():
            self.bg_pix = self.bg_pix.scaled(self.size(), Qt.KeepAspectRatioByExpanding)
        else:
            self.bg_pix = None
            # 加载失败用深色
            self.setStyleSheet("background: #0a0a20;")


        self.init_ui()
        self.start_animation()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        self.title_label = QLabel("正在进行召唤")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("SimHei", 20, QFont.Bold))
        self.card_label = QLabel("")
        self.card_label.setFixedSize(300, 400)
        self.card_label.setAlignment(Qt.AlignCenter)
        self.card_label.setStyleSheet("border-radius:10px;")
        self.info_label = QLabel("")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setFont(QFont("SimHei", 16))
        layout.addWidget(self.title_label)
        layout.addSpacing(30)
        layout.addWidget(self.card_label)
        layout.addSpacing(20)
        layout.addWidget(self.info_label)
        self.setLayout(layout)
        self.opacity_effect = QGraphicsOpacityEffect()
        self.card_label.setGraphicsEffect(self.opacity_effect)
        self.opacity_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.scale_anim = QPropertyAnimation(self.card_label, b"geometry")
        self.title_label.setStyleSheet("background:rgba(0,0,0,120); padding:6px; border-radius:8px;")
        self.info_label.setStyleSheet("background:rgba(0,0,0,120); padding:6px; border-radius:8px;")

    def start_animation(self):
        self.timer1 = QTimer()
        self.timer1.timeout.connect(self.stage2_show_card)
        self.timer1.start(800)

    def stage2_show_card(self):
        # 你原有卡牌样式、动画逻辑完全不动
        self.timer1.stop()
        if self.quality == "传说":
            card_style = """
                background: qlineargradient(0,0,0,1,stop(0,#ffd700),stop(1,#ff4500));
                border:4px solid gold; color:white; font-size:24px; font-weight:bold;
            """
            title_text = "★★★★★ 五星从者降临！"
            title_color = "#ffd700"
        elif self.quality == "史诗":
            card_style = """
                background: qlineargradient(0,0,0,1,stop(0,#9932cc),stop(1,#4b0082));
                border:3px solid #9932cc; color:white;
            """
            title_text = "四星稀有英灵"
            title_color = "#9932cc"
        elif self.quality == "稀有":
            card_style = """
                background: #4169e1; border:3px solid #87ceeb; color:white;
            """
            title_text = "三星英灵"
            title_color = "#87ceeb"
        else:
            card_style = "background:#888888; color:#222;"
            title_text = "普通英灵"
            title_color = "#aaaaaa"
        self.card_label.setStyleSheet(card_style)
        self.card_label.setText(self.card_name)
        self.title_label.setText(title_text)
        self.title_label.setStyleSheet(f"color:{title_color};")
        self.info_label.setText(f"【{self.quality}】{self.card_name}")
        self.opacity_anim.setDuration(1000)
        self.opacity_anim.setStartValue(0)
        self.opacity_anim.setEndValue(1)
        self.opacity_anim.start()
        if self.quality == "传说":
            rect_normal = self.card_label.geometry()
            rect_big = rect_normal.adjusted(-30, -30, 30, 30)
            self.scale_anim.setDuration(600)
            self.scale_anim.setStartValue(rect_normal)
            self.scale_anim.setEndValue(rect_big)
            self.scale_anim.start()
            QTimer.singleShot(600, lambda: self.scale_back(rect_normal))
            self.shake_window()
        QTimer.singleShot(3000, self.close)

    def scale_back(self, origin_rect):
        self.scale_anim.setStartValue(self.card_label.geometry())
        self.scale_anim.setEndValue(origin_rect)
        self.scale_anim.start()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # 第一步：统一绘制背景图
        if self.bg_pix is not None and not self.bg_pix.isNull():
            painter.drawPixmap(self.rect(), self.bg_pix)

        # 仅传说卡叠加金光光圈特效，普通卡只显示背景
        if self.quality == "传说":
            gradient = QLinearGradient(0,0,self.width(),self.height())
            gradient.setColorAt(0, QColor(255,215,0,80))
            gradient.setColorAt(0.5, QColor(255,69,0,60))
            gradient.setColorAt(1, QColor(255,215,0,80))
            painter.setBrush(QBrush(gradient))
            painter.drawEllipse(self.rect().center(), 220,220)
            # 随机星光
            painter.setBrush(QColor(255,255,255))
            for _ in range(20):
                x = random.randint(0, self.width())
                y = random.randint(0, self.height())
                size = random.randint(2,6)
                painter.drawEllipse(QPoint(x,y), size, size)
    def shake_window(self):
        from PyQt5.QtCore import QPropertyAnimation
        shake_anim = QPropertyAnimation(self, b"pos")
        start_pos = self.pos()
        offsets = [QPoint(-5,0), QPoint(5,0), QPoint(0,-5), QPoint(0,5)]
        for p in offsets:
            shake_anim.setStartValue(start_pos)
            shake_anim.setEndValue(start_pos + p)
            shake_anim.setDuration(50)
            shake_anim.start()
            start_pos = start_pos + p