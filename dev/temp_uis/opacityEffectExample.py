import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QGraphicsOpacityEffect, QLabel
from PySide6.QtCore import QPropertyAnimation


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Opacity Animation Example")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.fade_in_button = QPushButton("Fade In", self.central_widget)
        self.fade_in_button.clicked.connect(self.fade_in)

        self.fade_out_button = QPushButton("Fade Out", self.central_widget)
        self.fade_out_button.clicked.connect(self.fade_out)

        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.fade_in_button)
        layout.addWidget(self.fade_out_button)

        self.notification_widget = QWidget(self.central_widget)
        self.notification_widget.setStyleSheet(
            "background-color: blue; color: white;")
        layout.addWidget(self.notification_widget)

        self.notification_layout = QVBoxLayout(self.notification_widget)
        self.notification_label = QLabel(
            "This is a notification", self.notification_widget)
        self.notification_layout.addWidget(self.notification_label)

        self.opacity_effect = QGraphicsOpacityEffect()
        self.notification_widget.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0)

    def fade_in(self):
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(2000)
        self.animation.setStartValue(self.opacity_effect.opacity())
        self.animation.setEndValue(1)
        self.animation.start()

    def fade_out(self):
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(2000)
        self.animation.setStartValue(self.opacity_effect.opacity())
        self.animation.setEndValue(0)
        self.animation.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
