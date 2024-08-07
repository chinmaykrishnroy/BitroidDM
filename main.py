from interface import *
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QTimer
from PySide6.QtWidgets import QGraphicsOpacityEffect
import sys


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.sidebar_visible_min = 45
        self.sidebar_visible_max = 150
        self.sidebar_visible = True
        self.mediaplayer_visible = True
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.show()

        self.animation_time = 80
        self.allow_notification = True
        self.label_timeout = 2500

        self.edge_margin = 8
        self.resizing = False
        self.dragging = False
        self.resize_position = None
        self.drag_position = None

        self.sideBarAnimation = QPropertyAnimation(
            self.ui.leftMenuBar, b"minimumWidth")
        self.sideBarAnimation.setDuration(self.animation_time)
        self.sideBarAnimation.setEasingCurve(QEasingCurve.InOutExpo)

        self.opacityEffect = QGraphicsOpacityEffect()
        self.ui.notificationWidget.setGraphicsEffect(self.opacityEffect)
        self.opacityEffect.setOpacity(0)
        self.ui.notificationWidget.hide()

        self.notificationAnimation = QPropertyAnimation(
            self.opacityEffect, b"opacity")
        self.notificationAnimation.setDuration(int(2 * self.animation_time))
        self.notificationAnimation.setEasingCurve(QEasingCurve.InOutSine)

        self.mediaPlayerAnimation = QPropertyAnimation(
            self.ui.mediaPlayerWidget, b"maximumHeight")
        self.mediaPlayerAnimation.setDuration(int(1 * self.animation_time))
        self.mediaPlayerAnimation.setEasingCurve(QEasingCurve.InOutSine)

        self.ui.appCloseBtn.clicked.connect(lambda: self.close())
        self.ui.appMinBtn.clicked.connect(self.setMinimized)
        self.ui.appMaxBtn.clicked.connect(self.toggleMaximized)
        self.ui.mainMenuBtn.clicked.connect(self.toggleSidebar)
        self.ui.searchMenuBtn.clicked.connect(self.showSearch)
        self.ui.downloadsMenuBtn.clicked.connect(self.showDownloads)
        self.ui.filesMenuBtn.clicked.connect(self.showFiles)
        self.ui.favoritesMenuBtn.clicked.connect(self.showFavorites)
        self.ui.historyMenuBtn.clicked.connect(self.showHistory)
        self.ui.settingsMenuBtn.clicked.connect(self.showSettings)
        self.ui.helpMenuBtn.clicked.connect(self.showHelp)
        self.ui.mediaPlayerShowBtn.clicked.connect(self.toggleMediaPlayer)
        self.ui.notificationBtn.clicked.connect(
            lambda: self.pushNotification("Hello"))
        self.ui.closeNotificationBtn.clicked.connect(self.hideNotificationTab)

    def toggleMaximized(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def setMinimized(self):
        self.showMinimized()

    def toggleSidebar(self):
        self.sidebar_visible ^= True
        if self.sidebar_visible:
            self.sideBarAnimation.setStartValue(self.ui.leftMenuBar.width())
            self.sideBarAnimation.setEndValue(self.sidebar_visible_max)
        else:
            self.sideBarAnimation.setStartValue(self.ui.leftMenuBar.width())
            self.sideBarAnimation.setEndValue(self.sidebar_visible_min)
            self.ui.leftMenuBar.setMaximumWidth(self.sidebar_visible_min)
        self.sideBarAnimation.start()

    def showSearch(self):
        if self.ui.mainStack.currentIndex() != 0:
            self.ui.mainStack.setCurrentIndex(0)
        else:
            self.toggleSidebar()

    def showDownloads(self):
        if self.ui.mainStack.currentIndex() != 1:
            self.ui.mainStack.setCurrentIndex(1)
        else:
            self.toggleSidebar()

    def showFiles(self):
        if self.ui.mainStack.currentIndex() != 2:
            self.ui.mainStack.setCurrentIndex(2)
        else:
            self.toggleSidebar()

    def showFavorites(self):
        if self.ui.mainStack.currentIndex() != 3:
            self.ui.mainStack.setCurrentIndex(3)
        else:
            self.toggleSidebar()

    def showHistory(self):
        if self.ui.mainStack.currentIndex() != 4:
            self.ui.mainStack.setCurrentIndex(4)
        else:
            self.toggleSidebar()

    def showSettings(self):
        if self.ui.mainStack.currentIndex() != 5:
            self.ui.mainStack.setCurrentIndex(5)
        else:
            self.toggleSidebar()

    def showHelp(self):
        if self.ui.mainStack.currentIndex() != 6:
            self.ui.mainStack.setCurrentIndex(6)
        else:
            self.toggleSidebar()

    def showMediaPlayer(self):
        if not self.mediaplayer_visible:
            self.mediaPlayerAnimation.setStartValue(0)
            self.mediaPlayerAnimation.setEndValue(112)
            self.mediaPlayerAnimation.start()
            self.mediaplayer_visible = True

    def hideMediaPlayer(self):
        if self.mediaplayer_visible:
            self.mediaPlayerAnimation.setStartValue(
                self.ui.mediaPlayerWidget.height())
            self.mediaPlayerAnimation.setEndValue(0)
            self.mediaPlayerAnimation.start()
            self.ui.mediaPlayerWidget.setMaximumHeight(0)
            self.mediaplayer_visible = False

    def toggleMediaPlayer(self):
        if self.ui.mediaPlayerShowBtn.isChecked():
            self.showMediaPlayer()
        else:
            self.hideMediaPlayer()

    def pushNotification(self, notification_message, notification_volume=25, tone=True):
        self.notificationAnimation.stop()
        if self.allow_notification:
            if tone:
                pass
            self.ui.notificationWidget.show()
            self.notificationAnimation.setStartValue(
                self.opacityEffect.opacity())
            self.notificationAnimation.setEndValue(1)
            self.notificationAnimation.start()
            QTimer.singleShot(int(2 * self.label_timeout),
                              self.hideNotificationTab)

    def hideNotificationTab(self):
        self.notificationAnimation.setStartValue(self.opacityEffect.opacity())
        self.notificationAnimation.setEndValue(0)
        self.notificationAnimation.start()
        # self.ui.notificationLabel.setText("")
        QTimer.singleShot(int(2 * self.animation_time),
                          lambda: self.ui.notificationWidget.hide())

    def mousePressEvent(self, event):
        rect = self.rect()
        if (
                rect.topLeft().x() + self.edge_margin >= event.x()
                or rect.bottomRight().x() - self.edge_margin <= event.x()
                or rect.topLeft().y() + self.edge_margin >= event.y()
                or rect.bottomRight().y() - self.edge_margin <= event.y()
        ):
            self.resizing = True
            self.dragging = False
            self.resize_position = event.globalPos()
        else:
            self.resizing = False
            self.dragging = True
            self.drag_position = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event):
        if self.resizing:
            delta = event.globalPos() - self.resize_position
            new_width = max(self.width() + delta.x(), 100)
            new_height = max(self.height() + delta.y(), 100)
            self.resize(new_width, new_height)
            self.resize_position = event.globalPos()
            self.setCursor(Qt.SizeFDiagCursor)
        elif self.dragging:
            self.move(event.globalPos() - self.drag_position)
            self.setCursor(Qt.SizeAllCursor)

    def mouseReleaseEvent(self, event):
        self.resizing = False
        self.dragging = False
        self.unsetCursor()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
