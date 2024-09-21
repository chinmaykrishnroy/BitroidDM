
from PySide6.QtCore import QThread, Signal, Slot, QUrl
from PySide6.QtMultimedia import QMediaPlayer, QMediaContent
from PySide6.QtMultimediaWidgets import QVideoWidget

class MediaPlayerThread(QThread):
    # Signals for updating UI elements
    positionChanged = Signal(int, int)  # current position, max duration
    durationChanged = Signal(int)       # max duration
    currentDuration = Signal(int)       # current media duration
    volumeChanged = Signal(int)         # volume change
    stateChanged = Signal(int)          # playing/paused/stopped
    mediaChanged = Signal()             # media changed
    shuffleChanged = Signal(bool)       # shuffle mode changed
    repeatChanged = Signal(int)         # repeat mode changed
    playlistChanged = Signal(bool)      # playlist change
    surfaceChanged = Signal(bool)       # video surface change

    def __init__(self):
        super().__init__()
        self.player = QMediaPlayer()

        self.playlist = []   # List of media file paths
        self.current_index = -1  # Track current item

        # Connect internal signals
        self.player.positionChanged.connect(self.position_changed)
        self.player.durationChanged.connect(self.duration_changed)
        self.player.mediaStatusChanged.connect(self.media_changed)
        self.player.stateChanged.connect(self.state_changed)

    def run(self):
        self.exec_()

    # Slot to set the video output surface (e.g., QVideoWidget)
    @Slot(QVideoWidget)
    def set_video_surface(self, video_widget):
        self.player.setVideoOutput(video_widget)
        self.surfaceChanged.emit(True)

    # Slot to handle position change (updates slider position)
    @Slot(int)
    def position_changed(self, position):
        self.positionChanged.emit(position, self.player.duration())
        self.currentDuration.emit(position)

    # Slot to handle duration change (set the max slider range)
    @Slot(int)
    def duration_changed(self, duration):
        self.durationChanged.emit(duration)

    # Slot to handle media change
    @Slot()
    def media_changed(self):
        self.mediaChanged.emit()

    # Slot to handle state change (playing, paused, stopped)
    @Slot()
    def state_changed(self):
        state = self.player.state()
        self.stateChanged.emit(state)

    # Slot to handle play/pause
    @Slot()
    def play_pause(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.stateChanged.emit(QMediaPlayer.PausedState)
        else:
            self.player.play()
            self.stateChanged.emit(QMediaPlayer.PlayingState)

    # Slot to handle stop
    @Slot()
    def stop(self):
        self.player.stop()
        self.stateChanged.emit(QMediaPlayer.StoppedState)

    # Slot to set the playback position (slider control)
    @Slot(int)
    def set_position(self, position):
        self.player.setPosition(position)

    # Slot to set volume
    @Slot(int)
    def set_volume(self, volume):
        self.player.setVolume(volume)
        self.volumeChanged.emit(volume)

    # Slot to play the next media in the playlist
    @Slot()
    def next(self):
        if self.playlist:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            self.play_media_by_index(self.current_index)

    # Slot to play the previous media in the playlist
    @Slot()
    def previous(self):
        if self.playlist:
            self.current_index = (self.current_index - 1) % len(self.playlist)
            self.play_media_by_index(self.current_index)

    # Slot to seek forward/backward by offset in milliseconds
    @Slot(int)
    def seek(self, offset):
        self.player.setPosition(self.player.position() + offset)

    # Slot to mute/unmute audio
    @Slot()
    def mute_unmute(self):
        self.player.setMuted(not self.player.isMuted())

    # Slot to toggle shuffle mode
    @Slot()
    def toggle_shuffle(self):
        if hasattr(self, 'shuffle_mode') and self.shuffle_mode:
            self.shuffle_mode = False
            self.shuffleChanged.emit(False)
        else:
            self.shuffle_mode = True
            self.shuffleChanged.emit(True)

    # Slot to toggle repeat mode (not using QMediaPlaylist, so we'll manage manually)
    @Slot()
    def toggle_repeat(self):
        if hasattr(self, 'repeat_mode') and self.repeat_mode == 'loop':
            self.repeat_mode = 'none'
            self.repeatChanged.emit(0)  # No repeat
        else:
            self.repeat_mode = 'loop'
            self.repeatChanged.emit(1)  # Loop all

    # Slot to refresh playlist items with new items (list of dicts)
    @Slot(list)
    def refresh_playlist(self, items):
        self.playlist = [item['path'] for item in items if 'path' in item]
        self.playlistChanged.emit(True)

    # Slot to clear the playlist
    @Slot()
    def clear_playlist(self):
        self.playlist.clear()
        self.current_index = -1
        self.playlistChanged.emit(True)

    # Slot to stop the current media and play a new media from the given path
    @Slot(str)
    def play_from_path(self, path):
        self.player.stop()
        media = QMediaContent(QUrl.fromLocalFile(path))
        self.player.setMedia(media)
        self.player.play()
        self.mediaChanged.emit()

    # Play media by index from playlist
    def play_media_by_index(self, index):
        if 0 <= index < len(self.playlist):
            self.player.stop()
            media = QMediaContent(QUrl.fromLocalFile(self.playlist[index]))
            self.player.setMedia(media)
            self.player.play()
            self.mediaChanged.emit()

    # Slot for fullscreen toggle
    @Slot()
    def toggle_fullscreen(self):
        self.surfaceChanged.emit(True)

    # Slot for selecting a new media folder
    @Slot()
    def select_new_folder(self):
        # Placeholder for folder selection functionality
        pass

    # Slot for locking/unlocking the player (optional)
    @Slot()
    def lock_player(self):
        # Placeholder for player lock functionality
        pass