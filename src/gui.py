import sys

from PySide2 import QtWidgets, QtGui

from src.data import datatypes
from src.widgets import menu, overview, main_window


def get_overview(data_handler, datatype, parent_view, screen_resolution=None):
    """
    returns correct overview for datatype
    :param data_handler:
    :param datatype:
    :param parent_view:
    :return:
    """
    if (data_handler.empty(datatype)):
        # data is empty
        if datatype == datatypes.Raum:
            return overview.EmptyOverview(
                lambda: main_window.CentralWidget.get_instance().init_manuelle_eingabe(datatypes.Raum),
                lambda: data_handler.import_raeume_csv(parent_view), "Räume")
        elif datatype == datatypes.Aufsichtsperson:
            return overview.EmptyOverview(
                lambda: main_window.CentralWidget.get_instance().init_manuelle_eingabe(datatypes.Aufsichtsperson),
                lambda: data_handler.import_aufsichtspersonen_csv(parent_view), "Aufsichtspersonen")
        elif datatype == datatypes.Pruefung:
            return overview.EmptyOverview(
                lambda: main_window.CentralWidget.get_instance().init_manuelle_eingabe(datatypes.Pruefung),
                lambda: data_handler.import_pruefungen_csv(parent_view), "Prüfungen")
    else:
        return overview.Overview(data_handler, datatype)


def Window(data_handler):
    app = QtWidgets.QApplication([])

    app.setStyleSheet("QPushButton:focus {"
                      "outline: None"
                      "}")

    menubar_obj = menu.Menu(data_handler)
    central_widget_obj = main_window.CentralWidget(data_handler, get_overview)


    main_window_obj = main_window.MainWindow(menubar_obj, central_widget_obj)
    central_widget_obj.init_overview()
    main_window_obj.setMinimumWidth(700)
    main_window_obj.setMinimumHeight(480)
    main_window_obj.resize(700, 480)
    app.setWindowIcon(QtGui.QPixmap('resources/images/icon.png'))

    main_window_obj.show()

    sys.exit(app.exec_())
