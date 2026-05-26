import json
import os
from PySide6.QtCore import QThread, Signal, QMutex, QMutexLocker
from bitroid.core.paths import app_data_dir

class HistoryManager(QThread):
    historyListChanged = Signal(list)

    def __init__(self, history_file=None, parent=None):
        super().__init__(parent)
        self.history_file = history_file or str(app_data_dir() / 'history.json')
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
        if not os.path.exists(self.history_file):
            self.history = []
            self.next_index = 0
            self.save_history()
            self.historyListChanged.emit(self.history)
            return

        try:
            with open(self.history_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
            self.history = data.get('history', [])
            self.next_index = data.get('next_index', len(self.history))
        except (FileNotFoundError, json.JSONDecodeError, TypeError):
            self.history = []
            self.next_index = 0

        self.historyListChanged.emit(self.history)

    def save_history(self):
        try:
            directory = os.path.dirname(self.history_file)
            if directory:
                os.makedirs(directory, exist_ok=True)
            with open(self.history_file, 'w', encoding='utf-8') as file:
                data = {
                    'history': self.history,
                    'next_index': self.next_index
                }
                json.dump(data, file, indent=4)
        except IOError as e:
            print(f"Error saving history to file: {e}")
