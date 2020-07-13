from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog, QLabel, QPushButton, QGridLayout


class YesDialog(QDialog):
    '''
    Dialog template with text, yes-button
    '''

    def __init__(self, title, text, yes_function, parent=None, yes_text="&Ja"):
        super(YesDialog, self).__init__(parent,
                                        Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)  # flags disable hint

        self.yes_function = yes_function

        self.setWindowTitle(title)
        self.setMinimumWidth(300)

        # create label
        self.lable = QLabel(self)
        # create buttons
        self.yes_button = QPushButton(yes_text, self)
        # create layout
        self.layout = QGridLayout()

        # set label vars
        self.lable.setText(text)
        self.lable.setWordWrap(True)
        # set button action
        self.yes_button.clicked.connect(self.__yes_function)

        # add label and buttons to layout
        self.layout.addWidget(self.lable, 0, 0, 1, 0)
        self.layout.addWidget(self.yes_button, 1, 1)

        # set layout
        self.setLayout(self.layout)

    def __yes_function(self):
        """
        executed on yes_button press
        :return: None
        """
        self.close()
        if self.yes_function is not None:
            self.yes_function()
