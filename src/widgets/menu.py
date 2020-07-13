from PySide2 import QtCore, QtWidgets
from PySide2.QtCore import QVariantAnimation, QSize, QAbstractAnimation, QEasingCurve
from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap, QMatrix

from src.data import data_handler
from src.data import datatypes
from src.widgets import main_window

ANIMATION_DURATION_MENU = 200
ANIMATION_DURATION = 150


def get_line(parent):
    """
    returns line widget
    :param parent:
    :return:
    """
    widget = QtWidgets.QFrame(parent)
    widget.setMaximumHeight(1)
    widget.setMinimumHeight(1)
    widget.setStyleSheet("background-color: #707070;")
    return widget


class MenuDropdown(QtWidgets.QWidget):
    """
    dropdown menu handles animation on hide and show
    """
    margin = 20

    def __init__(self, parent):
        super(MenuDropdown, self).__init__(parent)

        self.__layout = QtWidgets.QVBoxLayout(self)
        self.__layout.setSpacing(0)
        self.__layout.setMargin(0)

        self.setLayout(self.__layout)

        self.setStyleSheet(("QPushButton {"
                            "font-size: 13px;"
                            "padding-left: 30px;"
                            "padding-right: 7px;"
                            "}"
                            "QFrame {"
                            "margin-left: %ipx;"
                            "margin-right: %ipx;"
                            "}") % (self.margin, self.margin))
        self.anim = None
        self.turned = False

    def init_animation(self):
        """
        inits animation
        :return:
        """
        self.anim = QVariantAnimation(self)

        self.anim.setStartValue(QSize(self.parent().parent().menu_width, 0))
        self.anim.setEndValue(QSize(self.parent().parent().menu_width, self.sizeHint().height()))
        self.anim.valueChanged.connect(self.setFixedSize)
        self.anim.finished.connect(self._anim_finished)
        self.anim.setDuration(ANIMATION_DURATION)

    def show(self):
        """
        show with animation
        :return:
        """
        if not self.turned:
            if self.anim == None:
                self.init_animation()
            self.anim.setDirection(QAbstractAnimation.Forward)
            self.anim.start()
            self.turned = not self.turned
        super().show()

    def hide(self):
        """
        hide with animation
        :return:
        """
        if self.turned:
            if self.anim == None:
                self.init_animation()
            self.anim.setDirection(QAbstractAnimation.Backward)
            self.anim.start()
            self.turned = not self.turned


    def super_hide(self):
        """
        hide without animation
        :return:
        """
        super().hide()

    def _anim_finished(self):
        """
        called when animation finished and finally hides the dropdown
        :return:
        """
        if self.height() == 0:
            super().hide()

    def add_widget(self, widget, with_dividing_line=True):
        """
        add new widget to dropdown
        :param widget:
        :param with_dividing_line: add dividing line?
        :return:
        """
        widget.setObjectName("dropdown")
        self.__layout.addWidget(widget)
        if with_dividing_line:
            self.__layout.addWidget(get_line(self))


class CustomMenu(QtWidgets.QMenu):
    """
    handles extra functions for animation
    """

    def __init__(self, parent, custom_close_funct):
        super(CustomMenu, self).__init__(parent)
        self.custom_close_funct = custom_close_funct

    def close(self) -> bool:
        self.custom_close_funct()

    def leaveEvent(self, event):
        self.custom_close_funct()

    def super_close(self) -> bool:
        return super().close()


class CustomIconButton(QtWidgets.QPushButton):
    """
    custom icon button which icon can turn by 180
    """

    def __init__(self, text_str, parent, turn_degree=180):
        super(CustomIconButton, self).__init__(text_str, parent)
        self.icon = None
        self.anim = None
        self.turned = False
        self.turn_degree = turn_degree

    def set_duration(self, duration):
        if self.anim is None:
            self.init_animation()

        self.anim.setDuration(duration)

    def setIcon(self, icon: QPixmap):
        self.icon = icon
        super().setIcon(self.icon)

    def turn_icon(self):
        """
        starts the turn anim
        :return:
        """
        if self.anim is None:
            self.init_animation()

        if not self.turned:
            self.anim.setDirection(QAbstractAnimation.Forward)
        else:
            self.anim.setDirection(QAbstractAnimation.Backward)

        self.turned = not self.turned

        self.anim.start()

    def _turn(self, var: QSize):
        """
        turns icon
        :param var:
        :return:
        """
        rm = QMatrix()
        rm.rotate(var.width())
        super().setIcon(self.icon.transformed(rm))

    def init_animation(self):
        """
        inits anim
        :return:
        """
        self.anim = QVariantAnimation(self)
        self.anim.setStartValue(QSize(0, 0))
        self.anim.setEndValue(QSize(self.turn_degree, 0))
        self.anim.setDuration(ANIMATION_DURATION)
        self.anim.valueChanged.connect(self._turn)


class Menu(QtWidgets.QWidget):
    button_disabled_stylesheet = "QPushButton#disabled {" \
                                 "color: #919191" \
                                 "}"
    menu_width = 270

    def __init__(self, data_handler: data_handler.DataHandler):
        super(Menu, self).__init__()

        self.closed_icon = QPixmap('resources/images/chevron-down-solid.svg')

        self.data_handler = data_handler
        self.menubar_layout = QtWidgets.QHBoxLayout()
        self.menubar_layout.setMargin(0)
        self.menubar_button = QtWidgets.QPushButton("Menu", self)
        self.menubar_button.setIcon(QPixmap("resources/images/bars-solid_bigger.png"))
        self.menubar_button.setIconSize(QSize(32, 16))
        self.menubar_button.setObjectName("menubar")
        self.menubar_button.clicked.connect(self.open_menu)
        self.menubar_label = QtWidgets.QLabel("Prüfungsplanug")
        self.menubar_label.setObjectName("menubar")
        self.menubar_layout.addWidget(self.menubar_button)
        self.menubar_layout.addWidget(self.menubar_label)
        self.menubar_layout.setAlignment(QtCore.Qt.AlignLeft)
        self.setLayout(self.menubar_layout)

        self.__init_menu()

        self.anim = None

        self.data_handler.add_update_listener(self.data_updated)
        self.setStyleSheet("QPushButton#menubar {"
                           "border: None;"
                           "color: #676767;"
                           "padding: 10px;"
                           "width: 100px;"
                           "font: 500 14px;"
                           "}"
                           "QPushButton#menubar:hover {"
                           "background-color: #DFDFDF;"
                           "}"
                           "QLabel#menubar {"
                           "color: #676767;"
                           "font: 500 14px;"
                           "}")
        self.menu.setStyleSheet("QWidget {"
                                "text-align: left;"
                                "font-size: 18px;"
                                "}"
                                "QMenu {"
                                "background-color: #EAEAEA;"
                                "}"
                                "QPushButton {"
                                "background-color: #EAEAEA;"
                                "border: None;"
                                "padding-top: 12px;"
                                "padding-bottom: 12px;"
                                "padding-left: 20px;"
                                "padding-right: 20px;"
                                "}"
                                "QPushButton:hover {"
                                "background-color: #DFDFDF;"
                                "}"
                                "QPushButton#dropdown {"
                                "padding-top: 10px;"
                                "padding-bottom: 10px;"
                                "}"
                                "QFrame {"
                                "margin-left: 10px;"
                                "margin-right: 10px;"
                                "}"
                                "QLabel#title {"
                                "background-color: #939393;"
                                "padding-left: 10px;"
                                "padding-top: 20px;"
                                "padding-bottom: 20px;"
                                "margin-left: 0px;"
                                "margin-right: 0px;"
                                "}")

    def set_title_text(self, newtext):
        """
        Changes the text in the menubar
        :param newtext: New text to be shown in the menubar
        :return:
        """
        self.menubar_label.setText(newtext)

    def open_menu(self):
        """
        opens the menu
        :return:
        """
        self.menu.move(self.mapToGlobal(self.pos()))
        self.menu.setFixedWidth(0)
        self.menu.show()
        if self.anim == None:
            self.menu.setMinimumHeight(self.parentWidget().size().height())
            self.init_animation()
        self.do_animation(True)

    def close_menu(self):
        """
        close with anim
        :return:
        """
        self.do_animation(False)

    def init_animation(self):
        """
        inits the animation
        :return:
        """
        self.anim = QVariantAnimation(self.menu)
        self.anim.valueChanged.connect(self.menu.setFixedSize)
        self.anim.finished.connect(self.finished_animation)
        self.anim.setStartValue(QSize(0, self.menu.height()))
        self.anim.setEndValue(QSize(self.menu_width, self.menu.height()))
        self.anim.setEasingCurve(QEasingCurve.InOutQuad)
        self.anim.setDuration(ANIMATION_DURATION_MENU)

    def do_animation(self, open):
        """
        do menu animation
        :param open:
        :return:
        """
        if open:
            self.anim.setDirection(QAbstractAnimation.Forward)
        else:
            self.anim.setDirection(QAbstractAnimation.Backward)
        self.anim.start()

    def finished_animation(self):
        """
        called when anim is finished and closes menu
        :return:
        """
        if self.menu.width() == 0:
            self.menu.super_close()

    def data_updated(self, datatype):
        """
        if data_updated update the buttons
        :param datatype:
        :return:
        """
        if self.data_handler.empty(datatype):
            self.__berechnen_disable()
            self.__export_disable(datatype)
        else:
            if not self.data_handler.empty(datatypes.Raum) \
                    and not self.data_handler.empty(datatypes.Aufsichtsperson) \
                    and not self.data_handler.empty(datatypes.Pruefung):
                self.__berechnen_enable()
            self.__export_enable(datatype)

    def __init_menu(self):
        """
        inits the menu
        :return:
        """
        self.menu = CustomMenu(self, self.close_menu)

        # layouts
        self.menu_layout = QtWidgets.QVBoxLayout(self.menu)
        self.menu_layout.setSpacing(0)
        self.menu_layout.setMargin(0)

        # dropdowns
        self.manuelle_eingabe_dropdown = MenuDropdown(self)
        self.import_dropdown = MenuDropdown(self)
        self.export_dropdown = MenuDropdown(self)

        # setting the Label
        self.menu_label = QtWidgets.QLabel("<font size=4><b>Menü</b></font><br>PrüPla")
        self.menu_layout.addWidget(self.menu_label)
        self.menu_label.setObjectName("title")

        # Defining the Buttons
        self.menu_uebersichtbutton = QtWidgets.QPushButton("Übersicht", self.menu)
        self.menu_berechnenbutton = QtWidgets.QPushButton("Berechnen", self.menu)
        self.menu_manuelle_eingabe_toggle = CustomIconButton("manuelle Eingabe", self.menu)
        self.menu_manuelle_eingabe_raum = QtWidgets.QPushButton("Manuelle Eingabe - Raum", self.menu)
        self.menu_manuelle_eingabe_aufsicht = QtWidgets.QPushButton("Manuelle Eingabe - Aufsichtsperson"
                                                                    , self.menu)
        self.menu_manuelle_eingabe_pruefung = QtWidgets.QPushButton("Manuelle Eingabe - Prüfung", self.menu)
        self.menu_import_toggle = CustomIconButton("Importieren", self.menu)
        self.menu_import_raum = QtWidgets.QPushButton("Raum CSV-Import", self.menu)
        self.menu_import_aufsicht = QtWidgets.QPushButton("Aufsichtsperson CSV-Import", self.menu)
        self.menu_import_pruefung = QtWidgets.QPushButton("Prüfung CSV-Import", self.menu)
        self.menu_export_toggle = CustomIconButton("Exportieren", self.menu)
        self.menu_export_raum = QtWidgets.QPushButton("Raum CSV-Export", self.menu)
        self.menu_export_aufsicht = QtWidgets.QPushButton("Aufsichtsperson CSV-Export", self.menu)
        self.menu_export_pruefung = QtWidgets.QPushButton("Prüfung CSV-Export", self.menu)

        self.menu_export_line = get_line(self)
        self.spacer = QtWidgets.QWidget(self.menu)

        # adding buttons to Layout
        self.menu_layout.addWidget(self.menu_uebersichtbutton)
        self.menu_layout.addWidget(get_line(self))
        self.menu_layout.addWidget(self.menu_berechnenbutton)
        self.menu_layout.addWidget(get_line(self))
        self.menu_layout.addWidget(self.menu_manuelle_eingabe_toggle)
        self.menu_layout.addWidget(get_line(self))
        self.menu_layout.addWidget(self.manuelle_eingabe_dropdown)
        self.menu_layout.addWidget(self.menu_import_toggle)
        self.menu_layout.addWidget(get_line(self))
        self.menu_layout.addWidget(self.import_dropdown)
        self.menu_layout.addWidget(self.menu_export_toggle)
        self.menu_layout.addWidget(self.menu_export_line)
        self.menu_layout.addWidget(self.export_dropdown)
        self.menu_layout.addWidget(self.spacer)

        # adding buttons to layout_manuelle_eingabe_dropdown
        self.manuelle_eingabe_dropdown.add_widget(self.menu_manuelle_eingabe_raum)
        self.manuelle_eingabe_dropdown.add_widget(self.menu_manuelle_eingabe_aufsicht)
        self.manuelle_eingabe_dropdown.add_widget(self.menu_manuelle_eingabe_pruefung)

        # adding buttons to layout_manuelle_eingabe_dropdown
        self.import_dropdown.add_widget(self.menu_import_raum)
        self.import_dropdown.add_widget(self.menu_import_aufsicht)
        self.import_dropdown.add_widget(self.menu_import_pruefung)

        # adding buttons to layout_manuelle_eingabe_dropdown
        self.export_dropdown.add_widget(self.menu_export_raum)
        self.export_dropdown.add_widget(self.menu_export_aufsicht)
        self.export_dropdown.add_widget(self.menu_export_pruefung, with_dividing_line=False)

        # binding the actions to the buttons
        self.menu_uebersichtbutton.clicked.connect(self.__uebersicht)
        self.menu_berechnenbutton.clicked.connect(self.__berechnen)
        self.menu_manuelle_eingabe_toggle.clicked.connect(self.__toggle_mauelle_eingabe)
        self.menu_manuelle_eingabe_raum.clicked.connect(self.__manuelle_eingabe_raum)
        self.menu_manuelle_eingabe_aufsicht.clicked.connect(self.__manuelle_eingabe_ausicht)
        self.menu_manuelle_eingabe_pruefung.clicked.connect(self.__manuelle_eingabe_pruefung)
        self.menu_import_toggle.clicked.connect(self.__toggle_import)
        self.menu_import_raum.clicked.connect(self.__import_raum)
        self.menu_import_aufsicht.clicked.connect(self.__import_aufsicht)
        self.menu_import_pruefung.clicked.connect(self.__import_pruefung)
        self.menu_export_toggle.clicked.connect(self.__toggle_export)
        self.menu_export_raum.clicked.connect(self.__export_raum)
        self.menu_export_aufsicht.clicked.connect(self.__export_aufsicht)
        self.menu_export_pruefung.clicked.connect(self.__export_pruefung)

        # deactivating not usable buttons
        if self.data_handler.empty(datatypes.Pruefung) or self.data_handler.empty(
                datatypes.Aufsichtsperson) or self.data_handler.empty(datatypes.Raum):
            self.__berechnen_disable()
        if self.data_handler.empty(datatypes.Raum):
            self.__export_disable(datatypes.Raum)
        if self.data_handler.empty(datatypes.Aufsichtsperson):
            self.__export_disable(datatypes.Aufsichtsperson)
        if self.data_handler.empty(datatypes.Pruefung):
            self.__export_disable(datatypes.Pruefung)

        # hiding secondary buttons
        self.manuelle_eingabe_dropdown.super_hide()
        self.import_dropdown.super_hide()
        self.export_dropdown.super_hide()
        self.menu_export_line.hide()

        # adding Icons
        self.menu_manuelle_eingabe_toggle.setIcon(self.closed_icon)
        self.menu_import_toggle.setIcon(self.closed_icon)
        self.menu_export_toggle.setIcon(self.closed_icon)

        self.menu_manuelle_eingabe_toggle.setLayoutDirection(Qt.RightToLeft)
        self.menu_import_toggle.setLayoutDirection(Qt.RightToLeft)
        self.menu_export_toggle.setLayoutDirection(Qt.RightToLeft)

        self.menu_layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.menu_layout)

    def __berechnen_disable(self):
        self.menu_berechnenbutton.setDisabled(True)
        self.menu_export_aufsicht.setStyleSheet(self.button_disabled_stylesheet)

    def __berechnen_enable(self):
        self.menu_berechnenbutton.setDisabled(False)
        self.menu_export_raum.setStyleSheet("")

    def __export_disable(self, datatype):
        if datatype == datatypes.Raum:
            self.menu_export_raum.setDisabled(True)
            self.menu_export_raum.setStyleSheet(self.button_disabled_stylesheet)
        elif datatype == datatypes.Aufsichtsperson:
            self.menu_export_aufsicht.setDisabled(True)
            self.menu_export_aufsicht.setStyleSheet(self.button_disabled_stylesheet)
        elif datatype == datatypes.Pruefung:
            self.menu_export_pruefung.setDisabled(True)
            self.menu_export_pruefung.setStyleSheet(self.button_disabled_stylesheet)

        if not self.menu_export_raum.isEnabled() \
                and not self.menu_export_aufsicht.isEnabled() \
                and not self.menu_export_pruefung.isEnabled():
            self.__close_export_dropdown()
            self.menu_export_toggle.setDisabled(True)
            self.menu_export_toggle.setStyleSheet(self.button_disabled_stylesheet)

    def __export_enable(self, datatype):
        if datatype == datatypes.Raum:
            self.menu_export_raum.setDisabled(False)
            self.menu_export_raum.setStyleSheet("")
        elif datatype == datatypes.Aufsichtsperson:
            self.menu_export_aufsicht.setDisabled(False)
            self.menu_export_aufsicht.setStyleSheet("")
        elif datatype == datatypes.Pruefung:
            self.menu_export_pruefung.setDisabled(False)
            self.menu_export_pruefung.setStyleSheet("")

        self.menu_export_toggle.setDisabled(False)
        self.menu_export_toggle.setStyleSheet("")

    def __uebersicht(self):
        self.parentWidget().centralWidget().init_overview()
        # self.menu.close()
        self.close_menu()

    def __berechnen(self):
        #algorithm.calc(self.data_handler)
        self.close_menu()
        main_window.MainWindow.get_instance().init_calc()

    def __toggle_mauelle_eingabe(self):
        if self.manuelle_eingabe_dropdown.isVisible():
            self.__close_manuelle_eingabe_dropdown()
        else:
            if self.import_dropdown.isVisible():
                self.__close_import_dropdown()
            if self.export_dropdown.isVisible():
                self.__close_export_dropdown()
            self.menu_manuelle_eingabe_toggle.turn_icon()
            self.manuelle_eingabe_dropdown.show()

    def __close_manuelle_eingabe_dropdown(self):
        self.menu_manuelle_eingabe_toggle.turn_icon()
        self.manuelle_eingabe_dropdown.hide()

    def __manuelle_eingabe_raum(self):
        self.close_menu()
        self.parentWidget().centralWidget().init_manuelle_eingabe(datatypes.Raum)

    def __manuelle_eingabe_ausicht(self):
        self.close_menu()
        self.parentWidget().centralWidget().init_manuelle_eingabe(datatypes.Aufsichtsperson)

    def __manuelle_eingabe_pruefung(self):
        self.close_menu()
        self.parentWidget().centralWidget().init_manuelle_eingabe(datatypes.Pruefung)

    def __toggle_import(self):
        if self.import_dropdown.isVisible():
            self.__close_import_dropdown()
        else:
            if self.manuelle_eingabe_dropdown.isVisible():
                self.__close_manuelle_eingabe_dropdown()
            if self.export_dropdown.isVisible():
                self.__close_export_dropdown()
            self.menu_import_toggle.turn_icon()
            self.import_dropdown.show()

    def __close_import_dropdown(self):
        self.menu_import_toggle.turn_icon()
        self.import_dropdown.hide()

    def __import_raum(self):
        self.data_handler.import_raeume_csv(self.parentWidget().centralWidget())
        self.close_menu()

    def __import_aufsicht(self):
        self.data_handler.import_aufsichtspersonen_csv(self.parentWidget().centralWidget())
        self.close_menu()

    def __import_pruefung(self):
        self.data_handler.import_pruefungen_csv(self.parentWidget().centralWidget())
        self.close_menu()

    def __toggle_export(self):
        if self.export_dropdown.isVisible():
            self.__close_export_dropdown()
        else:
            if self.manuelle_eingabe_dropdown.isVisible():
                self.__close_manuelle_eingabe_dropdown()
            if self.import_dropdown.isVisible():
                self.__close_import_dropdown()

            if not self.export_dropdown.turned:
                self.menu_export_toggle.turn_icon()
            self.export_dropdown.show()
            self.menu_export_line.show()

    def __close_export_dropdown(self):
        if self.export_dropdown.turned:
            self.menu_export_toggle.turn_icon()
        self.export_dropdown.hide()
        self.menu_export_line.hide()

    def __export_raum(self):
        self.data_handler.export_raeume_csv(self.parentWidget().centralWidget())
        self.close_menu()

    def __export_aufsicht(self):
        self.data_handler.export_aufsichtspersonen_csv(self.parentWidget().centralWidget())
        self.close_menu()

    def __export_pruefung(self):
        self.data_handler.export_pruefungen_csv(self.parentWidget().centralWidget())
        self.close_menu()

    def resizeEvent(self, event):
        super().resizeEvent(event)

        self.menu.setFixedHeight(self.parent().height())
        if not self.anim is None:
            self.anim.setStartValue(QSize(0, self.menu.height()))
            self.anim.setEndValue(QSize(self.menu_width, self.menu.height()))
