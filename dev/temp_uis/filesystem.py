import os, platform
from PySide6.QtWidgets import QApplication, QTreeView, QFileSystemModel, QFileIconProvider
from PySide6.QtCore import QDir, QFileInfo
class X:
    def __init__(self):
        a = QApplication([])
        self.b = QFileSystemModel()
        self.b.setRootPath(QDir.rootPath())
        self.c = QTreeView()
        self.c.setModel(self.b)
        self.c.setRootIndex(self.b.index(QDir.homePath()))
        self.c.setWindowTitle("Explorer")
        self.c.setWindowIcon(QFileIconProvider().icon(QFileIconProvider.IconType.Folder))
        self.c.doubleClicked.connect(self.d)
        self.c.show()
        a.exec()
    def d(self, index):
        e = self.b.filePath(index)
        f = QFileInfo(e)
        if f.isFile():self.g(e)
    def g(self, e):
        _ = platform.system()
        if _ == 'Windows':os.startfile(e)
        elif _ == 'Darwin':os._(f'open "{e}"')
        else:os._(f'xdg-open "{e}"')
X()