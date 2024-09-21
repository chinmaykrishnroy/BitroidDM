import os
import stat
import time
import platform
import asyncio
from PySide6.QtCore import QThread, Signal, QFileSystemWatcher, QObject
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QScrollArea, QGridLayout
from asyncqt import QEventLoop  # asyncqt allows combining asyncio with Qt event loop


class FileWatcher(QObject):
    files_updated = Signal(list)

    def __init__(self, directory, n=0):
        super().__init__()
        self.directory = directory
        self.n = n
        self.file_system_watcher = QFileSystemWatcher()
        self.files = []

        # Initial directory scan
        asyncio.ensure_future(self._scan_directory())

        # Connect signals for directory/file changes
        self.file_system_watcher.directoryChanged.connect(self.schedule_rescan)
        self.file_system_watcher.fileChanged.connect(self.schedule_rescan)

    async def _scan_directory(self):
        """Scans the directory asynchronously."""
        self.files = []
        base_depth = self.directory.rstrip(os.sep).count(os.sep)

        # Simulate async operation by using await asyncio.sleep (non-blocking sleep)
        for root, dirs, files in os.walk(self.directory):
            current_depth = root.count(os.sep) - base_depth
            if self.n != -1 and current_depth > self.n:
                del dirs[:]  # Prune subdirectories beyond the desired depth
                continue
            for file_name in files:
                file_path = os.path.join(root, file_name)
                self.files.append(self._get_file_info(file_path))
            await asyncio.sleep(0)  # Yield control back to event loop

        self.files_updated.emit(self.files)

    def _get_file_info(self, file_path):
        stats = os.stat(file_path)
        file_info = {
            'name': os.path.basename(file_path),
            'path': file_path,
            'size': stats.st_size,  # File size in bytes
            'type': os.path.splitext(file_path)[1],  # File extension/type
            'modified_time': time.ctime(stats.st_mtime),  # Last modification time
            'creation_time': time.ctime(stats.st_ctime),  # Creation time
            'last_access_time': time.ctime(stats.st_atime),  # Last access time
            'permissions': stat.filemode(stats.st_mode),  # File permissions in human-readable form
        }

        if platform.system() != 'Windows':
            import pwd, grp
            file_info.update({
                'owner': pwd.getpwuid(stats.st_uid).pw_name,
                'group': grp.getgrgid(stats.st_gid).gr_name,
            })

        return file_info

    def schedule_rescan(self, _):
        """Schedules an asynchronous rescan of the directory."""
        asyncio.ensure_future(self._scan_directory())

    def stop(self):
        """Stops the file watcher."""
        self.file_system_watcher.removePaths(self.file_system_watcher.files())
        self.file_system_watcher.removePaths(self.file_system_watcher.directories())


class FileViewer(QWidget):
    def __init__(self, file_watcher):
        super().__init__()
        self.file_watcher = file_watcher
        self.setWindowTitle("File Watcher")
        self.setGeometry(200, 200, 600, 400)

        layout = QVBoxLayout()

        # Create a scroll area to show the files
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        # Widget to hold the tiles (file names)
        self.files_widget = QWidget()
        self.files_layout = QGridLayout(self.files_widget)
        self.scroll_area.setWidget(self.files_widget)

        layout.addWidget(self.scroll_area)
        self.setLayout(layout)

        # Connect the file update signal to update the GUI
        self.file_watcher.files_updated.connect(self.update_file_list)

    def update_file_list(self, files):
        """Updates the file display with tiles of file names."""
        # Clear existing tiles
        for i in reversed(range(self.files_layout.count())):
            widget = self.files_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Create a label for each file
        for index, file_info in enumerate(files):
            file_label = QLabel(file_info['name'])
            self.files_layout.addWidget(file_label, index // 4, index % 4)


def main(directory):
    # Create QApplication with asyncio event loop
    app = QApplication([])
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    # Create file watcher
    file_watcher = FileWatcher(directory=directory, n=-1)

    # Create file viewer GUI
    viewer = FileViewer(file_watcher)
    viewer.show()

    # Run asyncio event loop
    with loop:
        loop.run_forever()


if __name__ == "__main__":
    # Start the application with the directory to watch
    directory_to_watch = "C:\\Users\\morph\\OneDrive\\Desktop\\Music"  # Change this to your directory
    main(directory_to_watch)
