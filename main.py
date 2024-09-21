import sys
import os
import platform
import math
import webbrowser

from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QTimer
from PySide6.QtWidgets import QGraphicsOpacityEffect
from searchthread import SearchThread
from networkthread import AppNetworkMonitor
from favoritethread import FavoriteTorrent
from historythread import HistoryManager
from filethread import FileWatcher
from datetime import datetime

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

        self.initNetworkMonitor()
        self.initFavorites()
        self.initHistory()
        self.initFileWatcher("C:\\Users\\morph\\Downloads", 0)

        self.video_formats = [".webm", ".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", "mpeg", ".3gp", ".mts", ".ts", ".vob"]
        self.audio_formats = [".mp3", ".wav", ".aac", ".m4a", ".flac", ".ogg", ".wma"]

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
        self.ui.filesReloadBtn.clicked.connect(self.reloadFiles)
        self.ui.notificationBtn.clicked.connect(
            lambda: self.pushNotification("Hello"))
        self.ui.closeNotificationBtn.clicked.connect(self.hideNotificationTab)

        self.ui.searchBtn.clicked.connect(self.searchTorrents)
        QTimer.singleShot(3000, self.stopInitAnimation)

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

    def stopInitAnimation(self):
        self.ui.initGif.stop()
        self.ui.mainStack.setCurrentIndex(0)

    def initFileWatcher(self, directory, depth):
        self.file_watcher = FileWatcher(directory, depth)
        self.file_watcher.files_updated.connect(self.updateFiles)
        self.file_watcher.start()

    def reloadFiles(self):
        self.file_watcher.rescan()
        self.pushNotification("Refreshed files for the selected directory with selected depth.", "Files Refreshed")

    def updateFiles(self, files):
        self.clearFilesTiles()
        if files:
            for file in files:
                self.createFileTile(file)
            endOfFileBtn = QPushButton(self.ui.filesScrollAreaContents)
            endOfFileBtn.setObjectName(u"endOfFileBtn")
            endOfFileBtn.setMinimumSize(QSize(0, 100))
            endOfFileBtn.setText(f"End of {len(files)} Files.")
            self.ui.verticalLayout_22.addWidget(endOfFileBtn)  
            verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
            self.ui.verticalLayout_22.addItem(verticalSpacer)
        else:
            endOfFileBtn = QPushButton(self.ui.filesScrollAreaContents)
            endOfFileBtn.setObjectName(u"endOfFileBtn")
            endOfFileBtn.setMinimumSize(QSize(0, 100))
            endOfFileBtn.setText("So Poor Over Here!")
            self.ui.verticalLayout_22.addWidget(endOfFileBtn)

    def convert_size(self, size_bytes):
        size_bytes = int(size_bytes)
        if size_bytes == 0:
            return "0 B"
        size_name = ("B", "KB", "MB", "GB", "TB",
                        "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_name[i]}"

    def createFileTile(self, file):
        # Create main file frame
        eachFileFrame = QFrame(self.ui.filesScrollAreaContents)
        eachFileFrame.setObjectName(u"eachFileFrame")
        eachFileFrame.setMinimumSize(QSize(0, 112))
        eachFileFrame.setFrameShape(QFrame.Shape.StyledPanel)
        eachFileFrame.setFrameShadow(QFrame.Shadow.Raised)

        # Layout for file frame
        verticalLayout_25 = QVBoxLayout(eachFileFrame)
        verticalLayout_25.setObjectName(u"verticalLayout_25")

        # File name label
        fileNameLabel = QLabel(eachFileFrame)
        fileNameLabel.setObjectName(u"fileNameLabel")
        fileNameLabel.setMinimumSize(QSize(0, 22))
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setBold(True)
        fileNameLabel.setFont(font)
        fileNameLabel.setText(os.path.splitext(file.get('name', 'N/A'))[0])
        verticalLayout_25.addWidget(fileNameLabel)

        # File info frame
        filesInfoFrame2 = QFrame(eachFileFrame)
        filesInfoFrame2.setObjectName(u"filesInfoFrame2")
        filesInfoFrame2.setMaximumSize(QSize(16777215, 22))
        filesInfoFrame2.setFrameShape(QFrame.Shape.StyledPanel)
        filesInfoFrame2.setFrameShadow(QFrame.Shadow.Raised)

        # Layout for file info
        horizontalLayout_21 = QHBoxLayout(filesInfoFrame2)
        horizontalLayout_21.setSpacing(0)
        horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        horizontalLayout_21.setContentsMargins(39, 0, 0, 0)

        # File size label
        fileSizeLabel = QLabel(filesInfoFrame2)
        fileSizeLabel.setObjectName(u"fileSizeLabel")
        fileSizeLabel.setText(f"Size: {self.convert_size(file.get('size', '0'))}")
        horizontalLayout_21.addWidget(fileSizeLabel)

        # File extension label
        fileExtensionLabel = QLabel(filesInfoFrame2)
        fileExtensionLabel.setObjectName(u"fileExtensionLabel")
        fileExtensionLabel.setText(f"Extension: {file.get('type', 'unknown')}")
        horizontalLayout_21.addWidget(fileExtensionLabel)

        verticalLayout_25.addWidget(filesInfoFrame2)

        # File buttons frame
        fileInfoBtnFrame = QFrame(eachFileFrame)
        fileInfoBtnFrame.setObjectName(u"fileInfoBtnFrame")
        fileInfoBtnFrame.setFrameShape(QFrame.Shape.StyledPanel)
        fileInfoBtnFrame.setFrameShadow(QFrame.Shadow.Raised)

        # Layout for buttons
        horizontalLayout_23 = QHBoxLayout(fileInfoBtnFrame)
        horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        horizontalLayout_23.setContentsMargins(0, 0, 0, 0)

        # Play file button
        playFileBtn = QPushButton(fileInfoBtnFrame)
        playFileBtn.setObjectName(u"playFileBtn")
        playFileBtn.setMaximumSize(QSize(32, 16777215))
        playFileBtn.setFont(QFont(u"Segoe UI", weight=QFont.Normal))
        icon21 = QIcon()
        icon21.addFile(u":/icons/icons/play.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        # icon21.addFile(u":/icons/icons/help-circle.svg", QSize(), QIcon.Mode.Disabled, QIcon.State.Off)
        playFileBtn.setIcon(icon21)
        playFileBtn.setIconSize(QSize(32, 32))
        horizontalLayout_23.addWidget(playFileBtn)
        

        # File additional info frame
        fileInfoFrame2 = QFrame(fileInfoBtnFrame)
        fileInfoFrame2.setObjectName(u"fileInfoFrame2")
        fileInfoFrame2.setMaximumSize(QSize(16777215, 22))
        fileInfoFrame2.setFrameShape(QFrame.Shape.StyledPanel)
        fileInfoFrame2.setFrameShadow(QFrame.Shadow.Raised)

        # Layout for file additional info
        horizontalLayout_22 = QHBoxLayout(fileInfoFrame2)
        horizontalLayout_22.setSpacing(0)
        horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        horizontalLayout_22.setContentsMargins(0, 0, 0, 0)

        # Media Type
        file_type = file.get('type', 'unknown')
        if file_type in self.audio_formats: file['type'], files_type = "Audio", 1
        elif file_type in self.video_formats: file['type'], files_type = "Video", 2
        else: 
            file['type'], files_type = f"{file['type'][1:].upper()} File", 0
            playFileBtn.setIcon(QIcon(":/icons/icons/file.svg"))

        # File type label
        fileTypeLabel = QLabel(fileInfoFrame2)
        fileTypeLabel.setObjectName(u"fileTypeLabel")
        fileTypeLabel.setText(f"Type: {file['type']}")
        horizontalLayout_22.addWidget(fileTypeLabel)

        # File modified date label
        fileModifiedLabel = QLabel(fileInfoFrame2)
        fileModifiedLabel.setObjectName(u"fileModifiedLabel")
        fileModifiedLabel.setText(f"Last Modified: {file.get('modified_time', 'Unknown')}")
        horizontalLayout_22.addWidget(fileModifiedLabel)
        horizontalLayout_23.addWidget(fileInfoFrame2)
        verticalLayout_25.addWidget(fileInfoBtnFrame)
        # Add the complete file frame to the parent layout
        self.ui.verticalLayout_22.addWidget(eachFileFrame)

        playFileBtn.clicked.connect(lambda _, file=file, files_type=files_type: self.playFromFileBtn(file, files_type))
    
    def playFromFileBtn(self, file, type):
        if not type: self.openFile(file.get('path'))
        else: 
            print("Media Files")
            self.openFile(file.get('path'))

    def openFile(self, path):
        system = platform.system()
        if system == 'Windows': os.startfile(path)
        elif system == 'Darwin': os.system(f'open "{path}"')
        else: os.system(f'xdg-open "{path}"')

    def clearFilesTiles(self):
        while self.ui.verticalLayout_22.count():
            item = self.ui.verticalLayout_22.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

    def initHistory(self):
        self.history_thread = HistoryManager()
        self.history_thread.historyListChanged.connect(self.updateHistory)
        self.history_thread.start()

    def clearHistoryTiles(self):
        while self.ui.verticalLayout_33.count():
            item = self.ui.verticalLayout_33.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

    def createHistoryTile(self, result, parent_widget, layout):
        # Create main frame for the history item
        historyItemFrame = QFrame(parent_widget)
        historyItemFrame.setObjectName("historyItemFrame")
        historyItemFrame.setMinimumSize(QSize(0, 112))
        historyItemFrame.setFrameShape(QFrame.Shape.StyledPanel)
        historyItemFrame.setFrameShadow(QFrame.Shadow.Raised)

        # Create vertical layout for the frame
        verticalLayout = QVBoxLayout(historyItemFrame)
        verticalLayout.setSpacing(4)
        verticalLayout.setContentsMargins(-1, -1, -1, 9)

        # History name label
        historyNameLabel = QLabel(historyItemFrame)
        historyNameLabel.setObjectName("historyNameLabel")
        historyNameLabel.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        historyNameLabel.setText(result.get('name', 'N/A'))
        verticalLayout.addWidget(historyNameLabel)

        # Info Frame 1 (Seeders, Leechers, Size, Path)
        infoFrame1 = QFrame(historyItemFrame)
        infoFrame1.setMinimumSize(QSize(0, 22))
        infoFrame1.setFrameShape(QFrame.Shape.StyledPanel)
        infoFrame1.setFrameShadow(QFrame.Shadow.Raised)

        infoLayout1 = QHBoxLayout(infoFrame1)
        infoLayout1.setSpacing(16)
        infoLayout1.setContentsMargins(0, 0, 0, 0)

        # Add Seeder label
        historySeederLabel = QLabel(infoFrame1)
        historySeederLabel.setMinimumSize(QSize(72, 0))
        historySeederLabel.setText(f"Seeders: {result.get('seeder', 'N/A')}")
        infoLayout1.addWidget(historySeederLabel)

        # Add Leecher label
        historyLeecherLabel = QLabel(infoFrame1)
        historyLeecherLabel.setMinimumSize(QSize(72, 0))
        historyLeecherLabel.setText(f"Leechers: {result.get('leecher', 'N/A')}")
        infoLayout1.addWidget(historyLeecherLabel)

        # Add Size label
        historySizeLabel = QLabel(infoFrame1)
        historySizeLabel.setMinimumSize(QSize(82, 0))
        historySizeLabel.setText(f"Size: {result.get('size', 'N/A')}")
        infoLayout1.addWidget(historySizeLabel)

        # Add Path label
        historyPathLabel = QLabel(infoFrame1)
        historyPathLabel.setText(result.get('path', 'N/A'))
        infoLayout1.addWidget(historyPathLabel)

        verticalLayout.addWidget(infoFrame1, 0, Qt.AlignmentFlag.AlignLeft)

        # Info Frame 2 (NSFW, Elapsed, Timestamp)
        infoFrame2 = QFrame(historyItemFrame)
        infoFrame2.setMinimumSize(QSize(0, 22))
        infoFrame2.setFrameShape(QFrame.Shape.StyledPanel)
        infoFrame2.setFrameShadow(QFrame.Shadow.Raised)

        infoLayout2 = QHBoxLayout(infoFrame2)
        infoLayout2.setSpacing(16)
        infoLayout2.setContentsMargins(0, 0, 0, 0)

        # Add NSFW label
        historyNsfwLabel = QLabel(infoFrame2)
        nsfwText = "NSFW" if result.get('nsfw', False) else "SAFE"
        historyNsfwLabel.setText(nsfwText)
        infoLayout2.addWidget(historyNsfwLabel)

        # Add Elapsed time label
        historyElapsedLabel = QLabel(infoFrame2)
        historyElapsedLabel.setMinimumSize(QSize(36, 0))
        historyElapsedLabel.setText(f"Elapsed: {result.get('elapsed', 'N/A')}")
        infoLayout2.addWidget(historyElapsedLabel)

        # Add Timestamp label
        historyTimestampLabel = QLabel(infoFrame2)
        historyTimestampLabel.setText(f"Time: {result.get('timestamp', 'N/A')}")
        infoLayout2.addWidget(historyTimestampLabel)

        verticalLayout.addWidget(infoFrame2, 0, Qt.AlignmentFlag.AlignLeft)

        # Buttons Frame (Delete, Magnet link)
        btnsFrame = QFrame(historyItemFrame)
        btnsFrame.setMinimumSize(QSize(0, 22))
        btnsFrame.setFrameShape(QFrame.Shape.StyledPanel)
        btnsFrame.setFrameShadow(QFrame.Shadow.Raised)

        btnsLayout = QHBoxLayout(btnsFrame)
        btnsLayout.setSpacing(32)
        btnsLayout.setContentsMargins(0, 0, 0, 0)

        # Delete button
        deleteHistoryBtn = QToolButton(btnsFrame)
        deleteHistoryBtn.setObjectName("deleteHistoryBtn")
        deleteHistoryBtn.setMinimumSize(QSize(22, 22))
        deleteHistoryBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        deleteHistoryBtn.setIcon(QIcon(":/icons/icons/trash-2.svg"))
        deleteHistoryBtn.setIconSize(QSize(20, 20))
        btnsLayout.addWidget(deleteHistoryBtn)

        # Magnet link button
        historyLinkBtn = QPushButton(btnsFrame)
        historyLinkBtn.setObjectName("historyLinkBtn")
        historyLinkBtn.setMinimumSize(QSize(58, 0))
        historyLinkBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        historyLinkBtn.setIcon(QIcon(":/icons/icons/cil-link.png"))
        historyLinkBtn.setIconSize(QSize(12, 12))
        historyLinkBtn.setText("Magnet")
        btnsLayout.addWidget(historyLinkBtn)

        verticalLayout.addWidget(btnsFrame, 0, Qt.AlignmentFlag.AlignLeft)

        # Add history item frame to the main layout
        layout.addWidget(historyItemFrame)

        # Connect button actions
        deleteHistoryBtn.clicked.connect(lambda _, res=result: self.removeHistory(res))
        historyLinkBtn.clicked.connect(lambda _, res=result: self.handleMagnetLink(res))

        return historyItemFrame

    def removeHistory(self, history):
        self.history_thread.remove_history(history['index'])

    def updateHistory(self, histories):
        self.clearHistoryTiles()
        if histories:
            for history in reversed(histories):
                self.createHistoryTile(history, self.ui.historyScrollAreaWidgetContents, self.ui.verticalLayout_33)
            endOfHistoryBtn = QPushButton(self.ui.historyScrollAreaWidgetContents)
            endOfHistoryBtn.setObjectName(u"endOfHistoryBtn")
            endOfHistoryBtn.setMinimumSize(QSize(0, 100))
            endOfHistoryBtn.setText(f"End of {len(histories)} History Items.")
            self.ui.verticalLayout_33.addWidget(endOfHistoryBtn)  
            verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
            self.ui.verticalLayout_33.addItem(verticalSpacer)
        else:
            endOfHistoryBtn = QPushButton(self.ui.historyScrollAreaWidgetContents)
            endOfHistoryBtn.setObjectName(u"endOfHistoryBtn")
            endOfHistoryBtn.setMinimumSize(QSize(0, 100))
            endOfHistoryBtn.setText("Looks Like You Don't Create Histories!")
            self.ui.verticalLayout_33.addWidget(endOfHistoryBtn)

    def timeNow(self):
        # print(datetime.now().strftime("%H:%M:%S %d/%m/%Y"))
        return datetime.now().strftime("%H:%M:%S %d/%m/%Y")

    def initFavorites(self):
        self.favorite_torrents = FavoriteTorrent()
        self.favorite_torrents.favoriteListChanged.connect(self.updateFavoriteTorrents)
        self.favorite_torrents.torrentExists.connect(self.favoriteExists)
        self.favorite_torrents.start()

    def favoriteExists(self, exists):
        if exists: 
            self.temporaryLog("Already Exist in Favorites", 1500)
        else: 
            self.temporaryLog(f"Added! Total Fav Count: {len(self.favorites_items)+1}", 1500)

    def clearFavTorrents(self):
        while self.ui.verticalLayout_29.count():
            item = self.ui.verticalLayout_29.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

    def createFavTile(self, result, parent_widget, layout):
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

        # Remove Favorite button
        removeFavoriteBtn = QToolButton(searchOutputBtnsFrame)
        removeFavoriteBtn.setObjectName("removeFavoriteBtn")
        removeFavoriteBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        removeFavoriteBtn.setIcon(QIcon(":/icons/icons/trash-2.svg"))
        removeFavoriteBtn.setIconSize(QSize(20, 20))
        horizontalLayout_15.addWidget(removeFavoriteBtn)

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
        removeFavoriteBtn.clicked.connect(lambda _, res=result: self.removeFavorite(res))
        downloadBtn.clicked.connect(lambda _, res=result: self.startDownload(res))
        magnetLinkBtn.clicked.connect(lambda _, res=result: self.handleMagnetLink(res))
        urlBtn.clicked.connect(lambda _, res=result: self.openUrl(res.get('url')))

        # Handle verified button if present
        if result.get('trusted', False):
            verifiedBtn.clicked.connect(lambda: self.onVerifiedBtnClicked())

        # Return the frame if needed
        return searchOutputFrame
    
    def removeFavorite(self, result):
        self.favorite_torrents.remove_favorite(result['magnet'])
        self.temporaryLog("Removed from the Favorites", 1500)
    
    def updateFavoriteTorrents(self, favorite_list):
        self.favorites_items = favorite_list
        self.clearFavTorrents()
        if favorite_list:
            for result in favorite_list:
                self.createFavTile(result, self.ui.favoritesScrollAreaWidgetContents, self.ui.verticalLayout_29)
            endOfFavoritesBtn = QPushButton(self.ui.favoritesScrollAreaWidgetContents)
            endOfFavoritesBtn.setObjectName(u"endOfFavoritesBtn")
            endOfFavoritesBtn.setMinimumSize(QSize(0, 100))
            endOfFavoritesBtn.setText(f"End of {len(favorite_list)} Favorite Items.")
            self.ui.verticalLayout_29.addWidget(endOfFavoritesBtn)  
            verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
            self.ui.verticalLayout_29.addItem(verticalSpacer)
        else:
            endOfFavoritesBtn = QPushButton(self.ui.favoritesScrollAreaWidgetContents)
            endOfFavoritesBtn.setObjectName(u"endOfFavoritesBtn")
            endOfFavoritesBtn.setMinimumSize(QSize(0, 100))
            endOfFavoritesBtn.setText("Add Items to Favorite First!")
            self.ui.verticalLayout_29.addWidget(endOfFavoritesBtn)  
    
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
        self.favorite_torrents.add_favorite(result)
    
    def startDownload(self, result):
        # print(f"Starting download for: {result['magnet']}")
        self.history_thread.add_history({
            "leecher": result['leecher'],
            "magnet": result['magnet'],
            "name": result['name'],
            "nsfw": result['nsfw'],
            "seeder": result['seeder'],
            "size": result['size'],
            "path": "N/A",
            "timestamp": self.timeNow(),
            "elapsed": "N/A"
        })

    def handleMagnetLink(self, result):
        if self.click_timer.isActive():
            self.click_timer.stop()
            self.temporaryLog("Magnet Link Copied to Clipboard!", 1500)
            self.copyToClipboard(result.get('magnet'))
        else:
            self.magnet_link = result.get('magnet')
            self.click_timer.start(350)

        self.history_thread.add_history({
            "leecher": result['leecher'],
            "magnet": result['magnet'],
            "name": result['name'],
            "nsfw": result['nsfw'],
            "seeder": result['seeder'],
            "size": result['size'],
            "path": "N/A",
            "timestamp": self.timeNow(),
            "elapsed": "N/A"
        })

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
                endOfSearchBtn.setText("Try Something More Relevant!")
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
        self.favorite_torrents.stop()
        self.history_thread.stop()
        self.file_watcher.stop()
        self.close()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
