from datetime import datetime

class Raum:
    def __init__(self, id, kapazitaet, verfuegbarkeit, timestamp):
        self.id = id
        self.kapazitaet = kapazitaet
        self.verfuegbarkeit = verfuegbarkeit
        self.timestamp = timestamp

class Aufsichtsperson:
    def __init__(self, name, vorname, kuerzel, verfuegbarkeit, timestamp):
        self.name = name
        self.vorname = vorname
        self.kuerzel = kuerzel
        self.verfuegbarkeit = verfuegbarkeit
        self.timestamp = timestamp

class Pruefung:
    def __init__(self, art, id, kuerzel, teilnehmer, dauer, timestamp):
        self.art = art
        self.id = id
        self.kuerzel = kuerzel
        self.teilnehmer = teilnehmer
        self.verfuegbarkeit = dauer
        self.timestamp = timestamp

class PruefungsplanElement:
    def __init__(self, pruefungs_art, pruefungs_id, pruefungs_kuerzel, pruefungs_teilnehmer, raum_id, aufischtsperson_name, aufsichtsperson_vorname, aufsichsperson_kuerzel, dauer, timestamp):
        self.pruefungs_art = pruefungs_art
        self.pruefungs_id = pruefungs_id
        self.pruefungs_kuerzel = pruefungs_kuerzel
        self.pruefungs_teilnehmer = pruefungs_teilnehmer
        self.raum_id = raum_id
        self.aufischtsperson_name = aufischtsperson_name
        self.aufsichtsperson_vorname = aufsichtsperson_vorname
        self.aufsichsperson_kuerzel = aufsichsperson_kuerzel
        self.verfuegbarkeit = dauer
        self.timestamp = timestamp


def timestamp_to_string(timestamp_in_milliseconds) -> str:
    timestamp = datetime.fromtimestamp(timestamp_in_milliseconds / 1000.0)
    return timestamp.strftime('%d.%m.%Y %H:%M Uhr')

def timestamp_to_datetime(timestamp_in_milliseconds) -> datetime:
    return datetime.fromtimestamp(timestamp_in_milliseconds / 1000.0)