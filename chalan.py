from queue_functions import *
from threading import Thread
from queue import Queue


# from Mesero import agregar_ordenes


class Chalan(Thread):

    # la funcion wait es para que el thread espere mientras el demas codigo se continua ejecutando
    def wait(self, waittime):
        time1 = time.time()
        while time.time() - time1 < waittime:
            pass

    def fill(self,taquero,filling):
        for i in taquero.fillings:
            if i == filling:
                if filling == "cilantro" or filling == "cebolla":
                    #     queremos que pasen 10 segundos, pero sin parartodo el codigo, solo el thread, por eso usamos nuesto metodo wait
                    print(f"{taquero.name} se ha quedado sin {filling}")
                    taquero.wait(10)
                    print(f"\t\t >>> Se ha rellendo -> {filling} de {taquero}")
                    taquero.fillings[filling] = 200

                # llenamos SALSA
                elif filling == "salsa":
                    print(f"{taquero.name} se ha quedado sin {filling}")
                    taquero.wait(15)
                    print(f"\t\t >>> Se ha rellenau el filling ->{filling} de {taquero}")
                    taquero.fillings[filling] = 150

                # llenamos GUACAMOLE
                elif filling == "guacamole":
                    print(f"{taquero.name} se ha quedado sin {filling}")
                    taquero.wait(20)
                    print(f"\t\t >>> Se ha rellenau el filling ->{filling} de {taquero}")
                    taquero.fillings[filling] = 100

                # Lo unico mas que queda por rellenar son las TORTILLAS
                else:
                    print(f"{taquero.name} se ha quedado sin {filling}")
                    taquero.wait(5)
                    print(f"\t\t >>> Se ha rellenau el filling ->{filling} de {taquero}")
                    taquero.fillings[filling] = 50
