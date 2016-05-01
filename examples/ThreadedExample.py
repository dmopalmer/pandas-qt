from __future__ import print_function
import sys
import time
from pandasqt.compat import QtCore, QtGui, QtWidgets, Qt, Slot, Signal
import os

# import imgs

from pandasqt.views.OverlayProgressView import OverlayProgressWidget

from pandasqt.models.ProgressThread import ProgressWorker, createThread

europe_png = os.path.join(os.path.dirname(__file__),'europe.png')

class ExampleWorker(ProgressWorker):
    def __init__(self, name, ticks):
        super(ExampleWorker, self).__init__(name)
        self.ticks = ticks

    def run(self):
        count = 0
        while count < 100:
            time.sleep(1)
            count += self.ticks
            if count > 100:
                count = 100
                self.progressChanged.emit(count)
                break

            self.progressChanged.emit(count)


class Example(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Example, self).__init__(parent)

        self.initUI()


    def initUI(self):
        self.setGeometry(100, 100, 300, 300)

        self.vlayout = QtWidgets.QVBoxLayout(self)

        self.imgContainer = QtWidgets.QLabel(self)
        img = QtGui.QPixmap(europe_png)
        self.imgContainer.setPixmap(img)
        size = img.size()
        self.imgContainer.resize(size.width(), self.height())

        self.vlayout.addWidget(self.imgContainer)
        self.vlayout.addWidget(QtWidgets.QLabel('FOOO',self))

        threads = []

        worker1 = ExampleWorker('foo', 10)
        worker2 = ExampleWorker('bar', 13)
        worker3 = ExampleWorker('spam', 25)

        workers = [worker1, worker2, worker3]
        for worker in workers:
            thread = createThread(self, worker)
            threads.append(thread)
            worker.finished.connect(self.debugPrint)

        self.pgFrame = OverlayProgressWidget(self.imgContainer, workers=workers)

        for t in threads:
            t.start()

    @Slot()
    def debugPrint(self):
        print('THREAD %s ended' % (self.sender().name, ))


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    widget = Example()
    widget.show()
    app.exec_()