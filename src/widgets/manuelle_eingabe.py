from PySide2.QtCore import Qt, QTime, QDate
from PySide2.QtGui import QIntValidator
from PySide2.QtWidgets import QWidget, QGridLayout, QPushButton, QVBoxLayout, QLabel, QSizePolicy, QTimeEdit, \
    QDateEdit, QHBoxLayout, QComboBox

from src.data import datatypes
from src.dialogs.yes_dialog import YesDialog
from src.widgets import main_window
from src.widgets.elements.line_edit import LineEdit


def new_text_input(parent, title_str, hint_str, only_numbers=False):
    """
    creates input with title
    :param parent:
    :param title_str:
    :param hint_str:
    :param only_numbers:
    :return:
    """
    widget = QWidget(parent)
    widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

    # layout
    layout = QVBoxLayout()
    layout.setMargin(0)
    layout.setSpacing(2)

    # label
    widget.label_title = QLabel(widget)
    widget.label_title.setText(title_str)
    widget.label_title.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

    # text edit
    widget.text_edit = LineEdit(widget, hint_str)
    if only_numbers:
        widget.text_edit.setValidator(QIntValidator(0, 100, widget))

    # add to layout
    layout.addWidget(widget.label_title)
    layout.addWidget(widget.text_edit)

    widget.setLayout(layout)

    return widget


def new_combobox_input(parent, title_str, items):
    """
    creates input with title
    :param parent:
    :param title_str:
    :param hint_str:
    :param only_numbers:
    :return:
    """
    widget = QWidget(parent)
    widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

    # layout
    layout = QVBoxLayout()
    layout.setMargin(0)
    layout.setSpacing(2)

    # label
    title = QLabel(widget)
    title.setText(title_str)
    title.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

    # text edit
    widget.combobox_widget = QComboBox(widget)

    # add items
    for item in items:
        widget.combobox_widget.addItem(item)

    # add to layout
    layout.addWidget(title)
    layout.addWidget(widget.combobox_widget)

    widget.setLayout(layout)

    return widget


def new_time_input(parent, title_str, time=None):
    """
    creates input with title
    :param parent:
    :param title_str:
    :param hint_str:
    :param only_numbers:
    :return:
    """
    widget = QWidget(parent)
    widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

    # layout
    layout = QVBoxLayout()
    layout.setMargin(0)
    layout.setSpacing(2)

    # label
    title = QLabel(widget)
    title.setText(title_str)
    title.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

    # text edit
    widget.time_input = QTimeEdit(widget)
    if time is None:
        widget.time_input.setTime(QTime.currentTime())
    else:
        widget.time_input.setTime(time)

    # add to layout
    layout.addWidget(title)
    layout.addWidget(widget.time_input)

    widget.setLayout(layout)

    return widget


def new_date_input(parent, title_str, date=None):
    """
    creates input with title
    :param parent:
    :param title_str:
    :param hint_str:
    :param only_numbers:
    :return:
    """
    widget = QWidget(parent)
    widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

    # layout
    layout = QVBoxLayout()
    layout.setMargin(0)
    layout.setSpacing(2)

    # label
    title = QLabel(widget)
    title.setText(title_str)
    title.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

    # text edit
    widget.date_input = QDateEdit(widget)

    if date is None:
        widget.date_input.setDate(QDate.currentDate())
    else:
        widget.date_input.setDate(date)

    # add to layout
    layout.addWidget(title)
    layout.addWidget(widget.date_input)

    widget.setLayout(layout)

    return widget


class ManuelleEingabe(QWidget):
    instance = None

    def __init__(self, data_handler, parent):
        super(ManuelleEingabe, self).__init__(parent)
        ManuelleEingabe.set_instance(self)

        self.data_handler = data_handler

        self.layout = QGridLayout()
        self.layout.setContentsMargins(30, 10, 0, 0)
        self.layout_buttons = QHBoxLayout()
        self.layout_buttons.setMargin(0)

        self.input = None
        self.current_datatype = None

        # title label
        self.label_title = QLabel(self)
        self.label_title.setObjectName("title")
        self.label_title.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # init buttons
        self.button_add = QPushButton(self)
        self.button_cancle = QPushButton(self)

        # add text
        self.button_add.setText("Hinzufügen")
        self.button_cancle.setText("Abbrechen")

        # add object name
        self.button_add.setObjectName("add")
        self.button_cancle.setObjectName("cancle")

        # add button action
        self.button_add.clicked.connect(self.__add)
        self.button_cancle.clicked.connect(self.__cancle)

        # add to layout

        self.layout_buttons.addWidget(self.button_add)
        self.layout_buttons.addWidget(self.button_cancle)

        self.layout.addWidget(self.label_title, 0, 0, 1, 4)
        self.layout.addLayout(self.layout_buttons, 2, 0, 1, 1)
        self.layout.setAlignment(Qt.AlignTop)

        self.setLayout(self.layout)

        self.setStyleSheet("QLabel {"
                           "font: 400 13px;"
                           "}"
                           "QLabel#title {"
                           "font-size: 20px;"
                           "font-weight: bold;"
                           "}"
                           "QLineEdit {"
                           "border-radius: 2;"
                           "border: 1px solid #DEDEDF;"
                           "padding: 3px;"
                           "}"
                           "QLineEdit:focus {"
                           "border: 1px solid #0078d7;"
                           "}"
                           "QTimeEdit {"
                           "border-radius: 2;"
                           "border: 1px solid #DEDEDF;"
                           "padding: 3px;"
                           "}"
                           "QTimeEdit:focus {"
                           "border: 1px solid #0078d7;"
                           "}"
                           "QTimeEdit::up-button {"
                           "border: 1px solid #adadad;"
                           "background-color: #DEDEDF;"
                           "border-top-right-radius:2px;"
                           "border-top-left-radius:2px;"
                           "image: url(resources/images/chevron-up-solid.svg);"
                           "width: 30px;"
                           "}"
                           "QTimeEdit::up-button:hover {"
                           "border: 1px solid #0078d7;"
                           "background-color: #e5f1fb;"
                           "}"
                           "QTimeEdit::down-button {"
                           "border: 1px solid #adadad;"
                           "background-color: #DEDEDF;"
                           "border-bottom-right-radius:2px;"
                           "border-bottom-left-radius:2px;"
                           "image: url(resources/images/chevron-down-solid.svg);"
                           "width: 30px;"
                           "}"
                           "QTimeEdit::down-button:hover {"
                           "border: 1px solid #0078d7;"
                           "background-color: #e5f1fb;"
                           "}"
                           "QDateEdit {"
                           "border-radius: 2;"
                           "border: 1px solid #DEDEDF;"
                           "padding: 3px;"
                           "}"
                           "QDateEdit:focus {"
                           "border: 1px solid #0078d7;"
                           "}"
                           "QDateEdit::up-button {"
                           "border: 1px solid #adadad;"
                           "background-color: #DEDEDF;"
                           "border-top-right-radius:2px;"
                           "border-top-left-radius:2px;"
                           "image: url(resources/images/chevron-up-solid.svg);"
                           "width: 30px;"
                           "}"
                           "QDateEdit::up-button:hover {"
                           "border: 1px solid #0078d7;"
                           "background-color: #e5f1fb;"
                           "}"
                           "QDateEdit::down-button {"
                           "border: 1px solid #adadad;"
                           "background-color: #DEDEDF;"
                           "border-bottom-right-radius:2px;"
                           "border-bottom-left-radius:2px;"
                           "image: url(resources/images/chevron-down-solid.svg);"
                           "width: 30px;"
                           "}"
                           "QDateEdit::down-button:hover {"
                           "border: 1px solid #0078d7;"
                           "background-color: #e5f1fb;"
                           "}"
                           "QComboBox {"
                           "border-radius: 2;"
                           "border: 1px solid #DEDEDF;"
                           "padding: 3px;"
                           "}"
                           "QComboBox::drop-down {"
                           "border: None;"
                           "background-color: None;"
                           "image: url(resources/images/chevron-down-solid.svg);"
                           "width: 10px;"
                           "margin-right: 10px"
                           "}"
                           "QComboBox::drop-down:on {"
                           "image: url(resources/images/chevron-up-solid.svg);"
                           "}"
                           "QComboBox:hover {"
                           "border: 1px solid #0078d7;"
                           "background-color: #e5f1fb;"
                           "}"
                           "QPushButton#add {"
                           "border: None;"
                           "background-color: #2185D0;"
                           "border-radius: 2;"
                           "padding: 3px;"
                           "font: bold 12px;"
                           "color: white;"
                           "padding: 5px;"
                           "}"
                           "QPushButton#add:hover {"
                           "background-color: white;"
                           "color: #2185D0;"
                           "}"
                           "QPushButton#cancle {"
                           "border: None;"
                           "background-color: #E0E1E2;"
                           "border-radius: 2;"
                           "padding: 3px;"
                           "font: bold 12px;"
                           "color: #676767;"
                           "padding: 5px;"
                           "}"
                           "QPushButton#cancle:hover {"
                           "background-color: #676767;"
                           "color: #E0E1E2;"
                           "}")

    def init_manuelle_eingabe_raum(self):
        """
        inits manuelle eingabe raum
        :return:
        """
        # delete old
        if not (self.input is None):
            self.layout.removeWidget(self.input)
            self.input.deleteLater()

        # add new
        self.input = ManuelleEingabeRaum(self)
        self.layout.addWidget(self.input, 1, 0, 1, 3)
        self.current_datatype = datatypes.Raum

        self.__add_mode()

    def init_manuelle_eingabe_aufsichtsperson(self):
        """
        inits manuelle eingabe aufsichtsperson
        :return:
        """
        # delete old
        if not (self.input is None):
            self.layout.removeWidget(self.input)
            self.input.deleteLater()

        # add new
        self.input = ManuelleEingabeAufsichtsperson(self)
        self.layout.addWidget(self.input, 1, 0, 1, 2)
        self.current_datatype = datatypes.Aufsichtsperson

        self.__add_mode()

    def init_manuelle_eingabe_pruefung(self):
        """
        inits manuelle eingabe pruefung
        :return:
        """
        # delete old
        if not (self.input is None):
            self.layout.removeWidget(self.input)
            self.input.deleteLater()

        # add new
        self.input = ManuelleEingabePruefung(self)
        self.layout.addWidget(self.input, 1, 0, 1, 2)
        self.current_datatype = datatypes.Pruefung

        self.__add_mode()

    def init_bearbeiten(self, data_object):
        """
        inits bearbeiten_raum
        :param data_object:
        :return:
        """
        # delete old
        if not (self.input is None):
            self.layout.removeWidget(self.input)
            self.input.deleteLater()

        # add new

        if isinstance(data_object, datatypes.Raum):
            self.input = ManuelleEingabeRaum(self, data_object)
        elif isinstance(data_object, datatypes.Aufsichtsperson):
            self.input = ManuelleEingabeAufsichtsperson(self, data_object)
        elif isinstance(data_object, datatypes.Pruefung):
            self.input = ManuelleEingabePruefung(self, data_object)

        self.layout.addWidget(self.input, 1, 0, 1, 2)
        self.current_datatype = data_object.__class__

        self.__edit_mode()

    def __add_mode(self):
        self.__mode_is_add = True
        self.button_add.setText("Hinzufügen")

    def __edit_mode(self):
        self.__mode_is_add = False
        self.button_add.setText("Speichern")

    def __add(self):
        """
        fuegt das data_object dem data_handler hinzu
        :return:
        """
        data_object = self.input.create_object()
        if data_object == False:
            YesDialog("manuelle Eingabe", "Es wurden nicht alle Felder ausgefüllt.", None, self, "OK").exec_()
        else:
            if self.__mode_is_add:
                self.data_handler.add(data_object)
                self.input.clear_inputs()
            else:
                self.data_handler.overwrite(self.input.data_object, data_object)
                main_window.MainWindow.get_instance().centralWidget().init_overview(self.current_datatype)

    def __cancle(self):
        """
        geht zurueck zur overview
        :return:
        """
        main_window.MainWindow.get_instance().centralWidget().init_overview(self.current_datatype)

    @staticmethod
    def set_instance(instance):
        ManuelleEingabe.instance = instance

    @staticmethod
    def get_instance():
        return ManuelleEingabe.instance


class ManuelleEingabeRaum(QWidget):
    def __init__(self, parent, data_object: datatypes.Raum = None):
        super(ManuelleEingabeRaum, self).__init__(parent)

        self.data_object = data_object

        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        parent.label_title.setText("Neuer Eintrag: Raum")

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)

        # create inputs
        self.input_raum_id = new_text_input(self, "Raum-ID", "Raum-ID")
        self.input_kapazitaet_id = new_text_input(self, "Kapazität", "Maximale Prüfungsplätze", True)
        self.input_verfuegbarkeit = new_text_input(self, "Verfügbarkeit", "in Minuten", True)
        self.input_time = new_time_input(self, "Uhrzeit")
        self.input_date = new_date_input(self, "Datum")

        # add to layout
        self.layout.addWidget(self.input_raum_id)
        self.layout.addWidget(self.input_kapazitaet_id)
        self.layout.addWidget(self.input_verfuegbarkeit)
        self.layout.addWidget(self.input_time)
        self.layout.addWidget(self.input_date)

        self.setLayout(self.layout)

        # if edit add old data
        if not data_object is None:
            self.input_raum_id.text_edit.setText(str(data_object.id))
            self.input_kapazitaet_id.text_edit.setText(str(data_object.kapazitaet))
            self.input_verfuegbarkeit.text_edit.setText(str(data_object.verfuegbarkeit))

            datetime = datatypes.timestamp_to_datetime(data_object.timestamp)
            time = QTime(datetime.hour, datetime.minute)
            date = QDate(datetime.year, datetime.month, datetime.day)

            self.input_time.time_input.setTime(time)
            self.input_date.date_input.setDate(date)

    def clear_inputs(self):
        self.input_raum_id.text_edit.clear()
        self.input_kapazitaet_id.text_edit.clear()
        self.input_verfuegbarkeit.text_edit.clear()

    def create_object(self):
        """
        creates data_object
        :return:
        """
        if self.input_raum_id.text_edit.empty() \
                or self.input_kapazitaet_id.text_edit.empty() \
                or self.input_verfuegbarkeit.text_edit.empty():
            return False  # failed
        else:
            timestamp = self.input_date.date_input.dateTime().toMSecsSinceEpoch() + self.input_time.time_input.time().msecsSinceStartOfDay()

            return datatypes.Raum(self.input_raum_id.text_edit.text(), int(self.input_kapazitaet_id.text_edit.text()),
                                  int(self.input_verfuegbarkeit.text_edit.text()), timestamp)


class ManuelleEingabeAufsichtsperson(QWidget):
    def __init__(self, parent, data_object: datatypes.Aufsichtsperson = None):
        super(ManuelleEingabeAufsichtsperson, self).__init__(parent)

        self.data_object = data_object

        parent.label_title.setText("Neuer Eintrag: Aufsichtsperson")

        self.layout = QVBoxLayout(self)
        self.layout_name = QHBoxLayout(self)

        self.layout.setSpacing(10)

        self.layout_name.setMargin(0)

        # create inputs
        self.input_name = new_text_input(self, "Name", "Name")
        self.input_vorname = new_text_input(self, "", "Vorname (optional)")
        self.input_kuerzel = new_text_input(self, "Namens-Kürzel", "Namens-Kürzel", False)
        self.input_verfuegbarkeit = new_text_input(self, "Verfügbarkeit", "in Minuten", True)
        self.input_time = new_time_input(self, "Uhrzeit")
        self.input_date = new_date_input(self, "Datum")

        # add to layout
        self.layout_name.addWidget(self.input_name)
        self.layout_name.addWidget(self.input_vorname)

        self.layout.addLayout(self.layout_name)
        self.layout.addWidget(self.input_kuerzel)
        self.layout.addWidget(self.input_verfuegbarkeit)
        self.layout.addWidget(self.input_time)
        self.layout.addWidget(self.input_date)

        self.setLayout(self.layout)

        # if edit add old data
        if not data_object is None:
            self.input_name.text_edit.setText(str(data_object.name))
            self.input_vorname.text_edit.setText(str(data_object.vorname))
            self.input_kuerzel.text_edit.setText(str(data_object.kuerzel))
            self.input_verfuegbarkeit.text_edit.setText(str(data_object.verfuegbarkeit))

            datetime = datatypes.timestamp_to_datetime(data_object.timestamp)
            time = QTime(datetime.hour, datetime.minute)
            date = QDate(datetime.year, datetime.month, datetime.day)

            self.input_time.time_input.setTime(time)
            self.input_date.date_input.setDate(date)

    def clear_inputs(self):
        self.input_name.text_edit.clear()
        self.input_vorname.text_edit.clear()
        self.input_kuerzel.text_edit.clear()
        self.input_verfuegbarkeit.text_edit.clear()

    def create_object(self):
        """
        creates data_object
        :return:
        """
        if self.input_name.text_edit.empty() \
                or self.input_kuerzel.text_edit.empty() \
                or self.input_verfuegbarkeit.text_edit.empty():
            return False  # failed
        else:
            timestamp = self.input_date.date_input.dateTime().toMSecsSinceEpoch() + self.input_time.time_input.time().msecsSinceStartOfDay()

            return datatypes.Aufsichtsperson(self.input_name.text_edit.text(), self.input_vorname.text_edit.text(),
                                             self.input_kuerzel.text_edit.text(),
                                             int(self.input_verfuegbarkeit.text_edit.text()), timestamp)


class ManuelleEingabePruefung(QWidget):
    def __init__(self, parent, data_object: datatypes.Pruefung = None):
        super(ManuelleEingabePruefung, self).__init__(parent)

        self.data_object = data_object

        parent.label_title.setText("Neuer Eintrag: Prüfung")

        self.layout = QVBoxLayout(self)
        self.layout_id = QHBoxLayout(self)

        self.layout.setSpacing(10)
        self.layout_id.setMargin(0)

        # create inputs
        self.art_input = new_combobox_input(self, "Prüfungsart", ["schriftlich", "mündlich"])
        self.input_id = new_text_input(self, "Prüfungs-ID", "Prüfungs-ID")
        self.input_kuerzel = new_text_input(self, "", "Prüfungs-Kürzel (optional)")
        self.input_verfuegbarkeit = new_text_input(self, "Dauer", "in Minuten", True)
        self.input_teilnehmer = new_text_input(self, "Anzahl der zu Prüfenden", "Anzahl der zu Prüfenden", True)
        self.input_time = new_time_input(self, "Uhrzeit")
        self.input_date = new_date_input(self, "Datum")

        # connect art
        self.art_input.combobox_widget.currentIndexChanged.connect(self.art_changed)

        # add to layout
        self.layout_id.addWidget(self.input_id)
        self.layout_id.addWidget(self.input_kuerzel)

        self.layout.addWidget(self.art_input)
        self.layout.addLayout(self.layout_id)
        self.layout.addWidget(self.input_verfuegbarkeit)
        self.layout.addWidget(self.input_teilnehmer)
        self.layout.addWidget(self.input_time)
        self.layout.addWidget(self.input_date)

        self.setLayout(self.layout)

        # if edit add old data
        if not data_object is None:
            # art
            art_index = 0 if data_object.art == 's' else 1
            self.art_input.combobox_widget.setCurrentIndex(art_index)

            self.input_id.text_edit.setText(str(data_object.id))
            self.input_kuerzel.text_edit.setText(str(data_object.kuerzel))
            if data_object.art == 'm':
                self.input_verfuegbarkeit.text_edit.setText(str(data_object.verfuegbarkeit // data_object.teilnehmer))
            else:
                self.input_verfuegbarkeit.text_edit.setText(str(data_object.verfuegbarkeit))

            self.input_teilnehmer.text_edit.setText(str(data_object.teilnehmer))

            datetime = datatypes.timestamp_to_datetime(data_object.timestamp)
            time = QTime(datetime.hour, datetime.minute)
            date = QDate(datetime.year, datetime.month, datetime.day)

            self.input_time.time_input.setTime(time)
            self.input_date.date_input.setDate(date)

    def art_changed(self, index):
        if self.art_input.combobox_widget.currentIndex() == 0:
            self.__set_text_schriftlich()
        else:
            self.__set_text_mündlich()

    def clear_inputs(self):
        self.input_id.text_edit.clear()
        self.input_kuerzel.text_edit.clear()
        self.input_verfuegbarkeit.text_edit.clear()
        self.input_teilnehmer.text_edit.clear()

    def create_object(self):
        """
        creates data_object
        :return:
        """
        if self.input_id.text_edit.empty() \
                or self.input_verfuegbarkeit.text_edit.empty() \
                or self.input_teilnehmer.text_edit.empty():
            return False  # failed
        else:
            timestamp = self.input_date.date_input.dateTime().toMSecsSinceEpoch() + self.input_time.time_input.time().msecsSinceStartOfDay()
            art = 's' if self.art_input.combobox_widget.currentIndex() == 0 else 'm'

            teilnehmer = int(self.input_teilnehmer.text_edit.text())
            dauer = int(self.input_verfuegbarkeit.text_edit.text())
            if art == 'm':
                dauer *= teilnehmer

            return datatypes.Pruefung(art, self.input_id.text_edit.text(), self.input_kuerzel.text_edit.text(),
                                      teilnehmer,
                                      dauer, timestamp)

    def __set_text_schriftlich(self):
        self.input_teilnehmer.label_title.setText("Anzahl der zu Prüfenden")

    def __set_text_mündlich(self):
        self.input_teilnehmer.label_title.setText("Prüfungsteilnehmer")
