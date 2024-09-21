import pickle
import os
from PySide6.QtCore import QThread, Signal, QMutex, QMutexLocker

class HistoryManager(QThread):
    historyListChanged = Signal(list)

    def __init__(self, bin_file='history.bin', parent=None):
        super().__init__(parent)
        self.bin_file = bin_file
        self.history = []
        self.next_index = 0
        self.mutex = QMutex()
        self.running = True
        self.load_history()

    def run(self):
        self.historyListChanged.emit(self.history)

    def stop(self):
        self.running = False
        self.quit()
        self.wait()

    def add_history(self, result):
        with QMutexLocker(self.mutex):
            result['index'] = self.next_index
            self.next_index += 1

            self.history.append(result)
            self.save_history()
            self.historyListChanged.emit(self.history)

    def remove_history(self, index):
        with QMutexLocker(self.mutex):
            self.history = [h for h in self.history if h.get("index") != index]
            self.save_history()
            self.historyListChanged.emit(self.history)

    def load_history(self):
        try:
            if os.path.exists(self.bin_file):
                with open(self.bin_file, 'rb') as file:
                    data = pickle.load(file)
                    self.history = data.get('history', [])
                    self.next_index = data.get('next_index', 1)
            else:
                self.history = []
                self.next_index = 0
        except (FileNotFoundError, EOFError, pickle.UnpicklingError):
            self.history = []
            self.next_index = 0
        self.historyListChanged.emit(self.history)

    def save_history(self):
        try:
            with open(self.bin_file, 'wb') as file:
                data = {
                    'history': self.history,
                    'next_index': self.next_index
                }
                pickle.dump(data, file)
        except IOError as e:
            print(f"Error saving history to file: {e}")