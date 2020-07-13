from PySide2.QtCore import QSize
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QPushButton


class FabButton(QPushButton):
    style_sheet = "QPushButton {" \
                  "border: 1px solid %s;" \
                  "background-color: %s;" \
                  "color: white;" \
                  "border-radius: %ipx;" \
                  "}" \
                  "QPushButton:hover {" \
                  "background-color: %s;" \
                  "}"

    def __init__(self, parent, size: int, padding=0, color="#FFFFFF", color_hovered="#000000"):
        super(FabButton, self).__init__(parent)

        self.icon_norm = None
        self.icon_hover = None

        self.padding = padding

        self.size = size

        self.setFixedSize(size, size)

        self.setStyleSheet(self.style_sheet % (color, color, int(size / 2), color_hovered))


    def setIcon(self, icon_norm: QPixmap, icon_hover: QPixmap = None):
        self.icon_norm = icon_norm
        self.icon_hover = icon_hover

        self.setIconSize(QSize(self.size * 0.5, self.size * 0.5))

        super().setIcon(icon_norm)


    def enterEvent(self, event):
        if not self.icon_hover is None:
            super().setIcon(self.icon_hover)


    def leaveEvent(self, event):
        if not self.icon_norm is None:
            super().setIcon(self.icon_norm)
