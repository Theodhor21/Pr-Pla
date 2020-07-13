
from pandas import DataFrame, read_csv

from src.data import datatypes


def import_csv(filepath, datatype):
    """
    import data from csvdd
    :param filepath: import path
    :return: data
    """
    df = read_csv(filepath)

    if datatype == datatypes.Raum:
        return [datatypes.Raum(row.id, row.kapazitaet, row.verfuegbarkeit, row.timestamp) for index, row in df.iterrows()]
    elif datatype == datatypes.Aufsichtsperson:
        return [datatypes.Aufsichtsperson(row.astype(object)[0], row.vorname, row.kuerzel, row.verfuegbarkeit, row.timestamp) for index, row in df.iterrows()]
    elif datatype == datatypes.Pruefung:
        return [datatypes.Pruefung(row.art, row.id, row.kuerzel, row.teilnehmer, row.dauer, row.timestamp) for index, row in df.iterrows()]
    return False

def export_csv(filepath, data):
    """
    export data to csv
    :param filepath: export path
    :param data: data to save
    :return: None
    """
    df = DataFrame.from_records([p.__dict__ for p in data])
    if isinstance(data[0], datatypes.Pruefung):
        df = df.rename(columns={"verfuegbarkeit": "dauer"})
    df.to_csv(filepath, index=None, header=True)
    return None