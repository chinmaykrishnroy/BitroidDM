from PySide6.QtCore import QThread, QUrl, Signal
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtWidgets import QApplication
import sys

class AudioPlayer(QThread):
    finished = Signal()

    def __init__(self, path, volume):
        super().__init__()
        self.path = path
        self.volume = volume
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.audio_output.setVolume(volume / 100)
        self.player.setAudioOutput(self.audio_output)
        self.player.setSource(QUrl.fromLocalFile(path))
        self.player.mediaStatusChanged.connect(self.on_media_status_changed)

    def run(self):
        self.player.play()
        self.exec()

    def on_media_status_changed(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.player.stop()
            self.finished.emit()
            self.quit()

def playSound(path, volume=15):
    player = AudioPlayer(path, volume)
    player.finished.connect(lambda: handle_finished(player))
    player.start()

def handle_finished(player):
    player.deleteLater()
    if all(player.isFinished() for player in QThread.allThreads() if isinstance(player, AudioPlayer)):
        QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    playSound("C:\\Users\\morph\\QTube\\sound\\cat.wav", volume=30)
    playSound("C:\\Users\\morph\\QTube\\sound\\drop.wav", volume=50)
    playSound("C:\\Users\\morph\\QTube\\sound\\start.wav", volume=20)

    sys.exit(app.exec())
