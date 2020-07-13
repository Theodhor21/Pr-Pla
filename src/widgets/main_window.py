import time

from PySide2.QtCore import QEvent, QThreadPool
from PySide2.QtGui import QColor, QPainter, QPaintEvent
from PySide2.QtWidgets import QMainWindow, QWidget, QGridLayout, QPushButton, QHBoxLayout

from src import algorithm
from src.data import datatypes
from src.dialogs.yes_dialog import YesDialog
from src.widgets import manuelle_eingabe
from src.widgets import overview
from src.widgets.elements import detailed_view
from src.widgets.elements.loading_bar import LoadingBar, Worker


class MainWindow(QMainWindow):
    instance = None
    def __init__(self, menubar, central_widget):
        super(MainWindow, self).__init__()
        self.threadpool = QThreadPool()

        MainWindow.set_instance(self)

        self.setWindowTitle("PrüPla")

        self.setMenuWidget(menubar)
        self.setCentralWidget(central_widget)

        self.loading_bar = None


    def enterEvent(self, event:QEvent):
        """
        close all detailed_views
        :param event:
        :return:
        """
        detailed_view.DetailedView.close_all()

    def resizeEvent(self, event):
        if not self.loading_bar is None:
            self.loading_bar.resize(self.width(), self.height())

    def calc_done(self, var):
        if not self.loading_bar is None:
            self.threadpool.clear()
            self.loading_bar.close()
            self.loading_bar = None

            if var[0]:
                self.centralWidget().data_handler.pruefungsplan = var[1]
                self.centralWidget().init_overview_pruefungsplan()
            else:
                YesDialog("Berechnung",
                          var[1], None,
                          self, "OK").exec_()
                self.centralWidget().get_instance().init_overview(datatypes.Raum)

    def cancle_calc(self):
        self.threadpool.clear()
        self.loading_bar.close()
        self.loading_bar = None

    def loading_bar_repaint(self):
        while True:
            if not self.loading_bar is None:
                self.loading_bar.update()
                time.sleep(0.03)
            else:
                break

    def init_calc(self):
        self.loading_bar = LoadingBar(self, algorithm.calc, (self.centralWidget().data_handler))
        self.loading_bar.move(0,0)
        self.loading_bar.signals.close.connect(self.cancle_calc)
        self.loading_bar.show()
        self.loading_bar.resize(self.width(), self.height())

        repaint_worker = Worker(self.loading_bar_repaint)
        self.threadpool.start(repaint_worker)


    @staticmethod
    def get_instance():
        return MainWindow.instance

    @staticmethod
    def set_instance(main_window):
        MainWindow.instance = main_window


class CentralWidget(QWidget):
    instance = None

    def __init__(self, data_handler, get_overview_funct):
        super(CentralWidget, self).__init__()
        CentralWidget.set_instance(self)

        self.data_handler = data_handler

        self.overview = CentralWidgetOverview(data_handler, get_overview_funct)

        self.overview_pruefungsplan = None

        self.manuelle_eingabe = manuelle_eingabe.ManuelleEingabe(data_handler, self)

        self.layout = QHBoxLayout(self)

        self.layout.setMargin(0)

        self.setLayout(self.layout)

    def init_overview(self, datatype=None):
        MainWindow.get_instance().menuWidget().set_title_text("Prüfungsplanung")
        if(self.layout.count() > 0):
            self.layout.removeWidget(self.manuelle_eingabe)
            self.manuelle_eingabe.hide()
            if not self.overview_pruefungsplan is None:
                self.layout.removeWidget(self.overview_pruefungsplan)
                self.overview_pruefungsplan.deleteLater()
                self.overview_pruefungsplan = None

        if not(datatype is None):
            self.overview.update_current_datatype(datatype, True)
        else:
            self.overview.update_current_datatype(self.overview.current_datatype, True)

        self.layout.addWidget(self.overview)
        self.overview.show()

    def init_overview_pruefungsplan(self):
        MainWindow.get_instance().menuWidget().set_title_text("Prüfungsplanung - Berechnet")
        if(self.layout.count() > 0):
            self.layout.removeWidget(self.overview)
            self.overview.hide()
            self.layout.removeWidget(self.manuelle_eingabe)
            self.manuelle_eingabe.hide()
            if not self.overview_pruefungsplan is None:
                self.layout.removeWidget(self.overview_pruefungsplan)
                self.overview_pruefungsplan.deleteLater()
                self.overview_pruefungsplan = None

        self.overview_pruefungsplan = overview.Overview(self.data_handler, datatypes.PruefungsplanElement)
        self.layout.addWidget(self.overview_pruefungsplan)
        self.overview_pruefungsplan.show()

    def init_manuelle_eingabe(self, datatype):
        MainWindow.get_instance().menuWidget().set_title_text("Prüfungsplanung - Manuelle Eingabe")
        if(self.layout.count() > 0):
            self.layout.removeWidget(self.overview)
            self.overview.hide()
            if not self.overview_pruefungsplan is None:
                self.layout.removeWidget(self.overview_pruefungsplan)
                self.overview_pruefungsplan.deleteLater()
                self.overview_pruefungsplan = None

        if datatype == datatypes.Raum:
            self.manuelle_eingabe.init_manuelle_eingabe_raum()
        elif datatype == datatypes.Aufsichtsperson:
            self.manuelle_eingabe.init_manuelle_eingabe_aufsichtsperson()
        elif datatype == datatypes.Pruefung:
            self.manuelle_eingabe.init_manuelle_eingabe_pruefung()

        self.layout.addWidget(self.manuelle_eingabe)
        self.manuelle_eingabe.show()

    def init_bearbeiten(self, data_object):
        MainWindow.get_instance().menuWidget().set_title_text("Prüfungsplanung - Bearbeiten")
        if(self.layout.count() > 0):
            self.layout.removeWidget(self.overview)
            self.overview.hide()
            if not self.overview_pruefungsplan is None:
                self.layout.removeWidget(self.overview_pruefungsplan)
                self.overview_pruefungsplan.deleteLater()
                self.overview_pruefungsplan = None

        self.manuelle_eingabe.init_bearbeiten(data_object)

        self.layout.addWidget(self.manuelle_eingabe)
        self.manuelle_eingabe.show()

    @staticmethod
    def get_instance():
        return CentralWidget.instance

    @staticmethod
    def set_instance(central_widget):
        CentralWidget.instance = central_widget

class CentralWidgetOverview(QWidget):
    """
    CentralWidget of MainWindow
    """

    __selected_stylesheet = ("QPushButton {"
                           "border: 1px solid #adadad;"
                           "background-color: #ffffff;"
                           "padding-top: 3px;"
                           "padding-bottom: 3px;"
                           "border-top-left-radius:5px;"
                           "border-top-right-radius:5px;"
                           "}"
                           "QPushButton:hover {"
                           "border: 1px solid #0078d7;"
                           "background-color: #e5f1fb;"
                           "}")

    __normal_stylesheet = ("QPushButton {"
                           "border: 1px solid #adadad;"
                           "background-color: #D9D9DA;"
                           "padding-top: 3px;"
                           "padding-bottom: 3px;"
                           "border-top-left-radius:5px;"
                           "border-top-right-radius:5px;"
                           "}"
                           "QPushButton:hover {"
                           "border: 1px solid #0078d7;"
                           "background-color: #e5f1fb;"
                           "}")
    current_datatype = datatypes.Raum
    instance = None

    def __init__(self, data_handler, get_overview_funct, current_datatype=None):
        super(CentralWidgetOverview, self).__init__()
        CentralWidgetOverview.set_instance(self)

        self.data_handler = data_handler
        self.get_overview_funct = get_overview_funct
        self.current_overview = None

        if not (current_datatype is None):
            CentralWidgetOverview.set_current_datatype(current_datatype)

        # tabs
        self.tab_raeume = QPushButton("Räume")
        self.tab_aufsichtspersonen = QPushButton("Aufsichtspersonen")
        self.tab_pruefungen = QPushButton("Prüfungen")

        self.tab_raeume.clicked.connect(lambda: self.update_current_datatype(datatypes.Raum))
        self.tab_aufsichtspersonen.clicked.connect(lambda: self.update_current_datatype(datatypes.Aufsichtsperson))
        self.tab_pruefungen.clicked.connect(lambda: self.update_current_datatype(datatypes.Pruefung))

        self.tab_raeume.setStyleSheet(self.__normal_stylesheet)
        self.tab_aufsichtspersonen.setStyleSheet(self.__normal_stylesheet)
        self.tab_pruefungen.setStyleSheet(self.__normal_stylesheet)


        #layout
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        self.grid_layout.setHorizontalSpacing(0)
        self.grid_layout.setVerticalSpacing(0)

        self.grid_layout.addWidget(self.tab_raeume,0,0)
        self.grid_layout.addWidget(self.tab_aufsichtspersonen,0,1)
        self.grid_layout.addWidget(self.tab_pruefungen,0,2)
        self.grid_layout.setMargin(0)

        #overview
        self.update_current_datatype(CentralWidgetOverview.get_current_datatype(), force_update=True)

        # add update listener
        data_handler.add_update_listener(self.data_updated)



    def data_updated(self, datatype):
        """
        called when data updated
        :param datatype: class of datatypes.py
        :return:
        """
        if CentralWidgetOverview.get_current_datatype() == datatype:
            # remove old overview
            if self.current_overview != None:
                self.grid_layout.removeWidget(self.current_overview)
                self.current_overview.deleteLater()

            self.set_current_overview()
        else:
            self.update_current_datatype(datatype)


    def update_current_datatype(self, datatype, force_update = False):
        """
        updates the widget based on datatype
        :param datatype: class of datatypes.py
        :return: None
        """
        if CentralWidgetOverview.get_current_datatype() != datatype or force_update:
            # update button paletts
            if CentralWidgetOverview.get_current_datatype() == datatypes.Raum:
                self.tab_raeume.setStyleSheet(self.__normal_stylesheet)
            elif CentralWidgetOverview.get_current_datatype() == datatypes.Aufsichtsperson:
                self.tab_aufsichtspersonen.setStyleSheet(self.__normal_stylesheet)
            elif CentralWidgetOverview.get_current_datatype() == datatypes.Pruefung:
                self.tab_pruefungen.setStyleSheet(self.__normal_stylesheet)

            if datatype == datatypes.Raum:
                self.tab_raeume.setStyleSheet(self.__selected_stylesheet)
            elif datatype == datatypes.Aufsichtsperson:
                self.tab_aufsichtspersonen.setStyleSheet(self.__selected_stylesheet)
            elif datatype == datatypes.Pruefung:
                self.tab_pruefungen.setStyleSheet(self.__selected_stylesheet)

            #remove old overview
            if self.current_overview != None:
                self.grid_layout.removeWidget(self.current_overview)
                self.current_overview.deleteLater()

            #update overview
            CentralWidgetOverview.set_current_datatype(datatype)
            self.set_current_overview()

    def set_current_overview(self):
        """
        sets the overview and adds it to layout
        :return: None
        """
        self.current_overview = self.get_overview_funct(self.data_handler, CentralWidgetOverview.get_current_datatype(), self)
        self.grid_layout.addWidget(self.current_overview,1,0,1,6)

    def paintEvent(self, event:QPaintEvent):
        """
        draws background
        :param event:
        :return: None
        """
        color = QColor(240,240,240)
        white = QColor(255,255,255)
        custom_painter = QPainter(self)
        custom_painter.fillRect(self.rect(), white)

    @staticmethod
    def set_current_datatype(datatype):
        CentralWidgetOverview.current_datatype = datatype
    @staticmethod
    def get_current_datatype():
        return CentralWidgetOverview.current_datatype


    @staticmethod
    def set_instance(instance):
        CentralWidgetOverview.instance = instance
    @staticmethod
    def get_instance():
        return CentralWidgetOverview.instance
