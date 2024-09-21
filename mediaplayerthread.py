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

    def connect_ui(self):
        self.ui.mediaProgressSlider.sliderMoved.connect(self.set_position)
        self.ui.mediaVolumeSlider.sliderMoved.connect(self.set_volume)
        self.ui.mediaPlayBtn.clicked.connect(self.play_pause)
        self.ui.mediaNextBtn.clicked.connect(self.next)
        self.ui.mediaPreviousBtn.clicked.connect(self.previous)
        self.ui.seekForwardBtn.clicked.connect(lambda: self.seek(10000))
        self.ui.seekBackwardBtn.clicked.connect(lambda: self.seek(-10000))
        self.ui.mediaStopBtn.clicked.connect(self.stop)
        self.ui.mediaMuteBtn.clicked.connect(self.mute_unmute)
        self.ui.playSoundBtn.clicked.connect(self.mute_unmute)
        self.ui.mediaRepeatBtn.clicked.connect(self.toggle_repeat)
        self.ui.mediaShuffleBtn.clicked.connect(self.toggle_shuffle)
        self.ui.playbackSpeedCombobox.currentIndexChanged.connect(
            self.set_playback_speed)
        self.ui.playerUndockBtn.clicked.connect(self.toggle_fullscreen)
        self.ui.mediaFolderBtn.clicked.connect(self.select_new_folder)
        self.ui.playerLockBtn.clicked.connect(self.lock_player)

    def connect_signals(self):
        self.media_player.positionChanged.connect(self.update_position)
        self.media_player.durationChanged.connect(self.update_duration)
        self.media_player.volumeChanged.connect(self.update_volume)
        self.media_player.stateChanged.connect(self.update_state)
        self.playlist.currentMediaChanged.connect(self.update_media)

    def run(self):
        self.exec()