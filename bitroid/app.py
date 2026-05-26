import sys
import os
import platform
import math
import subprocess
import webbrowser
import random
import shutil
from pathlib import Path

from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QTimer, QFileSystemWatcher, QUrl, QEvent
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWidgets import (
    QDialog,
    QFileDialog,
    QFormLayout,
    QGraphicsOpacityEffect,
    QMenu,
)
from bitroid.core.paths import app_data_dir, user_files_root
from bitroid.core.settings import AppSettings
from bitroid.features.search.search_thread import SearchThread
from bitroid.services.network import InternetChecker
from bitroid.services.favorites import FavoriteTorrent
from bitroid.services.history import HistoryManager
from datetime import datetime
from bitroid.platform.window_chrome import enable_native_window_shadow

from bitroid.ui.interface import *


class ElidedLabel(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(parent)
        self._full_text = ""
        self.setMinimumWidth(0)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.setText(text)

    def setText(self, text):
        self._full_text = str(text)
        self.setToolTip(self._full_text)
        self.updateElidedText()

    def fullText(self):
        return self._full_text

    def updateElidedText(self):
        available_width = max(0, self.width() - 4)
        if available_width <= 0:
            QLabel.setText(self, self._full_text)
            return
        elided = self.fontMetrics().elidedText(
            self._full_text,
            Qt.TextElideMode.ElideRight,
            available_width,
        )
        QLabel.setText(self, elided)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateElidedText()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.sidebar_visible_min = 45
        self.sidebar_visible_max = 150
        self.sidebar_visible = True
        self.mediaplayer_visible = True
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon(u":/icons/icons/activity.svg"))
        self.setMouseTracking(True)
        self.setAcceptDrops(True)
        self.ui.centralwidget.setMouseTracking(True)
        self.ui.headerContainer.setMouseTracking(True)
        self.show()
        QTimer.singleShot(0, lambda: enable_native_window_shadow(self))

        self.animation_time = 80
        self.allow_notification = True
        self.label_timeout = 2500
        self.dark_theme = True
        self.include_nsfw = False
        self.data_dir = app_data_dir()
        self.settings = AppSettings(self.data_dir / "settings.json")

        self.edge_margin = 8
        self.resizing = False
        self.dragging = False
        self.resize_edges = None
        self.resize_start_geometry = None
        self.resize_position = None
        self.drag_position = None
        self._cursor_shape = Qt.ArrowCursor
        self.refresh_api_timeout = 30000

        self.internet_connection = False
        self.torrent_engine_active = False
        self.current_directory = Path(self.settings.get("file_manager", "current_dir", str(user_files_root()))).expanduser()
        if not self.current_directory.is_dir():
            self.current_directory = user_files_root()
        self.file_back_stack = []
        self.file_forward_stack = []
        self.file_items = []
        self.file_clipboard_paths = []
        self.file_system_watcher = QFileSystemWatcher(self)
        self.file_refresh_timer = QTimer(self)
        self.file_refresh_timer.setSingleShot(True)
        self.file_refresh_timer.timeout.connect(lambda: self.loadDirectory(self.current_directory, remember=False))
        self.media_playlist = []
        self.media_current_index = -1
        self.media_duration = 0
        self.media_repeat_mode = self.settings.get("media_player", "repeat_mode", "off")
        self.media_shuffle = bool(self.settings.get("media_player", "shuffle", False))
        self.player_locked = False
        self._updating_media_slider = False

        self.initNetworkMonitor()
        self.initFavorites(self.data_dir / "favourites.json")
        self.initHistory(self.data_dir / "history.json")

        self.video_formats = [".webm", ".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", "mpeg", ".3gp", ".mts", ".ts", ".vob"]
        self.audio_formats = [".mp3", ".wav", ".aac", ".m4a", ".flac", ".ogg", ".wma"]
        self.initMediaPlayer()
        self.initFileManager()

        self.sideBarAnimation = QPropertyAnimation(
            self.ui.leftMenuBar, b"minimumWidth")
        self.sideBarAnimation.setDuration(self.animation_time)
        self.sideBarAnimation.setEasingCurve(QEasingCurve.InOutExpo)

        self.opacityEffect = QGraphicsOpacityEffect()
        self.ui.notificationWidget.setGraphicsEffect(self.opacityEffect)
        self.opacityEffect.setOpacity(0)
        self.ui.notificationWidget.hide()

        self.notificationAnimation = QPropertyAnimation(self.opacityEffect, b"opacity")
        self.notificationAnimation.setDuration(int(2 * self.animation_time))
        self.notificationAnimation.setEasingCurve(QEasingCurve.InOutSine)

        self.mediaPlayerAnimation = QPropertyAnimation(
            self.ui.mediaPlayerWidget, b"maximumHeight")
        self.mediaPlayerAnimation.setDuration(int(1 * self.animation_time))
        self.mediaPlayerAnimation.setEasingCurve(QEasingCurve.InOutSine)
        if not bool(self.settings.get("media_player", "visible", True)):
            self.ui.mediaPlayerWidget.setMaximumHeight(0)
            self.ui.mediaPlayerShowBtn.setChecked(False)
            self.mediaplayer_visible = False

        self.dots = ""
        self.dots_timer = QTimer(self)
        self.dots_timer.timeout.connect(self.updateDots)

        self.click_timer = QTimer(self)
        self.click_timer.setSingleShot(True)
        self.click_timer.timeout.connect(self.openDefaultMagnet)

        self.notification_timer = QTimer(self)
        self.notification_timer.setSingleShot(True)
        self.notification_timer.timeout.connect(self.hideNotificationTab)

        self.search_api_refresh_timer = QTimer(self)
        self.search_api_refresh_timer.timeout.connect(self.refreshSearchApi)
        # self.search_api_refresh_timer.start(self.refresh_api_timeout)

        self.ui.appCloseBtn.clicked.connect(lambda: self.close())
        self.ui.appMinBtn.clicked.connect(self.setMinimized)
        self.ui.appMaxBtn.clicked.connect(self.toggleMaximized)
        self.ui.themeBtn.clicked.connect(self.toggleTheme)
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
        self.ui.filesBackBtn.clicked.connect(self.goBackDirectory)
        self.ui.filesForwardBtn.clicked.connect(self.goForwardDirectory)
        self.ui.filesUpBtn.clicked.connect(self.goUpDirectory)
        self.ui.filesHomeBtn.clicked.connect(self.goHomeDirectory)
        self.ui.filesPathInput.returnPressed.connect(self.openPathFromInput)
        self.ui.filesSortComboBox.currentTextChanged.connect(self.changeFileSort)
        self.ui.notificationBtn.clicked.connect(
            lambda: self.pushNotification("Hello"))
        self.ui.closeNotificationBtn.clicked.connect(self.hideNotificationTab)
        self.ui.searchBtn.clicked.connect(self.searchTorrents)
        self.ui.qSettingNsfwBtn.clicked.connect(self.toggleNsfw)
        self.updateNsfwButton()
        QTimer.singleShot(self.label_timeout, self.stopLoadingAnimation)

    def toggleMaximized(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def setMinimized(self):
        self.showMinimized()

    def toggleNsfw(self):
        self.include_nsfw = not self.include_nsfw
        self.updateNsfwButton()
        self.pushNotification(
            f"NSFW search results are now {'enabled' if self.include_nsfw else 'disabled'}.",
            "Search Filter",
        )

    def updateNsfwButton(self):
        self.ui.qSettingNsfwBtn.setText("Enabled" if self.include_nsfw else "Disabled")

    def toggleTheme(self):
        if self.dark_theme :
            self.ui.themeBtn.setIcon(QIcon(':/icons/icons/cil-moon.png'))
            self.pushNotification("Theme changed to 'Retro' for the Bitroid DM", "Retro Theme")
            self.setStyleSheet(styles_retro)
            self.dark_theme = False
        else:
            self.ui.themeBtn.setIcon(QIcon(':/icons/icons/cil-lightbulb.png'))
            self.pushNotification("Theme changed to 'Default' for the Bitroid DM", "Default Theme")
            self.setStyleSheet(styles_default)
            self.dark_theme = True

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
            self.settings.set("media_player", "visible", True)

    def hideMediaPlayer(self):
        if self.mediaplayer_visible:
            self.mediaPlayerAnimation.setStartValue(
                self.ui.mediaPlayerWidget.height())
            self.mediaPlayerAnimation.setEndValue(0)
            self.mediaPlayerAnimation.start()
            self.ui.mediaPlayerWidget.setMaximumHeight(0)
            self.mediaplayer_visible = False
            self.settings.set("media_player", "visible", False)

    def toggleMediaPlayer(self):
        if self.ui.mediaPlayerShowBtn.isChecked():
            self.showMediaPlayer()
        else:
            self.hideMediaPlayer()

    def pushNotification(self, notification_message, notification_title='Notification', notification_volume=25, tone=True):
        if self.notification_timer.isActive():
            self.notificationAnimation.stop()
            self.ui.notificationWidget.hide()
            self.notification_timer.stop()

        if self.allow_notification:
            if tone:
                pass
            self.ui.notificationWidget.show()
            self.notificationAnimation.setStartValue(self.opacityEffect.opacity())
            self.notificationAnimation.setEndValue(1)
            self.notificationAnimation.start()
            if notification_title: self.ui.notificationTitleLabel.setText(notification_title)
            else: self.ui.notificationTitleLabel.hide()
            self.ui.notificationTextLabel.setText(notification_message)
            self.notification_timer.start(int(2 * self.label_timeout))

    def hideNotificationTab(self):
        self.notificationAnimation.setStartValue(self.opacityEffect.opacity())
        self.notificationAnimation.setEndValue(0)
        self.notificationAnimation.start()
        # self.ui.notificationLabel.setText("")
        QTimer.singleShot(int(2 * self.animation_time),
                          lambda: self.ui.notificationWidget.hide())

    def _resize_edges_at(self, position):
        if self.isMaximized():
            return None

        rect = self.rect()
        x = int(position.x())
        y = int(position.y())
        margin = self.edge_margin
        edges = {
            "left": x <= margin,
            "right": x >= rect.width() - margin,
            "top": y <= margin,
            "bottom": y >= rect.height() - margin,
        }
        return edges if any(edges.values()) else None

    def _cursor_for_edges(self, edges):
        if not edges:
            return Qt.ArrowCursor
        if (edges["left"] and edges["top"]) or (edges["right"] and edges["bottom"]):
            return Qt.SizeFDiagCursor
        if (edges["right"] and edges["top"]) or (edges["left"] and edges["bottom"]):
            return Qt.SizeBDiagCursor
        if edges["left"] or edges["right"]:
            return Qt.SizeHorCursor
        return Qt.SizeVerCursor

    def _set_cursor_once(self, cursor_shape):
        if self._cursor_shape == cursor_shape:
            return
        self._cursor_shape = cursor_shape
        if cursor_shape == Qt.ArrowCursor:
            self.unsetCursor()
        else:
            self.setCursor(cursor_shape)

    def _is_interactive_widget(self, widget):
        while widget is not None and widget is not self:
            if isinstance(widget, (QPushButton, QToolButton, QLineEdit, QComboBox, QSlider, QScrollArea)):
                return True
            widget = widget.parentWidget()
        return False

    def _is_titlebar_drag_area(self, position):
        header = self.ui.headerContainer
        top_left = header.mapTo(self, QPoint(0, 0))
        header_rect = QRect(top_left, header.size())
        if not header_rect.contains(position):
            return False

        child = self.childAt(position)
        return not self._is_interactive_widget(child)

    def _resize_from_edges(self, global_position):
        if not self.resize_edges or self.resize_start_geometry is None:
            return

        delta = global_position - self.resize_position
        geometry = QRect(self.resize_start_geometry)
        min_width = max(self.minimumWidth(), 100)
        min_height = max(self.minimumHeight(), 100)

        if self.resize_edges["left"]:
            geometry.setLeft(min(geometry.left() + delta.x(), geometry.right() - min_width))
        if self.resize_edges["right"]:
            geometry.setRight(max(geometry.right() + delta.x(), geometry.left() + min_width))
        if self.resize_edges["top"]:
            geometry.setTop(min(geometry.top() + delta.y(), geometry.bottom() - min_height))
        if self.resize_edges["bottom"]:
            geometry.setBottom(max(geometry.bottom() + delta.y(), geometry.top() + min_height))

        self.setGeometry(geometry)

    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton:
            super().mousePressEvent(event)
            return

        position = event.position().toPoint()
        edges = self._resize_edges_at(position)
        if edges:
            self.resizing = True
            self.dragging = False
            self.resize_edges = edges
            self.resize_position = event.globalPosition().toPoint()
            self.resize_start_geometry = QRect(self.geometry())
            event.accept()
            return

        if self._is_titlebar_drag_area(position):
            self.dragging = True
            self.resizing = False
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
            return

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        global_position = event.globalPosition().toPoint()

        if self.resizing:
            self._resize_from_edges(global_position)
            event.accept()
            return

        if self.dragging:
            self.move(global_position - self.drag_position)
            event.accept()
            return

        edges = self._resize_edges_at(event.position())
        self._set_cursor_once(self._cursor_for_edges(edges))
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.resizing = False
        self.dragging = False
        self.resize_edges = None
        self.resize_start_geometry = None
        self.resize_position = None
        self.drag_position = None
        self._set_cursor_once(self._cursor_for_edges(self._resize_edges_at(event.position())))
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton and self._is_titlebar_drag_area(event.position().toPoint()):
            self.toggleMaximized()
            event.accept()
            return
        super().mouseDoubleClickEvent(event)

    def leaveEvent(self, event):
        if not self.resizing and not self.dragging:
            self._set_cursor_once(Qt.ArrowCursor)
        super().leaveEvent(event)

    def keyPressEvent(self, event):
        if not self.ui.mainStack.currentIndex() and (event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter):
            self.ui.searchBtn.click() 

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dropEvent(self, event):
        handled = False
        for url in event.mimeData().urls():
            path = Path(url.toLocalFile())
            if path.is_dir():
                self.loadDirectory(path)
                handled = True
            elif path.is_file() and self.mediaKind(path.suffix.lower()):
                self.playMediaPath(path)
                handled = True
        if handled:
            event.acceptProposedAction()
        else:
            super().dropEvent(event)

    def stopLoadingAnimation(self,index=0):
        self.ui.initGif.stop()
        self.ui.mainStack.setCurrentIndex(index)

    def startLoadingAnimation(self):
        self.ui.initGif.start()
        self.ui.mainStack.setCurrentIndex(7)

    def initFileManager(self):
        saved_sort = self.settings.get("file_manager", "sort_by", "Name")
        index = self.ui.filesSortComboBox.findText(saved_sort)
        self.ui.filesSortComboBox.setCurrentIndex(max(index, 0))
        self.ui.filesPathInput.installEventFilter(self)
        self.ui.filesPathDropdownBtn.clicked.connect(self.showPathParentsMenu)
        self.file_system_watcher.directoryChanged.connect(
            lambda _: self.file_refresh_timer.start(250)
        )
        self.loadDirectory(self.current_directory, remember=False)

    def eventFilter(self, watched, event):
        if watched is self.ui.filesPathInput:
            if event.type() == QEvent.Type.FocusIn:
                self.showFullPathForEditing()
            elif event.type() == QEvent.Type.FocusOut:
                QTimer.singleShot(0, self.updateFilePathDisplay)
        return super().eventFilter(watched, event)

    def currentDirectoryDisplayName(self, directory=None):
        directory = Path(directory or self.current_directory)
        return directory.name or str(directory)

    def updateFilePathDisplay(self):
        display_text = self.currentDirectoryDisplayName()
        self.ui.filesPathInput.setText(display_text)
        self.ui.filesPathInput.setToolTip(str(self.current_directory))
        self.ui.filesPathDropdownBtn.setToolTip(str(self.current_directory))

    def showFullPathForEditing(self):
        self.ui.filesPathInput.setText(str(self.current_directory))
        self.ui.filesPathInput.selectAll()

    def showPathParentsMenu(self):
        parents = []
        path = self.current_directory
        while path.parent != path:
            path = path.parent
            parents.append(path)
        if not parents:
            parents.append(self.current_directory)

        menu = self.createBitroidMenu()
        for parent in parents:
            label = parent.name or str(parent)
            action = menu.addAction(QIcon(":/icons/icons/cil-folder-open.png"), label)
            action.setToolTip(str(parent))
            action.triggered.connect(lambda checked=False, target=parent: self.loadDirectory(target))

        menu.exec(self.ui.filesPathDropdownBtn.mapToGlobal(QPoint(0, self.ui.filesPathDropdownBtn.height())))

    def reloadFiles(self):
        self.loadDirectory(self.current_directory, remember=False)
        self.pushNotification("Folder refreshed.", "Files")

    def changeFileSort(self, sort_by):
        if not sort_by:
            return
        self.settings.set("file_manager", "sort_by", sort_by)
        self.loadDirectory(self.current_directory, remember=False)

    def openPathFromInput(self):
        raw_path = self.ui.filesPathInput.text().strip()
        if not raw_path:
            self.updateFilePathDisplay()
            return

        if raw_path in (self.currentDirectoryDisplayName(), str(self.current_directory)):
            path = self.current_directory
        else:
            path = Path(raw_path).expanduser()
            if not path.is_absolute():
                path = self.current_directory / path

        if path.is_dir():
            self.loadDirectory(path)
            self.updateFilePathDisplay()
        elif path.is_file():
            self.openFileFromBrowser(path)
            self.updateFilePathDisplay()
        else:
            self.pushNotification("That path does not exist.", "Files")

    def goHomeDirectory(self):
        self.loadDirectory(user_files_root())

    def goUpDirectory(self):
        parent = self.current_directory.parent
        if parent != self.current_directory:
            self.loadDirectory(parent)

    def goBackDirectory(self):
        if not self.file_back_stack:
            return
        target = self.file_back_stack.pop()
        self.file_forward_stack.append(self.current_directory)
        self.loadDirectory(target, remember=False)

    def goForwardDirectory(self):
        if not self.file_forward_stack:
            return
        target = self.file_forward_stack.pop()
        self.file_back_stack.append(self.current_directory)
        self.loadDirectory(target, remember=False)

    def loadDirectory(self, directory, remember=True):
        directory = Path(directory).expanduser()
        if not directory.is_dir():
            self.pushNotification("Folder is not available anymore.", "Files")
            directory = user_files_root()

        if remember and directory != self.current_directory:
            self.file_back_stack.append(self.current_directory)
            self.file_forward_stack.clear()

        self.current_directory = directory
        self.settings.set("file_manager", "current_dir", str(directory))
        self.updateFilePathDisplay()
        self.ui.fileStackTitleBtn.setText(directory.name or str(directory))
        self.updateFileNavigationState()
        self.updateCurrentDirectoryWatcher()

        try:
            entries = list(os.scandir(directory))
        except OSError as error:
            self.clearFilesTiles()
            self.createFileEmptyState(f"Cannot open this folder: {error.strerror or error}")
            return

        show_hidden = bool(self.settings.get("file_manager", "show_hidden", False))
        items = []
        for entry in entries:
            if not show_hidden and entry.name.startswith("."):
                continue
            try:
                items.append(self.buildFileItem(entry))
            except OSError:
                continue

        self.file_items = self.sortFileItems(items)
        self.renderFileItems()

    def updateCurrentDirectoryWatcher(self):
        watched = self.file_system_watcher.directories()
        if watched:
            self.file_system_watcher.removePaths(watched)
        if self.current_directory.is_dir():
            self.file_system_watcher.addPath(str(self.current_directory))

    def updateFileNavigationState(self):
        self.ui.filesBackBtn.setEnabled(bool(self.file_back_stack))
        self.ui.filesForwardBtn.setEnabled(bool(self.file_forward_stack))
        self.ui.filesUpBtn.setEnabled(self.current_directory.parent != self.current_directory)

    def buildFileItem(self, entry):
        stat_result = entry.stat(follow_symlinks=False)
        suffix = Path(entry.name).suffix.lower()
        is_dir = entry.is_dir(follow_symlinks=False)
        is_file = entry.is_file(follow_symlinks=False)
        media_kind = self.mediaKind(suffix) if is_file else None
        return {
            "name": entry.name,
            "path": Path(entry.path),
            "is_dir": is_dir,
            "is_file": is_file,
            "size": 0 if is_dir else stat_result.st_size,
            "type": "Folder" if is_dir else (suffix[1:].upper() or "File"),
            "modified": stat_result.st_mtime,
            "media_kind": media_kind,
        }

    def sortFileItems(self, items):
        sort_by = self.ui.filesSortComboBox.currentText() or "Name"

        def key(item):
            folder_rank = 0 if item["is_dir"] else 1
            if sort_by == "Size":
                value = item["size"]
            elif sort_by == "Type":
                value = item["type"].lower()
            elif sort_by == "Date":
                value = -item["modified"]
            else:
                value = item["name"].lower()
            return (folder_rank, value, item["name"].lower())

        return sorted(items, key=key)

    def renderFileItems(self):
        self.clearFilesTiles()
        self.updatePlaylistFromCurrentDirectory()

        if not self.file_items:
            self.createFileEmptyState("This folder is empty.")
        else:
            for item in self.file_items:
                self.createFileRow(item)

        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.ui.verticalLayout_22.addItem(verticalSpacer)

    def createFileEmptyState(self, text):
        empty_frame = QFrame(self.ui.filesScrollAreaContents)
        empty_frame.setObjectName("fileEmptyStateFrame")
        empty_frame.setMinimumSize(QSize(0, 96))
        layout = QVBoxLayout(empty_frame)
        layout.setContentsMargins(16, 16, 16, 16)
        label = QLabel(empty_frame)
        label.setObjectName("fileEmptyStateLabel")
        label.setText(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        self.ui.verticalLayout_22.addWidget(empty_frame)

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

    def createFileRow(self, item):
        row = QFrame(self.ui.filesScrollAreaContents)
        row.setObjectName("fileManagerRow")
        row.setProperty("filePath", str(item["path"]))
        row.setMinimumSize(QSize(0, 58))
        row.setFrameShape(QFrame.Shape.StyledPanel)
        row.setFrameShadow(QFrame.Shadow.Raised)
        row.mouseDoubleClickEvent = lambda event, item=item: self.openFileManagerItem(item)
        self.bindFileContextMenu(row, item)

        row_layout = QHBoxLayout(row)
        row_layout.setSpacing(10)
        row_layout.setContentsMargins(10, 6, 10, 6)

        open_btn = QPushButton(row)
        open_btn.setObjectName("fileManagerOpenBtn")
        open_btn.setFixedSize(36, 36)
        open_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        open_btn.setIcon(self.fileIconForItem(item))
        open_btn.setIconSize(QSize(22, 22))
        row_layout.addWidget(open_btn)
        self.bindFileContextMenu(open_btn, item)

        info_frame = QFrame(row)
        info_frame.setObjectName("fileManagerInfoFrame")
        info_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        info_layout = QVBoxLayout(info_frame)
        info_layout.setSpacing(4)
        info_layout.setContentsMargins(0, 0, 0, 0)
        self.bindFileContextMenu(info_frame, item)

        name_label = ElidedLabel(item["name"], info_frame)
        name_label.setObjectName("fileManagerNameLabel")
        name_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        name_label.mouseDoubleClickEvent = (
            lambda event, item=item, label=name_label, layout=info_layout:
                self.startInlineRename(item, label, layout, event)
        )
        info_layout.addWidget(name_label)
        self.bindFileContextMenu(name_label, item)

        meta_label = QLabel(info_frame)
        meta_label.setObjectName("fileManagerMetaLabel")
        meta_label.setText(self.fileMetaText(item))
        info_layout.addWidget(meta_label)
        self.bindFileContextMenu(meta_label, item)
        row_layout.addWidget(info_frame, 1)

        open_btn.clicked.connect(lambda _, item=item: self.openFileManagerItem(item))
        self.ui.verticalLayout_22.addWidget(row)

    def bindFileContextMenu(self, widget, item):
        widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        widget.customContextMenuRequested.connect(
            lambda position, source=widget, selected=item:
                self.showFileContextMenu(selected, source.mapToGlobal(position))
        )

    def createBitroidMenu(self):
        menu = QMenu(self)
        menu.setObjectName("bitroidContextMenu")
        return menu

    def showFileContextMenu(self, item, global_position):
        path = item["path"]
        menu = self.createBitroidMenu()

        open_action = menu.addAction(self.fileIconForItem(item), "Open")
        open_with_action = menu.addAction(QIcon(":/icons/icons/external-link.svg"), "Open with")

        add_playlist_action = None
        if item["is_dir"]:
            add_playlist_action = menu.addAction(QIcon(":/icons/icons/cil-featured-playlist.png"), "Add to playlist")

        menu.addSeparator()
        copy_action = menu.addAction(QIcon(":/icons/icons/copy.svg"), "Copy")
        paste_action = menu.addAction(QIcon(":/icons/icons/clipboard.svg"), "Paste")
        paste_action.setEnabled(bool(self.file_clipboard_paths))
        copy_path_action = menu.addAction(QIcon(":/icons/icons/cil-clipboard.png"), "Copy as path")

        menu.addSeparator()
        rename_action = menu.addAction(QIcon(":/icons/icons/edit-2.svg"), "Rename")
        properties_action = menu.addAction(QIcon(":/icons/icons/info.svg"), "Properties")

        selected_action = menu.exec(global_position)
        if selected_action == open_action:
            self.openFileManagerItem(item)
        elif selected_action == open_with_action:
            self.openWithFileItem(path)
        elif selected_action == add_playlist_action:
            self.addFolderToPlaylist(path)
        elif selected_action == copy_action:
            self.copyFileItem(path)
        elif selected_action == paste_action:
            destination = path if item["is_dir"] else self.current_directory
            self.pasteFileItems(destination)
        elif selected_action == copy_path_action:
            self.copyPathToClipboard(path)
        elif selected_action == rename_action:
            self.promptRenameFileItem(item)
        elif selected_action == properties_action:
            self.showFileProperties(path)

    def startInlineRename(self, item, name_label, info_layout, event=None):
        if event is not None:
            event.accept()

        path = item["path"]
        if not path.exists():
            self.pushNotification("This item is not available anymore.", "Rename")
            self.loadDirectory(self.current_directory, remember=False)
            return

        editor = QLineEdit(name_label.parentWidget())
        editor.setObjectName("fileManagerRenameInput")
        editor.setText(item["name"])

        index = info_layout.indexOf(name_label)
        name_label.hide()
        info_layout.insertWidget(max(index, 0), editor)

        state = {"done": False, "cancel": False}
        original_key_press = editor.keyPressEvent

        def keyPressEvent(key_event):
            if key_event.key() == Qt.Key_Escape:
                state["cancel"] = True
                finishRename()
                key_event.accept()
                return
            original_key_press(key_event)

        def finishRename():
            if state["done"]:
                return
            state["done"] = True
            new_name = editor.text().strip()
            info_layout.removeWidget(editor)
            editor.deleteLater()
            name_label.show()

            if state["cancel"] or not new_name or new_name == item["name"]:
                return
            self.renameFileItem(item, new_name)

        editor.keyPressEvent = keyPressEvent
        editor.editingFinished.connect(finishRename)
        editor.setFocus()
        if item["is_file"] and path.suffix:
            editor.setSelection(0, len(path.stem))
        else:
            editor.selectAll()

    def promptRenameFileItem(self, item):
        row = self.findFileRowForPath(item["path"])
        if not row:
            return
        label = row.findChild(QLabel, "fileManagerNameLabel")
        layout_owner = label.parentWidget() if label else None
        layout = layout_owner.layout() if layout_owner else None
        if label and layout:
            self.startInlineRename(item, label, layout)

    def findFileRowForPath(self, path):
        target = str(path)
        for index in range(self.ui.verticalLayout_22.count()):
            layout_item = self.ui.verticalLayout_22.itemAt(index)
            widget = layout_item.widget() if layout_item else None
            if widget and widget.property("filePath") == target:
                return widget
        return None

    def isValidFileName(self, name):
        if not name or name in (".", ".."):
            return False
        separators = [os.sep]
        if os.altsep:
            separators.append(os.altsep)
        if any(separator in name for separator in separators):
            return False
        if platform.system() == "Windows":
            return not any(character in name for character in '<>:"/\\|?*')
        return True

    def renameFileItem(self, item, new_name):
        if not self.isValidFileName(new_name):
            self.pushNotification("That file name is not valid.", "Rename")
            return

        source = item["path"]
        destination = source.with_name(new_name)
        if destination == source:
            return
        if destination.exists():
            self.pushNotification("An item with that name already exists.", "Rename")
            return

        try:
            source.rename(destination)
        except OSError as error:
            self.pushNotification(str(error), "Rename Failed")
            return

        self.loadDirectory(self.current_directory, remember=False)
        self.pushNotification(f"Renamed to {destination.name}.", "Files")

    def copyFileItem(self, path):
        path = Path(path)
        self.file_clipboard_paths = [path]
        QApplication.clipboard().setText(str(path))
        self.pushNotification(f"Copied {path.name}.", "Files")

    def copyPathToClipboard(self, path):
        QApplication.clipboard().setText(str(Path(path)))
        self.pushNotification("Path copied to clipboard.", "Files")

    def pasteFileItems(self, destination_dir):
        destination_dir = Path(destination_dir)
        if not destination_dir.is_dir():
            destination_dir = self.current_directory

        copied = 0
        for source in list(self.file_clipboard_paths):
            source = Path(source)
            if not source.exists():
                continue

            if source.is_dir():
                try:
                    if destination_dir.resolve().is_relative_to(source.resolve()):
                        self.pushNotification("A folder cannot be copied into itself.", "Paste")
                        continue
                except OSError:
                    pass

            destination = self.uniqueCopyDestination(destination_dir / source.name, source.is_file())
            try:
                if source.is_dir():
                    shutil.copytree(source, destination)
                else:
                    shutil.copy2(source, destination)
                copied += 1
            except OSError as error:
                self.pushNotification(str(error), "Paste Failed")

        if copied:
            self.loadDirectory(self.current_directory, remember=False)
            self.pushNotification(f"Pasted {copied} item{'s' if copied != 1 else ''}.", "Files")

    def uniqueCopyDestination(self, destination, is_file):
        destination = Path(destination)
        if not destination.exists():
            return destination

        stem = destination.stem if is_file else destination.name
        suffix = destination.suffix if is_file else ""
        for index in range(1, 1000):
            copy_label = "Copy" if index == 1 else f"Copy {index}"
            candidate = destination.with_name(f"{stem} - {copy_label}{suffix}")
            if not candidate.exists():
                return candidate
        return destination.with_name(f"{stem} - Copy {datetime.now().strftime('%Y%m%d%H%M%S')}{suffix}")

    def openWithFileItem(self, path):
        path = Path(path)
        try:
            if platform.system() == "Windows":
                subprocess.Popen(["rundll32.exe", "shell32.dll,OpenAs_RunDLL", str(path)])
                return

            app_path, _ = QFileDialog.getOpenFileName(self, "Open with", str(user_files_root()))
            if app_path:
                subprocess.Popen([app_path, str(path)])
        except OSError as error:
            self.pushNotification(str(error), "Open With Failed")

    def showFileProperties(self, path):
        path = Path(path)
        if not path.exists():
            self.pushNotification("This item is not available anymore.", "Properties")
            return

        stat_result = path.stat()
        dialog = QDialog(self)
        dialog.setObjectName("filePropertiesDialog")
        dialog.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        dialog.setModal(True)
        dialog.setMinimumWidth(430)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(10)
        layout.setContentsMargins(14, 12, 14, 12)

        header = QFrame(dialog)
        header.setObjectName("filePropertiesHeader")
        header_layout = QHBoxLayout(header)
        header_layout.setSpacing(8)
        header_layout.setContentsMargins(0, 0, 0, 0)

        header_title = QLabel("Properties", header)
        header_title.setObjectName("filePropertiesHeaderTitle")
        header_layout.addWidget(header_title, 1)

        title_close_btn = QToolButton(header)
        title_close_btn.setObjectName("filePropertiesTitleCloseBtn")
        title_close_btn.setFixedSize(24, 24)
        title_close_btn.setIcon(QIcon(":/icons/icons/x.svg"))
        title_close_btn.setIconSize(QSize(14, 14))
        title_close_btn.clicked.connect(dialog.reject)
        header_layout.addWidget(title_close_btn)
        layout.addWidget(header)

        title = QLabel(path.name, dialog)
        title.setObjectName("filePropertiesTitle")
        title.setWordWrap(True)
        title.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(title)

        form = QFormLayout()
        form.setSpacing(8)
        form.setContentsMargins(0, 4, 0, 4)

        details = [
            ("Type", "Folder" if path.is_dir() else (path.suffix[1:].upper() or "File")),
            ("Location", str(path.parent)),
            ("Size", self.folderSummary(path) if path.is_dir() else self.convert_size(stat_result.st_size)),
            ("Modified", datetime.fromtimestamp(stat_result.st_mtime).strftime("%d %b %Y, %H:%M:%S")),
            ("Created", datetime.fromtimestamp(stat_result.st_ctime).strftime("%d %b %Y, %H:%M:%S")),
            ("Readable", "Yes" if os.access(path, os.R_OK) else "No"),
            ("Writable", "Yes" if os.access(path, os.W_OK) else "No"),
        ]

        for key, value in details:
            key_label = QLabel(f"{key}:", dialog)
            value_label = QLabel(value, dialog)
            value_label.setWordWrap(True)
            value_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            form.addRow(key_label, value_label)

        layout.addLayout(form)

        close_btn = QPushButton("Close", dialog)
        close_btn.setObjectName("filePropertiesCloseBtn")
        close_btn.setFixedSize(QSize(76, 28))
        close_btn.clicked.connect(dialog.reject)
        layout.addWidget(close_btn, 0, Qt.AlignmentFlag.AlignRight)
        dialog.exec()

    def folderSummary(self, path):
        try:
            count = sum(1 for _ in os.scandir(path))
        except OSError:
            return "Folder"
        return f"{count} item{'s' if count != 1 else ''}"

    def addFolderToPlaylist(self, directory):
        media_paths = self.collectMediaPaths(directory)
        added = 0
        for path in media_paths:
            path_text = str(path)
            if path_text not in self.media_playlist:
                self.media_playlist.append(path_text)
                added += 1

        if self.media_current_index < 0 and self.media_playlist:
            self.media_current_index = 0

        if added:
            self.showMediaPlayer()
            self.ui.mediaPlayerShowBtn.setChecked(True)
            self.pushNotification(f"Added {added} media file{'s' if added != 1 else ''} to playlist.", "Media Player")
        else:
            self.pushNotification("No new supported media files found in this folder.", "Media Player")

    def collectMediaPaths(self, directory):
        media_paths = []
        for root, dirnames, filenames in os.walk(directory):
            dirnames[:] = [dirname for dirname in dirnames if not dirname.startswith(".")]
            for filename in filenames:
                path = Path(root) / filename
                if self.mediaKind(path.suffix.lower()):
                    media_paths.append(path)
        return sorted(media_paths, key=lambda path: str(path).lower())

    def fileIconForItem(self, item):
        if item["is_dir"]:
            return QIcon(":/icons/icons/cil-folder.png")
        if item["media_kind"] == "audio":
            return QIcon(":/icons/icons/music.svg")
        if item["media_kind"] == "video":
            return QIcon(":/icons/icons/film.svg")
        return QIcon(":/icons/icons/file.svg")

    def fileMetaText(self, item):
        modified = datetime.fromtimestamp(item["modified"]).strftime("%d %b %Y, %H:%M")
        if item["is_dir"]:
            return f"Folder  •  Modified {modified}"
        return f"{item['type']}  •  {self.convert_size(item['size'])}  •  Modified {modified}"

    def mediaKind(self, suffix):
        if suffix in self.audio_formats:
            return "audio"
        if suffix in self.video_formats:
            return "video"
        return None

    def openFileManagerItem(self, item):
        path = item["path"]
        if item["is_dir"]:
            self.loadDirectory(path)
        elif item["media_kind"]:
            self.playMediaPath(path)
        else:
            self.openFile(path)

    def openFileFromBrowser(self, path):
        suffix = path.suffix.lower()
        if self.mediaKind(suffix):
            self.playMediaPath(path)
        else:
            self.openFile(path)

    def openFile(self, path):
        if not path:
            return
        path = str(path)
        system = platform.system()
        try:
            if system == 'Windows':
                os.startfile(path)
            elif system == 'Darwin':
                subprocess.Popen(["open", path])
            else:
                subprocess.Popen(["xdg-open", path])
        except OSError as error:
            self.pushNotification(str(error), "Open Failed")

    def initMediaPlayer(self):
        self.audio_output = QAudioOutput(self)
        self.media_player = QMediaPlayer(self)
        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.setVideoOutput(self.ui.videoOutputFrame)

        volume = int(self.settings.get("media_player", "volume", 60))
        self.ui.mediaVolumeSlider.setRange(0, 100)
        self.ui.mediaVolumeSlider.setValue(max(0, min(volume, 100)))
        self.audio_output.setVolume(self.ui.mediaVolumeSlider.value() / 100)

        self.ui.mediaProgressSlider.setRange(0, 0)
        self.ui.currentPlayingBtn.setText("00:00")
        self.ui.remainingMediaBtn.setText("-00:00")

        playback_rate = float(self.settings.get("media_player", "playback_rate", 1.0))
        for index in range(self.ui.playbackSpeedCombobox.count()):
            try:
                if float(self.ui.playbackSpeedCombobox.itemText(index).replace("x", "")) == playback_rate:
                    self.ui.playbackSpeedCombobox.setCurrentIndex(index)
                    break
            except ValueError:
                continue
        self.media_player.setPlaybackRate(playback_rate)

        self.ui.mediaPlayBtn.clicked.connect(self.toggleMediaPlayback)
        self.ui.mediaStopBtn.clicked.connect(self.stopMedia)
        self.ui.mediaPreviousBtn.clicked.connect(self.playPreviousMedia)
        self.ui.mediaNextBtn.clicked.connect(self.playNextMedia)
        self.ui.seekBackwardBtn.clicked.connect(lambda: self.seekMediaBy(-10000))
        self.ui.seekForwardBtn.clicked.connect(lambda: self.seekMediaBy(10000))
        self.ui.mediaMuteBtn.clicked.connect(self.toggleMediaMute)
        self.ui.mediaRepeatBtn.clicked.connect(self.toggleMediaRepeat)
        self.ui.mediaShuffleBtn.clicked.connect(self.toggleMediaShuffle)
        self.ui.playerLockBtn.clicked.connect(self.togglePlayerLock)
        self.ui.mediaFolderBtn.clicked.connect(self.chooseMediaFolder)
        self.ui.playerUndockBtn.clicked.connect(lambda: self.pushNotification("Undocked video will be added after the embedded player is stable.", "Media Player"))
        self.ui.mediaVolumeSlider.valueChanged.connect(self.changeMediaVolume)
        self.ui.mediaProgressSlider.sliderMoved.connect(self.seekMediaTo)
        self.ui.playbackSpeedCombobox.currentTextChanged.connect(self.changePlaybackRate)

        self.media_player.positionChanged.connect(self.updateMediaPosition)
        self.media_player.durationChanged.connect(self.updateMediaDuration)
        self.media_player.playbackStateChanged.connect(self.updateMediaPlaybackState)
        self.media_player.mediaStatusChanged.connect(self.handleMediaStatus)
        self.media_player.errorOccurred.connect(self.handleMediaError)

        self.updateMediaRepeatIcon()
        self.updateMediaShuffleIcon()
        self.updateMediaMuteIcon()
        self.updateMediaPlaybackState(self.media_player.playbackState())

    def updatePlaylistFromCurrentDirectory(self):
        previous_current = self.currentMediaPath()
        playlist = [
            str(item["path"])
            for item in self.file_items
            if item["is_file"] and item["media_kind"]
        ]
        self.media_playlist = playlist
        if previous_current in playlist:
            self.media_current_index = playlist.index(previous_current)
        elif playlist:
            self.media_current_index = 0
        else:
            self.media_current_index = -1

    def currentMediaPath(self):
        if 0 <= self.media_current_index < len(self.media_playlist):
            return self.media_playlist[self.media_current_index]
        return None

    def chooseMediaFolder(self):
        directory = QFileDialog.getExistingDirectory(self, "Open Media Folder", str(self.current_directory))
        if directory:
            self.loadDirectory(Path(directory))
            if self.media_playlist:
                self.playMediaPath(self.media_playlist[0])
            else:
                self.pushNotification("No supported media files in this folder.", "Media Player")

    def playMediaPath(self, path):
        path = str(path)
        if path not in self.media_playlist:
            self.media_playlist.append(path)
        self.media_current_index = self.media_playlist.index(path)

        suffix = Path(path).suffix.lower()
        if self.mediaKind(suffix) == "video":
            self.media_player.setVideoOutput(self.ui.videoOutputFrame)
            self.ui.videoOutputFrame.show()
        else:
            self.ui.videoOutputFrame.hide()

        self.media_player.setSource(QUrl.fromLocalFile(path))
        self.media_player.play()
        self.showMediaPlayer()
        self.ui.mediaPlayerShowBtn.setChecked(True)
        self.ui.logLabel.setText(f"Playing {Path(path).name}")

    def toggleMediaPlayback(self):
        if not self.media_player.source().isValid():
            current = self.currentMediaPath()
            if current:
                self.playMediaPath(current)
            else:
                self.pushNotification("Open a media file first.", "Media Player")
            return

        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()

    def stopMedia(self):
        self.media_player.stop()
        self.ui.mediaProgressSlider.setValue(0)

    def playNextMedia(self):
        if not self.media_playlist:
            return
        if self.media_repeat_mode == "one":
            self.seekMediaTo(0)
            self.media_player.play()
            return
        if self.media_shuffle and len(self.media_playlist) > 1:
            next_index = random.choice([i for i in range(len(self.media_playlist)) if i != self.media_current_index])
        else:
            next_index = self.media_current_index + 1
            if next_index >= len(self.media_playlist):
                if self.media_repeat_mode == "all":
                    next_index = 0
                else:
                    self.media_player.pause()
                    return
        self.playMediaPath(self.media_playlist[next_index])

    def playPreviousMedia(self):
        if not self.media_playlist:
            return
        previous_index = self.media_current_index - 1
        if previous_index < 0:
            previous_index = len(self.media_playlist) - 1 if self.media_repeat_mode == "all" else 0
        self.playMediaPath(self.media_playlist[previous_index])

    def seekMediaBy(self, milliseconds):
        duration = max(self.media_player.duration(), 0)
        position = max(0, min(self.media_player.position() + milliseconds, duration))
        self.media_player.setPosition(position)

    def seekMediaTo(self, position):
        self.media_player.setPosition(int(position))

    def changeMediaVolume(self, value):
        self.audio_output.setVolume(value / 100)
        if value > 0 and self.audio_output.isMuted():
            self.audio_output.setMuted(False)
        self.settings.set("media_player", "volume", value)
        self.updateMediaMuteIcon()

    def toggleMediaMute(self):
        self.audio_output.setMuted(not self.audio_output.isMuted())
        self.updateMediaMuteIcon()

    def updateMediaMuteIcon(self):
        muted = self.audio_output.isMuted() or self.ui.mediaVolumeSlider.value() == 0
        self.ui.mediaMuteBtn.setIcon(QIcon(":/icons/icons/cil-volume-off.png" if muted else ":/icons/icons/cil-volume-high.png"))

    def toggleMediaRepeat(self):
        modes = ["off", "all", "one"]
        current = modes.index(self.media_repeat_mode) if self.media_repeat_mode in modes else 0
        self.media_repeat_mode = modes[(current + 1) % len(modes)]
        self.settings.set("media_player", "repeat_mode", self.media_repeat_mode)
        self.updateMediaRepeatIcon()

    def updateMediaRepeatIcon(self):
        icon = {
            "off": ":/icons/icons/cil-loop.png",
            "all": ":/icons/icons/cil-loop-circular.png",
            "one": ":/icons/icons/cil-loop-1.png",
        }.get(self.media_repeat_mode, ":/icons/icons/cil-loop.png")
        self.ui.mediaRepeatBtn.setIcon(QIcon(icon))

    def toggleMediaShuffle(self):
        self.media_shuffle = not self.media_shuffle
        self.settings.set("media_player", "shuffle", self.media_shuffle)
        self.updateMediaShuffleIcon()

    def updateMediaShuffleIcon(self):
        self.ui.mediaShuffleBtn.setIcon(QIcon(":/icons/icons/cil-layers.png" if self.media_shuffle else ":/icons/icons/cil-infinity.png"))

    def togglePlayerLock(self):
        self.player_locked = not self.player_locked
        self.ui.playerLockBtn.setIcon(QIcon(":/icons/icons/cil-lock-locked.png" if self.player_locked else ":/icons/icons/cil-lock-unlocked.png"))
        for widget in (
            self.ui.mediaFolderBtn,
            self.ui.playbackSpeedCombobox,
            self.ui.playerUndockBtn,
            self.ui.mediaStopBtn,
            self.ui.seekBackwardBtn,
            self.ui.mediaPreviousBtn,
            self.ui.mediaPlayBtn,
            self.ui.mediaNextBtn,
            self.ui.seekForwardBtn,
            self.ui.mediaRepeatBtn,
            self.ui.mediaShuffleBtn,
            self.ui.mediaMuteBtn,
            self.ui.mediaVolumeSlider,
            self.ui.mediaProgressSlider,
        ):
            widget.setEnabled(not self.player_locked)
        self.ui.playerLockBtn.setEnabled(True)

    def changePlaybackRate(self, text):
        try:
            rate = float(text.replace("x", ""))
        except ValueError:
            return
        self.media_player.setPlaybackRate(rate)
        self.settings.set("media_player", "playback_rate", rate)

    def updateMediaDuration(self, duration):
        self.media_duration = max(duration, 0)
        self.ui.mediaProgressSlider.setRange(0, self.media_duration)
        self.ui.remainingMediaBtn.setText(f"-{self.format_time(self.media_duration)}")

    def updateMediaPosition(self, position):
        self._updating_media_slider = True
        self.ui.mediaProgressSlider.setValue(position)
        self._updating_media_slider = False
        self.ui.currentPlayingBtn.setText(self.format_time(position))
        remaining = max(self.media_duration - position, 0)
        self.ui.remainingMediaBtn.setText(f"-{self.format_time(remaining)}")

    def updateMediaPlaybackState(self, state):
        is_playing = state == QMediaPlayer.PlaybackState.PlayingState
        self.ui.mediaPlayBtn.setIcon(QIcon(":/icons/icons/cil-media-pause.png" if is_playing else ":/icons/icons/play.svg"))

    def handleMediaStatus(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            if self.media_repeat_mode == "one":
                self.seekMediaTo(0)
                self.media_player.play()
            else:
                self.playNextMedia()

    def handleMediaError(self, error, error_string):
        if error != QMediaPlayer.Error.NoError:
            self.pushNotification(error_string or "Could not play this media file.", "Media Error")

    def format_time(self, ms):
        seconds = max(int(ms / 1000), 0)
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return f"{minutes:02d}:{seconds:02d}"

    def clearFilesTiles(self):
        while self.ui.verticalLayout_22.count():
            item = self.ui.verticalLayout_22.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

    def initHistory(self, history_file=None):
        self.history_thread = HistoryManager(str(history_file) if history_file else None)
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

    def initFavorites(self, favorites_file=None):
        self.favorite_torrents = FavoriteTorrent(str(favorites_file) if favorites_file else None)
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
            endOfFavoriteBtn = QPushButton(self.ui.favoritesScrollAreaWidgetContents)
            endOfFavoriteBtn.setObjectName(u"endOfFavoriteBtn")
            endOfFavoriteBtn.setMinimumSize(QSize(0, 100))
            endOfFavoriteBtn.setText(f"End of {len(favorite_list)} Favorite Items.")
            self.ui.verticalLayout_29.addWidget(endOfFavoriteBtn)  
            verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
            self.ui.verticalLayout_29.addItem(verticalSpacer)
        else:
            endOfFavoriteBtn = QPushButton(self.ui.favoritesScrollAreaWidgetContents)
            endOfFavoriteBtn.setObjectName(u"endOfFavoriteBtn")
            endOfFavoriteBtn.setMinimumSize(QSize(0, 100))
            endOfFavoriteBtn.setText("Add Items to Favorite First!")
            self.ui.verticalLayout_29.addWidget(endOfFavoriteBtn)  
    
    def initNetworkMonitor(self):
        self.network_monitor = InternetChecker()
        self.network_monitor.connectivity_changed.connect(self.updateNetConnectivity)
        self.network_monitor.network_speed.connect(self.updateNetSpeed)
        self.network_monitor.start()

    def updateNetConnectivity(self, connected):
        self.internet_connection = connected
        if connected and not self.torrent_engine_active: self.initSearchThread()
        self.temporaryLog("Conected to Internet!" if connected else "No Internet!", 1500)
        self.ui.internetConnectivityBtn.setIcon(QIcon(':/icons/icons/cil-wifi-signal-4.png' if connected else ':/icons/icons/cil-wifi-signal-off.png'))

    def updateNetSpeed(self, speed):
        if hasattr(speed, "download_bps") and hasattr(speed, "upload_bps"):
            download_bps = int(speed.download_bps)
            upload_bps = int(speed.upload_bps)
        elif isinstance(speed, dict):
            download_bps = int(speed.get("download_bps", 0))
            upload_bps = int(speed.get("upload_bps", 0))
        else:
            download_bps = int(speed)
            upload_bps = 0

        self.ui.netSpeedBtn.setText(self.formatNetSpeed(download_bps + upload_bps))
        self.ui.downloadSpeedBtn.setText(self.formatNetSpeed(download_bps))
        self.ui.uploadSpeedBtn.setText(self.formatNetSpeed(upload_bps))

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

    def refreshSearchApi(self):
        if self.torrent_engine_active: 
            self.search_thread.stop()
            self.torrent_engine_active = False
        self.initSearchThread()

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
            "leecher": result.get('leecher', 'N/A'),
            "magnet": result.get('magnet', ''),
            "name": result.get('name', 'N/A'),
            "nsfw": result.get('nsfw', False),
            "seeder": result.get('seeder', 'N/A'),
            "size": result.get('size', 'N/A'),
            "path": "N/A",
            "timestamp": self.timeNow(),
            "elapsed": "N/A"
        })
        self.openUrl(result.get('magnet'), "Opening magnet in default torrent app...", 3000)

    def handleMagnetLink(self, result):
        if self.click_timer.isActive():
            self.click_timer.stop()
            self.temporaryLog("Magnet Link Copied to Clipboard!", 1500)
            self.copyToClipboard(result.get('magnet'))
        else:
            self.magnet_link = result.get('magnet')
            self.click_timer.start(350)

        self.history_thread.add_history({
            "leecher": result.get('leecher', 'N/A'),
            "magnet": result.get('magnet', ''),
            "name": result.get('name', 'N/A'),
            "nsfw": result.get('nsfw', False),
            "seeder": result.get('seeder', 'N/A'),
            "size": result.get('size', 'N/A'),
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

    def temporaryLog(self, text, duration=5000):
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
                self.stopLoadingAnimation()
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
                self.stopLoadingAnimation()
                self.ui.logLabel.setText("No result found!")
                endOfSearchBtn = QPushButton(self.ui.scrollAreaContents)
                endOfSearchBtn.setObjectName(u"endOfSearchBtn")
                endOfSearchBtn.setMinimumSize(QSize(0, 100))
                endOfSearchBtn.setText("Try Something More Relevant!")
                self.ui.verticalLayout_13.addWidget(endOfSearchBtn)  
        else:
            self.dots_timer.stop()
            self.stopLoadingAnimation()
            self.pushNotification(f"Search failed due to some unexpected errors, this error is from torrent search API. More info: {comment}", "Search Failed")
            self.ui.logLabel.setText("Search Failed!")
    
    def searchTorrents(self):
        query = self.ui.searchInputText.text().strip()
        if self.internet_connection:
            if self.torrent_engine_active: 
                if len(query) >= 3:
                    self.dots_timer.start(500)
                    self.ui.logLabel.setText("Searching")
                    self.startLoadingAnimation()
                    self.search_thread.start_search(query=query, sort="MAX_SEED", include_nsfw=self.include_nsfw)
                else: self.pushNotification("Query can't be blank or less than 3 letter, please enter a query meeting the minimum requirements before hitting the search button", "Blank Query")
            else: 
                self.initSearchThread()
                self.pushNotification("Due to network error, torrent engine was left uninitialized while initializing the application. Trying to reinitialize torrent engine, retry with your query!", "Uninitialized Torrent Engine")
        else:
            self.pushNotification("No internet connection available! What do you expect?", "No Internet")

    def closeEvent(self, event):
        self.hide()
        if self.torrent_engine_active: self.search_thread.stop()
        self.media_player.stop()
        self.network_monitor.stop()
        self.favorite_torrents.stop()
        self.history_thread.stop()
        self.settings.set("file_manager", "current_dir", str(self.current_directory))
        self.settings.save()
        event.accept()

def run():
    app = QApplication(sys.argv)
    window = MainWindow()
    return app.exec()


if __name__ == "__main__":
    sys.exit(run())
