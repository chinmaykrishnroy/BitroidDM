from PySide6.QtCore import QThread, QUrl, Signal, Slot
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget


class MediaPlayerThread(QThread):
    positionChanged = Signal(int, int)
    durationChanged = Signal(int)
    currentDuration = Signal(int)
    volumeChanged = Signal(int)
    stateChanged = Signal(QMediaPlayer.PlaybackState)
    mediaChanged = Signal()
    shuffleChanged = Signal(bool)
    repeatChanged = Signal(str)
    playlistChanged = Signal(bool)
    surfaceChanged = Signal(bool)

    def __init__(self):
        super().__init__()
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.playlist = []
        self.current_index = -1
        self.shuffle_mode = False
        self.repeat_mode = "off"

        self.player.positionChanged.connect(self.position_changed)
        self.player.durationChanged.connect(self.duration_changed)
        self.player.mediaStatusChanged.connect(lambda _: self.mediaChanged.emit())
        self.player.playbackStateChanged.connect(self.stateChanged.emit)

    def run(self):
        self.exec()

    @Slot(QVideoWidget)
    def set_video_surface(self, video_widget):
        self.player.setVideoOutput(video_widget)
        self.surfaceChanged.emit(True)

    @Slot(int)
    def position_changed(self, position):
        self.positionChanged.emit(position, self.player.duration())
        self.currentDuration.emit(position)

    @Slot(int)
    def duration_changed(self, duration):
        self.durationChanged.emit(duration)

    @Slot()
    def play_pause(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    @Slot()
    def stop(self):
        self.player.stop()

    @Slot(int)
    def set_position(self, position):
        self.player.setPosition(position)

    @Slot(int)
    def set_volume(self, volume):
        volume = max(0, min(volume, 100))
        self.audio_output.setVolume(volume / 100)
        self.volumeChanged.emit(volume)

    @Slot(float)
    def set_playback_rate(self, rate):
        self.player.setPlaybackRate(rate)

    @Slot()
    def next(self):
        if self.playlist:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            self.play_media_by_index(self.current_index)

    @Slot()
    def previous(self):
        if self.playlist:
            self.current_index = (self.current_index - 1) % len(self.playlist)
            self.play_media_by_index(self.current_index)

    @Slot(int)
    def seek(self, offset):
        duration = max(self.player.duration(), 0)
        position = max(0, min(self.player.position() + offset, duration))
        self.player.setPosition(position)

    @Slot()
    def mute_unmute(self):
        self.audio_output.setMuted(not self.audio_output.isMuted())

    @Slot()
    def toggle_shuffle(self):
        self.shuffle_mode = not self.shuffle_mode
        self.shuffleChanged.emit(self.shuffle_mode)

    @Slot()
    def toggle_repeat(self):
        modes = ["off", "all", "one"]
        index = modes.index(self.repeat_mode) if self.repeat_mode in modes else 0
        self.repeat_mode = modes[(index + 1) % len(modes)]
        self.repeatChanged.emit(self.repeat_mode)

    @Slot(list)
    def refresh_playlist(self, items):
        self.playlist = [str(item["path"]) for item in items if item.get("path")]
        self.current_index = 0 if self.playlist else -1
        self.playlistChanged.emit(True)

    @Slot()
    def clear_playlist(self):
        self.playlist.clear()
        self.current_index = -1
        self.playlistChanged.emit(True)

    @Slot(str)
    def play_from_path(self, path):
        self.player.stop()
        self.player.setSource(QUrl.fromLocalFile(path))
        self.player.play()
        self.mediaChanged.emit()

    def play_media_by_index(self, index):
        if 0 <= index < len(self.playlist):
            self.current_index = index
            self.play_from_path(self.playlist[index])

    @Slot()
    def toggle_fullscreen(self):
        self.surfaceChanged.emit(True)
