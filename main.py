import sys

from Common.cmain import cmain
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)

if __name__ == "__main__":
    if cmain():
        sys.exit(app.exec_())
