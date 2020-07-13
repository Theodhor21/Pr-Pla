from PySide2.QtCore import QCoreApplication
from PySide2.QtGui import QColor, QPaintEvent, QPainter, QMouseEvent, QCursor, QResizeEvent
from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel

from src.widgets import overview


class DetailedView(QWidget):
    title_text_size = 18
    content_text_size = 14
    border_color = QColor(112,112,112)
    back_color = QColor(255,255,255)

    visible_widgets = []

    def __init__(self, title="", content="", _parent=None):
        super(DetailedView, self).__init__(overview.Overview.get_instance())

        self._parent = _parent
        self.widget_resolution = overview.Overview.get_instance().frameGeometry()

        QCoreApplication.instance()
        # init
        self.layout = QVBoxLayout()

        self.lable_title = QLabel(title)
        self.lable_content = QLabel(content)

        # font
        title_font = self.lable_title.font()
        title_font.setPixelSize(self.title_text_size)
        content_font = self.lable_content.font()
        content_font.setPixelSize(self.content_text_size)

        self.lable_title.setFont(title_font)
        self.lable_content.setFont(content_font)

        # layout
        self.layout.addWidget(self.lable_title)
        self.layout.addWidget(self.lable_content)

        self.setLayout(self.layout)

        # flags
        self.setMouseTracking(True)



    def calc_min_size(self):
        # width
        if self.lable_title.sizeHint().width() > self.lable_content.sizeHint().width():
            self.setMinimumWidth(self.lable_title.sizeHint().width() + (self.layout.margin() * 2))
        else:
            self.setMinimumWidth(self.lable_content.sizeHint().width() + (self.layout.margin() * 2))

        # height
        height = self.lable_title.sizeHint().height()
        height += self.lable_content.sizeHint().height()
        self.setMinimumHeight(height + (self.layout.margin() * 2))


    def set_title(self, title):
        """
        set title
        :param title: str
        :return:
        """
        self.lable_title.setText(title)
        self.calc_min_size()

    def set_content(self, content):
        """
        set content
        :param content: str
        :return:
        """
        self.lable_content.setText(content)
        self.calc_min_size()


    def move_to_mouse(self):
        """
        moves self to mouse and show
        :return:
        """

        # turn if out of dekstop
        pos = self.cursor().pos()
        pos = overview.Overview.get_instance().mapFromGlobal(pos)

        if pos.x() + self.rect().width() > self.widget_resolution.width():
            pos.setX(pos.x()-self.rect().width())
        if pos.y() + self.rect().height() > self.widget_resolution.height():
            pos.setY(pos.y()-self.rect().height())

        #move
        self.move(pos)
        # if self.isVisible():
        #     if not self.isActiveWindow():
        #         # back to foreground
        #         self.activateWindow()
        # else:
        DetailedView.close_all()
        DetailedView.add_to_visible(self)
        self.show()

    def ask_close(self):
        """
        parent can ask for close
        :return:
        """
        if not self.mouse_is_over_parent():
            DetailedView.remove_visible(self)
            self.close()

    def close(self):
        DetailedView.remove_visible(self)
        super().close()

    def mouse_is_over_parent(self):
        """
        returns if mouse if over _parent
        :return: bool
        """
        mouse_pos = self._parent.mapFromGlobal(QCursor.pos())
        margin = 1
        return mouse_pos.x() > margin and mouse_pos.y() > margin and mouse_pos.x() < self._parent.rect().width() - margin and mouse_pos.y() < self._parent.rect().height() - margin

    def mouseMoveEvent(self, event:QMouseEvent):
        """
        mouse move event
        :param event:
        :return:
        """
        if self.mouse_is_over_parent():
            self.move_to_mouse()
        else:
            self.close()

    def deleteLater(self):
        DetailedView.remove_visible(self)
        super().deleteLater()

    def mousePressEvent(self, event:QMouseEvent):
        """
        redirect mouse press to _parent
        :param event:
        :return:
        """
        self._parent.mousePressEvent(event)


    def paintEvent(self, event:QPaintEvent):
        """
        draws background
        :param event:
        :return: None
        """
        custom_painter = QPainter(self)
        custom_painter.fillRect(self.rect(), self.back_color)

        custom_painter.setPen(self.border_color)
        custom_painter.drawRect(0,0, self.rect().width()-1, self.rect().height()-1)

    def resizeEvent(self, event:QResizeEvent):
        self.widget_resolution = overview.Overview.get_instance().frameGeometry()
        super().resizeEvent(event)

    @staticmethod
    def add_to_visible(detailed_view):
        if not detailed_view in DetailedView.visible_widgets:
            DetailedView.visible_widgets.append(detailed_view)

    @staticmethod
    def remove_visible(detailed_view):
        if detailed_view in DetailedView.visible_widgets:
            DetailedView.visible_widgets.remove(detailed_view)

    @staticmethod
    def close_all():
        for detailed_view in DetailedView.visible_widgets:
            detailed_view.ask_close()
