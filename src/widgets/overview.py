from datetime import datetime, timedelta
from enum import Enum

from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtGui import QResizeEvent, QColor, QPainter, QPaintEvent, QPixmap

from src.data import datatypes
from src.widgets import main_window
from src.widgets.elements.clickable_label import ClickableLabel
from src.widgets.elements.dataobject_widgets import RaumWidget, AufsichtspersonWidget, PruefungWidget, \
    PruefungsplanWidget, DataObjectWidget
from src.widgets.elements.fab_button import FabButton

widget_colors = [QColor(53, 216, 178),
                 QColor(255, 214, 132),
                 QColor(164,111,183),
                 QColor(255,108,108),
                 QColor(204,246,120),
                 QColor(88,233,255),
                 QColor(193, 231, 227),
                 QColor(220, 255, 251),
                 QColor(118, 158, 203),
                 QColor(157, 186, 213),
                 QColor(250, 243, 221),
                 QColor(200, 214, 185),
                 QColor(143, 193, 169),
                 QColor(124, 170, 152),
                 QColor(68, 211, 98),
                 QColor(119, 223, 121),
                 QColor(152, 230, 144),
                 QColor(230, 230, 202),
                 QColor(230, 185, 161),
                 QColor(224, 254, 254),
                 QColor(199, 206, 234),
                 QColor(255, 218, 193),
                 QColor(255, 154, 162),
                 QColor(255, 255, 216),
                 QColor(181, 234, 215)]

class view(Enum):
    week_view = 1
    day_view = 2

class Overview(QtWidgets.QWidget):
    __cols = 6; # dont change! 5 days + time
    __rows = 7  # currently seven times

    current_view = view.week_view
    week_start = None
    weekday = 0

    instance = None

    color_usages = dict()


    def __init__(self, data_handler, datatype):
        super(Overview, self).__init__(main_window.CentralWidgetOverview.get_instance())
        Overview.set_instance(self)

        self.col_layout_cols = 120
        self.row_layout_rows = 12 # one row 10 minutes
        self.__minutes_per_row = 120 / self.row_layout_rows

        self.data_handler = data_handler



        # save data
        if datatype == datatypes.Raum:
            self.data = data_handler.raeume[:]
        elif datatype == datatypes.Aufsichtsperson:
            self.data = data_handler.aufsichtspersonen[:]
        elif datatype == datatypes.Pruefung:
            self.data = data_handler.pruefungen[:]
        elif datatype == datatypes.PruefungsplanElement:
            self.data = data_handler.pruefungsplan[:]

        self.data.sort(key=lambda a: a.timestamp)

        # zeitraum
        if Overview.get_week_start() is None:
            self.week_start_to_first_element()
        else:
            self.week_start = Overview.get_week_start()
            self.week_end = self.week_start + timedelta(days=4)

            self.week_end = self.week_end.replace(hour=23, minute=59)

        # init layout and widgets
        self.init_layout()

        if Overview.get_current_view() == view.week_view:
            self.init_week_view(self.week_start, self.week_end)
        else:
            self.init_day_view(self.week_start + timedelta(days=Overview.get_weekday()))


        # if pruefungsplan -> fab
        if datatype == datatypes.PruefungsplanElement:
            self.fab = FabButton(self, 60, 10, "#2185D0", "white")
            self.fab.setIcon(QPixmap("resources/images/save-solid-white.svg"), QPixmap("resources/images/save-solid-blue.svg"))
            self.fab.clicked.connect(lambda: self.data_handler.export_pruefungsplan_csv(self))
            self.__fab_move()
            self.fab.show()
        else:
            self.fab = None

    def __create_fab(self, size=60, padding=10):
        """
        creates fab button
        :param size:
        :param padding:
        :return:
        """
        self.fab.size = size
        self.fab.padding = padding

        # size
        self.fab.setFixedWidth(size)
        self.fab.setFixedHeight(size)

        #design
        self.fab.setStyleSheet("QPushButton {"
                               "border: 1px solid #2185D0;"
                               "background-color: #2185D0;"
                               "color: white;" +
                               ("border-radius: %ipx;" % (int(size/2))) +
                               "}"
                               "QPushButton:hover {"
                               "background-color: white;"
                               "}"
                               "QAbstractButton {"
                               "qproperty-icon: url(resources/images/save-solid-white.svg) on, url(resources/images/save-solid-blue.svg) off;"
                               "}")

        # self.fab.setIcon(QPixmap("resources/images/save-solid.svg"))

        # mask to round
        # rect = QRect(0,0,size, size)
        # region = QRegion(rect, QRegion.Ellipse)
        # self.fab.setMask(region)

        # add action

        # move and show

    def __fab_move(self):
        """
        moves fab button to correct pos
        :return:
        """
        if not self.fab is None:
            pos_x = self.frameGeometry().width() - self.fab.size - self.fab.padding
            pos_y = self.frameGeometry().height() - self.fab.size - self.fab.padding
            self.fab.move(pos_x, pos_y)


    def resizeEvent(self, event:QResizeEvent):
        self.__fab_move()

    def init_layout(self):
        """
        inits the grid layout
        :return:
        """
        self.layout = QtWidgets.QGridLayout()
        self.layout.setSpacing(0)
        self.layout.setMargin(0)
        for i in range(0, self.col_layout_cols * self.__cols):
            self.layout.setColumnStretch(i, 1)
        for i in range(0, self.row_layout_rows * self.__rows):
            self.layout.setRowStretch(i, 1)


        self.setLayout(self.layout)

    def init_time_label(self):
        """
        init the time label (first column)
        :return:
        """
        # init label
        self.label_zeitraum = ClickableLabel("", "", self.zeitraum_to_first_element)

        self.label_time0 = QtWidgets.QLabel("ab 8:00 Uhr")
        self.label_time1 = QtWidgets.QLabel("ab 10:00 Uhr")
        self.label_time2 = QtWidgets.QLabel("ab 12:00 Uhr")
        self.label_time3 = QtWidgets.QLabel("ab 14:00 Uhr")
        self.label_time4 = QtWidgets.QLabel("ab 16:00 Uhr")
        self.label_time5 = QtWidgets.QLabel("ab 18:00 Uhr")

        # set alignment
        self.label_zeitraum.setAlignment(Qt.AlignCenter)

        self.label_time0.setAlignment(Qt.AlignTop)
        self.label_time1.setAlignment(Qt.AlignTop)
        self.label_time2.setAlignment(Qt.AlignTop)
        self.label_time3.setAlignment(Qt.AlignTop)
        self.label_time4.setAlignment(Qt.AlignTop)
        self.label_time5.setAlignment(Qt.AlignTop)

        # set margin
        self.label_time0.setMargin(10)
        self.label_time1.setMargin(10)
        self.label_time2.setMargin(10)
        self.label_time3.setMargin(10)
        self.label_time4.setMargin(10)
        self.label_time5.setMargin(10)

        # init buttons
        self.left_button = QtWidgets.QPushButton()
        self.right_button = QtWidgets.QPushButton()

        # set button icons
        self.left_button.setIcon(QPixmap('resources/images/chevron-left-solid.svg'))
        self.right_button.setIcon(QPixmap('resources/images/chevron-right-solid.svg'))

        # set button stylesheet
        self.left_button.setStyleSheet("QPushButton{border:none;}")
        self.right_button.setStyleSheet("QPushButton{border:none;}")

        # set button action
        self.left_button.clicked.connect(lambda : self.move_zeitraum(False))
        self.right_button.clicked.connect(lambda : self.move_zeitraum(True))

        # zeitraum hbox
        self.layout_zeitraum = QtWidgets.QHBoxLayout()
        self.layout_zeitraum.addWidget(self.left_button)
        self.layout_zeitraum.addWidget(self.label_zeitraum)
        self.layout_zeitraum.addWidget(self.right_button)



        # add to layout
        self.layout.addLayout(self.layout_zeitraum, 0, 0, self.row_layout_rows, self.col_layout_cols)

        self.layout.addWidget(self.label_time0, 1 * self.row_layout_rows, 0, self.row_layout_rows, self.col_layout_cols)
        self.layout.addWidget(self.label_time1, 2 * self.row_layout_rows, 0, self.row_layout_rows, self.col_layout_cols)
        self.layout.addWidget(self.label_time2, 3 * self.row_layout_rows, 0, self.row_layout_rows, self.col_layout_cols)
        self.layout.addWidget(self.label_time3, 4 * self.row_layout_rows, 0, self.row_layout_rows, self.col_layout_cols)
        self.layout.addWidget(self.label_time4, 5 * self.row_layout_rows, 0, self.row_layout_rows, self.col_layout_cols)
        self.layout.addWidget(self.label_time5, 6 * self.row_layout_rows, 0, self.row_layout_rows, self.col_layout_cols)



    def init_dataobject_widgets(self, start_timestamp, end_timestamp):
        """
        inits dataobject widgets and adds them to layout
        :return: None
        """
        cols = dict()
        max_cols = 0

        for data_object in self.data:
            if data_object.timestamp < start_timestamp or data_object.timestamp > end_timestamp:
                # out of timerange
                continue

            col = self.col_layout_cols + ((data_object.timestamp - start_timestamp) // 86400000.0 * self.col_layout_cols)  # 86400000 == day in milliseconds
            row = self.row_layout_rows + (((data_object.timestamp - start_timestamp) % 86400000) // 60000) // self.__minutes_per_row  # 60000 minute in milliseconds
            height = data_object.verfuegbarkeit / 10

            if not (col in cols):
                cols[col] = []

            data_object_container = self.__create_dataobject_widget(data_object)

            cols[col].append([data_object_container, row, height])


        for col, value in cols.items():

            cols_usage = int((self.col_layout_cols if (Overview.get_current_view() == view.week_view) else self.col_layout_cols*(self.__cols-1)) / len(value))  # cols used by container
            col_offset = 0

            for data_object_container, row, height in value:
                data_object_container.init_detailed_view()
                self.layout.addWidget(data_object_container, row, col+col_offset, height, cols_usage)
                col_offset += cols_usage


    def init_week_view(self, start_datetime, end_datetime):
        """
        inits week view
        :return: None
        """

        self.reset_layout()
        Overview.set_current_view(view.week_view)
        self.repaint()

        self.init_time_label()

        # init label<
        self.label_zeitraum.setText("%s\nbis %s" % (start_datetime.strftime("%d.%m.%Y"), end_datetime.strftime("%d.%m.%Y")))
        self.label_zeitraum.setHoverText("<u>%s<br>bis %s</u>" % (start_datetime.strftime("%d.%m.%Y"), end_datetime.strftime("%d.%m.%Y")))

        self.label_monday = ClickableLabel("Montag", "<u>Montag</u>", lambda: self.init_day_view(start_datetime))
        self.label_tuesday = ClickableLabel("Dienstag", "<u>Dienstag</u>", lambda: self.init_day_view(start_datetime + timedelta(days=1)))
        self.label_wednesday = ClickableLabel("Mittwoch", "<u>Mittwoch</u>", lambda: self.init_day_view(start_datetime + timedelta(days=2)))
        self.label_thursday = ClickableLabel("Donnerstag", "<u>Donnerstag</u>", lambda: self.init_day_view(start_datetime + timedelta(days=3)))
        self.label_friday = ClickableLabel("Freitag", "<u>Freitag</u>", lambda: self.init_day_view(start_datetime + timedelta(days=4)))


        # set alignment
        self.label_monday.setAlignment(Qt.AlignCenter)
        self.label_tuesday.setAlignment(Qt.AlignCenter)
        self.label_wednesday.setAlignment(Qt.AlignCenter)
        self.label_thursday.setAlignment(Qt.AlignCenter)
        self.label_friday.setAlignment(Qt.AlignCenter)


        # add to layout
        self.layout.addWidget(self.label_monday, 0, 1 * self.col_layout_cols, self.row_layout_rows, self.col_layout_cols)
        self.layout.addWidget(self.label_tuesday, 0, 2 * self.col_layout_cols, self.row_layout_rows, self.col_layout_cols)
        self.layout.addWidget(self.label_wednesday, 0, 3 * self.col_layout_cols, self.row_layout_rows, self.col_layout_cols)
        self.layout.addWidget(self.label_thursday, 0, 4 * self.col_layout_cols, self.row_layout_rows, self.col_layout_cols)
        self.layout.addWidget(self.label_friday, 0, 5 * self.col_layout_cols, self.row_layout_rows, self.col_layout_cols)


        # init dataobjects
        start_timestamp = start_datetime.timestamp() * 1000
        end_timestamp = end_datetime.timestamp() * 1000
        self.init_dataobject_widgets(start_timestamp, end_timestamp)


    def init_day_view(self, start_datetime):
        """
        inits the day view
        :param day_name: str
        :param start_datetime: datetime
        :return:
        """
        self.reset_layout()
        Overview.set_current_view(view.day_view)
        self.repaint()

        self.init_time_label()

        self.weekday = start_datetime.weekday()
        Overview.set_weekday(self.weekday)
        # to str
        if self.weekday == 0:
            day_name = "Montag"
        elif self.weekday == 1:
            day_name = "Dienstag"
        elif self.weekday == 2:
            day_name = "Mittwoch"
        elif self.weekday == 3:
            day_name = "Donnerstag"
        elif self.weekday == 4:
            day_name = "Freitag"

        # set zeitraum
        self.label_zeitraum.setText("%s" % (start_datetime.strftime("%d.%m.%Y")))
        self.label_zeitraum.setHoverText("<u>%s</u>" % (start_datetime.strftime("%d.%m.%Y")))

        # add day
        self.label_day = ClickableLabel(day_name, "<u>" + day_name + "</u>", lambda: self.init_week_view(self.week_start, self.week_end))
        self.label_day.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.label_day, 0, 1 * self.col_layout_cols, self.row_layout_rows, (self.__cols-1) * self.col_layout_cols)

        # init dataobjects
        end_datetime = start_datetime.replace(hour=23, minute=59)
        start_timestamp = start_datetime.timestamp() * 1000
        end_timestamp = end_datetime.timestamp() * 1000

        self.init_dataobject_widgets(start_timestamp, end_timestamp)


    def reset_layout(self, layout=None):
        """
        resets the grid layout
        :return:
        """
        # remove old
        if layout is None:
            layout = self.layout

        while layout.count():
            item = layout.takeAt(0)
            if item.layout() is None:
                widget = item.widget()
                widget.deleteLater()
            else:
                tmp_layout = item.layout()
                self.reset_layout(tmp_layout)
                tmp_layout.deleteLater()


    def __create_dataobject_widget(self, data_object) -> DataObjectWidget:
        """
        creates widget based on dataobject
        :param data_object: instance of datatype
        :return: child of dataobject_widgets.DataObjectWidget
        """
        if isinstance(data_object, datatypes.Raum):
            # choose color
            color = Overview.get_color_usage(data_object.id, data_object.__class__)
            # create widget
            data_object_container = RaumWidget(data_object, color, parent=self)
        elif isinstance(data_object, datatypes.Aufsichtsperson):
            # choose color
            if isinstance(data_object.kuerzel, str):
                color = Overview.get_color_usage(data_object.kuerzel, data_object.__class__)
            else:
                color = Overview.get_color_usage(data_object.name+data_object.vorname, data_object.__class__)
            # create widget
            data_object_container = AufsichtspersonWidget(data_object, color, parent=self)
        elif isinstance(data_object, datatypes.Pruefung):
            # choose color
            if isinstance(data_object.kuerzel, str):
                color = Overview.get_color_usage(data_object.kuerzel, data_object.__class__)
            else:
                color = Overview.get_color_usage(data_object.id, data_object.__class__)
            # create widget
            data_object_container = PruefungWidget(data_object, color, parent=self)
        elif isinstance(data_object, datatypes.PruefungsplanElement):
            # choose color
            if isinstance(data_object.pruefungs_kuerzel, str):
                color = Overview.get_color_usage(data_object.pruefungs_kuerzel, data_object.__class__)
            else:
                color = Overview.get_color_usage(data_object.pruefungs_id, data_object.__class__)
            # create widget
            data_object_container = PruefungsplanWidget(data_object, color, parent=self)

        data_object_container.lower()
        return data_object_container

    def week_start_to_first_element(self):
        tmp_first_element_time = datetime.fromtimestamp(self.data[0].timestamp / 1000.0)
        self.week_start = tmp_first_element_time - timedelta(days=tmp_first_element_time.weekday())
        Overview.set_week_start(self.week_start)
        self.week_end = self.week_start + timedelta(days=4)

        self.week_start = self.week_start.replace(hour=8, minute=0)
        self.week_end = self.week_end.replace(hour=23, minute=59)

        Overview.set_week_start(self.week_start)

    def zeitraum_to_first_element(self):
        self.week_start_to_first_element()
        self.init_week_view(self.week_start, self.week_end)
        Overview.set_current_view(view.week_view)



    def move_zeitraum(self, up:bool):
        """
        changes the zeitraum
        :param up: bool -> True=increase date
        :return: None
        """
        if Overview.get_current_view() == view.week_view:
            if up:
                self.week_start = self.week_start + timedelta(days=7)
                self.week_end = self.week_end + timedelta(days=7)
                self.init_week_view(self.week_start, self.week_end)
            else:
                self.week_start = self.week_start - timedelta(days=7)
                self.week_end = self.week_end - timedelta(days=7)
                self.init_week_view(self.week_start, self.week_end)
        else:
            if up:
                if self.weekday == 4: # if freitag -> skip to monday next week
                    self.week_start = self.week_start + timedelta(days=7)
                    self.week_end = self.week_end + timedelta(days=7)

                    self.init_day_view(self.week_start)
                else:
                    self.init_day_view(self.week_start + timedelta(days=self.weekday+1))
            else:
                if self.weekday == 0: # if monday -> skip to friday last week
                    self.week_start = self.week_start - timedelta(days=7)
                    self.week_end = self.week_end - timedelta(days=7)

                    self.init_day_view(self.week_start + timedelta(days=4))
                else:
                    self.init_day_view(self.week_start + timedelta(days=self.weekday-1))

        Overview.set_week_start(self.week_start)

    def deleteLater(self):
        self.reset_layout()
        super().deleteLater()

    def paintEvent(self, event:QPaintEvent):
        """
        draws background
        :param event:
        :return: None
        """
        background_color = QColor(255,255,255)
        first_row_background = QColor(241,241,241)
        line_color = QColor(226,226,226)


        painter = QPainter(self)

        width = self.frameGeometry().width()
        height = self.frameGeometry().height()

        cell_width = width/self.__cols
        cell_height = height/self.__rows

        #draw background
        painter.fillRect(self.rect(), background_color)

        # draw grid
        painter.fillRect(0,0,width,cell_height, first_row_background)

        painter.setPen(line_color)
        for col in range(0, self.__cols if (Overview.get_current_view() == view.week_view) else 2):
            painter.drawLine(col*cell_width, 0, col*cell_width, height)

        for row in range(0, self.__rows):
            painter.drawLine(0, row*cell_height, width, row*cell_height)


    @staticmethod
    def set_current_view(view):
        Overview.current_view = view

    @staticmethod
    def get_current_view():
        return Overview.current_view
    @staticmethod
    def set_week_start(week_start:datetime):
        Overview.week_start = week_start
    @staticmethod
    def get_week_start() -> datetime:
        return Overview.week_start

    @staticmethod
    def set_weekday(weekday:int):
        Overview.weekday = weekday
    @staticmethod
    def get_weekday() -> int:
        return Overview.weekday


    @staticmethod
    def set_instance(instance):
        Overview.instance = instance
    @staticmethod
    def get_instance():
        return Overview.instance

    @staticmethod
    def add_color_usage(key, color_index, datatype):
        if not datatype in Overview.color_usages.keys():
            Overview.color_usages[datatype] = dict()

        Overview.color_usages[datatype][key] = color_index
    @staticmethod
    def get_color_usage(key, datatype):
        if datatype in Overview.color_usages.keys():
            if key in Overview.color_usages[datatype].keys():
                return widget_colors[Overview.color_usages[datatype][key]]

        # add if dont exist
        index = Overview.get_color_index(datatype)
        Overview.add_color_usage(key, index, datatype)
        return widget_colors[index]

    @staticmethod
    def get_color_index(datatype):
        if not "index" in Overview.color_usages.keys():
            Overview.color_usages["index"] = dict()

        if not datatype in Overview.color_usages.keys():
            Overview.color_usages["index"][datatype] = 0
            return 0
        else:
            index = (Overview.color_usages["index"][datatype] + 1) % len(widget_colors)
            Overview.color_usages["index"][datatype] = index
            return index

class EmptyOverview(QtWidgets.QWidget):
    def __init__(self, manuelle_eingabe_funct, csv_import_funct, type_str):
        super(EmptyOverview, self).__init__()



        self.help_1_label = QtWidgets.QLabel("Bitte trage erst über:")
        self.help_2_label = ClickableLabel("- die <font color=\"blue\">manuelle Eingabe</font>",
                                           "- die <font color=\"blue\"><u>manuelle Eingabe<u></font>",
                                           manuelle_eingabe_funct)
        self.help_3_label = ClickableLabel("- den <font color=\"blue\">CSV-Import</font>",
                                           "- den <font color=\"blue\"><u>CSV-Import<u></font>",
                                           csv_import_funct)
        self.help_4_label = QtWidgets.QLabel("%s ein." % type_str)

        font = self.help_1_label.font()

        font.setPixelSize(16)

        self.help_1_label.setFont(font)
        self.help_2_label.setFont(font)
        self.help_3_label.setFont(font)
        self.help_4_label.setFont(font)


        self.box_layout = QtWidgets.QVBoxLayout()
        self.box_layout.addWidget(self.help_1_label)
        self.box_layout.addWidget(self.help_2_label)
        self.box_layout.addWidget(self.help_3_label)
        self.box_layout.addWidget(self.help_4_label)
        self.box_layout.setAlignment(Qt.AlignCenter)

        self.setLayout(self.box_layout)

    def paintEvent(self, event:QPaintEvent):
        """
        draws background
        :param event:
        :return: None
        """
        color = QColor(206, 206, 206)
        custom_painter = QPainter(self)
        custom_painter.fillRect(self.rect(), color)

