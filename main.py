import sys
import webbrowser

from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QTimer
from PySide6.QtWidgets import QGraphicsOpacityEffect
from searchthread import SearchThread
from networkthread import AppNetworkMonitor

from interface import *


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

        self.internet_connection = False
        self.torrent_engine_active = False

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

        self.dots = ""
        self.dots_timer = QTimer(self)
        self.dots_timer.timeout.connect(self.updateDots)

        self.click_timer = QTimer(self)
        self.click_timer.setSingleShot(True)
        self.click_timer.timeout.connect(self.openDefaultMagnet)

        self.initNetworkMonitor()

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
        self.ui.settingsBtn.clicked.connect(lambda: self.ui.mainStack.setCurrentIndex(5))
        self.ui.helpMenuBtn.clicked.connect(self.showHelp)
        self.ui.mediaPlayerShowBtn.clicked.connect(self.toggleMediaPlayer)
        self.ui.notificationBtn.clicked.connect(
            lambda: self.pushNotification("Hello"))
        self.ui.closeNotificationBtn.clicked.connect(self.hideNotificationTab)

        self.ui.searchBtn.clicked.connect(self.searchTorrents)

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

    def pushNotification(self, notification_message, notification_title='Notification', notification_volume=25, tone=True):
        self.notificationAnimation.stop()
        if self.allow_notification:
            if tone:
                pass
            self.ui.notificationWidget.show()
            self.notificationAnimation.setStartValue(
                self.opacityEffect.opacity())
            self.notificationAnimation.setEndValue(1)
            self.notificationAnimation.start()
            if notification_title: self.ui.notificationTitleLabel.setText(notification_title)
            else: self.ui.notificationTitleLabel.hide()
            self.ui.notificationTextLabel.setText(notification_message)
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
                rect.topLeft().x() + self.edge_margin >= event.position().x()
                or rect.bottomRight().x() - self.edge_margin <= event.position().x()
                or rect.topLeft().y() + self.edge_margin >= event.position().y()
                or rect.bottomRight().y() - self.edge_margin <= event.position().y()
        ):
            self.resizing = True
            self.dragging = False
            self.resize_position = event.globalPosition().toPoint()
        else:
            self.resizing = False
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.pos()

    def mouseMoveEvent(self, event):
        self.unsetCursor()
        if self.resizing:
            delta = event.globalPosition().toPoint() - self.resize_position
            new_width = max(self.width() + delta.x(), 100)
            new_height = max(self.height() + delta.y(), 100)
            self.resize(new_width, new_height)
            self.resize_position = event.globalPosition().toPoint()
            self.setCursor(Qt.SizeFDiagCursor)
        elif self.dragging:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            self.setCursor(Qt.SizeAllCursor)

    def mouseReleaseEvent(self, event):
        self.resizing = False
        self.dragging = False
        self.unsetCursor()

    def initNetworkMonitor(self):
        self.network_monitor = AppNetworkMonitor()
        self.network_monitor.connectivity_changed.connect(self.updateNetConnectivity)
        self.network_monitor.speed_changed.connect(self.updateNetSpeed)
        self.network_monitor.start()

    def updateNetConnectivity(self, connected):
        self.internet_connection = connected
        if connected and not self.torrent_engine_active: self.initSearchThread()
        self.temporaryLog("Conected to Internet!" if connected else "No Internet!", 1500)
        self.ui.internetConnectivityBtn.setIcon(QIcon(':/icons/icons/cil-wifi-signal-4.png' if connected else ':/icons/icons/cil-wifi-signal-off.png'))

    def updateNetSpeed(self, speed):
        self.ui.netSpeedBtn.setText(self.formatNetSpeed(speed))

    def formatNetSpeed(self, speed):
        units = ["B/s", "KB/s", "MB/s", "GB/s", "TB/s"]
        unit_index = 0
        while speed >= 1024 and unit_index < len(units) - 1:
            speed /= 1024.0
            unit_index += 1
        return f"{speed:.2f} {units[unit_index]}"

    def updateDots(self, number_of_dots=3):
        if not hasattr(self, 'baseText'): self.baseText = self.ui.logLabel.text()
        if len(self.dots) < number_of_dots: self.dots += "."
        else: self.dots = ""
        self.ui.logLabel.setText(f"{self.baseText}{self.dots}")

    def initSearchThread(self):
        self.search_thread = SearchThread()
        self.search_thread.search_result.connect(self.showSearchResult)
        self.torrent_engine_active = True

    def clearTorrentResults(self):
        while self.ui.verticalLayout_13.count():
            item = self.ui.verticalLayout_13.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

    def createResultTile(self, result, parent_widget, layout):
        searchOutputFrame = QFrame(parent_widget)
        searchOutputFrame.setObjectName("searchOutputFrame")
        searchOutputFrame.setMinimumSize(QSize(0, 112))
        searchOutputFrame.setFrameShape(QFrame.Shape.StyledPanel)
        searchOutputFrame.setFrameShadow(QFrame.Shadow.Raised)

        verticalLayout_14 = QVBoxLayout(searchOutputFrame)
        verticalLayout_14.setSpacing(4)
        verticalLayout_14.setContentsMargins(-1, -1, -1, 9)

        # Result name label
        resultNameLabel = QLabel(searchOutputFrame)
        resultNameLabel.setObjectName("resultNameLabel")
        resultNameLabel.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        resultNameLabel.setText(result.get('name', 'N/A'))
        verticalLayout_14.addWidget(resultNameLabel)

        # Info Frame 1
        searchOutputInfoFrame1 = QFrame(searchOutputFrame)
        searchOutputInfoFrame1.setMinimumSize(QSize(0, 22))
        searchOutputInfoFrame1.setFrameShape(QFrame.Shape.StyledPanel)
        searchOutputInfoFrame1.setFrameShadow(QFrame.Shadow.Raised)

        horizontalLayout_13 = QHBoxLayout(searchOutputInfoFrame1)
        horizontalLayout_13.setSpacing(16)
        horizontalLayout_13.setContentsMargins(0, 0, 0, 0)

        # Seeder label
        resultSeederLabel = QLabel(searchOutputInfoFrame1)
        resultSeederLabel.setMinimumSize(QSize(72, 0))
        resultSeederLabel.setText(f"Seeders: {result.get('seeder', 'N/A')}")
        horizontalLayout_13.addWidget(resultSeederLabel)

        # Leecher label
        resultLeecherLabel = QLabel(searchOutputInfoFrame1)
        resultLeecherLabel.setMinimumSize(QSize(72, 0))
        resultLeecherLabel.setText(f"Leechers: {result.get('leecher', 'N/A')}")
        horizontalLayout_13.addWidget(resultLeecherLabel)

        # Size label
        resultSizeLabel = QLabel(searchOutputInfoFrame1)
        resultSizeLabel.setMinimumSize(QSize(82, 0))
        resultSizeLabel.setText(f"Size: {result.get('size', 'N/A')}")
        horizontalLayout_13.addWidget(resultSizeLabel)

        # NSFW label
        nsfwLabel = QLabel(searchOutputInfoFrame1)
        nsfwLabel.setMinimumSize(QSize(36, 0))
        nsfwText = "NSFW" if result.get('nsfw', False) else "SAFE"
        nsfwLabel.setText(nsfwText)
        horizontalLayout_13.addWidget(nsfwLabel)

        verticalLayout_14.addWidget(searchOutputInfoFrame1, 0, Qt.AlignmentFlag.AlignLeft)

        # Info Frame 2
        searchOutputInfoFrame2 = QFrame(searchOutputFrame)
        searchOutputInfoFrame2.setMinimumSize(QSize(0, 22))
        searchOutputInfoFrame2.setFrameShape(QFrame.Shape.StyledPanel)
        searchOutputInfoFrame2.setFrameShadow(QFrame.Shadow.Raised)

        horizontalLayout_14 = QHBoxLayout(searchOutputInfoFrame2)
        horizontalLayout_14.setSpacing(16)
        horizontalLayout_14.setContentsMargins(0, 0, 0, 0)

        # Age label
        resultAgeLabel = QLabel(searchOutputInfoFrame2)
        resultAgeLabel.setText(f"Age: {result.get('age', 'N/A')}")
        horizontalLayout_14.addWidget(resultAgeLabel)

        # Site label
        resultSiteLabel = QLabel(searchOutputInfoFrame2)
        resultSiteLabel.setText(f"Site: {result.get('site', 'N/A')}")
        horizontalLayout_14.addWidget(resultSiteLabel)

        # Type label
        resultTypeLabel = QLabel(searchOutputInfoFrame2)
        resultTypeLabel.setMinimumSize(QSize(130, 0))
        resultTypeLabel.setText(f"Type: {result.get('type', 'N/A')}")
        horizontalLayout_14.addWidget(resultTypeLabel)

        verticalLayout_14.addWidget(searchOutputInfoFrame2, 0, Qt.AlignmentFlag.AlignLeft)

        # Buttons Frame
        searchOutputBtnsFrame = QFrame(searchOutputFrame)
        searchOutputBtnsFrame.setObjectName("searchOutputBtnsFrame")
        searchOutputBtnsFrame.setMinimumSize(QSize(0, 22))
        searchOutputBtnsFrame.setFrameShape(QFrame.Shape.StyledPanel)
        searchOutputBtnsFrame.setFrameShadow(QFrame.Shadow.Raised)

        horizontalLayout_15 = QHBoxLayout(searchOutputBtnsFrame)
        horizontalLayout_15.setSpacing(16)
        horizontalLayout_15.setContentsMargins(0, 0, 0, 0)

        # Favorite button
        favoriteBtn = QToolButton(searchOutputBtnsFrame)
        favoriteBtn.setObjectName("favoriteBtn")
        favoriteBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        favoriteBtn.setIcon(QIcon(":/icons/icons/heart.svg"))
        favoriteBtn.setIconSize(QSize(20, 20))
        horizontalLayout_15.addWidget(favoriteBtn)

        # Magnet link button
        magnetLinkBtn = QPushButton(searchOutputBtnsFrame)
        magnetLinkBtn.setObjectName("magnetLinkBtn")
        magnetLinkBtn.setMinimumSize(QSize(58, 0))
        magnetLinkBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        magnetLinkBtn.setIcon(QIcon(":/icons/icons/cil-link.png"))
        magnetLinkBtn.setIconSize(QSize(12, 12))
        magnetLinkBtn.setText("Magnet")
        horizontalLayout_15.addWidget(magnetLinkBtn)

        # Download button
        downloadBtn = QPushButton(searchOutputBtnsFrame)
        downloadBtn.setObjectName("downloadBtn")
        downloadBtn.setMinimumSize(QSize(68, 0))
        downloadBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        downloadBtn.setIcon(QIcon(":/icons/icons/download.png"))
        downloadBtn.setIconSize(QSize(12, 12))
        downloadBtn.setText("Download")
        horizontalLayout_15.addWidget(downloadBtn)

        # URL button
        urlBtn = QPushButton(searchOutputBtnsFrame)
        urlBtn.setObjectName("urlBtn")
        urlBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        urlBtn.setIcon(QIcon(":/icons/icons/cil-link-alt.png"))
        urlBtn.setIconSize(QSize(12, 12))
        urlBtn.setText("Page URL")
        horizontalLayout_15.addWidget(urlBtn)

        # Verified button (only if 'trusted' is True)
        if result.get('trusted', False):
            verifiedBtn = QPushButton(searchOutputBtnsFrame)
            verifiedBtn.setObjectName("verifiedBtn")
            verifiedBtn.setMinimumSize(QSize(0, 0))
            verifiedBtn.setIcon(QIcon(":/icons/icons/cil-check-alt.png"))
            verifiedBtn.setIconSize(QSize(12, 12))
            verifiedBtn.setText("Verified")
            horizontalLayout_15.addWidget(verifiedBtn)

        verticalLayout_14.addWidget(searchOutputBtnsFrame, 0, Qt.AlignmentFlag.AlignLeft)

        # Add the result tile to the main layout
        layout.addWidget(searchOutputFrame)

        # Connect buttons to their handlers
        favoriteBtn.clicked.connect(lambda _, res=result: self.add2favorite(res))
        downloadBtn.clicked.connect(lambda _, res=result: self.startDownload(res))
        magnetLinkBtn.clicked.connect(lambda _, res=result: self.handleMagnetLink(res))
        # magnetLinkBtn.installEventFilter(self)
        # magnetLinkBtn.result = result  # Store result for event filter
        urlBtn.clicked.connect(lambda _, res=result: self.openUrl(res.get('url')))

        # Handle verified button if present
        if result.get('trusted', False):
            verifiedBtn.clicked.connect(lambda: self.onVerifiedBtnClicked())

        # Return the frame if needed
        return searchOutputFrame
    
    def add2favorite(self, result):
        print(f"Added to favorites: {result['name']}")
        self.temporaryLog("Torrent Added to Favorites", 1500)
    
    def startDownload(self, result):
        print(f"Starting download for: {result['magnet']}")

    def handleMagnetLink(self, result):
        if self.click_timer.isActive():
            self.click_timer.stop()
            self.temporaryLog("Magnet Link Copied to Clipboard!", 1500)
            self.copyToClipboard(result.get('magnet'))
        else:
            self.magnet_link = result.get('magnet')
            self.click_timer.start(350)

    def openDefaultMagnet(self):
        self.openUrl(self.magnet_link, "Redirecting Magnet Link...", 3000)
    
    def openUrl(self, url, text="Opening Website...", timeout=3000):
        if url:
            self.temporaryLog(text, timeout)
            webbrowser.open(url)
    
    def copyToClipboard(self, text):
        clipboard = QApplication.clipboard()
        clipboard.setText(text)

    def temporaryLog(self, text, duration):
        old_text = self.ui.logLabel.text()
        self.ui.logLabel.setText(text)
        QTimer.singleShot(duration, lambda: self.ui.logLabel.setText(old_text))

    def showSearchResult(self, status: int, results: list, comment: str):
        if status == 1:
            results = [result for result in results if 'magnet' in result]
            self.clearTorrentResults()
            if results:
                for result in results:
                    self.createResultTile(result, self.ui.scrollAreaContents, self.ui.verticalLayout_13)
                self.dots_timer.stop()
                self.ui.logLabel.setText(f"{len(results)} Results Found.")
                endOfSearchBtn = QPushButton(self.ui.scrollAreaContents)
                endOfSearchBtn.setObjectName(u"endOfSearchBtn")
                endOfSearchBtn.setMinimumSize(QSize(0, 100))
                endOfSearchBtn.setText("No More Results!")
                self.ui.verticalLayout_13.addWidget(endOfSearchBtn)  
                verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
                self.ui.verticalLayout_13.addItem(verticalSpacer)
            else:
                self.dots_timer.stop()
                self.ui.logLabel.setText("No result found!")
                endOfSearchBtn = QPushButton(self.ui.scrollAreaContents)
                endOfSearchBtn.setObjectName(u"endOfSearchBtn")
                endOfSearchBtn.setMinimumSize(QSize(0, 100))
                endOfSearchBtn.setText("No More Results!")
                self.ui.verticalLayout_13.addWidget(endOfSearchBtn)  
        else:
            self.dots_timer.stop()
            self.ui.logLabel.setText("Search Failed!")
            self.pushNotification(f"Search failed due to some unexpected errors, this error is from torrent search API. More info: {comment}", "Search Failed")
    
    def searchTorrents(self):
        query = self.ui.searchInputText.text()
        if self.internet_connection:
            if self.torrent_engine_active: 
                if query:
                    self.dots_timer.start(500)
                    self.ui.logLabel.setText("Searching")
                    self.search_thread.start_search(query=query, sort="MAX_SEED", include_nsfw=True)
                else: self.pushNotification("Query can't be blank or less than 3 letter, please enter a query before hitting the search button", "Blank Query")
            else: 
                self.initSearchThread()
                self.pushNotification("Due to network error, torrent engine was left uninitialized while initializing the application. Trying to reinitialize torrent engine, retry with your query!", "Uninitialized Torrent Engine")
        else:
            self.pushNotification("No internet connection available! What do you expect?", "No Internet")

    def closeEvent(self, event):
        self.hide()
        if self.torrent_engine_active: self.search_thread.stop()
        self.network_monitor.stop()
        self.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
