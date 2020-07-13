import abc

from PySide2 import QtWidgets
from PySide2.QtCore import Qt, QEvent
from PySide2.QtGui import QPaintEvent, QPainter, QColor, QResizeEvent, QFontMetrics, QMouseEvent, QPixmap

from src.data import datatypes
from src.widgets import main_window
from src.widgets.elements import detailed_view


class BetterLabel(QtWidgets.QLabel):
    def __init__(self, parent):
        super(BetterLabel, self).__init__(parent)

        self.setMouseTracking(True)

    def mouseMoveEvent(self, ev: QMouseEvent):
        self.parent().mouseMoveEvent(ev)


class DataObjectWidget(QtWidgets.QWidget):
    border_color = QColor(112, 112, 112)

    def __init__(self, color: QColor, with_menu=True, parent=None):
        super(DataObjectWidget, self).__init__(parent)

        self.data = None

        self.back_color = color

        # policy
        self.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)

        # init
        self.label = BetterLabel(self)

        # layout
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setMargin(3)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.addWidget(self.label)

        self.setLayout(self.layout)

        # flags
        self.setMouseTracking(True)

        # menu
        if with_menu:
            self.menu = QtWidgets.QMenu(self)
            self.add_menu_actions()
        else:
            self.menu = None

    def init_detailed_view(self):
        """
        inits detailed view
        :return:
        """
        self.detailed_view = detailed_view.DetailedView(_parent=self)
        self.detailed_view.close()

    def add_menu_actions(self):
        """
        adds actions to menu
        :return:
        """
        # init
        edit = QtWidgets.QAction(self)
        delete = QtWidgets.QAction(self)

        # trigger
        edit.triggered.connect(self.edit)
        delete.triggered.connect(self.delete)

        # text
        edit.setText("Bearbeiten")
        delete.setText("Löschen")

        edit.setIcon(QPixmap("resources/images/pen-solid.svg"))
        delete.setIcon(QPixmap("resources/images/trash-solid.svg"))

        # add
        self.menu.addAction(edit)
        self.menu.addAction(delete)

    def edit(self):
        """
        edit data
        :return:
        """
        main_window.CentralWidget.get_instance().init_bearbeiten(self.data)

    def delete(self):
        """
        delete data
        :return:
        """
        self.parent().data_handler.remove(self.data)



    def paintEvent(self, event: QPaintEvent):
        """
        draws background
        :param event:
        :return: None
        """
        custom_painter = QPainter(self)
        custom_painter.fillRect(self.rect(), self.back_color)

        custom_painter.setPen(self.border_color)
        custom_painter.drawRect(0, 0, self.rect().width() - 1, self.rect().height() - 1)

    def resizeEvent(self, event: QResizeEvent):
        """
        set correct text on resize
        :param event:
        :return:
        """
        text = self.normal_text()

        if self.get_text_width(text, 0.7) > self.label.frameGeometry().width():
            text = self.medium_text()

            if self.get_text_width(text, 0.5) > self.label.frameGeometry().width():
                text = self.small_text()

        self.label.setText(text)

        self.detailed_view.resizeEvent(event)

    def get_text_width(self, text, factor):
        text = text.split('<br>')
        # test text width
        font_width = 0
        for t in text:
            tmp_font_width = QFontMetrics(self.label.font()).boundingRect(t).width()
            if tmp_font_width > font_width:
                font_width = tmp_font_width

        return font_width * factor

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.RightButton and not(self.menu is None):
            # right click
            self.detailed_view.close()
            self.menu.move(self.cursor().pos())
            self.menu.show()

    def mouseMoveEvent(self, event: QMouseEvent):
        self.detailed_view.move_to_mouse()

    def leaveEvent(self, event: QEvent):
        self.detailed_view.ask_close()

    def deleteLater(self):
        self.detailed_view.deleteLater()
        super().deleteLater()

    @abc.abstractmethod
    def normal_text(self):
        return

    @abc.abstractmethod
    def medium_text(self):
        return

    @abc.abstractmethod
    def small_text(self):
        return


class RaumWidget(DataObjectWidget):
    """
    widget for overview
    """

    def __init__(self, raum: datatypes.Raum, color: QColor, parent=None):
        super().__init__(color, parent=parent)

        self.data = raum

        self.normal_text()

    def init_detailed_view(self):
        super().init_detailed_view()
        # detailed view text
        self.detailed_view.set_title("Raum-ID: %s" % self.data.id)
        self.detailed_view.set_content("Kapazität: %i\nVom: %s\nBis zum: %s" % (
            self.data.kapazitaet, datatypes.timestamp_to_string(self.data.timestamp),
            datatypes.timestamp_to_string(self.data.timestamp + self.data.verfuegbarkeit * 60 * 1000)))

    def normal_text(self):
        return ("<font size=\"5\">Raum-ID: %s</font><br>Kapazität: %i" % (self.data.id, self.data.kapazitaet))

    def medium_text(self):
        return ("<font size=\"5\">ID: %s</font><br>Teilnehmer: %i" % (self.data.id, self.data.kapazitaet))

    def small_text(self):
        return ("%s" % (self.data.id))


class AufsichtspersonWidget(DataObjectWidget):
    """
    widget for overview
    """

    def __init__(self, aufsichtsperson: datatypes.Aufsichtsperson, color: QColor, parent=None, ):
        super().__init__(color, parent=parent)

        self.data = aufsichtsperson

        self.normal_text()

    def init_detailed_view(self):
        super().init_detailed_view()
        # detailed view text
        self.detailed_view.set_title("Name: %s" % self.data.name)

        if isinstance(self.data.kuerzel, str):
            self.detailed_view.set_content("Vorname: %s\nKürzel: %s\nVom: %s\nBis zum: %s" % (
                self.data.vorname, self.data.kuerzel,
                datatypes.timestamp_to_string(self.data.timestamp),
                datatypes.timestamp_to_string(
                    self.data.timestamp + self.data.verfuegbarkeit * 60 * 1000)))

        else:
            self.detailed_view.set_content("Vorname: %s\nVom: %s\nBis zum: %s" % (
                self.data.vorname,
                datatypes.timestamp_to_string(self.data.timestamp),
                datatypes.timestamp_to_string(
                    self.data.timestamp + self.data.verfuegbarkeit * 60 * 1000)))

    def normal_text(self):
        return ("<font size=\"5\">Name: %s" % (self.data.name))

    def medium_text(self):
        return ("<font size=\"5\">%s</font>" % (self.data.name))

    def small_text(self):
        if isinstance(self.data.kuerzel, str):
            return ("%s" % (self.data.kuerzel))
        else:
            return ("%s" % (self.data.name))


class PruefungWidget(DataObjectWidget):
    """
    widget for overview
    """

    def __init__(self, pruefung: datatypes.Pruefung, color: QColor, parent=None):
        super().__init__(color, parent=parent)

        self.data = pruefung

        self.normal_text()

        # detailed view text


    def init_detailed_view(self):
        super().init_detailed_view()

        pruefungs_art = 'schriftlich' if self.data.art == 's' else 'mündlich'

        self.detailed_view.set_title("Prüfungs-ID: %s" % self.data.id)
        if isinstance(self.data.kuerzel, str):
            self.detailed_view.set_content(
                "Kürzel: %s\nTeilnehmer: %i\nPrüfungsart: %s\nVom: %s\nBis zum: %s" % (self.data.kuerzel,
                                                                                       self.data.teilnehmer,
                                                                                       pruefungs_art,
                                                                                       datatypes.timestamp_to_string(
                                                                                           self.data.timestamp),
                                                                                       datatypes.timestamp_to_string(
                                                                                           self.data.timestamp + self.data.verfuegbarkeit * 60 * 1000)))
        else:
            self.detailed_view.set_content(
                "Teilnehmer: %i\nPrüfungsart: %s\nVom: %s\nBis zum: %s" % (self.data.teilnehmer,
                                                                           pruefungs_art,
                                                                           datatypes.timestamp_to_string(
                                                                               self.data.timestamp),
                                                                           datatypes.timestamp_to_string(
                                                                               self.data.timestamp + self.data.verfuegbarkeit * 60 * 1000)))

    def normal_text(self):
        return ("<font size=\"5\">Prüfungs-ID: %s</font><br>Teilnehmer: %i" % (self.data.id, self.data.teilnehmer))

    def medium_text(self):
        return ("<font size=\"5\">ID: %s</font><br>Teilnehmer: %i" % (self.data.id, self.data.teilnehmer))

    def small_text(self):
        return ("%s" % (self.data.id))


class PruefungsplanWidget(DataObjectWidget):
    """
    widget for overview
    """

    def __init__(self, pruefungsplan_element: datatypes.PruefungsplanElement, color: QColor, parent=None):
        super().__init__(color, False, parent=parent)

        self.data = pruefungsplan_element

        self.normal_text()

    def init_detailed_view(self):
        super().init_detailed_view()

        # detailed view text
        pruefungs_art = 'schriftlich' if self.data.pruefungs_art == 's' else 'mündlich'

        self.detailed_view.set_title("Prüfungs-ID: %s" % self.data.pruefungs_id)

        detailed_view_content_str = ""
        if isinstance(self.data.pruefungs_kuerzel, str):
            detailed_view_content_str += "Kürzel: %s\n" % self.data.pruefungs_kuerzel
        detailed_view_content_str += "Aufsichtsperson: %s" % self.data.aufischtsperson_name
        if isinstance(self.data.aufsichtsperson_vorname, str):
            detailed_view_content_str += " %s" % self.data.aufsichtsperson_vorname
        detailed_view_content_str += "\nRaum-ID: %s\nTeilnehmer: %i\nPrüfungsart: %s\nVom: %s\nBis zum: %s" % (
            self.data.raum_id,
            self.data.pruefungs_teilnehmer,
            pruefungs_art,
            datatypes.timestamp_to_string(
                self.data.timestamp),
            datatypes.timestamp_to_string(
                self.data.timestamp + self.data.verfuegbarkeit * 60 * 1000))

        self.detailed_view.set_content(detailed_view_content_str)


    def normal_text(self):
        return ("<font size=\"5\">Prüfungs-ID: %s</font><br>Raum-ID: %s<br>Aufsicht: %s" % (
            self.data.pruefungs_id, self.data.raum_id, self.data.aufischtsperson_name))

    def medium_text(self):
        return ("<font size=\"5\">P-ID: %s</font><br>R-ID: %s<br>%s" % (
            self.data.pruefungs_id, self.data.raum_id, self.data.aufischtsperson_name))

    def small_text(self):
        return ("%s" % (self.data.pruefungs_id))
