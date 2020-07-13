from PySide2.QtWidgets import QWidget


class Manuelle_Eingabe_Räume(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(" Manuelle Eingabe Räume ")
        self.setGeometry(612, 318, 600, 520)


class Manuelle_Eingabe_Aufsichtspersonen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(" Manuelle Eingabe Aufsichtspersonen ")
        self.setGeometry(612, 318, 600, 520)


class Manuelle_Eingabe_Prüfungen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(" Manuelle Eingabe Prüfungen ")
        self.setGeometry(612, 318, 600, 520)