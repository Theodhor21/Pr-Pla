from PySide2.QtWidgets import QFileDialog

def open_csv(parent_widget, title):
    """
    opens file browser to choose open path
    :param parent_widget: parent window
    :param title: title in unicode
    :return: filepath
    """
    return QFileDialog.getOpenFileName(parent_widget, title, filter='CSV (*.csv)')[0]

def save_csv(parent_widget, title, filename = ""):
    """
    opens file browser to choose save path
    :param parent_widget: parent window
    :param title: title in unicode
    :return: filepath
    """
    return QFileDialog.getSaveFileName(parent_widget, title, filename, filter='CSV (*.csv)')[0]
