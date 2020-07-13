from os import path

from src.data import io_handler, datatypes
from src.dialogs import yes_no_dialog, yes_dialog
from src.widgets import io
from src.widgets import main_window

_IMPORT_TITLE_EXPLORER = "%s CSV-Datei Öffnen"
_EXPORT_TITLE_EXPLORER = "%s CSV-Datei Speichern"

_TITLE_DIALOG = "%s CSV-Datei Import"
_STORAGE_USED = "Es wurden bereits %s eingetragen. Wenn Sie fortfahren, werden diese überschrieben."
_FILE_CORRUPT = "Die ausgewählte Datei ist nicht kompatibel."

_OK = "OK"
_CANCLE = "Abbrechen"

_ROOMS = "Räume"
_PERSONS = "Aufsichtspersonen"
_EXAMS = "Prüfungen"
_PLAN = "Prüfungsplan"

class DataHandler:
    def __init__(self):
        self.raeume = []
        self.aufsichtspersonen = []
        self.pruefungen = []
        self.pruefungsplan = []

        self.__update_listeners = []

    def update(self, updated_type:datatypes):
        """
        called when data_changed
        :param updated_type: the datatype which was updated
        :return:
        """
        for update_funct in self.__update_listeners:
            update_funct(updated_type)

    def add_update_listener(self, update_funct):
        """
        add a function which is called, when updated data
        :param update_funct: funct with param datatype
        :return:
        """
        self.__update_listeners.append(update_funct)

    def import_raeume_csv(self, parent_view, filepath=None, test_storage=True):
        """
        import a csv file and insert into local array
        :param parent_view: parent view
        :param filepath: of csv, if none opens explorer to choose
        :param test_storage: test if storage is already used
        :return:
        """
        if filepath == None:
            filepath = io.open_csv(parent_view, _IMPORT_TITLE_EXPLORER % (_ROOMS))

        if path.exists(filepath):  # does path exist?
            if test_storage and len(self.raeume) > 0:
                dialog = yes_no_dialog.YesNoDialog(_TITLE_DIALOG % _ROOMS,
                                                   _STORAGE_USED % _ROOMS,
                                                   lambda: self.import_raeume_csv(parent_view, filepath, False),
                                                   None,
                                                   parent_view,
                                                   _OK,
                                                   _CANCLE)
                dialog.exec_()
            else:
                try:
                    # import csv
                    self.raeume = io_handler.import_csv(filepath, datatypes.Raum)
                except:  # data is corrupt
                    dialog = yes_dialog.YesDialog(_TITLE_DIALOG % _ROOMS,
                                                  _FILE_CORRUPT,
                                                  None,
                                                  parent_view,
                                                  _OK)
                    dialog.exec_()
                self.update(datatypes.Raum)
            main_window.CentralWidget.get_instance().init_overview(datatypes.Raum)

    def import_aufsichtspersonen_csv(self, parent_view, filepath=None, test_storage=True):
        """
        import a csv file and insert into local array
        :param parent_view: parent view
        :param filepath: of csv, if none opens explorer to choose
        :param test_storage: test if storage is already used
        :return:
        """
        if filepath == None:
            filepath = io.open_csv(parent_view, _IMPORT_TITLE_EXPLORER % (_PERSONS))

        if path.exists(filepath):  # does path exist?
            if test_storage and len(self.aufsichtspersonen) > 0:
                dialog = yes_no_dialog.YesNoDialog(_TITLE_DIALOG % _PERSONS,
                                                   _STORAGE_USED % _PERSONS,
                                                   lambda: self.import_aufsichtspersonen_csv(parent_view, filepath, False),
                                                   None,
                                                   parent_view,
                                                   _OK,
                                                   _CANCLE)
                dialog.exec_()
            else:
                try:
                    # import csv
                    self.aufsichtspersonen = io_handler.import_csv(filepath, datatypes.Aufsichtsperson)
                except:  # data is corrupt
                    dialog = yes_dialog.YesDialog(_TITLE_DIALOG % _PERSONS,
                                                  _FILE_CORRUPT,
                                                  None,
                                                  parent_view,
                                                  _OK)
                    dialog.exec_()
                self.update(datatypes.Aufsichtsperson)
            main_window.CentralWidget.get_instance().init_overview(datatypes.Aufsichtsperson)

    def import_pruefungen_csv(self, parent_view, filepath=None, test_storage=True):
        """
        import a csv file and insert into local array
        :param parent_view: parent view
        :param filepath: of csv, if none opens explorer to choose
        :param test_storage: test if storage is already used
        :return:
        """
        if filepath == None:
            filepath = io.open_csv(parent_view, _IMPORT_TITLE_EXPLORER % (_EXAMS))

        if path.exists(filepath):  # does path exist?
            if test_storage and len(self.pruefungen) > 0:
                dialog = yes_no_dialog.YesNoDialog(_TITLE_DIALOG % _EXAMS,
                                                   _STORAGE_USED % _EXAMS,
                                                   lambda: self.import_pruefungen_csv(parent_view, filepath, False),
                                                   None,
                                                   parent_view,
                                                   _OK,
                                                   _CANCLE)
                dialog.exec_()
            else:
                try:
                    # import csv
                    self.pruefungen = io_handler.import_csv(filepath, datatypes.Pruefung)
                except:  # data is corrupt
                    dialog = yes_dialog.YesDialog(_TITLE_DIALOG % _EXAMS,
                                                  _FILE_CORRUPT,
                                                  None,
                                                  parent_view,
                                                  _OK)
                    dialog.exec_()
                self.update(datatypes.Pruefung)
            main_window.CentralWidget.get_instance().init_overview(datatypes.Pruefung)
                    
    

    def export_raeume_csv(self, parent_view, filepath=None):
        """
        export a csv file and insert into local array
        :param parent_view: parent view
        :param filepath: of csv, if none opens explorer to choose
        :return:
        """
        if filepath == None:
            filepath = io.save_csv(parent_view, _EXPORT_TITLE_EXPLORER % (_ROOMS), _ROOMS.lower() + ".csv")

        if len(filepath) > 0:  # does path exist?
            io_handler.export_csv(filepath, self.raeume)

        self.update(datatypes.Raum)

    def export_aufsichtspersonen_csv(self, parent_view, filepath=None):
        """
        export a csv file and insert into local array
        :param parent_view: parent view
        :param filepath: of csv, if none opens explorer to choose
        :return:
        """
        if filepath == None:
            filepath = io.save_csv(parent_view, _EXPORT_TITLE_EXPLORER % (_PERSONS), _PERSONS.lower() + ".csv")

        if len(filepath) > 0:  # does path exist?
            io_handler.export_csv(filepath, self.aufsichtspersonen)
        self.update(datatypes.Aufsichtsperson)

    def export_pruefungen_csv(self, parent_view, filepath=None):
        """
        export a csv file and insert into local array
        :param parent_view: parent view
        :param filepath: of csv, if none opens explorer to choose
        :return:
        """
        if filepath == None:
            filepath = io.save_csv(parent_view, _EXPORT_TITLE_EXPLORER % (_EXAMS), _EXAMS.lower() + ".csv")

        if len(filepath) > 0:  # does path exist?
            io_handler.export_csv(filepath, self.pruefungen)
        self.update(datatypes.Pruefung)

    def export_pruefungsplan_csv(self, parent_view, filepath=None):
        """
        export a csv file and insert into local array
        :param parent_view: parent view
        :param filepath: of csv, if none opens explorer to choose
        :return:
        """
        if filepath == None:
            filepath = io.save_csv(parent_view, _EXPORT_TITLE_EXPLORER % (_PLAN), _PLAN.lower() + ".csv")

        if len(filepath) > 0:  # does path exist?
            io_handler.export_csv(filepath, self.pruefungsplan)


    def add(self, object):
        """
        add object to array
        :param object: instance of class in datatypes
        :return: None
        """
        if isinstance(object, datatypes.Raum):
            self.raeume.append(object)
            self.update(datatypes.Raum)
        elif isinstance(object, datatypes.Aufsichtsperson):
            self.aufsichtspersonen.append(object)
            self.update(datatypes.Aufsichtsperson)
        elif isinstance(object, datatypes.Pruefung):
            self.pruefungen.append(object)
            self.update(datatypes.Pruefung)
        elif isinstance(object, datatypes.PruefungsplanElement):
            self.pruefungsplan.append(object)

    def remove(self, object):
        """
        remove object from array
        :param object: instance of class in datatypes
        :return: None
        """
        if isinstance(object, datatypes.Raum):
            self.raeume.remove(object)
            self.update(datatypes.Raum)
        elif isinstance(object, datatypes.Aufsichtsperson):
            self.aufsichtspersonen.remove(object)
            self.update(datatypes.Aufsichtsperson)
        elif isinstance(object, datatypes.Pruefung):
            self.pruefungen.remove(object)
            self.update(datatypes.Pruefung)
        elif isinstance(object, datatypes.PruefungsplanElement):
            self.pruefungsplan.remove(object)
            self.update(datatypes.PruefungsplanElement)

    def overwrite(self, old_object, new_object):
        """
        overwrites old_object with new_object
        :param old_object: instance of class in datatypes
        :param new_object: instance of class in datatypes
        :return: None
        """
        if isinstance(old_object, datatypes.Raum):
            self.raeume[self.raeume.index(old_object)] = new_object
            self.update(datatypes.Raum)
        elif isinstance(old_object, datatypes.Aufsichtsperson):
            self.aufsichtspersonen[self.aufsichtspersonen.index(old_object)] = new_object
            self.update(datatypes.Aufsichtsperson)
        elif isinstance(old_object, datatypes.Pruefung):
            self.pruefungen[self.pruefungen.index(old_object)] = new_object
            self.update(datatypes.Pruefung)
        elif isinstance(old_object, datatypes.PruefungsplanElement):
            self.pruefungsplan[self.pruefungsplan.index(old_object)] = new_object
            self.update(datatypes.PruefungsplanElement)

    def empty(self, datatype):
        """
        get if list is empty
        :param datatype: class in datatypes
        :return: boolean
        """
        if datatype == datatypes.Raum:
            return not self.raeume
        elif datatype == datatypes.Aufsichtsperson:
            return not self.aufsichtspersonen
        elif datatype == datatypes.Pruefung:
            return not self.pruefungen
        elif datatype == datatypes.Pruefung:
            return not self.pruefungsplan

    def clear(self, datatype):
        """
        clears list - only available for pruefungsplan
        :param datatype:
        :return: succesfull?
        """
        if datatype == datatypes.Raum:
            return False
        elif datatype == datatypes.Aufsichtsperson:
            return False
        elif datatype == datatypes.Pruefung:
            return False
        elif datatype == datatypes.PruefungsplanElement:
            self.pruefungsplan.clear()
            return True
