from PySide2.QtWidgets import QLabel


class ClickableLabel(QLabel):
    """
    clickable QLable
    """
    def __init__(self, text, text_hover, mouse_click_function):
        super(ClickableLabel, self).__init__()

        self.__text = text
        self.__text_hover = text_hover
        self.setText(self.__text)

        self.__mouse_click_function = mouse_click_function

    def mousePressEvent(self, QMouseEvent):
        self.__mouse_click_function()

    def enterEvent(self, QEvent):
        super(ClickableLabel, self).setText(self.__text_hover)

    def leaveEvent(self, QEvent):
        super(ClickableLabel, self).setText(self.__text)

    def setText(self, arg__1:str):
        self.__text = arg__1
        super(ClickableLabel, self).setText(arg__1)

    def setHoverText(self, arg__1:str):
        self.__text_hover = arg__1

