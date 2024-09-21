import os
import stat
import time
import platform
from PySide6.QtCore import QThread, Signal, QFileSystemWatcher, QTimer

class FileWatcher(QThread):
    files_updated = Signal(list)

    def __init__(self, directory, n=0, debounce_ms=3000):
        super().__init__()
        self.directory = directory
        self.n = n
        self.debounce_ms = debounce_ms
        self.file_system_watcher = QFileSystemWatcher()
        self.files = []
        self.running = True

        # Debounce timer to avoid frequent re-scanning
        self.debounce_timer = QTimer()
        self.debounce_timer.setInterval(self.debounce_ms)
        self.debounce_timer.setSingleShot(True)
        self.debounce_timer.timeout.connect(self._scan_directory)

        # Initial directory scan and setup file watcher
        self._scan_directory()
        self.file_system_watcher.directoryChanged.connect(self.on_directory_changed)
        self.file_system_watcher.fileChanged.connect(self.on_file_changed)

    def _scan_directory(self):
        self.files = []
        base_depth = self.directory.rstrip(os.sep).count(os.sep)

        # Walk through the directory and collect file information
        for root, dirs, files in os.walk(self.directory):
            current_depth = root.count(os.sep) - base_depth
            if self.n != -1 and current_depth > self.n:
                del dirs[:]
                continue
            for file_name in files:
                file_path = os.path.join(root, file_name)
                self.files.append(self._get_file_info(file_path))

        # Add files and directories to QFileSystemWatcher
        self._add_paths_to_watcher()

        # Emit the updated list of files
        self.files_updated.emit(self.files)

    def _get_file_info(self, file_path):
        stats = os.stat(file_path)
        file_info = {
            'name': os.path.basename(file_path),
            'path': file_path,
            'size': stats.st_size,  # File size in bytes
            'type': os.path.splitext(file_path)[1],  # File extension/type
            'modified_time': time.ctime(stats.st_mtime),  # Last modification time
            'creation_time': time.ctime(stats.st_birthtime),  # Creation time (may vary by system)
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
        # Add the directory and files to QFileSystemWatcher
        self.file_system_watcher.addPath(self.directory)
        for file_info in self.files:
            if os.path.exists(file_info['path']):
                self.file_system_watcher.addPath(file_info['path'])

    def run(self):
        self._scan_directory()

    def on_directory_changed(self, path):
        # Directory change event handler
        self.debounce_timer.start()

    def on_file_changed(self, path):
        # File change event handler
        self.debounce_timer.start()

    def stop(self):
        # Stop the thread and cleanup
        self.running = False
        self.quit()
        self.wait()

    def rescan(self):
        # Manual trigger for directory rescan
        self._scan_directory()
