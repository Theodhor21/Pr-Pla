
import sys
import traceback

from PySide2.QtCore import QRunnable, Slot, QObject, Signal, Qt, QRect
from PySide2.QtGui import QColor, QFont, QPainter
from PySide2.QtSvg import QSvgRenderer
from PySide2.QtWidgets import QWidget, QPushButton

from src.widgets import main_window


class LoadingBarSignals(QObject):
    # SIGNALS
    close = Signal()

class LoadingBar(QWidget):
    def __init__(self, parent, fn, *args):
        super(LoadingBar, self).__init__(parent)

        self.fn = fn
        self.args = args
        self.worker = Worker(fn, *args)
        self.worker.signals.result.connect(main_window.MainWindow.get_instance().calc_done)


        main_window.MainWindow.get_instance().threadpool.start(self.worker)

        # overlay
        # make the window frameless
        self.loading_icon = QSvgRenderer('resources/images/loading_icon.svg')
        self.qp = QPainter()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.fillColor = QColor(30, 30, 30, 120)
        self.penColor = QColor("#333333")

        self.close_btn = QPushButton(self)
        self.close_btn.setText("Abbrechen")

        font = QFont()
        font.setPixelSize(18)
        font.setBold(True)
        self.close_btn.setFont(font)
        self.close_btn.setStyleSheet("QPushButton {"
                                "background-color: #EAEAEA;"
                                "border: None;"
                                "padding-top: 12px;"
                                "padding-bottom: 12px;"
                                "padding-left: 20px;"
                                "padding-right: 20px;"
                                "}"
                                "QPushButton:hover {"
                                "background-color: #DFDFDF;"
                                "}")
        #self.close_btn.setFixedSize(30, 30)
        self.close_btn.clicked.connect(self._onclose)

        self.signals = LoadingBarSignals()

    def resizeEvent(self, event=None):
        button_x = (self.width() - self.close_btn.width()) / 2
        button_y = (self.height() - self.close_btn.height()) / 2 + 60
        self.close_btn.move(button_x, button_y)

    def paintEvent(self, event):
        # This method is, in practice, drawing the contents of
        # your window.

        # get current window size
        s = self.size()
        self.qp.begin(self)
        self.qp.setRenderHint(QPainter.Antialiasing, True)
        self.qp.setPen(self.penColor)
        self.qp.setBrush(self.fillColor)
        self.qp.drawRect(0, 0, s.width(), s.height())

        icon_size = 180
        self.loading_icon.render(self.qp, QRect((self.width()-icon_size) / 2, (self.height() - icon_size) / 2 - 60, icon_size, icon_size))
        self.qp.end()


    def _onclose(self):
        self.signals.close.emit()


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        `tuple` (exctype, value, traceback.format_exc() )

    result
        `object` data returned from processing, anything

    progress
        `int` indicating % progress

    '''
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(int)


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done