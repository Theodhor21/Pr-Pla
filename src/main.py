from src import gui
from src.data.data_handler import DataHandler
# from src.data.io_handler import import_csv
# from src.data import datatypes
#
#
data_handler = DataHandler()
#
# data_handler.raeume = import_csv("test/files/t10_alles_richtig_vervierfacht/raeume_t10.csv", datatypes.Raum)
# data_handler.aufsichtspersonen = import_csv("test/files/t10_alles_richtig_vervierfacht/aufsichtspersonen_t10.csv", datatypes.Aufsichtsperson)
# data_handler.pruefungen = import_csv("test/files/t10_alles_richtig_vervierfacht/pruefungen_t10.csv", datatypes.Pruefung)

# data_handler.raeume = import_csv("../SWE_D2-create_csv/data/raeume.csv", datatypes.Raum)
# data_handler.aufsichtspersonen = import_csv("../SWE_D2-create_csv/data/aufsichtspersonen.csv", datatypes.Aufsichtsperson)
# data_handler.pruefungen = import_csv("../SWE_D2-create_csv/data/pruefungen.csv", datatypes.Pruefung)

# data_handler.raeume = import_csv("test/files/raeume_kleine_tests.csv", datatypes.Raum)
# data_handler.aufsichtspersonen = import_csv("test/files/aufsichtspersonen_kleine_tests.csv", datatypes.Aufsichtsperson)
# data_handler.pruefungen = import_csv("test/files/pruefungen_kleine_tests.csv", datatypes.Pruefung)

#a = Algorithm()
#a.calc(data_handler=data_handler)

gui.Window(data_handler)
