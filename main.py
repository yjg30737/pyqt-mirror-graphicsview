import os, sys

# Get the absolute path of the current script file
from findPathWidget import FindPathWidget
from imageView import ImageView
from slider import ModernSlider

script_path = os.path.abspath(__file__)

# Get the root directory by going up one level from the script directory
project_root = os.path.dirname(os.path.dirname(script_path))

sys.path.insert(0, project_root)
sys.path.insert(0, os.getcwd())  # Add the current directory as well

from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QVBoxLayout, QWidget, QHBoxLayout, QFileDialog
from PyQt5.QtCore import Qt, QCoreApplication, QThread
from PyQt5.QtGui import QFont, QIcon, QPixmap, QPainter

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)  # HighDPI support

QApplication.setFont(QFont('Arial', 12))


class Thread(QThread):
    def __init__(self):
        super(Thread, self).__init__()

    def run(self):
        try:
            pass
        except Exception as e:
            raise Exception(e)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.__initUi()

    def __initUi(self):
        self.__findPathWidget = FindPathWidget()
        self.__findPathWidget.added.connect(self.__added)
        self.__imageView = ImageView()

        self.__hflipBtn = QPushButton()
        self.__hflipBtn.setIcon(QIcon('hflip.png'))
        self.__hflipBtn.clicked.connect(self.__hflip)
        self.__slider = ModernSlider()
        self.__slider.valueChanged.connect(self.__valueChanged)

        self.__saveBtn = QPushButton('Save')
        self.__saveBtn.clicked.connect(self.__save)

        lay = QHBoxLayout()
        lay.addWidget(self.__hflipBtn)
        lay.addWidget(self.__slider)

        bottomWidget = QWidget()
        bottomWidget.setLayout(lay)

        lay = QVBoxLayout()
        lay.addWidget(self.__findPathWidget)
        lay.addWidget(self.__imageView)
        lay.addWidget(bottomWidget)
        lay.addWidget(self.__saveBtn)

        mainWidget = QWidget()
        mainWidget.setLayout(lay)
        self.setCentralWidget(mainWidget)

        self.__hflipBtn.setEnabled(False)
        self.__slider.setEnabled(False)
        self.__saveBtn.setEnabled(False)

    def __added(self, filename):
        self.__imageView.setFilename(filename)
        self.__hflipBtn.setEnabled(True)
        self.__slider.setEnabled(True)
        self.__saveBtn.setEnabled(True)

    def __hflip(self):
        self.__imageView.hflip()

    def __valueChanged(self, v):
        v = v + 1 if v != 0 else 0
        self.__imageView.setValue(v)

    def __save(self):
        # Open a file dialog to get the save location and file type
        fileName, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Image Files (*.png *.jpg *.bmp)")
        if fileName:
            # Create a QPixmap of the same size as the view/scene
            pixmap = QPixmap(self.__imageView.sceneRect().size().toSize())
            # Create a QPainter to draw the scene onto the pixmap
            painter = QPainter(pixmap)
            # Render the scene onto the pixmap
            self.__imageView.scene().render(painter)
            # Save the pixmap to the file
            pixmap.save(fileName)
            painter.end()  # End the QPainter session

    def __started(self):
        print('started')

    def __finished(self):
        print('finished')


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())