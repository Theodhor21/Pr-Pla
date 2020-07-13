from src.data import datatypes
from src.data.datatypes import Raum, Aufsichtsperson
from src.widgets import main_window
import time

MAX_ROOMS = 50


class PruefungErweitert():
    """
    Data class
    with pruefung, possibel rooms, used rooms, used person
    """

    def __init__(self, pruefung):
        self.pruefung = pruefung  # pruefung
        self.raeume = []  # array von raeume
        self.useraeume = []  # benutzte räume
        self.useperson = []  # benutzte personen


def calc(data_handler):
    """
    :param data_handler:
    main function
    :return: when failed
    """
    data_handler.clear(datatypes.PruefungsplanElement)
    # data class
    pruefung_erweitert_array = []
    # Copy of data_handler arrays
    raeume_kopie = data_handler.raeume[:]
    personen_kopie = data_handler.aufsichtspersonen[:]
    pruefungen_kopie = data_handler.pruefungen[:]
    # sort by start
    pruefungen_kopie.sort(key=lambda prue: prue.timestamp)

    data_handler_pruefungen_erweitert = []
    for pruefung in pruefungen_kopie:
        pruefung_erweitert = PruefungErweitert(pruefung)
        pruefung_erweitert.raeume = alle_passenden_raeume(raeume_kopie, pruefung)
        pruefung_erweitert.raeume.sort(key=lambda raum: raum.kapazitaet)
        if raum_fuer_pruefung(pruefung_erweitert, raeume_kopie):
            for i in range(0, len(pruefung_erweitert.useraeume)):
                if person_fuer_pruefung(pruefung_erweitert.pruefung.timestamp, personen_kopie, pruefung_erweitert,
                                        endzeitpunkt(pruefung_erweitert.pruefung.timestamp,
                                                     pruefung_erweitert.pruefung.verfuegbarkeit),
                                        data_handler_pruefungen_erweitert, pruefung_erweitert.useraeume[i]):
                    continue
                else:
                    # not enough people
                    return False, "Für die Prüfung mit der ID \"%s\", konnte keine Aufsichtsperson eingeteilt werden." % pruefung.id
            # find everything and go on
        else:
            # not enough rooms
            return False, "Für die Prüfung mit der ID \"%s\", konnte kein Raum eingeteilt werden." % pruefung.id
        # find everything and add to array
        pruefung_erweitert_array.append(pruefung_erweitert)
    # show plan
    # main_window.CentralWidget.get_instance().init_overview_pruefungsplan()
    return True, data_handler_pruefungen_erweitert


def person_fuer_pruefung(start, person_kopie, pruefung_erweitert, end, data_handler_pruefungen_erweitert, raum):
    """
    :param start: time were the person has to start
    :param person_kopie: all persone that can be used
    :param pruefung_erweitert: data class
    :param end: end of pruefung
    :return: if possibility or not
    """

    app = alle_passenden_personen(person_kopie, start, end)
    # no persons available
    if len(app) == 0 or app[0].timestamp > start:
        return False

    app.sort(key=lambda person: endzeitpunkt(person.timestamp, person.verfuegbarkeit), reverse=True)
    app.sort(key=lambda person: person.timestamp)
    pruefung_erweitert.useperson.append(app[0])
    end_person = endzeitpunkt(app[0].timestamp, app[0].verfuegbarkeit)
    del_person_element(person_kopie, app[0], start, end)

    # end of time from person smaller than end time => recursion
    if end_person < endzeitpunkt(pruefung_erweitert.pruefung.timestamp, pruefung_erweitert.pruefung.verfuegbarkeit):
        # recursion
        data_handler_pruefungen_erweitert.append(
            datatypes.PruefungsplanElement(pruefung_erweitert.pruefung.art, pruefung_erweitert.pruefung.id,
                                           pruefung_erweitert.pruefung.kuerzel,
                                           raum.kapazitaet,
                                           raum.id,
                                           pruefung_erweitert.useperson[-1].name,
                                           pruefung_erweitert.useperson[-1].vorname,
                                           pruefung_erweitert.useperson[-1].kuerzel,
                                           verfuegbarkeitraum(start, end_person),
                                           start))
        if person_fuer_pruefung(end_person, person_kopie, pruefung_erweitert, end, data_handler_pruefungen_erweitert, raum):
            return True
        else:
            return False
    else:
        data_handler_pruefungen_erweitert.append(
            datatypes.PruefungsplanElement(pruefung_erweitert.pruefung.art, pruefung_erweitert.pruefung.id,
                                           pruefung_erweitert.pruefung.kuerzel,
                                           raum.kapazitaet,
                                           raum.id,
                                           pruefung_erweitert.useperson[-1].name,
                                           pruefung_erweitert.useperson[-1].vorname,
                                           pruefung_erweitert.useperson[-1].kuerzel,
                                           verfuegbarkeitraum(start, end),
                                           start))
        return True


def raum_fuer_pruefung(pruefung_erweitert, raeume_kopie):
    """
    :param pruefung_erweitert: data class
    :param raeume_kopie: list of used rooms
    :return: if possibility or not
    """
    # room available
    if len(pruefung_erweitert.raeume) == 0:
        return False
    # oral exam
    elif pruefung_erweitert.pruefung.art == 'm':
        pruefung_erweitert.useraeume.append(pruefung_erweitert.raeume[0])
        del_raum_element(raeume_kopie, pruefung_erweitert.raeume[0], pruefung_erweitert.pruefung)
        return True
    # is written exam
    else:
        anz_teilnehmer = pruefung_erweitert.pruefung.teilnehmer
        # as long as rooms are available
        while len(pruefung_erweitert.raeume) > 0:
            # has a room perfect capacity
            for raum in pruefung_erweitert.raeume:
                if raum.kapazitaet >= anz_teilnehmer:
                    del_raum_element(raeume_kopie, raum, pruefung_erweitert.pruefung)  # benutzter raum
                    pruefung_erweitert.useraeume.append(raum)
                    return True
            # take biggest and go again
            anz_teilnehmer -= pruefung_erweitert.raeume[-1].kapazitaet
            del_raum_element(raeume_kopie, pruefung_erweitert.raeume[-1],
                             pruefung_erweitert.pruefung)  # benutzter raum reicht aber nicht
            pruefung_erweitert.useraeume.append(pruefung_erweitert.raeume[-1])
            del pruefung_erweitert.raeume[-1]
        # failed
        return False


def alle_passenden_raeume(raeume, prue):
    """
    gibt alle passenden raueme zur pruefung zurueck
    :param raeume: raeume array
    :param prue: instance of datatypes.py::Pruefung
    :return: integer array with index of raum
    """
    alle_passende_raeume = []
    for index in range(0, len(raeume)):
        raum = raeume[index]
        if (prue.timestamp >= raum.timestamp) and (
                endzeitpunkt(prue.timestamp, prue.verfuegbarkeit) <= endzeitpunkt(raum.timestamp, raum.verfuegbarkeit)):
            alle_passende_raeume.append(raum)
    return alle_passende_raeume


def del_raum_element(raum_list, raum_del, prue):
    """
    :param raum_list: usable rooms
    :param raum_del:
    :param prue: exam for end and start time
    :return: new usable room list
    """
    for raume in raum_list:
        if raume == raum_del:
            timestamp = endzeitpunkt(prue.timestamp, prue.verfuegbarkeit)
            raum_neu = Raum(raum_del.id, raum_del.kapazitaet,
                            verfuegbarkeitraum(timestamp, endzeitpunkt(raum_del.timestamp, raum_del.verfuegbarkeit)),
                            timestamp)
            raum_list.remove(raum_del)
            raum_list.append(raum_neu)


def del_person_element(person_list, person_del, start_punkt, end_punkt):
    """
    :param person_list: usable person
    :param person_del:
    :param start_punkt: timestamp
    :param end_punkt:  timestamp
    :return: new usable person list
    """
    # ende ist nur wichtig da sortierte pruefungen
    for person in person_list:
        if person == person_del:
            # hat vorher schon zeit
            if person.timestamp < start_punkt:
                person_neu = Aufsichtsperson(person.name, person.vorname, person.kuerzel,
                                             verfuegbarkeitraum(person.timestamp,
                                                                start_punkt),
                                             person.timestamp)
                person_list.append(person_neu)
            # hat dannach noch zeit
            if end_punkt < endzeitpunkt(person.timestamp, person.verfuegbarkeit):
                person_neu = Aufsichtsperson(person.name, person.vorname, person.kuerzel,
                                             verfuegbarkeitraum(end_punkt,
                                                                endzeitpunkt(person.timestamp, person.verfuegbarkeit)),
                                             end_punkt)
                person_list.append(person_neu)
            person_list.remove(person)


def alle_passenden_personen(personen, prue_start, prue_end):  # wenn nur eine person für jeden raum zulässt klappt es
    """
    :param personen: usable person
    :param prue: instance of datatypes.py::Pruefung
    :return: person array
    """
    alle_passende_personen = []
    for index in range(0, len(personen)):
        person = personen[index]
        if ((prue_start >= person.timestamp) and (
                prue_start < endzeitpunkt(person.timestamp, person.verfuegbarkeit))) or (
                (prue_end > person.timestamp) and (
                prue_end <= endzeitpunkt(person.timestamp, person.verfuegbarkeit))):  # personen mit größerer zeit in
            alle_passende_personen.append(person)
    return alle_passende_personen


def verfuegbarkeitraum(start, end):
    return (end - start) / (60 * 1000)


def endzeitpunkt(start, dauer):
    return start + dauer * 60 * 1000


def pruefungs_ueberschneidung(prue1: datatypes.Pruefung, prue2: datatypes.Pruefung):
    return prue1.timestamp >= prue2.timestamp and prue1.timestamp <= endzeitpunkt(prue2.timestamp, prue2.verfuegbarkeit)
    # braucht man nicht, da prue2 immer nach prue1:
    #      (prue1.timestamp <= prue2.timestamp and prue2.timestamp <= endzeitpunkt(prue1.timestamp, prue1.verfuegbarkeit))
