from PySide2.QtGui import QFocusEvent
from PySide2.QtWidgets import QLineEdit


class LineEdit(QLineEdit):
    """
    QLineEdit with hint
    """
    def __init__(self, parent, hint=""):
        super(LineEdit, self).__init__(parent)

        self.hint = hint

        self.__set_hint()

    def empty(self):
        return self.hint_is_set

    def clear(self):
        self.__set_hint()

    def text(self) -> str:
        if self.hint_is_set:
            return ""
        else:
            return super().text()

    def setText(self, arg__1:str):
        if not arg__1 is None:
            self.__unset_hint()
            super().setText(arg__1)

    def focusInEvent(self, arg__1:QFocusEvent):
        """
        unset hint
        :param arg__1:
        :return:
        """
        super().focusInEvent(arg__1)
        if self.hint_is_set:
            self.__unset_hint()

    def focusOutEvent(self, arg__1:QFocusEvent):
        """
        set hint if is empty
        :param arg__1:
        :return:
        """
        super().focusOutEvent(arg__1)
        if len(self.text()) == 0:
            self.__set_hint()

    def __set_hint(self):
        """
        set hint
        :return:
        """
        self.hint_is_set = True
        super().setText(self.hint)
        self.setStyleSheet("color: gray;")

    def __unset_hint(self):
        """
        unset hint
        :return:
        """
        super().setText("")
        self.hint_is_set = False
        self.setObjectName("norm")
        self.setStyleSheet("color: black;")
