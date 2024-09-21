import os
import stat
import time
import platform
import sys
from PySide6.QtCore import Qt, QThread, Signal, QFileSystemWatcher
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QScrollArea, QGridLayout

class FileWatcher(QThread):
    files_updated = Signal(list)

    def __init__(self, directory, n=1):
        super().__init__()
        self.directory = directory
        self.n = n
        self.file_system_watcher = QFileSystemWatcher()
        self.files = []
        self.running = True

        # Watch the initial directory and subdirectories
        self._scan_directory()
        self.file_system_watcher.directoryChanged.connect(self.on_directory_changed)
        self.file_system_watcher.fileChanged.connect(self.on_file_changed)

    def _scan_directory(self):
        """Scans the directory recursively up to n levels and stores file details."""
        self.files = []
        base_depth = self.directory.rstrip(os.sep).count(os.sep)  # Base depth of the top-level directory

        for root, dirs, files in os.walk(self.directory):
            current_depth = root.count(os.sep) - base_depth
            if self.n != -1 and current_depth > self.n:
                # Skip directories that exceed the desired depth
                del dirs[:]  # This prevents os.walk from going deeper
                continue
            for file_name in files:
                file_path = os.path.join(root, file_name)
                self.files.append(self._get_file_info(file_path))

        # Watch all subdirectories and files for changes
        self._add_paths_to_watcher()

        # Emit the updated file list
        self.files_updated.emit(self.files)

    def _get_file_info(self, file_path):
        """Returns file info as a dictionary."""
        stats = os.stat(file_path)
        file_info = {
            'name': os.path.basename(file_path),
            'path': file_path,
            'size': stats.st_size,  # File size in bytes
            'type': os.path.splitext(file_path)[1],  # File extension/type
            'modified_time': time.ctime(stats.st_mtime),  # Last modification time
            'creation_time': time.ctime(stats.st_ctime),  # Creation time (may vary by system)
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

    def _add_paths_to_watcher(self):
        """Adds directories and files to the QFileSystemWatcher."""
        self.file_system_watcher.addPath(self.directory)
        for file_info in self.files:
            self.file_system_watcher.addPath(file_info['path'])

    def run(self):
        """Main method of the thread."""
        self._scan_directory()  # Initial scan

    def on_directory_changed(self, path):
        """Called when a directory change is detected by the file system watcher."""
        self._scan_directory()

    def on_file_changed(self, path):
        """Called when a file change is detected by the file system watcher."""
        self._scan_directory()

    def stop(self):
        """Stops the file watcher."""
        self.running = False
        self.quit()
        self.wait()

    def rescan(self):
        """Rescans the directory."""
        self._scan_directory()

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

        # Start the file watcher thread
        self.file_watcher.start()

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

    def closeEvent(self, event):
        """Handle the window close event to stop the file watcher."""
        self.file_watcher.stop()
        super().closeEvent(event)

def main(directory):
    app = QApplication(sys.argv)

    # Create file watcher thread
    file_watcher = FileWatcher(directory=directory, n=0)  # Set appropriate depth level here
    
    # Create the file viewer GUI
    viewer = FileViewer(file_watcher)
    viewer.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    # Start the application with the directory to watch
    directory_to_watch = "C:\\Users\\morph\\OneDrive\\Desktop\\Music"  # Change this to the directory you want to watch
    main(directory_to_watch)
