import sys
import os
import json
import platform
import math
import subprocess
import webbrowser
import random
import shutil
import time
from pathlib import Path

from bitroid.services.libtorrent_loader import LibtorrentUnavailableError, load_libtorrent

try:
    load_libtorrent()
except LibtorrentUnavailableError:
    pass

from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QTimer, QFileSystemWatcher, QUrl, QEvent
from PySide6.QtGui import QColor, QPainter, QPixmap
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QDialog,
    QFileDialog,
    QFormLayout,
    QGraphicsOpacityEffect,
    QHeaderView,
    QInputDialog,
    QMenu,
    QProgressBar,
    QSplitter,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QTreeWidget,
    QTreeWidgetItem,
    QWidget,
)
from bitroid.core.paths import app_data_dir, user_files_root
from bitroid.core.settings import AppSettings
from bitroid.features.search.search_thread import SearchThread
from bitroid.services.network import InternetChecker
from bitroid.services.favorites import FavoriteTorrent
from bitroid.services.history import HistoryManager
from bitroid.services.torrent_engine import TorrentEngine
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


class ScrollingLabel(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(parent)
        self._full_text = ""
        self._scroll_offset = 0
        self._scroll_padding = "    "
        self._scroll_timer = QTimer(self)
        self._scroll_timer.setInterval(150)
        self._scroll_timer.timeout.connect(self.advanceScroll)
        self.setText(text)

    def setText(self, text):
        self._full_text = str(text)
        self._scroll_offset = 0
        self.setToolTip(self._full_text)
        self.renderText()

    def text(self):
        return self._full_text

    def renderText(self):
        if not self._full_text:
            self._scroll_timer.stop()
            QLabel.setText(self, "")
            return

        available_width = max(0, self.width() - 12)
        if available_width <= 0 or self.fontMetrics().horizontalAdvance(self._full_text) <= available_width:
            self._scroll_timer.stop()
            QLabel.setText(self, self._full_text)
            return

        stream = self._full_text + self._scroll_padding
        char_width = max(self.fontMetrics().averageCharWidth(), 1)
        visible_chars = max(1, int(available_width / char_width))
        offset = self._scroll_offset % len(stream)
        repeated = stream * ((visible_chars // len(stream)) + 3)
        QLabel.setText(self, repeated[offset:offset + visible_chars])
        if not self._scroll_timer.isActive():
            self._scroll_timer.start()

    def advanceScroll(self):
        if not self._full_text:
            return
        self._scroll_offset = (self._scroll_offset + 1) % len(self._full_text + self._scroll_padding)
        self.renderText()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.renderText()


class TorrentPieceMap(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._segments = []
        self.setObjectName("torrentPieceMap")
        self.setMinimumHeight(18)
        self.setMaximumHeight(18)

    def setSegments(self, segments):
        self._segments = [max(0.0, min(float(value), 1.0)) for value in segments if value is not None]
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect().adjusted(1, 1, -1, -1)
        painter.fillRect(rect, QColor("#1a1b1e"))
        painter.setPen(QColor("#3b3d40"))
        painter.drawRect(rect)

        if not self._segments:
            return

        count = max(len(self._segments), 1)
        width = max(rect.width() / count, 1)
        for index, value in enumerate(self._segments):
            if value <= 0:
                color = QColor("#f4f4f4") if index % 2 else QColor("#e8e8e8")
            elif value >= 0.999:
                color = QColor("#a7b308")
            else:
                color = QColor("#387780")
            x = int(rect.left() + index * width)
            painter.fillRect(x, rect.top() + 1, max(int(width), 1), rect.height() - 1, color)


TORRENT_HEADER_FONT = ("Segoe UI", 9)


def configure_torrent_header(view, widths=None, stretch_last=False):
    if hasattr(view, "horizontalHeader"):
        header = view.horizontalHeader()
    else:
        header = view.header()

    header.setObjectName("torrentHeader")
    header.setFont(QFont(*TORRENT_HEADER_FONT))
    header.setFixedHeight(22)
    header.setMinimumSectionSize(42)
    header.setDefaultSectionSize(86)
    header.setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
    header.setSectionsMovable(True)
    header.setHighlightSections(False)
    header.setStretchLastSection(stretch_last)

    column_count = view.columnCount()
    for column in range(column_count):
        header.setSectionResizeMode(column, QHeaderView.ResizeMode.Interactive)
        if widths and column < len(widths):
            view.setColumnWidth(column, widths[column])

    if hasattr(view, "verticalHeader"):
        view.verticalHeader().hide()
        view.verticalHeader().setDefaultSectionSize(22)

    view.setFont(QFont("Segoe UI", 9))
    view.setAlternatingRowColors(True)
    view.setTextElideMode(Qt.TextElideMode.ElideRight)
    if hasattr(view, "setWordWrap"):
        view.setWordWrap(False)
    if hasattr(view, "setShowGrid"):
        view.setShowGrid(False)
    if hasattr(view, "setUniformRowHeights"):
        view.setUniformRowHeights(True)

    repolish_widget(header)
    repolish_widget(view)


def repolish_widget(widget):
    style = widget.style()
    style.unpolish(widget)
    style.polish(widget)
    try:
        widget.update()
    except TypeError:
        if hasattr(widget, "viewport"):
            widget.viewport().update()
        else:
            widget.repaint()


class TorrentAddDialog(QDialog):
    PRIORITIES = ("Skip", "Low", "Normal", "High", "Maximum")

    def __init__(self, result, default_save_path, parent=None):
        super().__init__(parent)
        self.setObjectName("torrentAddDialog")
        self.result = result or {}
        self.default_save_path = Path(default_save_path).expanduser()
        self.selected_files = []
        self._syncing_file_checks = False
        self.setWindowTitle(f"Add Torrent - {self.torrentName()}")
        self.setMinimumSize(640, 440)
        self.resize(740, 500)
        self.setModal(True)
        self._buildUi()
        QTimer.singleShot(650, self.populateMetadataPreview)

    def torrentName(self):
        return self.result.get("name") or self.result.get("title") or "Magnet link"

    def torrentSize(self):
        return self.result.get("size") or "Metadata pending"

    def selectedOptions(self):
        return {
            "name": self.torrentName(),
            "magnet": self.result.get("magnet", ""),
            "path": self.result.get("path", ""),
            "size": self.torrentSize(),
            "site": self.result.get("site", ""),
            "save_path": self.savePathInput.text().strip(),
            "start": self.startTorrentCheck.isChecked(),
            "sequential": self.sequentialCheck.isChecked(),
            "first_last": self.firstLastCheck.isChecked(),
            "skip_hash_check": self.skipHashCheck.isChecked(),
            "files": self.collectFiles(),
        }

    def collectFiles(self):
        files = []
        for index in range(self.filesTree.topLevelItemCount()):
            item = self.filesTree.topLevelItem(index)
            self._collectFileItem(item, files)
        return files

    def _collectFileItem(self, item, files):
        if item.childCount():
            for child_index in range(item.childCount()):
                self._collectFileItem(item.child(child_index), files)
            return
        files.append({
            "name": item.toolTip(0) or item.text(0),
            "size": item.text(1),
            "priority": item.text(2),
            "selected": item.checkState(0) == Qt.CheckState.Checked,
            "index": item.data(0, Qt.ItemDataRole.UserRole),
        })

    def _buildUi(self):
        root = QVBoxLayout(self)
        root.setSpacing(0)
        root.setContentsMargins(0, 0, 0, 0)

        body = QSplitter(Qt.Orientation.Horizontal, self)
        body.setObjectName("torrentAddSplitter")
        body.setHandleWidth(4)
        root.addWidget(body, 1)

        left = QFrame(body)
        left.setObjectName("torrentAddOptionsPane")
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(12, 10, 10, 10)
        left_layout.setSpacing(10)
        body.addWidget(left)

        save_group = QFrame(left)
        save_group.setObjectName("torrentAddSection")
        save_layout = QVBoxLayout(save_group)
        save_layout.setContentsMargins(10, 8, 10, 10)
        save_layout.setSpacing(7)
        save_title = QLabel("Save at", save_group)
        save_title.setObjectName("torrentAddSectionTitle")
        save_layout.addWidget(save_title)
        save_row = QHBoxLayout()
        self.savePathInput = QLineEdit(str(self.default_save_path), save_group)
        self.savePathInput.setObjectName("torrentAddPathInput")
        save_row.addWidget(self.savePathInput, 1)
        browse_btn = QToolButton(save_group)
        browse_btn.setObjectName("torrentAddBrowseBtn")
        browse_btn.setIcon(QIcon(":/icons/icons/folder.svg"))
        browse_btn.setIconSize(QSize(16, 16))
        browse_btn.clicked.connect(self.chooseSavePath)
        save_row.addWidget(browse_btn)
        save_layout.addLayout(save_row)
        self.rememberPathCheck = QCheckBox("Remember last used save path", save_group)
        self.rememberPathCheck.setObjectName("torrentAddCheck")
        save_layout.addWidget(self.rememberPathCheck)
        left_layout.addWidget(save_group)

        options_group = QFrame(left)
        options_group.setObjectName("torrentAddSection")
        options_layout = QVBoxLayout(options_group)
        options_layout.setContentsMargins(10, 8, 10, 10)
        options_layout.setSpacing(8)
        options_title = QLabel("Torrent options", options_group)
        options_title.setObjectName("torrentAddSectionTitle")
        options_layout.addWidget(options_title)
        self.startTorrentCheck = QCheckBox("Start torrent after adding", options_group)
        self.startTorrentCheck.setObjectName("torrentAddCheck")
        self.startTorrentCheck.setChecked(True)
        self.sequentialCheck = QCheckBox("Download in sequential order", options_group)
        self.sequentialCheck.setObjectName("torrentAddCheck")
        self.firstLastCheck = QCheckBox("Download first and last pieces first", options_group)
        self.firstLastCheck.setObjectName("torrentAddCheck")
        self.skipHashCheck = QCheckBox("Skip hash check", options_group)
        self.skipHashCheck.setObjectName("torrentAddCheck")
        for checkbox in (self.startTorrentCheck, self.sequentialCheck, self.firstLastCheck, self.skipHashCheck):
            options_layout.addWidget(checkbox)
        left_layout.addWidget(options_group)

        info_group = QFrame(left)
        info_group.setObjectName("torrentAddSection")
        info_layout = QFormLayout(info_group)
        info_layout.setContentsMargins(10, 8, 10, 10)
        info_layout.setSpacing(8)
        self.infoSizeLabel = QLabel("Metadata pending", info_group)
        self.infoHashLabel = ElidedLabel((self.result.get("magnet", "") or "N/A"), info_group)
        self.infoSeedLabel = QLabel(str(self.result.get("seeder", "N/A")), info_group)
        self.infoSiteLabel = QLabel(str(self.result.get("site", "N/A")), info_group)
        for value_label in (self.infoSizeLabel, self.infoHashLabel, self.infoSeedLabel, self.infoSiteLabel):
            value_label.setObjectName("torrentAddInfoValue")
        for caption, value_label in (
            ("Size:", self.infoSizeLabel),
            ("Info hash:", self.infoHashLabel),
            ("Seeders:", self.infoSeedLabel),
            ("Source:", self.infoSiteLabel),
        ):
            caption_label = QLabel(caption, info_group)
            caption_label.setObjectName("torrentAddInfoLabel")
            info_layout.addRow(caption_label, value_label)
        left_layout.addWidget(info_group)
        left_layout.addStretch(1)

        right = QFrame(body)
        right.setObjectName("torrentAddFilesPane")
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(10, 10, 12, 10)
        right_layout.setSpacing(8)
        body.addWidget(right)

        files_toolbar = QFrame(right)
        files_toolbar.setObjectName("torrentAddFilesToolbar")
        files_toolbar_layout = QHBoxLayout(files_toolbar)
        files_toolbar_layout.setContentsMargins(0, 0, 0, 0)
        files_toolbar_layout.setSpacing(8)
        select_all_btn = QPushButton("Select All", files_toolbar)
        select_all_btn.setObjectName("torrentMiniButton")
        select_all_btn.clicked.connect(lambda: self.setAllFilesChecked(True))
        select_none_btn = QPushButton("Select None", files_toolbar)
        select_none_btn.setObjectName("torrentMiniButton")
        select_none_btn.clicked.connect(lambda: self.setAllFilesChecked(False))
        self.fileFilterInput = QLineEdit(files_toolbar)
        self.fileFilterInput.setObjectName("torrentFilterInput")
        self.fileFilterInput.setPlaceholderText("Filter files...")
        self.fileFilterInput.textChanged.connect(self.filterFiles)
        files_toolbar_layout.addWidget(select_all_btn)
        files_toolbar_layout.addWidget(select_none_btn)
        files_toolbar_layout.addStretch(1)
        files_toolbar_layout.addWidget(self.fileFilterInput)
        right_layout.addWidget(files_toolbar)

        self.filesTree = QTreeWidget(right)
        self.filesTree.setObjectName("torrentAddFilesTree")
        self.filesTree.setColumnCount(3)
        self.filesTree.setHeaderLabels(["Name", "Total Size", "Download Priority"])
        configure_torrent_header(self.filesTree, [260, 110, 130])
        self.filesTree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.filesTree.customContextMenuRequested.connect(self.showPriorityMenu)
        self.filesTree.itemChanged.connect(self.syncFileCheckState)
        right_layout.addWidget(self.filesTree, 1)

        footer = QFrame(self)
        footer.setObjectName("torrentAddFooter")
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(12, 8, 12, 10)
        footer_layout.setSpacing(8)
        self.metadataProgress = QProgressBar(footer)
        self.metadataProgress.setObjectName("torrentMetadataProgress")
        self.metadataProgress.setRange(0, 0)
        self.metadataProgress.setTextVisible(False)
        self.metadataProgress.setFixedWidth(110)
        footer_layout.addWidget(self.metadataProgress)
        self.metadataStatusLabel = QLabel("Retrieving metadata...", footer)
        self.metadataStatusLabel.setObjectName("torrentAddStatusLabel")
        footer_layout.addWidget(self.metadataStatusLabel)
        self.saveTorrentBtn = QPushButton("Save as .torrent file...", footer)
        self.saveTorrentBtn.setObjectName("torrentSecondaryButton")
        footer_layout.addWidget(self.saveTorrentBtn)
        footer_layout.addStretch(1)
        cancel_btn = QPushButton("Cancel", footer)
        cancel_btn.setObjectName("torrentSecondaryButton")
        cancel_btn.clicked.connect(self.reject)
        add_btn = QPushButton("Add Torrent", footer)
        add_btn.setObjectName("torrentPrimaryButton")
        add_btn.clicked.connect(self.accept)
        footer_layout.addWidget(cancel_btn)
        footer_layout.addWidget(add_btn)
        root.addWidget(footer)
        body.setSizes([320, 440])

    def chooseSavePath(self):
        directory = QFileDialog.getExistingDirectory(self, "Select save path", self.savePathInput.text())
        if directory:
            self.savePathInput.setText(directory)

    def populateMetadataPreview(self):
        self.metadataStatusLabel.setText("Metadata ready")
        self.metadataProgress.setRange(0, 1)
        self.metadataProgress.setValue(1)
        self.infoSizeLabel.setText(str(self.torrentSize()))
        self.filesTree.clear()
        if self.populateTorrentFilePreview():
            return
        name = self.torrentName()
        size = str(self.torrentSize())
        root = QTreeWidgetItem([name, size, "Normal"])
        root.setFlags(root.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        root.setCheckState(0, Qt.CheckState.Checked)
        root.setIcon(0, QIcon(":/icons/icons/folder.svg"))
        if self._looksLikeCollection(name):
            for index, label in enumerate(("Part 1", "Part 2", "Extras")):
                child = QTreeWidgetItem([f"{name} - {label}", "Metadata", "Normal"])
                child.setFlags(child.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                child.setCheckState(0, Qt.CheckState.Checked)
                child.setIcon(0, QIcon(":/icons/icons/file.svg"))
                root.addChild(child)
        else:
            root.setIcon(0, QIcon(":/icons/icons/file.svg"))
        self.filesTree.addTopLevelItem(root)
        root.setExpanded(True)

    def populateTorrentFilePreview(self):
        torrent_path = self.result.get("path")
        if not torrent_path:
            return False
        try:
            lt, _dll_dir, _handle = load_libtorrent()
            torrent_info = lt.torrent_info(str(torrent_path))
            files = torrent_info.files()
        except Exception as error:
            self.metadataStatusLabel.setText("Metadata preview unavailable")
            self.infoSiteLabel.setToolTip(str(error))
            return False

        total_size = sum(int(files.file_size(index)) for index in range(files.num_files()))
        root = QTreeWidgetItem([torrent_info.name() or self.torrentName(), self._formatBytes(total_size), "Normal"])
        root.setFlags(root.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        root.setCheckState(0, Qt.CheckState.Checked)
        root.setIcon(0, QIcon(":/icons/icons/folder.svg"))
        parent_items = {(): root}
        for index in range(files.num_files()):
            path_text = str(files.file_path(index))
            parts = [part for part in path_text.replace("\\", "/").split("/") if part]
            parent = root
            folder_key = ()
            for folder in parts[:-1]:
                folder_key = (*folder_key, folder)
                if folder_key not in parent_items:
                    folder_item = QTreeWidgetItem([folder, "-", "Normal"])
                    folder_item.setFlags(folder_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                    folder_item.setCheckState(0, Qt.CheckState.Checked)
                    folder_item.setIcon(0, QIcon(":/icons/icons/folder.svg"))
                    parent.addChild(folder_item)
                    parent_items[folder_key] = folder_item
                parent = parent_items[folder_key]
            display_name = parts[-1] if parts else path_text
            child = QTreeWidgetItem([display_name, self._formatBytes(files.file_size(index)), "Normal"])
            child.setFlags(child.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            child.setCheckState(0, Qt.CheckState.Checked)
            child.setData(0, Qt.ItemDataRole.UserRole, index)
            child.setToolTip(0, path_text)
            child.setIcon(0, QIcon(":/icons/icons/file.svg"))
            parent.addChild(child)
        self.infoSizeLabel.setText(self._formatBytes(total_size))
        self.filesTree.addTopLevelItem(root)
        root.setExpanded(True)
        return True

    def _formatBytes(self, size_bytes):
        units = ("B", "KB", "MB", "GB", "TB")
        value = float(max(int(size_bytes or 0), 0))
        unit_index = 0
        while value >= 1024 and unit_index < len(units) - 1:
            value /= 1024.0
            unit_index += 1
        return f"{value:.2f} {units[unit_index]}"

    def _looksLikeCollection(self, name):
        lowered = name.lower()
        return any(token in lowered for token in ("complete", "collection", "season", "pack"))

    def setAllFilesChecked(self, checked):
        state = Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked
        for index in range(self.filesTree.topLevelItemCount()):
            self._setItemChecked(self.filesTree.topLevelItem(index), state)

    def _setItemChecked(self, item, state):
        item.setCheckState(0, state)
        for index in range(item.childCount()):
            self._setItemChecked(item.child(index), state)

    def syncFileCheckState(self, item, column):
        if column != 0 or self._syncing_file_checks:
            return
        self._syncing_file_checks = True
        try:
            state = item.checkState(0)
            for index in range(item.childCount()):
                self._setItemChecked(item.child(index), state)
        finally:
            self._syncing_file_checks = False

    def filterFiles(self, text):
        pattern = text.strip().lower()
        for index in range(self.filesTree.topLevelItemCount()):
            self._filterItem(self.filesTree.topLevelItem(index), pattern)

    def _filterItem(self, item, pattern):
        child_match = False
        for index in range(item.childCount()):
            child_match = self._filterItem(item.child(index), pattern) or child_match
        own_match = not pattern or pattern in item.text(0).lower()
        item.setHidden(not own_match and not child_match)
        return own_match or child_match

    def showPriorityMenu(self, position):
        item = self.filesTree.itemAt(position)
        if item is None:
            return
        menu = QMenu(self)
        for priority in self.PRIORITIES:
            action = menu.addAction(priority)
            action.triggered.connect(lambda checked=False, value=priority, target=item: self.setPriority(target, value))
        menu.exec(self.filesTree.viewport().mapToGlobal(position))

    def setPriority(self, item, priority):
        item.setText(2, priority)
        for index in range(item.childCount()):
            self.setPriority(item.child(index), priority)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.sidebar_visible_min = 45
        self.sidebar_visible_max = 150
        self.sidebar_visible = True
        self.mediaplayer_visible = True
        self.ui.setupUi(self)
        self.installFooterLogScroller()
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
        self.include_nsfw = False
        self.data_dir = app_data_dir()
        self.settings = AppSettings(self.data_dir / "settings.json")
        self.dark_theme = self.settings.get("appearance", "theme", "dark") != "retro"
        self.setStyleSheet(styles_default if self.dark_theme else styles_retro)

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
        self._media_slider_scrubbing = False
        self.download_items = []
        self.download_engine = None
        self.torrent_state_dir = self.data_dir / "torrent_state"
        self.torrent_state_path = self.torrent_state_dir / "downloads.json"
        self.torrent_row_by_id = {}
        self.torrent_logs_by_id = {}
        self.torrent_files_by_id = {}
        self.torrent_trackers_by_id = {}
        self.torrent_peers_by_id = {}
        self.active_torrent_filter = self.settings.get("torrent", "active_filter", "all")
        self.total_downloaded_bytes = int(self.settings.get("torrent", "total_downloaded_bytes", 0) or 0)
        self._updating_torrent_details = False
        self._last_detail_refresh = {}
        self._last_resume_export = 0.0
        self._torrent_notification_events = set()
        self.default_download_dir = Path(self.settings.get("torrent", "download_dir", str(Path.home() / "Downloads"))).expanduser()

        self.initNetworkMonitor()
        self.initFavorites(self.data_dir / "favourites.json")
        self.initHistory(self.data_dir / "history.json")

        self.video_formats = [".webm", ".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", "mpeg", ".3gp", ".mts", ".ts", ".vob"]
        self.audio_formats = [".mp3", ".wav", ".aac", ".m4a", ".flac", ".ogg", ".wma"]
        self.initMediaPlayer()
        self.initFileManager()
        self.initDownloadManagerUi()

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

        self.torrent_poll_timer = QTimer(self)
        self.torrent_poll_timer.timeout.connect(self.pollTorrentEngine)
        self.torrent_poll_timer.setInterval(int(self.settings.get("torrent", "poll_interval_ms", 1000)))

        self.torrent_state_save_timer = QTimer(self)
        self.torrent_state_save_timer.setSingleShot(True)
        self.torrent_state_save_timer.timeout.connect(self.saveTorrentState)

        self.updateTotalDownloadedLabel()
        self.applyTheme(self.settings.get("appearance", "theme", "dark"), notify=False)
        self.restoreTorrentState()
        self.applyTorrentSidebarFilter(self.active_torrent_filter)

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
        self.ui.appResetBtn.setToolTip("Reload Bitroid services")
        self.ui.mediaProgressSlider.setToolTip("Drag to preview, release to seek")
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
        self.ui.appResetBtn.clicked.connect(self.reloadAppServices)
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

    def installFooterLogScroller(self):
        old_label = self.ui.logLabel
        new_label = ScrollingLabel(old_label.text(), old_label.parent())
        new_label.setObjectName(old_label.objectName())
        new_label.setSizePolicy(old_label.sizePolicy())
        new_label.setMinimumSize(old_label.minimumSize())
        new_label.setMaximumSize(old_label.maximumSize())
        new_label.setFont(old_label.font())
        new_label.setTextFormat(old_label.textFormat())
        new_label.setAlignment(old_label.alignment())
        new_label.setWordWrap(False)
        self.ui.horizontalLayout_10.replaceWidget(old_label, new_label)
        old_label.setParent(None)
        old_label.deleteLater()
        self.ui.logLabel = new_label

    def themedIcon(self, icon_path, size=18):
        icon = QIcon(icon_path)
        if self.dark_theme:
            return icon
        pixmap = icon.pixmap(size, size)
        if pixmap.isNull():
            return icon
        tinted = QPixmap(pixmap.size())
        tinted.fill(Qt.GlobalColor.transparent)
        painter = QPainter(tinted)
        painter.drawPixmap(0, 0, pixmap)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        painter.fillRect(tinted.rect(), QColor("#7b3f10"))
        painter.end()
        return QIcon(tinted)

    def setThemedButtonIcon(self, button, icon_path, size=None):
        button.setProperty("iconPath", icon_path)
        icon_size = size or max(button.iconSize().width(), button.iconSize().height(), 18)
        button.setIconSize(QSize(icon_size, icon_size))
        button.setIcon(self.themedIcon(icon_path, icon_size))

    def updateThemedIcons(self):
        for button in getattr(self, "torrentToolButtons", []):
            icon_path = button.property("iconPath")
            if icon_path:
                self.setThemedButtonIcon(button, icon_path, 18)

        media_icons = (
            (self.ui.mediaFolderBtn, ":/icons/icons/cil-folder-open.png", 18),
            (self.ui.playerUndockBtn, ":/icons/icons/cil-input.png", 16),
            (self.ui.mediaStopBtn, ":/icons/icons/cil-media-stop.png", 18),
            (self.ui.seekBackwardBtn, ":/icons/icons/cil-media-skip-backward.png", 20),
            (self.ui.mediaPreviousBtn, ":/icons/icons/cil-media-step-backward.png", 20),
            (self.ui.mediaNextBtn, ":/icons/icons/cil-media-step-forward.png", 20),
            (self.ui.seekForwardBtn, ":/icons/icons/cil-media-skip-forward.png", 20),
        )
        for button, icon_path, size in media_icons:
            self.setThemedButtonIcon(button, icon_path, size)
        if hasattr(self.ui, "appResetBtn"):
            self.setThemedButtonIcon(self.ui.appResetBtn, ":/icons/icons/cil-reload.png", 14)
        self.updateMediaRepeatIcon()
        self.updateMediaShuffleIcon()
        self.updateMediaMuteIcon()
        self.updatePlayerLockIcon()
        if hasattr(self, "media_player"):
            self.updateMediaPlaybackState(self.media_player.playbackState())

    def applyTheme(self, theme, notify=False):
        theme = "retro" if theme == "retro" else "dark"
        if theme == "retro":
            self.ui.themeBtn.setIcon(QIcon(':/icons/icons/cil-moon.png'))
            self.setStyleSheet(styles_retro)
            self.dark_theme = False
            if notify:
                self.pushNotification("Theme changed to 'Retro' for the Bitroid DM", "Retro Theme")
        else:
            self.ui.themeBtn.setIcon(QIcon(':/icons/icons/cil-lightbulb.png'))
            self.setStyleSheet(styles_default)
            self.dark_theme = True
            if notify:
                self.pushNotification("Theme changed to 'Default' for the Bitroid DM", "Default Theme")
        self.settings.set("appearance", "theme", theme)
        self.updateThemedIcons()
        self.repolishTorrentUi()
        QTimer.singleShot(0, self.repolishTorrentUi)

    def toggleTheme(self):
        self.applyTheme("retro" if self.dark_theme else "dark", notify=True)

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

    def initDownloadManagerUi(self):
        self._clearLayout(self.ui.verticalLayout_15)

        container = QFrame(self.ui.downloadStack)
        container.setObjectName("torrentManagerWidget")
        root = QVBoxLayout(container)
        root.setContentsMargins(8, 8, 8, 6)
        root.setSpacing(8)

        toolbar = QFrame(container)
        toolbar.setObjectName("torrentToolbar")
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(0, 0, 0, 0)
        toolbar_layout.setSpacing(6)

        self.torrentAddMagnetBtn = self._torrentToolButton("Add magnet", ":/icons/icons/cil-link.png")
        self.torrentAddFileBtn = self._torrentToolButton("Add torrent file", ":/icons/icons/file-plus.svg")
        self.torrentStartAllBtn = self._torrentToolButton("Start all", ":/icons/icons/play.svg")
        self.torrentPauseAllBtn = self._torrentToolButton("Pause all", ":/icons/icons/pause.svg")
        self.torrentRemoveBtn = self._torrentToolButton("Remove", ":/icons/icons/trash-2.svg")
        self.torrentSettingsBtn = self._torrentToolButton("Torrent settings", ":/icons/icons/settings.svg")
        self.torrentToolButtons = (
            self.torrentAddMagnetBtn,
            self.torrentAddFileBtn,
            self.torrentStartAllBtn,
            self.torrentPauseAllBtn,
            self.torrentRemoveBtn,
            self.torrentSettingsBtn,
        )
        for button in self.torrentToolButtons:
            toolbar_layout.addWidget(button)
        toolbar_layout.addStretch(1)

        self.torrentFilterInput = QLineEdit(toolbar)
        self.torrentFilterInput.setObjectName("torrentFilterInput")
        self.torrentFilterInput.setPlaceholderText("Filter torrents...")
        self.torrentFilterInput.textChanged.connect(self.filterDownloadRows)
        toolbar_layout.addWidget(self.torrentFilterInput)

        self.torrentFilterCombo = QComboBox(toolbar)
        self.torrentFilterCombo.setObjectName("torrentFilterCombo")
        self.torrentFilterCombo.addItems(["Name", "Status", "Save path"])
        self.torrentFilterCombo.currentTextChanged.connect(self.filterDownloadRows)
        toolbar_layout.addWidget(self.torrentFilterCombo)
        root.addWidget(toolbar)

        manager_splitter = QSplitter(Qt.Orientation.Horizontal, container)
        manager_splitter.setObjectName("torrentMainSplitter")
        manager_splitter.setHandleWidth(4)
        root.addWidget(manager_splitter, 1)

        sidebar = QFrame(manager_splitter)
        sidebar.setObjectName("torrentSidebar")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(8, 8, 8, 8)
        sidebar_layout.setSpacing(4)
        self.torrentFilterButtons = {}
        self._addTorrentSidebarGroup(sidebar_layout, "STATUS", [
            ("all", "All"),
            ("downloading", "Downloading"),
            ("seeding", "Seeding"),
            ("completed", "Completed"),
            ("running", "Running"),
            ("paused", "Paused"),
            ("checking", "Checking"),
            ("errored", "Errored"),
        ])
        self._addTorrentSidebarGroup(sidebar_layout, "TRACKERS", [("tracker_all", "All"), ("tracker_error", "With errors")])
        sidebar_layout.addStretch(1)
        manager_splitter.addWidget(sidebar)

        right_pane = QFrame(manager_splitter)
        right_pane.setObjectName("torrentRightPane")
        right_layout = QVBoxLayout(right_pane)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(8)
        manager_splitter.addWidget(right_pane)

        self.torrentDetailSplitter = QSplitter(Qt.Orientation.Vertical, right_pane)
        self.torrentDetailSplitter.setObjectName("torrentDetailSplitter")
        self.torrentDetailSplitter.setHandleWidth(6)
        right_layout.addWidget(self.torrentDetailSplitter, 1)

        self.torrentTable = QTableWidget(0, 10, self.torrentDetailSplitter)
        self.torrentTable.setObjectName("torrentTable")
        self.torrentTable.setHorizontalHeaderLabels(["Name", "Size", "Progress", "Availability", "Status", "Seeds", "Peers", "Down Speed", "Up Speed", "ETA"])
        self.torrentTable.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.torrentTable.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        configure_torrent_header(self.torrentTable, [320, 74, 86, 86, 82, 58, 58, 92, 82, 70])
        self.torrentTable.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.torrentTable.itemSelectionChanged.connect(self.updateTorrentDetailsFromSelection)
        self.torrentTable.customContextMenuRequested.connect(self.showTorrentContextMenu)
        self.torrentDetailSplitter.addWidget(self.torrentTable)

        detail_tabs = QTabWidget(self.torrentDetailSplitter)
        detail_tabs.setObjectName("torrentDetailTabs")
        self.torrentDetailTabs = detail_tabs
        detail_tabs.addTab(self._buildTorrentOverviewTab(), QIcon(":/icons/icons/info.svg"), "Overview")
        detail_tabs.addTab(self._buildTorrentFilesTab(), QIcon(":/icons/icons/folder.svg"), "Files")
        detail_tabs.addTab(self._buildTorrentTrackersTab(), QIcon(":/icons/icons/globe.svg"), "Trackers")
        detail_tabs.addTab(self._buildTorrentPeersTab(), QIcon(":/icons/icons/users.svg"), "Peers")
        detail_tabs.addTab(self._buildTorrentLogsTab(), QIcon(":/icons/icons/terminal.svg"), "Logs")
        detail_tabs.currentChanged.connect(lambda _index: self.updateTorrentDetailsFromSelection())
        self.torrentDetailSplitter.addWidget(detail_tabs)
        self.torrentDetailSplitter.setStretchFactor(0, 3)
        self.torrentDetailSplitter.setStretchFactor(1, 2)
        self.torrentDetailSplitter.setSizes([360, 220])

        manager_splitter.setSizes([150, 680])
        self.ui.verticalLayout_15.addWidget(container)

        self.torrentAddMagnetBtn.clicked.connect(self.openManualMagnetDialog)
        self.torrentAddFileBtn.clicked.connect(self.openTorrentFileDialog)
        self.torrentStartAllBtn.clicked.connect(self.resumeSelectedOrAllTorrents)
        self.torrentPauseAllBtn.clicked.connect(self.pauseSelectedOrAllTorrents)
        self.torrentRemoveBtn.clicked.connect(self.removeSelectedTorrent)
        self.updateDownloadSidebarCounts()
        self.showEmptyTorrentDetails()
        self.repolishTorrentUi()

    def _clearLayout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            child_layout = item.layout()
            widget = item.widget()
            if child_layout is not None:
                self._clearLayout(child_layout)
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

    def _torrentToolButton(self, tooltip, icon_path):
        button = QToolButton()
        button.setObjectName("torrentToolButton")
        button.setProperty("iconPath", icon_path)
        button.setToolTip(tooltip)
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(18, 18))
        button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        return button

    def _addTorrentSidebarGroup(self, layout, title, items):
        title_label = QLabel(title)
        title_label.setObjectName("torrentSidebarTitle")
        layout.addWidget(title_label)
        for key, label in items:
            button = QPushButton()
            button.setObjectName("torrentSidebarButton")
            button.setText(f"{label} (0)")
            button.setProperty("filterKey", key)
            button.setCheckable(True)
            button.setChecked(key == self.active_torrent_filter)
            button.setProperty("active", key == self.active_torrent_filter)
            button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            button.clicked.connect(lambda checked=False, value=key: self.applyTorrentSidebarFilter(value))
            self.torrentFilterButtons[key] = button
            layout.addWidget(button)

    def repolishTorrentUi(self):
        widgets = []
        for name in (
            "torrentTable",
            "torrentFilesTree",
            "torrentAddMagnetBtn",
            "torrentAddFileBtn",
            "torrentStartAllBtn",
            "torrentPauseAllBtn",
            "torrentRemoveBtn",
            "torrentSettingsBtn",
            "torrentFilterCombo",
            "torrentFilterInput",
            "torrentTrackersTable",
            "torrentPeersTable",
            "torrentLogsTable",
            "torrentDetailTabs",
            "torrentDetailSplitter",
            "torrentPieceMap",
        ):
            widget = getattr(self, name, None)
            if widget is not None:
                widgets.append(widget)
                if hasattr(widget, "horizontalHeader"):
                    header = widget.horizontalHeader()
                    self.applyTorrentHeaderStyle(header)
                    widgets.append(header)
                elif hasattr(widget, "header"):
                    header = widget.header()
                    self.applyTorrentHeaderStyle(header)
                    widgets.append(header)
        for table in getattr(self, "torrentOverviewTables", {}).values():
            widgets.append(table)
            self.applyTorrentHeaderStyle(table.horizontalHeader())
            widgets.append(table.horizontalHeader())
        widgets.extend(getattr(self, "torrentFilterButtons", {}).values())
        for widget in widgets:
            repolish_widget(widget)

    def applyTorrentHeaderStyle(self, header):
        if self.dark_theme:
            background = "#2f3136"
            foreground = "#dddddd"
            border = "#3b3d40"
            pressed = "#363941"
        else:
            background = "#efc58d"
            foreground = "#080808"
            border = "#d8a06c"
            pressed = "#e2b276"
        header.setStyleSheet(f"""
            QHeaderView {{
                background: {background};
                color: {foreground};
                border: 0px;
            }}
            QHeaderView::section {{
                background: {background};
                color: {foreground};
                font-size: 12px;
                font-family: "Segoe UI";
                font-weight: 600;
                padding: 1px 6px;
                min-height: 18px;
                border: 0px;
                border-right: 1px solid {border};
                border-bottom: 1px solid {border};
            }}
            QHeaderView::section:pressed,
            QHeaderView::section:checked {{
                background: {pressed};
                color: {foreground};
            }}
        """)

    def _buildTorrentOverviewTab(self):
        tab = QScrollArea()
        tab.setObjectName("torrentOverviewScroll")
        tab.setWidgetResizable(True)
        content = QFrame()
        content.setObjectName("torrentOverviewTab")
        layout = QVBoxLayout(content)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        self.torrentOverviewProgress = QProgressBar(content)
        self.torrentOverviewProgress.setObjectName("torrentOverviewProgress")
        self.torrentOverviewProgress.setRange(0, 1000)
        layout.addWidget(self.torrentOverviewProgress)

        self.torrentPieceMap = TorrentPieceMap(content)
        layout.addWidget(self.torrentPieceMap)

        self.torrentOverviewLabels = {}
        self.torrentOverviewTables = {}
        for section, fields in {
            "Transfer": ("Status", "Availability", "Downloaded", "Uploaded", "Download Speed", "Upload Speed", "ETA", "Seeds", "Peers", "Connections", "Share Ratio"),
            "Information": ("Name", "Total Size", "Save Path", "Info Hash", "Added On", "Completed On"),
        }.items():
            frame = QFrame(content)
            frame.setObjectName("torrentInfoSection")
            frame_layout = QVBoxLayout(frame)
            frame_layout.setContentsMargins(10, 8, 10, 10)
            frame_layout.setSpacing(6)
            title = QLabel(section, frame)
            title.setObjectName("torrentSectionTitle")
            frame_layout.addWidget(title)
            table = QTableWidget(len(fields), 2, frame)
            table.setObjectName("torrentOverviewTable")
            table.setHorizontalHeaderLabels(["Field", "Value"])
            configure_torrent_header(table, [132, 420], stretch_last=True)
            table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
            table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            for row, field in enumerate(fields):
                field_item = QTableWidgetItem(field)
                field_item.setFlags(field_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                value_item = QTableWidgetItem("-")
                value_item.setFlags(value_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                table.setItem(row, 0, field_item)
                table.setItem(row, 1, value_item)
                self.torrentOverviewLabels[field] = value_item
            table.setMinimumHeight(22 * (len(fields) + 1) + 6)
            frame_layout.addWidget(table)
            self.torrentOverviewTables[section] = table
            layout.addWidget(frame)
        layout.addStretch(1)
        tab.setWidget(content)
        return tab

    def _buildTorrentFilesTab(self):
        tab = QFrame()
        tab.setObjectName("torrentFilesTab")
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        toolbar = QHBoxLayout()
        select_all_btn = QPushButton("Select All")
        select_all_btn.setObjectName("torrentMiniButton")
        select_none_btn = QPushButton("Select None")
        select_none_btn.setObjectName("torrentMiniButton")
        select_all_btn.clicked.connect(lambda: self.setDownloadDetailFilesChecked(True))
        select_none_btn.clicked.connect(lambda: self.setDownloadDetailFilesChecked(False))
        self.torrentFilesFilterInput = QLineEdit()
        self.torrentFilesFilterInput.setObjectName("torrentFilterInput")
        self.torrentFilesFilterInput.setPlaceholderText("Filter files...")
        self.torrentFilesFilterInput.textChanged.connect(self.filterDownloadDetailFiles)
        toolbar.addWidget(select_all_btn)
        toolbar.addWidget(select_none_btn)
        toolbar.addStretch(1)
        toolbar.addWidget(self.torrentFilesFilterInput)
        layout.addLayout(toolbar)
        self.torrentFilesTree = QTreeWidget(tab)
        self.torrentFilesTree.setObjectName("torrentFilesTree")
        self.torrentFilesTree.setColumnCount(5)
        self.torrentFilesTree.setHeaderLabels(["Name", "Total Size", "Progress", "Priority", "Remaining"])
        configure_torrent_header(self.torrentFilesTree, [320, 90, 86, 90, 90])
        self.torrentFilesTree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.torrentFilesTree.customContextMenuRequested.connect(self.showDownloadFilePriorityMenu)
        self.torrentFilesTree.itemChanged.connect(self.syncDownloadFileCheckState)
        layout.addWidget(self.torrentFilesTree)
        return tab

    def _buildTorrentTrackersTab(self):
        self.torrentTrackersTable = QTableWidget(0, 6)
        self.torrentTrackersTable.setObjectName("torrentTrackersTable")
        self.torrentTrackersTable.setHorizontalHeaderLabels(["URL / Announce", "Tier", "Protocol", "Status", "Peers", "Seeds"])
        configure_torrent_header(self.torrentTrackersTable, [300, 60, 80, 120, 70, 70])
        return self.torrentTrackersTable

    def _buildTorrentPeersTab(self):
        self.torrentPeersTable = QTableWidget(0, 7)
        self.torrentPeersTable.setObjectName("torrentPeersTable")
        self.torrentPeersTable.setHorizontalHeaderLabels(["Country", "IP / Address", "Port", "Connection", "Client", "Progress", "Down Speed"])
        configure_torrent_header(self.torrentPeersTable, [70, 190, 70, 100, 160, 80, 90])
        return self.torrentPeersTable

    def _buildTorrentLogsTab(self):
        self.torrentLogsTable = QTableWidget(0, 3)
        self.torrentLogsTable.setObjectName("torrentLogsTable")
        self.torrentLogsTable.setHorizontalHeaderLabels(["Time", "Event", "Message"])
        configure_torrent_header(self.torrentLogsTable, [120, 140, 520])
        return self.torrentLogsTable

    def openManualMagnetDialog(self):
        dialog = QDialog(self)
        dialog.setObjectName("torrentMagnetDialog")
        dialog.setWindowTitle("Add magnet link")
        dialog.setMinimumSize(520, 140)
        dialog.resize(560, 150)
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(14, 12, 14, 14)
        layout.setSpacing(10)
        title = QLabel("Add magnet link", dialog)
        title.setObjectName("torrentAddTitle")
        layout.addWidget(title)
        magnet_input = QLineEdit(dialog)
        magnet_input.setObjectName("torrentAddPathInput")
        magnet_input.setPlaceholderText("Paste magnet link...")
        clipboard_text = QApplication.clipboard().text().strip()
        if clipboard_text.startswith("magnet:"):
            magnet_input.setText(clipboard_text)
        layout.addWidget(magnet_input)
        actions = QHBoxLayout()
        actions.addStretch(1)
        cancel_btn = QPushButton("Cancel", dialog)
        cancel_btn.setObjectName("torrentSecondaryButton")
        cancel_btn.clicked.connect(dialog.reject)
        continue_btn = QPushButton("Continue", dialog)
        continue_btn.setObjectName("torrentPrimaryButton")
        continue_btn.clicked.connect(dialog.accept)
        actions.addWidget(cancel_btn)
        actions.addWidget(continue_btn)
        layout.addLayout(actions)
        if dialog.exec() == QDialog.DialogCode.Accepted and magnet_input.text().strip():
            self.showAddTorrentDialog({"name": "Magnet link", "magnet": magnet_input.text().strip(), "size": "Metadata pending"})

    def openTorrentFileDialog(self):
        torrent_path, _ = QFileDialog.getOpenFileName(self, "Open torrent file", str(self.default_download_dir), "Torrent files (*.torrent)")
        if not torrent_path:
            return
        path = Path(torrent_path)
        self.showAddTorrentDialog({"name": path.stem, "magnet": "", "size": self.formatFileSize(path.stat().st_size), "path": str(path)})

    def showAddTorrentDialog(self, result):
        dialog = TorrentAddDialog(result, self.default_download_dir, self)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        options = dialog.selectedOptions()
        if dialog.rememberPathCheck.isChecked():
            self.default_download_dir = Path(options["save_path"]).expanduser()
            self.settings.set("torrent", "download_dir", str(self.default_download_dir))
        self.addTorrentDownload(options)

    def ensureTorrentDownloadEngine(self, quiet=False):
        if self.download_engine is not None:
            return True

        session_settings = {
            "enable_dht": bool(self.settings.get("torrent", "enable_dht", True)),
            "enable_lsd": bool(self.settings.get("torrent", "enable_lsd", True)),
            "enable_upnp": bool(self.settings.get("torrent", "enable_upnp", True)),
            "enable_natpmp": bool(self.settings.get("torrent", "enable_natpmp", True)),
            "listen_interfaces": self.settings.get("torrent", "listen_interfaces", "0.0.0.0:6881,[::]:6881"),
        }
        try:
            self.download_engine = TorrentEngine(self.default_download_dir, session_settings=session_settings)
            self.download_engine.enable_client_alerts()
            self.download_engine.on("*", self.handleTorrentEngineEvent)
        except LibtorrentUnavailableError as error:
            if not quiet:
                self.pushNotification(str(error), "Torrent Engine")
            self.download_engine = None
            return False
        except Exception as error:
            if not quiet:
                self.pushNotification(f"Could not start torrent engine: {error}", "Torrent Engine")
            self.download_engine = None
            return False

        if not quiet:
            self.pushNotification("Torrent engine is ready.", "Torrent Engine")
        return True

    def addTorrentDownload(self, options, restoring=False):
        item = self.createDownloadPayload(options)
        row = self.addDownloadRow(item)
        self.torrentTable.selectRow(row)
        if not restoring:
            self.showDownloads()

        if not self.ensureTorrentDownloadEngine(quiet=restoring):
            item["status"] = "Engine unavailable"
            item["error"] = "libtorrent unavailable"
            self.refreshTorrentRow(row, item)
            self.saveTorrentState()
            return

        try:
            paused = bool(options.get("paused", not options.get("start", True)))
            if options.get("resume_data"):
                torrent_id = self.download_engine.add_resume_data(
                    options["resume_data"],
                    options.get("save_path", self.default_download_dir),
                    paused=paused,
                    sequential=bool(options.get("sequential", False)),
                )
            elif options.get("path"):
                torrent_id = self.download_engine.add_torrent_file(
                    options["path"],
                    options.get("save_path", self.default_download_dir),
                    paused=paused,
                    sequential=bool(options.get("sequential", False)),
                )
            else:
                magnet = options.get("magnet", "").strip()
                if not magnet:
                    raise ValueError("No magnet link or .torrent file was provided.")
                torrent_id = self.download_engine.add_magnet(
                    magnet,
                    options.get("save_path", self.default_download_dir),
                    paused=paused,
                    sequential=bool(options.get("sequential", False)),
                )
        except Exception as error:
            item["status"] = "Errored"
            item["error"] = str(error)
            self.refreshTorrentRow(row, item)
            self.saveTorrentState()
            if not restoring:
                self.pushNotification(str(error), "Torrent Add Failed")
            return

        item["torrent_id"] = torrent_id
        self.torrent_row_by_id[torrent_id] = row
        self.torrent_logs_by_id.setdefault(torrent_id, [])
        self.applyInitialFilePriorities(torrent_id, options.get("files", []))
        self.refreshTorrentRow(row, item)
        self.updateDownloadSidebarCounts()
        if not self.torrent_poll_timer.isActive():
            self.torrent_poll_timer.start()
        self.pollTorrentEngine()
        self.saveTorrentState(force_resume=True)
        if not restoring:
            self.pushNotification("Torrent attached to Bitroid engine.", "Torrent Added")

    def applyInitialFilePriorities(self, torrent_id, files):
        if self.download_engine is None or not torrent_id:
            return
        for file in files or []:
            file_index = file.get("index")
            if not isinstance(file_index, int) or file_index < 0:
                continue
            selected = bool(file.get("selected", True))
            priority = self.priorityValue(file.get("priority", "Normal")) if selected else 0
            try:
                self.download_engine.set_file_priority(torrent_id, file_index, priority)
            except Exception as error:
                self.appendTorrentLog(torrent_id, "file_priority_failed", str(error))

    def createDownloadPayload(self, options):
        status = options.get("status") or ("Queued" if options.get("start", True) else "Paused")
        return {
            "torrent_id": options.get("torrent_id", ""),
            "name": options.get("name", "Torrent"),
            "size": options.get("size") or self._firstKnownSize(options),
            "progress": float(options.get("progress", 0.0) or 0.0),
            "availability": options.get("availability", "-"),
            "status": status,
            "seeds": options.get("seeds", "-"),
            "peers": options.get("peers", "-"),
            "connections": options.get("connections", "-"),
            "download_speed": options.get("download_speed", "0.00 B/s"),
            "upload_speed": options.get("upload_speed", "0.00 B/s"),
            "downloaded": options.get("downloaded", "0.00 B"),
            "uploaded": options.get("uploaded", "0.00 B"),
            "eta": options.get("eta", "-"),
            "save_path": options.get("save_path", str(self.default_download_dir)),
            "files": options.get("files", []),
            "trackers": options.get("trackers", []),
            "peers_list": options.get("peers_list", []),
            "magnet": options.get("magnet", ""),
            "path": options.get("path", ""),
            "resume_data": options.get("resume_data", ""),
            "site": options.get("site", ""),
            "sequential": bool(options.get("sequential", False)),
            "first_last": bool(options.get("first_last", False)),
            "skip_hash_check": bool(options.get("skip_hash_check", False)),
            "paused_intent": bool(options.get("paused", not options.get("start", True))),
            "engine_downloaded_bytes": int(options.get("engine_downloaded_bytes", 0) or 0),
            "added_on": options.get("added_on", self.timeNow()),
            "completed_on": options.get("completed_on", "-"),
            "error": options.get("error", ""),
        }

    def addDownloadPreview(self, options):
        item = self.createDownloadPayload(options)
        row = self.addDownloadRow(item)
        self.torrentTable.selectRow(row)
        self.showDownloads()

    def formatStorageAmount(self, size_bytes):
        units = ("B", "KB", "MB", "GB", "TB", "PB")
        value = float(max(int(size_bytes or 0), 0))
        unit_index = 0
        while value >= 1024.0 and unit_index < len(units) - 1:
            value /= 1024.0
            unit_index += 1
        return f"{value:.1f} {units[unit_index]}"

    def updateTotalDownloadedLabel(self):
        self.ui.totalDownloadedLabel.setText(self.formatStorageAmount(self.total_downloaded_bytes))
        self.ui.totalDownloadedLabel.setToolTip("Total downloaded by Bitroid torrent client")

    def scheduleTorrentStateSave(self):
        if hasattr(self, "torrent_state_save_timer"):
            if not self.torrent_state_save_timer.isActive():
                self.torrent_state_save_timer.start(1500)
        else:
            self.saveTorrentState()

    def torrentStatePayload(self, export_resume=False):
        torrents = []
        for item in self.download_items:
            payload = dict(item)
            torrent_id = payload.get("torrent_id", "")
            if export_resume and self.download_engine is not None and torrent_id:
                try:
                    payload["resume_data"] = self.download_engine.export_resume_data(torrent_id)
                except Exception:
                    pass
            for transient_key in ("download_speed", "upload_speed", "peers_list"):
                payload.pop(transient_key, None)
            torrents.append(payload)
        return {
            "version": 1,
            "active_filter": self.active_torrent_filter,
            "total_downloaded_bytes": self.total_downloaded_bytes,
            "torrents": torrents,
        }

    def saveTorrentState(self, force_resume=False):
        try:
            self.torrent_state_dir.mkdir(parents=True, exist_ok=True)
            now = time.monotonic()
            export_resume = force_resume or (now - self._last_resume_export >= 30.0)
            if export_resume:
                self._last_resume_export = now
            temp_path = self.torrent_state_path.with_suffix(".json.tmp")
            with open(temp_path, "w", encoding="utf-8") as file:
                json.dump(self.torrentStatePayload(export_resume=export_resume), file, indent=4)
                file.write("\n")
            temp_path.replace(self.torrent_state_path)
            self.settings.set("torrent", "total_downloaded_bytes", self.total_downloaded_bytes)
            self.settings.set("torrent", "active_filter", self.active_torrent_filter)
            self.settings.save()
        except OSError as error:
            self.pushNotification(str(error), "Torrent State Save Failed")

    def loadTorrentState(self):
        try:
            with open(self.torrent_state_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            return data if isinstance(data, dict) else {}
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            return {}

    def restoreTorrentState(self):
        data = self.loadTorrentState()
        self.active_torrent_filter = data.get("active_filter", self.active_torrent_filter)
        self.total_downloaded_bytes = int(data.get("total_downloaded_bytes", self.total_downloaded_bytes) or 0)
        for saved in data.get("torrents", []):
            if not isinstance(saved, dict):
                continue
            options = dict(saved)
            status = str(options.get("status", "")).lower()
            options["paused"] = bool(options.get("paused_intent", status in ("paused", "stopped", "completed")))
            options["start"] = not options["paused"]
            source_available = options.get("resume_data") or options.get("path") or options.get("magnet")
            if source_available:
                self.addTorrentDownload(options, restoring=True)
            else:
                row = self.addDownloadRow(self.createDownloadPayload(options))
                self.refreshTorrentRow(row, self._downloadPayloadForRow(row))
        self.updateTotalDownloadedLabel()

    def addDownloadRow(self, item):
        self.download_items.append(item)
        row = self.torrentTable.rowCount()
        self.torrentTable.insertRow(row)
        self._setTorrentTableItem(row, 0, item["name"], item)
        self._setTorrentTableItem(row, 1, item["size"])
        progress = QProgressBar(self.torrentTable)
        progress.setObjectName("torrentRowProgress")
        progress.setRange(0, 1000)
        progress_value = float(item.get("progress", 0.0) or 0.0)
        progress.setValue(int(progress_value * 10))
        progress.setFormat(f"{progress_value:.1f}%")
        self.torrentTable.setCellWidget(row, 2, progress)
        for column, key in enumerate(("availability", "status", "seeds", "peers", "download_speed", "upload_speed", "eta"), start=3):
            self._setTorrentTableItem(row, column, str(item[key]))
        self.updateDownloadSidebarCounts()
        return row

    def _firstKnownSize(self, options):
        files = options.get("files") or []
        for file in files:
            size = file.get("size")
            if size and size != "Metadata":
                return size
        return self.resultSizeFallback(options.get("name", ""))

    def resultSizeFallback(self, name):
        return "Metadata ready" if name == "Magnet link" else "Metadata"

    def _setTorrentTableItem(self, row, column, text, payload=None):
        table_item = QTableWidgetItem(str(text))
        table_item.setFlags(table_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        table_item.setToolTip(str(text))
        if payload is not None:
            table_item.setData(Qt.ItemDataRole.UserRole, payload)
        self.torrentTable.setItem(row, column, table_item)

    def setTorrentCellText(self, row, column, text):
        item = self.torrentTable.item(row, column)
        if item is None:
            self._setTorrentTableItem(row, column, text)
            return
        item.setText(str(text))
        item.setToolTip(str(text))

    def refreshTorrentRow(self, row, payload):
        if row < 0 or row >= self.torrentTable.rowCount():
            return
        name_item = self.torrentTable.item(row, 0)
        if name_item is not None:
            name_item.setData(Qt.ItemDataRole.UserRole, payload)
        self.setTorrentCellText(row, 0, payload.get("name", "-"))
        self.setTorrentCellText(row, 1, payload.get("size", "-"))
        progress = self.torrentTable.cellWidget(row, 2)
        if isinstance(progress, QProgressBar):
            percent = float(payload.get("progress", 0.0))
            progress.setValue(int(percent * 10))
            progress.setFormat(f"{percent:.1f}%")
        for column, key in enumerate(("availability", "status", "seeds", "peers", "download_speed", "upload_speed", "eta"), start=3):
            self.setTorrentCellText(row, column, payload.get(key, "-"))

    def pollTorrentEngine(self):
        if self.download_engine is None:
            self.torrent_poll_timer.stop()
            self.network_monitor.set_app_network_rates(0, 0)
            return

        try:
            snapshot = self.download_engine.tick()
        except Exception as error:
            self.pushNotification(f"Torrent engine polling failed: {error}", "Torrent Engine")
            self.torrent_poll_timer.stop()
            return

        speed = snapshot.get("speed", {})
        self.network_monitor.set_app_network_rates(
            speed.get("download_bps", 0),
            speed.get("upload_bps", 0),
        )
        for status in snapshot.get("statuses", []):
            self.applyTorrentStatusSnapshot(status)

        current_payload = self.selectedTorrentPayload()
        torrent_id = current_payload.get("torrent_id") if current_payload else ""
        if torrent_id:
            self.refreshSelectedTorrentDetails(torrent_id)

        self.updateDownloadSidebarCounts()
        if not snapshot.get("statuses"):
            self.torrent_poll_timer.stop()
            self.network_monitor.set_app_network_rates(0, 0)
        self.scheduleTorrentStateSave()

    def applyTorrentStatusSnapshot(self, status):
        torrent_id = status.get("torrent_id", "")
        row = self.torrent_row_by_id.get(torrent_id)
        if row is None:
            return
        payload = self._downloadPayloadForRow(row)
        if not payload:
            return

        progress_percent = float(status.get("progress", 0.0)) * 100.0
        total_wanted = int(status.get("total_wanted", 0))
        total_done = int(status.get("total_wanted_done", 0))
        all_time_download = int(status.get("all_time_download", 0))
        all_time_upload = int(status.get("all_time_upload", 0))
        previous_downloaded = int(payload.get("engine_downloaded_bytes", 0) or 0)
        if all_time_download > previous_downloaded:
            self.total_downloaded_bytes += all_time_download - previous_downloaded
            payload["engine_downloaded_bytes"] = all_time_download
            self.updateTotalDownloadedLabel()
        if status.get("name"):
            payload["name"] = status["name"]
        if total_wanted:
            payload["size"] = self.convert_size(total_wanted)
        payload["progress"] = progress_percent
        payload["availability"] = self.formatAvailability(status.get("distributed_copies", 0.0))
        payload["status"] = self.torrentStatusText(status)
        payload["seeds"] = str(status.get("num_seeds", 0))
        payload["peers"] = str(status.get("num_peers", 0))
        payload["connections"] = str(status.get("num_connections", 0))
        payload["download_speed"] = self.formatNetSpeed(int(status.get("download_rate", 0)))
        payload["upload_speed"] = self.formatNetSpeed(int(status.get("upload_rate", 0)))
        payload["downloaded"] = self.convert_size(total_done)
        payload["uploaded"] = self.convert_size(all_time_upload)
        payload["eta"] = self.formatEta(status.get("eta_seconds"))
        payload["save_path"] = status.get("save_path") or payload.get("save_path", "")
        payload["has_metadata"] = bool(status.get("has_metadata", False))
        payload["info_hash"] = torrent_id
        payload["error"] = status.get("error", "")
        if status.get("is_finished") and payload.get("completed_on") == "-":
            payload["completed_on"] = self.timeNow()
            self.notifyTorrentEvent(
                torrent_id,
                "finished",
                "Torrent Downloaded",
                f"{payload.get('name', 'Torrent')} is complete.",
            )
        self.refreshTorrentRow(row, payload)
        self.filterDownloadRows()

    def torrentStatusText(self, status):
        if status.get("error"):
            return "Errored"
        if status.get("is_seeding"):
            return "Seeding"
        if status.get("is_finished"):
            return "Completed"
        if status.get("paused"):
            return "Paused"
        if not status.get("has_metadata", False):
            return "Retrieving metadata"
        state = str(status.get("state", "")).replace("_", " ").strip()
        return state.title() if state else "Running"

    def formatAvailability(self, copies):
        try:
            value = float(copies)
        except (TypeError, ValueError):
            return "-"
        return f"{value:.3f}" if value > 0 else "-"

    def formatEta(self, seconds):
        if seconds is None:
            return "-"
        try:
            seconds = int(seconds)
        except (TypeError, ValueError):
            return "-"
        if seconds <= 0:
            return "0s"
        hours, remainder = divmod(seconds, 3600)
        minutes, secs = divmod(remainder, 60)
        if hours:
            return f"{hours}h {minutes}m"
        if minutes:
            return f"{minutes}m {secs}s"
        return f"{secs}s"

    def selectedTorrentPayload(self):
        return self._downloadPayloadForRow(self.torrentTable.currentRow())

    def selectedTorrentId(self):
        payload = self.selectedTorrentPayload()
        return payload.get("torrent_id", "") if payload else ""

    def handleTorrentEngineEvent(self, payload):
        event = payload.get("event", "alert")
        torrent_id = payload.get("torrent_id")
        if not torrent_id:
            return

        if event in {"alert", "piece_finished", "peer_connected", "peer_disconnected"}:
            return

        message = payload.get("message") or event.replace("_", " ").title()
        self.appendTorrentLog(torrent_id, event, message)
        self.notifyTorrentAlert(torrent_id, event, message)
        if event in {"metadata_received", "finished", "paused", "resumed", "checked", "storage_moved", "file_priority_changed", "resume_data_ready"}:
            self.scheduleTorrentStateSave()

    def notifyTorrentAlert(self, torrent_id, event, message):
        titles = {
            "metadata_received": "Torrent Metadata Ready",
            "finished": "Torrent Downloaded",
            "checked": "Torrent Checked",
            "storage_moved": "Torrent Moved",
            "error": "Torrent Error",
            "metadata_failed": "Metadata Failed",
            "resume_data_failed": "Torrent State Warning",
            "storage_move_failed": "Move Failed",
            "tracker_error": "Tracker Warning",
        }
        title = titles.get(event)
        if not title:
            return
        row = self.torrent_row_by_id.get(torrent_id, -1)
        payload = self._downloadPayloadForRow(row) or {}
        name = payload.get("name") or payload.get("torrent_id") or "Torrent"
        if event == "finished":
            message = f"{name} is complete."
        elif event == "metadata_received":
            message = f"{name} is ready to download."
        else:
            message = str(message)
        self.notifyTorrentEvent(torrent_id, event, title, message)

    def notifyTorrentEvent(self, torrent_id, event, title, message):
        key = (str(torrent_id), str(event))
        if key in self._torrent_notification_events:
            return
        self._torrent_notification_events.add(key)
        self.pushNotification(message, title)

    def appendTorrentLog(self, torrent_id, event, message):
        rows = self.torrent_logs_by_id.setdefault(torrent_id, [])
        rows.append((self.timeNow(), str(event), str(message)))
        del rows[:-300]
        if self.selectedTorrentId() == torrent_id:
            self.populateTorrentLogs(rows)

    def refreshSelectedTorrentDetails(self, torrent_id, force=False):
        now = time.monotonic()
        if not force and now - self._last_detail_refresh.get(torrent_id, 0.0) < 2.0:
            return
        self._last_detail_refresh[torrent_id] = now

        if self.download_engine is None:
            return
        payload = self.selectedTorrentPayload()
        if not payload or payload.get("torrent_id") != torrent_id:
            return

        active_tab = self.torrentDetailTabs.currentIndex() if hasattr(self, "torrentDetailTabs") else 0
        files = payload.get("files", [])
        trackers = payload.get("trackers", [])
        peers = payload.get("peers_list", [])
        try:
            if active_tab == 1:
                files = [file.to_dict() for file in self.download_engine.file_statuses(torrent_id)]
            elif active_tab == 2:
                trackers = self.download_engine.tracker_statuses(torrent_id)
            elif active_tab == 3:
                peers = self.download_engine.peer_statuses(torrent_id)
        except Exception as error:
            self.appendTorrentLog(torrent_id, "details_error", str(error))
            return

        payload["files"] = files
        payload["trackers"] = trackers
        payload["peers_list"] = peers
        self.torrent_files_by_id[torrent_id] = files
        self.torrent_trackers_by_id[torrent_id] = trackers
        self.torrent_peers_by_id[torrent_id] = peers
        self.populateTorrentDetails(payload)

    def showTorrentContextMenu(self, position):
        row = self.torrentTable.rowAt(position.y())
        if row < 0:
            return
        self.torrentTable.selectRow(row)
        payload = self._downloadPayloadForRow(row)
        if not payload:
            return

        menu = QMenu(self)
        stop_action = menu.addAction(QIcon(":/icons/icons/pause.svg"), "Stop")
        resume_action = menu.addAction(QIcon(":/icons/icons/play.svg"), "Force Start")
        menu.addSeparator()
        remove_action = menu.addAction(QIcon(":/icons/icons/trash-2.svg"), "Remove")
        menu.addSeparator()
        location_action = menu.addAction(QIcon(":/icons/icons/folder.svg"), "Set location...")
        rename_action = menu.addAction(QIcon(":/icons/icons/edit-2.svg"), "Rename...")
        menu.addSeparator()
        sequential_action = menu.addAction("Download in sequential order")
        sequential_action.setCheckable(True)
        sequential_action.setChecked(bool(payload.get("sequential", False)))
        first_last_action = menu.addAction("Download first and last pieces first")
        first_last_action.setCheckable(True)
        first_last_action.setChecked(bool(payload.get("first_last", False)))
        menu.addSeparator()
        recheck_action = menu.addAction(QIcon(":/icons/icons/refresh-cw.svg"), "Force recheck")
        resume_data_action = menu.addAction(QIcon(":/icons/icons/save.svg"), "Save resume data")
        menu.addSeparator()
        open_folder_action = menu.addAction(QIcon(":/icons/icons/folder.svg"), "Open destination folder")
        copy_magnet_action = menu.addAction(QIcon(":/icons/icons/clipboard.svg"), "Copy magnet link")
        copy_hash_action = menu.addAction(QIcon(":/icons/icons/hash.svg"), "Copy info hash")

        has_engine_id = bool(payload.get("torrent_id"))
        for action in (
            stop_action,
            resume_action,
            remove_action,
            location_action,
            recheck_action,
            resume_data_action,
            sequential_action,
            first_last_action,
        ):
            action.setEnabled(has_engine_id)

        chosen = menu.exec(self.torrentTable.viewport().mapToGlobal(position))
        if chosen is None:
            return
        if chosen == stop_action:
            self.pauseSelectedTorrent()
        elif chosen == resume_action:
            self.resumeSelectedTorrent()
        elif chosen == remove_action:
            self.removeSelectedTorrent()
        elif chosen == location_action:
            self.moveSelectedTorrent()
        elif chosen == rename_action:
            self.renameSelectedTorrent()
        elif chosen == sequential_action:
            self.setSelectedTorrentSequential(sequential_action.isChecked())
        elif chosen == first_last_action:
            payload["first_last"] = first_last_action.isChecked()
            self.scheduleTorrentStateSave()
            self.pushNotification("First/last piece mode will apply when the engine exposes that toggle safely.", "Torrent Option")
        elif chosen == recheck_action:
            self.forceRecheckSelectedTorrent()
        elif chosen == resume_data_action:
            self.requestSelectedTorrentResumeData()
        elif chosen == open_folder_action:
            self.openSelectedTorrentFolder()
        elif chosen == copy_magnet_action:
            self.copyToClipboard(payload.get("magnet", ""))
        elif chosen == copy_hash_action:
            self.copyToClipboard(payload.get("info_hash") or payload.get("torrent_id", ""))

    def pauseSelectedTorrent(self):
        torrent_id = self.selectedTorrentId()
        payload = self.selectedTorrentPayload()
        if self.download_engine is None or not torrent_id:
            return
        try:
            self.download_engine.pause(torrent_id)
            if payload:
                payload["paused_intent"] = True
                payload["status"] = "Completed" if float(payload.get("progress", 0) or 0) >= 99.9 else "Paused"
                self.refreshTorrentRow(self.torrentTable.currentRow(), payload)
                self.populateTorrentDetails(payload)
                self.updateDownloadSidebarCounts()
                self.scheduleTorrentStateSave()
                self.pushNotification(f"{payload.get('name', 'Torrent')} paused.", "Torrent Paused")
        except Exception as error:
            self.pushNotification(str(error), "Pause Failed")

    def resumeSelectedTorrent(self):
        torrent_id = self.selectedTorrentId()
        payload = self.selectedTorrentPayload()
        if self.download_engine is None or not torrent_id:
            return
        try:
            self.download_engine.resume(torrent_id)
            if payload:
                payload["paused_intent"] = False
                payload["status"] = "Queued"
                self.refreshTorrentRow(self.torrentTable.currentRow(), payload)
                self.populateTorrentDetails(payload)
                self.updateDownloadSidebarCounts()
                self.scheduleTorrentStateSave()
                self.pushNotification(f"{payload.get('name', 'Torrent')} resumed.", "Torrent Resumed")
            if not self.torrent_poll_timer.isActive():
                self.torrent_poll_timer.start()
        except Exception as error:
            self.pushNotification(str(error), "Resume Failed")

    def pauseSelectedOrAllTorrents(self):
        if self.selectedTorrentId():
            self.pauseSelectedTorrent()
        else:
            self.pauseAllTorrents()

    def resumeSelectedOrAllTorrents(self):
        if self.selectedTorrentId():
            self.resumeSelectedTorrent()
        else:
            self.resumeAllTorrents()

    def pauseAllTorrents(self):
        if self.download_engine is None:
            return
        for torrent_id in list(self.torrent_row_by_id):
            try:
                self.download_engine.pause(torrent_id)
                row = self.torrent_row_by_id.get(torrent_id, -1)
                payload = self._downloadPayloadForRow(row)
                if payload:
                    payload["paused_intent"] = True
                    payload["status"] = "Completed" if float(payload.get("progress", 0) or 0) >= 99.9 else "Paused"
                    self.refreshTorrentRow(row, payload)
            except Exception as error:
                self.appendTorrentLog(torrent_id, "pause_failed", str(error))
        self.updateDownloadSidebarCounts()
        self.scheduleTorrentStateSave()
        self.pushNotification("All torrents are paused.", "Torrent Paused")

    def resumeAllTorrents(self):
        if self.download_engine is None:
            return
        for torrent_id in list(self.torrent_row_by_id):
            try:
                self.download_engine.resume(torrent_id)
                row = self.torrent_row_by_id.get(torrent_id, -1)
                payload = self._downloadPayloadForRow(row)
                if payload:
                    payload["paused_intent"] = False
                    payload["status"] = "Queued"
                    self.refreshTorrentRow(row, payload)
            except Exception as error:
                self.appendTorrentLog(torrent_id, "resume_failed", str(error))
        if self.torrent_row_by_id and not self.torrent_poll_timer.isActive():
            self.torrent_poll_timer.start()
        self.updateDownloadSidebarCounts()
        self.scheduleTorrentStateSave()
        self.pushNotification("All torrents are resuming.", "Torrent Resumed")

    def removeSelectedTorrent(self):
        torrent_id = self.selectedTorrentId()
        row = self.torrentTable.currentRow()
        if row < 0:
            return
        try:
            if self.download_engine is not None and torrent_id:
                self.download_engine.remove(torrent_id)
        except Exception as error:
            self.pushNotification(str(error), "Remove Failed")
            return
        self.torrent_row_by_id.pop(torrent_id, None)
        self.torrent_logs_by_id.pop(torrent_id, None)
        self.torrent_files_by_id.pop(torrent_id, None)
        self.torrent_trackers_by_id.pop(torrent_id, None)
        self.torrent_peers_by_id.pop(torrent_id, None)
        if 0 <= row < len(self.download_items):
            self.download_items.pop(row)
        self.torrentTable.removeRow(row)
        self.rebuildTorrentRowIndex()
        self.updateDownloadSidebarCounts()
        if self.torrentTable.rowCount():
            self.torrentTable.selectRow(min(row, self.torrentTable.rowCount() - 1))
        else:
            self.showEmptyTorrentDetails()
        self.saveTorrentState()
        self.pushNotification("Torrent removed from Bitroid.", "Torrent Removed")

    def rebuildTorrentRowIndex(self):
        self.torrent_row_by_id.clear()
        for row in range(self.torrentTable.rowCount()):
            payload = self._downloadPayloadForRow(row)
            if payload and payload.get("torrent_id"):
                self.torrent_row_by_id[payload["torrent_id"]] = row

    def moveSelectedTorrent(self):
        payload = self.selectedTorrentPayload()
        torrent_id = self.selectedTorrentId()
        if not payload or self.download_engine is None or not torrent_id:
            return
        directory = QFileDialog.getExistingDirectory(self, "Set torrent location", payload.get("save_path", str(self.default_download_dir)))
        if not directory:
            return
        try:
            self.download_engine.move_storage(torrent_id, directory)
            payload["save_path"] = directory
            self.populateTorrentDetails(payload)
            self.scheduleTorrentStateSave()
            self.pushNotification("Torrent destination updated.", "Torrent Moved")
        except Exception as error:
            self.pushNotification(str(error), "Move Failed")

    def renameSelectedTorrent(self):
        payload = self.selectedTorrentPayload()
        if not payload:
            return
        text, accepted = QInputDialog.getText(self, "Rename torrent", "Name:", text=payload.get("name", ""))
        if not accepted or not text.strip():
            return
        payload["name"] = text.strip()
        row = self.torrentTable.currentRow()
        self.refreshTorrentRow(row, payload)
        self.populateTorrentDetails(payload)
        self.scheduleTorrentStateSave()
        self.pushNotification(f"Renamed to {payload['name']}.", "Torrent Renamed")

    def setSelectedTorrentSequential(self, enabled):
        payload = self.selectedTorrentPayload()
        torrent_id = self.selectedTorrentId()
        if not payload or self.download_engine is None or not torrent_id:
            return
        try:
            self.download_engine.set_sequential_download(torrent_id, enabled)
            payload["sequential"] = bool(enabled)
            self.scheduleTorrentStateSave()
        except Exception as error:
            self.pushNotification(str(error), "Torrent Option Failed")

    def forceRecheckSelectedTorrent(self):
        torrent_id = self.selectedTorrentId()
        if self.download_engine is None or not torrent_id:
            return
        try:
            self.download_engine.force_recheck(torrent_id)
            self.pushNotification("Torrent recheck requested.", "Torrent Recheck")
        except Exception as error:
            self.pushNotification(str(error), "Recheck Failed")

    def requestSelectedTorrentResumeData(self):
        torrent_id = self.selectedTorrentId()
        if self.download_engine is None or not torrent_id:
            return
        try:
            self.download_engine.request_resume_data(torrent_id)
            self.pushNotification("Resume data save requested.", "Torrent State")
        except Exception as error:
            self.pushNotification(str(error), "Resume Data Failed")

    def openSelectedTorrentFolder(self):
        payload = self.selectedTorrentPayload()
        if not payload:
            return
        directory = payload.get("save_path")
        if directory:
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(directory)))

    def filterDownloadRows(self, *args):
        text = self.torrentFilterInput.text().strip().lower()
        field = self.torrentFilterCombo.currentText()
        field_index = {"Name": 0, "Status": 4, "Save path": 0}.get(field, 0)
        for row in range(self.torrentTable.rowCount()):
            payload = self._downloadPayloadForRow(row) or {}
            visible = self.isTorrentVisibleForSidebar(payload, self.active_torrent_filter)
            if field == "Save path":
                haystack = str(payload.get("save_path", "")).lower()
            else:
                item = self.torrentTable.item(row, field_index)
                haystack = item.text().lower() if item else ""
            if text and text not in haystack:
                visible = False
            self.torrentTable.setRowHidden(row, not visible)

    def applyTorrentSidebarFilter(self, filter_key):
        self.active_torrent_filter = filter_key or "all"
        for key, button in self.torrentFilterButtons.items():
            active = key == self.active_torrent_filter
            button.setChecked(active)
            button.setProperty("active", active)
            repolish_widget(button)
        self.settings.set("torrent", "active_filter", self.active_torrent_filter)
        self.filterDownloadRows()
        self.scheduleTorrentStateSave()

    def isTorrentVisibleForSidebar(self, payload, filter_key):
        status = str(payload.get("status", "")).lower()
        if filter_key in ("all", "tracker_all"):
            return True
        if filter_key == "downloading":
            return status == "downloading"
        if filter_key == "seeding":
            return status == "seeding"
        if filter_key == "completed":
            return status in ("finished", "completed", "seeding")
        if filter_key == "running":
            return status in ("downloading", "seeding", "queued", "retrieving metadata")
        if filter_key == "paused":
            return status == "paused"
        if filter_key == "checking":
            return status == "checking"
        if filter_key == "errored":
            return status in ("error", "errored", "engine unavailable")
        if filter_key == "tracker_error":
            trackers = payload.get("trackers", []) or []
            return any("error" in str(tracker.get("status", "")).lower() for tracker in trackers if isinstance(tracker, dict))
        return True

    def refreshTorrentFilterRows(self):
        for row in range(self.torrentTable.rowCount()):
            payload = self._downloadPayloadForRow(row) or {}
            visible = self.isTorrentVisibleForSidebar(payload, self.active_torrent_filter)
            self.torrentTable.setRowHidden(row, not visible)

    def updateDownloadSidebarCounts(self):
        counts = {
            "all": len(self.download_items),
            "downloading": 0,
            "seeding": 0,
            "completed": 0,
            "running": 0,
            "paused": 0,
            "checking": 0,
            "errored": 0,
            "tracker_all": len(self.download_items),
            "tracker_error": 0,
        }
        for item in self.download_items:
            status = str(item.get("status", "")).lower()
            if status in counts:
                counts[status] += 1
            if status in ("downloading", "queued", "seeding", "retrieving metadata"):
                counts["running"] += 1
            if status in ("finished", "completed", "seeding"):
                counts["completed"] += 1
        labels = {
            "all": "All",
            "downloading": "Downloading",
            "seeding": "Seeding",
            "completed": "Completed",
            "running": "Running",
            "paused": "Paused",
            "checking": "Checking",
            "errored": "Errored",
            "tracker_all": "All",
            "tracker_error": "With errors",
        }
        for key, button in self.torrentFilterButtons.items():
            button.setText(f"{labels.get(key, key)} ({counts.get(key, 0)})")

    def updateTorrentDetailsFromSelection(self):
        row = self.torrentTable.currentRow()
        payload = self._downloadPayloadForRow(row)
        if not payload:
            self.showEmptyTorrentDetails()
            return
        torrent_id = payload.get("torrent_id", "")
        if torrent_id and self.download_engine is not None:
            self.refreshSelectedTorrentDetails(torrent_id, force=True)
            return
        self.populateTorrentDetails(payload)

    def _downloadPayloadForRow(self, row):
        if row < 0:
            return None
        item = self.torrentTable.item(row, 0)
        return item.data(Qt.ItemDataRole.UserRole) if item else None

    def showEmptyTorrentDetails(self):
        payload = {
            "name": "-",
            "size": "-",
            "progress": 0,
            "availability": "-",
            "status": "-",
            "download_speed": "0.00 B/s",
            "upload_speed": "0.00 B/s",
            "downloaded": "0.00 B",
            "uploaded": "0.00 B",
            "connections": "-",
            "eta": "-",
            "save_path": "-",
            "files": [],
            "trackers": [],
            "peers_list": [],
            "magnet": "",
            "info_hash": "",
            "added_on": "-",
            "completed_on": "-",
        }
        self.populateTorrentDetails(payload)

    def populateTorrentDetails(self, payload):
        progress = int(float(payload.get("progress", 0)) * 10)
        self.torrentOverviewProgress.setValue(progress)
        self.torrentOverviewProgress.setFormat(f"{payload.get('progress', 0):.1f}%")
        self.updateTorrentPieceMap(payload)
        values = {
            "Status": payload.get("status", "-"),
            "Availability": payload.get("availability", "-"),
            "Downloaded": f"{payload.get('downloaded', '0.00 B')} / {payload.get('size', '-')}",
            "Uploaded": payload.get("uploaded", "0.00 B"),
            "Download Speed": payload.get("download_speed", "0.00 B/s"),
            "Upload Speed": payload.get("upload_speed", "0.00 B/s"),
            "ETA": payload.get("eta", "-"),
            "Seeds": payload.get("seeds", "-"),
            "Peers": payload.get("peers", "-"),
            "Connections": payload.get("connections", "-"),
            "Share Ratio": "0.00",
            "Name": payload.get("name", "-"),
            "Total Size": payload.get("size", "-"),
            "Save Path": payload.get("save_path", "-"),
            "Info Hash": (payload.get("info_hash") or payload.get("magnet", "")[:56] or "N/A"),
            "Added On": payload.get("added_on", "-"),
            "Completed On": payload.get("completed_on", "-"),
        }
        for key, value in values.items():
            if key in self.torrentOverviewLabels:
                self.torrentOverviewLabels[key].setText(str(value))
        active_tab = self.torrentDetailTabs.currentIndex() if hasattr(self, "torrentDetailTabs") else 0
        empty_payload = not payload.get("torrent_id")
        if active_tab == 1 or empty_payload:
            self.populateTorrentFiles(payload.get("files", []), payload.get("name", "Torrent"), payload.get("size", "-"))
        if active_tab == 2 or empty_payload:
            self.populateTorrentTrackers(payload.get("trackers", []), payload)
        if active_tab == 3 or empty_payload:
            self.populateTorrentPeers(payload.get("peers_list", []))
        if active_tab == 4 or empty_payload:
            self.populateTorrentLogs(self.torrent_logs_by_id.get(payload.get("torrent_id", ""), []))

    def updateTorrentPieceMap(self, payload):
        files = payload.get("files", []) or []
        segments = []
        for file in files:
            try:
                size = int(file.get("size", 0) or 0)
                done = int(file.get("progress", 0) or 0)
            except (TypeError, ValueError):
                continue
            if size <= 0:
                continue
            ratio = max(0.0, min(done / size, 1.0))
            weight = max(1, min(10, round(size / (16 * 1024 * 1024))))
            segments.extend([ratio] * weight)
            if len(segments) >= 160:
                break
        if not segments:
            try:
                ratio = max(0.0, min(float(payload.get("progress", 0.0)) / 100.0, 1.0))
            except (TypeError, ValueError):
                ratio = 0.0
            segments = [ratio] * 64
        self.torrentPieceMap.setSegments(segments[:160])

    def populateTorrentFiles(self, files, root_name, total_size):
        self._updating_torrent_details = True
        self.torrentFilesTree.clear()
        try:
            root = QTreeWidgetItem([root_name, total_size, "0.0%", "Normal", total_size])
            root.setFlags(root.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            root.setCheckState(0, Qt.CheckState.Checked)
            root.setIcon(0, QIcon(":/icons/icons/folder.svg"))
            folder_items = {(): root}
            for file in files:
                if "path" in file and "progress" in file:
                    size = int(file.get("size", 0))
                    progress_bytes = int(file.get("progress", 0))
                    percent = (progress_bytes / size * 100.0) if size else 0.0
                    priority = self.priorityText(file.get("priority", 0))
                    remaining = self.convert_size(max(size - progress_bytes, 0))
                    child_values = [
                        str(file.get("path", "-")),
                        self.convert_size(size),
                        f"{percent:.1f}%",
                        priority,
                        remaining,
                    ]
                    selected = int(file.get("priority", 0)) > 0
                    file_index = int(file.get("index", -1))
                    path_parts = [part for part in child_values[0].replace("\\", "/").split("/") if part]
                else:
                    child_values = [
                        str(file.get("name", "-")),
                        str(file.get("size", "-")),
                        "0.0%",
                        str(file.get("priority", "Normal")),
                        str(file.get("size", "-")),
                    ]
                    selected = bool(file.get("selected", True))
                    file_index = -1
                    path_parts = [part for part in child_values[0].replace("\\", "/").split("/") if part]
                parent = root
                folder_key = ()
                for folder in path_parts[:-1]:
                    folder_key = (*folder_key, folder)
                    if folder_key not in folder_items:
                        folder_item = QTreeWidgetItem([folder, "-", "-", "Normal", "-"])
                        folder_item.setFlags(folder_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                        folder_item.setCheckState(0, Qt.CheckState.Checked)
                        folder_item.setIcon(0, QIcon(":/icons/icons/folder.svg"))
                        parent.addChild(folder_item)
                        folder_items[folder_key] = folder_item
                    parent = folder_items[folder_key]
                child = QTreeWidgetItem([
                    path_parts[-1] if path_parts else child_values[0],
                    child_values[1],
                    child_values[2],
                    child_values[3],
                    child_values[4],
                ])
                child.setFlags(child.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                child.setCheckState(0, Qt.CheckState.Checked if selected else Qt.CheckState.Unchecked)
                child.setData(0, Qt.ItemDataRole.UserRole, file_index)
                child.setToolTip(0, child_values[0])
                child.setIcon(0, QIcon(":/icons/icons/file.svg"))
                parent.addChild(child)
            self.torrentFilesTree.addTopLevelItem(root)
            root.setExpanded(True)
        finally:
            self._updating_torrent_details = False

    def priorityText(self, priority):
        try:
            priority = int(priority)
        except (TypeError, ValueError):
            return str(priority)
        if priority <= 0:
            return "Skip"
        if priority <= 2:
            return "Low"
        if priority <= 5:
            return "Normal"
        if priority <= 6:
            return "High"
        return "Maximum"

    def priorityValue(self, priority):
        return {
            "Skip": 0,
            "Low": 1,
            "Normal": 4,
            "High": 6,
            "Maximum": 7,
        }.get(priority, 4)

    def populateTorrentTrackers(self, trackers, payload):
        rows = []
        if trackers:
            rows = [
                (
                    tracker.get("url", "-"),
                    tracker.get("tier", ""),
                    tracker.get("protocol", ""),
                    tracker.get("status", ""),
                    tracker.get("peers", "N/A"),
                    tracker.get("seeds", "N/A"),
                )
                for tracker in trackers
            ]
        else:
            rows = [
                ("** DHT **", "", "DHT", "Waiting for peers", "N/A", "N/A"),
                ("** PeX **", "", "PeX", "Waiting for peers", "N/A", "N/A"),
                (payload.get("site", "Tracker metadata") or "-", "", "BT", "Pending", "N/A", "N/A"),
            ]
        self._populateTable(self.torrentTrackersTable, rows)

    def populateTorrentPeers(self, peers):
        if peers:
            rows = [
                (
                    peer.get("country", ""),
                    peer.get("ip", "-"),
                    peer.get("port", ""),
                    peer.get("connection", ""),
                    peer.get("client", ""),
                    f"{float(peer.get('progress', 0.0)) * 100:.1f}%",
                    self.formatNetSpeed(int(peer.get("down_speed", 0))),
                )
                for peer in peers
            ]
        else:
            rows = [("-", "Waiting for peers", "-", "-", "-", "-", "-")]
        self._populateTable(self.torrentPeersTable, rows)

    def populateTorrentLogs(self, rows):
        self._populateTable(self.torrentLogsTable, rows or [(self.timeNow(), "Ready", "Waiting for torrent engine events")])

    def _populateTable(self, table, rows):
        table.setRowCount(0)
        for row_values in rows:
            row = table.rowCount()
            table.insertRow(row)
            for column, value in enumerate(row_values):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                item.setToolTip(str(value))
                table.setItem(row, column, item)

    def setDownloadDetailFilesChecked(self, checked):
        state = Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked
        for index in range(self.torrentFilesTree.topLevelItemCount()):
            self._setDownloadDetailItemChecked(self.torrentFilesTree.topLevelItem(index), state)

    def _setDownloadDetailItemChecked(self, item, state):
        item.setCheckState(0, state)
        for index in range(item.childCount()):
            self._setDownloadDetailItemChecked(item.child(index), state)

    def syncDownloadFileCheckState(self, item, column):
        if column != 0 or self._updating_torrent_details:
            return
        self._updating_torrent_details = True
        try:
            state = item.checkState(0)
            for index in range(item.childCount()):
                self._setDownloadDetailItemChecked(item.child(index), state)
        finally:
            self._updating_torrent_details = False
        priority = "Skip" if item.checkState(0) == Qt.CheckState.Unchecked else (item.text(3) if item.text(3) != "Skip" else "Normal")
        self.setDownloadFilePriority(item, priority)

    def filterDownloadDetailFiles(self, text):
        pattern = text.strip().lower()
        for index in range(self.torrentFilesTree.topLevelItemCount()):
            self._filterDownloadDetailItem(self.torrentFilesTree.topLevelItem(index), pattern)

    def _filterDownloadDetailItem(self, item, pattern):
        child_match = False
        for index in range(item.childCount()):
            child_match = self._filterDownloadDetailItem(item.child(index), pattern) or child_match
        own_match = not pattern or pattern in item.text(0).lower()
        item.setHidden(not own_match and not child_match)
        return own_match or child_match

    def showDownloadFilePriorityMenu(self, position):
        item = self.torrentFilesTree.itemAt(position)
        if item is None:
            return
        menu = QMenu(self)
        for priority in TorrentAddDialog.PRIORITIES:
            action = menu.addAction(priority)
            action.triggered.connect(lambda checked=False, value=priority, target=item: self.setDownloadFilePriority(target, value))
        menu.exec(self.torrentFilesTree.viewport().mapToGlobal(position))

    def setDownloadFilePriority(self, item, priority):
        item.setText(3, priority)
        file_index = item.data(0, Qt.ItemDataRole.UserRole)
        torrent_id = self.selectedTorrentId()
        if self.download_engine is not None and torrent_id and isinstance(file_index, int) and file_index >= 0:
            try:
                self.download_engine.set_file_priority(torrent_id, file_index, self.priorityValue(priority))
            except Exception as error:
                self.pushNotification(str(error), "File Priority Failed")
        self.scheduleTorrentStateSave()
        for index in range(item.childCount()):
            self.setDownloadFilePriority(item.child(index), priority)

    def formatFileSize(self, size):
        units = ["B", "KB", "MB", "GB", "TB"]
        value = float(max(int(size), 0))
        index = 0
        while value >= 1024 and index < len(units) - 1:
            value /= 1024
            index += 1
        return f"{value:.2f} {units[index]}"

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
        self.ui.mediaProgressSlider.sliderPressed.connect(self.beginMediaSeek)
        self.ui.mediaProgressSlider.sliderMoved.connect(self.previewMediaSeek)
        self.ui.mediaProgressSlider.sliderReleased.connect(self.commitMediaSeek)
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

    def beginMediaSeek(self):
        self._media_slider_scrubbing = True

    def previewMediaSeek(self, position):
        position = int(position)
        self.ui.currentPlayingBtn.setText(self.format_time(position))
        remaining = max(self.media_duration - position, 0)
        self.ui.remainingMediaBtn.setText(f"-{self.format_time(remaining)}")

    def commitMediaSeek(self):
        position = int(self.ui.mediaProgressSlider.value())
        self._media_slider_scrubbing = False
        self.seekMediaTo(position)
        self.previewMediaSeek(position)

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
        self.setThemedButtonIcon(self.ui.mediaMuteBtn, ":/icons/icons/cil-volume-off.png" if muted else ":/icons/icons/cil-volume-high.png", 16)

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
        self.setThemedButtonIcon(self.ui.mediaRepeatBtn, icon, 18)

    def toggleMediaShuffle(self):
        self.media_shuffle = not self.media_shuffle
        self.settings.set("media_player", "shuffle", self.media_shuffle)
        self.updateMediaShuffleIcon()

    def updateMediaShuffleIcon(self):
        self.setThemedButtonIcon(self.ui.mediaShuffleBtn, ":/icons/icons/cil-layers.png" if self.media_shuffle else ":/icons/icons/cil-infinity.png", 18)

    def togglePlayerLock(self):
        self.player_locked = not self.player_locked
        self.updatePlayerLockIcon()
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

    def updatePlayerLockIcon(self):
        self.setThemedButtonIcon(self.ui.playerLockBtn, ":/icons/icons/cil-lock-locked.png" if self.player_locked else ":/icons/icons/cil-lock-unlocked.png", 18)

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
        if self._media_slider_scrubbing:
            return
        self._updating_media_slider = True
        self.ui.mediaProgressSlider.setValue(position)
        self._updating_media_slider = False
        self.previewMediaSeek(position)

    def updateMediaPlaybackState(self, state):
        is_playing = state == QMediaPlayer.PlaybackState.PlayingState
        self.setThemedButtonIcon(self.ui.mediaPlayBtn, ":/icons/icons/cil-media-pause.png" if is_playing else ":/icons/icons/play.svg", 40)

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

    def reloadAppServices(self):
        refreshed = []
        if self.torrent_engine_active and hasattr(self, "search_thread") and self.search_thread.isRunning():
            self.pushNotification("Search is running, so the search worker was left alone.", "Reload")
        else:
            if self.torrent_engine_active and hasattr(self, "search_thread"):
                self.search_thread.stop()
                self.torrent_engine_active = False
            self.initSearchThread()
            refreshed.append("search")

        self.loadDirectory(self.current_directory, remember=False)
        refreshed.append("files")

        if self.download_engine is not None:
            if self.torrent_row_by_id and not self.torrent_poll_timer.isActive():
                self.torrent_poll_timer.start()
            self.pollTorrentEngine()
            refreshed.append("torrent")

        self.favorite_torrents.load_favorites()
        self.history_thread.load_history()
        refreshed.extend(("favorites", "history"))
        self.network_monitor.set_app_network_rates(0, 0)
        self.temporaryLog("Bitroid services refreshed.", 2500)
        self.pushNotification(f"Refreshed {', '.join(refreshed)}.", "Bitroid Reload")

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
        self.showAddTorrentDialog(result)
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
        if hasattr(self, "torrent_state_save_timer"):
            self.torrent_state_save_timer.stop()
        self.saveTorrentState(force_resume=True)
        self.torrent_poll_timer.stop()
        if self.download_engine is not None:
            try:
                self.download_engine.close()
            except Exception:
                pass
            self.download_engine = None
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
