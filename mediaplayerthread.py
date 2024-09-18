import os

from PySide6.QtCore import QThread, Signal, Slot, QUrl, QSize, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PySide6.QtWidgets import QFileDialog
from PySide6.QtMultimediaWidgets import QVideoWidget
from videowindow import VideoWindow


class MediaPlayer(QThread):
    positionChanged = Signal(int)
    durationChanged = Signal(int)
    volumeChanged = Signal(int)
    stateChanged = Signal(QMediaPlayer.State)
    mediaChanged = Signal(str)

    def __init__(self, ui, mainwindow):
        super().__init__()
        self.ui = ui
        self.mainwindow = mainwindow