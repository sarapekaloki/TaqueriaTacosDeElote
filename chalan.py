from queue_functions import *
from threading import Thread
from queue import Queue


# from Mesero import agregar_ordenes


class Chalan():
    def __init__(self, taqueros:list):
        self.taqueros = taqueros


    # la funcion wait es para que el thread espere mientras el demas codigo se continua ejecutando
    def wait(self, waittime):
        time1 = time.time()
        while time.time() - time1 < waittime:
            pass

    def fill_fillings(self):
        for taquero in self.taqueros:
            for filling in taquero.fillings:
                if taquero.fillings[filling] <= 5:

                    # llenamos CILANTRO O CEBOLLA
                    if filling == "cilantro" or filling == "cebolla":
                        #     queremos que pasen 10 segundos, pero sin parartodo el codigo, solo el thread, por eso usamos nuesto metodo wait
                        self.wait(10)
                        print(f"\t\t >>> Se ha rellenau el filling ->{filling}")
                        taquero.fillings[filling] = 200

                    # llenamos SALSA
                    elif filling == "salsa":
                        self.wait(15)
                        print(f"\t\t >>> Se ha rellenau el filling ->{filling}")
                        taquero.fillings[filling] = 150

                    # llenamos GUACAMOLE
                    elif filling == "guacamole":
                        self.wait(20)
                        print(f"\t\t >>> Se ha rellenau el filling ->{filling}")
                        taquero.fillings[filling] = 100
                    
                    # Lo unico mas que queda por rellenar son las TORTILLAS
                    else:
                        self.wait(5)
                        print(f"\t\t >>> Se ha rellenau el filling ->{filling}")
                        taquero.fillings[filling] = 50
