import threading
from queue_functions import *
from queue import Queue
from Taquero import Taquero
from Quesadillero import Quesadillero
from os import system as sys
from threading import Thread
from chalan import Chalan



class Taqueria():
    def __init__(self,taquero1,taquero2,taquero3,taquero4,quesadillero):
        self.taquero1 = taquero1
        self.taquero2 = taquero2
        self.taquero3 = taquero3
        self.taquero4 = taquero4
        self.quesadillero = quesadillero
        self.taqueros = [self.taquero1,self.taquero2,self.taquero3,self.taquero4]

        self.ordenesPendientes = 0
        self.ordenesTerminadas = 0
        self.chalan1Info = "OFF"
        self.chalan2Info = "OFF"
        # num orden, descanso, ventilador, tortillas, ingredientes (agua, cebolla,cilantro,salsa),queue
        self.taquero1Info = [0, "OFF", "OFF", 50, [100, 200, 200, 150], 1]
        self.taquero2Info = [0, "OFF", "OFF", 50, [100, 200, 200, 150], 1]
        self.taquero3Info = [0, "OFF", "OFF", 50, [100, 200, 200, 150], 1]
        self.taquero4Info = [0, "OFF", "OFF", 50, [100, 200, 200, 150], 1]
        self.quesadilleroInfo = [0, 0]

        # start end steps requestid subordenes status
        self.output = [0, 0, 0, 0, 0, 0]

    def run(self):
        # t1,t2 = self.threads()
        # t1.start()
        # t2.start()
        while True:
            self.agregar_ordenes()
            self.print()

            r1 = self.taquero1.atender_orden()
            r2 = self.taquero2.atender_orden()
            if r1 != None:
                self.agregar_ordenes(r1)
            if r2 != None:
                self.agregar_ordenes(r2)



    def threads(self):
        thread1 = Thread(target=self.taquero1.atender_orden,args=(self.taqueros,self.quesadillero,))
        thread2 = Thread(target=self.taquero2.atender_orden,args=(self.taqueros,self.quesadillero,))
        return thread1,thread2

    def agregar_ordenes(self,ogOrden=None):
        taqueros_aux = self.taqueros.copy()
        taqueros_aux2 = self.taqueros.copy()
        if ogOrden == None:
            m, orden = read_message()
            cantidad = 0
            # "Queue vacio"
            if m == "":
                return

            self.ordenesPendientes+= 1
            # Borrar mensaje del sqs
            delete_message(m[0]['ReceiptHandle'])
            # Si llegan 300 o mas tacos no se atendera orden
            for batch in orden['orden']:
                cantidad += batch['quantity']
                if cantidad >= 300:
                    # print("Orden rechazada ")
                    self.output= [None,None,None,orden['request-id'],"rejected"]
                    self.ordenesTerminadas +=1
                    return
            # Agregar seccion answer
            orden['Answer'] = {'start_time': str(datetime.now()), "end_time": "", "steps": []}
        else:
            orden = ogOrden

        carnes = set()
        queue_lengths = []
        for batch in orden['orden']:
            if batch['status'] == 'open':
                if batch['type'] == 'quesadilla':
                    carnes.add(batch['type'])
                    batch["quantity2"] = 0
                else:
                    carnes.add(batch['meat'])
        for taquero in taqueros_aux:
            if taquero.tipos[0] not in carnes and taquero.tipos[1] not in carnes:
                taqueros_aux2.remove(taquero)
        if 'quesadilla' in carnes:
            taqueros_aux2.append(self.quesadillero)
        for taquero in taqueros_aux2:
            queue_lengths.append(taquero.queue_1.qsize() + taquero.queue_2.qsize())

        # Aqui, si queue_lengths es 0 es porque ya se termino la orden, porque ningun cocinero tuvo un tipo de carne que existiera en la orden. Ahi a ver que
        # se les ocurre hacer con esto. Y chequen que la funcionalidad de pasar entre queues si funcione
        if len(queue_lengths) <= 0:
            orden['Answer']['end_time'] = str(datetime.now())
            orden['status'] = 'closed'
            self.ordenesTerminadas += 1
            self.ordenesPendientes -=1
            self.output= [orden['Answer']['start_time'],orden['Answer']['end_time'],len(orden['Answer']['steps']),orden['request-id'],len(orden['orden']),orden['status']]

            return
        max_length = min(queue_lengths)
        winner = taqueros_aux2[queue_lengths.index(max_length)]
        # winner.queue_1.put(orden)
        if len(orden['Answer']['steps'])>0:
            winner.queue_2.put(orden)
        else:
            winner.queue_1.put(orden)
        return
        # print(orden)

    def print(self):
        # windows
        # sys("cls")
        # linux ubuntu mac
        sys("clear")
        print(
            "••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••• TAQUERIA: “TACOS DE ELOTE” ••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••")
        print(
            "	•••••••••••••••••••••••••••••                          •••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••                ••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••")
        print(
            "	           ORDENES:                                                      		   TAQUERO ADOBADA:                                                                               TAQUERO TRIPA Y CABEZA:                               ")
        print(
            "	                             			         	TRABAJANDO EN ORDEN:{0}                                                                            TRABAJANDO EN ORDEN:{1}                                                            ".format(
                self.taquero1Info[0], self.taquero2Info[0]))
        print(
            "	     #PENDIENTES:{0}          			         	INGREDIENTES:                                                                                    INGREDIENTES:                                                                    ".format(
                self.ordenesPendientes))
        print(
            "	•••••••••••••••••••••••••••••         			   		AGUACATE: {0}                                                                                    AGUACATE: {1}                                                                        ".format(
                self.taquero1Info[4][0], self.taquero2Info[4][0]))
        print(
            "	                                    			   		CEBOLLA: {0}                                                                                       CEBOLLA: {1}                                                                           ".format(
                self.taquero1Info[4][1], self.taquero2Info[4][1]))
        print(
            "	                                    			   		CILANTRO: {0}                                                                                      CILANTRO: {1}                                                                           ".format(
                self.taquero1Info[4][2], self.taquero2Info[4][2]))
        print(
            "	                                    			   		SALSA: {0}                                                                                         SALSA: {1}                                                                           ".format(
                self.taquero1Info[4][3], self.taquero2Info[4][3]))
        print(
            "	                             			         	 DESCANSO:{0}                                                                                     DESCANSO:{1}                                                            ".format(
                self.taquero1Info[1], self.taquero2Info[1]))
        print(
            "	                             			         	 VENTILADOR:{0}                                                                                   VENTILADOR:{1}                                                            ".format(
                self.taquero1Info[2], self.taquero2Info[2]))
        print(
            "	                             			         	 TORTILLAS:{0}                                                                                    TORTILLAS:{1}                                                            ".format(
                self.taquero1Info[3], self.taquero2Info[3]))
        print(
            "	                             			         	 QUEUE:{0}                                                                                        QUEUE:{1}                                                            ".format(
                self.taquero1Info[5], self.taquero2Info[5]))
        print(
            "	                                                       •••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••                ••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••")
        print(
            "	•••••••••••••••••••••••••••••                          •••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••                ••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••")
        print(
            "	           ORDENES:                                                      	TAQUERO ASADA Y SUADERO:                                                                       TAQUERO ASADA Y SUADERO:                               ")
        print(
            "	                             			         	    TRABAJANDO EN ORDEN:{0}                                                                            TRABAJANDO EN ORDEN:{1}                                                            ".format(
                self.taquero3Info[0], self.taquero4Info[0]))
        print(
            "	     #TERMINADAS:{0}          			         	    INGREDIENTES:                                                                                    INGREDIENTES:                                                                    ".format(
                self.ordenesTerminadas))
        print(
            "	•••••••••••••••••••••••••••••         			   		  AGUACATE: {0}                                                                                    AGUACATE: {1}                                                                        ".format(
                self.taquero3Info[4][0], self.taquero4Info[4][0]))
        print(
            "	                                    			   		  CEBOLLA: {0}                                                                                       CEBOLLA: {1}                                                                           ".format(
                self.taquero3Info[4][1], self.taquero4Info[4][1]))
        print(
            "	                                    			   		  CILANTRO: {0}                                                                                      CILANTRO: {1}                                                                           ".format(
                self.taquero3Info[4][2], self.taquero4Info[4][2]))
        print(
            "	                                    			   		  SALSA: {0}                                                                                         SALSA: {1}                                                                           ".format(
                self.taquero3Info[4][3], self.taquero4Info[4][3]))
        print(
            "	                             			         	   DESCANSO:{0}                                                                                     DESCANSO:{1}                                                            ".format(
                self.taquero3Info[1], self.taquero4Info[1]))
        print(
            "	                             			         	   VENTILADOR:{0}                                                                                  VENTILADOR:{1}                                                            ".format(
                self.taquero3Info[2], self.taquero4Info[2]))
        print(
            "	                             			         	   TORTILLAS:{0}                                                                                    TORTILLAS:{1}                                                            ".format(
                self.taquero3Info[3], self.taquero4Info[3]))
        print(
            "	                             			         	   QUEUE:{0}                                                                                         QUEUE:{1}                                                            ".format(
                self.taquero3Info[5], self.taquero4Info[5]))
        print(
            "	                                                       •••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••                ••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••")
        print(
            "	••••••••••••••••••••••••••••••                         •••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••")
        print(
            "	           CHALANES:                                                                      QUESADILLERO:")
        print(
            "	        #1:  {0}                               			     	TRABAJANDO EN ORDEN:{1}    ".format(
                self.chalan1Info, self.quesadilleroInfo[0]))
        print(
            "	        #2:  {0}           			     	                QUESADILLAS REALIZADAS:{1}   ".format(
                self.chalan2Info, self.quesadilleroInfo[1]))
        print(
            "	••••••••••••••••••••••••••••••                         •••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••")
        print("\n")
        print(
            " ••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••")
        print(
            "                                                            OUTPUT JSON:                                                                      ")
        print(
            "                  START TIME:                                    STEPS:{0}                   REQUEST_ID:{1}                      SUBORDENES:{2}              ".format(self.output[2],self.output[3],self.output[4]))
        print(
            "                  {0}                                 ".format(self.output[0]))
        print("                  END TIME:                                    STATUS:{0}".format(self.output[5]))
        print("		  {0}                           ".format(self.output[1]))
        print(
            " ••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••")
        time.sleep(1)

if __name__ == "__main__":
    mutex1 = threading.Lock()
    mutex2 = threading.Lock()
    queue1 = Queue()
    queue2 = Queue()
    queue3 = Queue()
    queue4 = Queue()
    queue5 = Queue()
    queue6 = Queue()
    queuesadilla1 = Queue()
    queuesadilla2 = Queue()
    chalan1 = Chalan()
    chalan2 = Chalan()
    taquero1 = Taquero(queue1, queue2, ['adobada', None], chalan1, mutex1, "SaraPeka")
    taquero2 = Taquero(queue3, queue4, ['asada', 'suadero'], chalan1, mutex1, "Almamado")
    taquero3 = Taquero(queue3, queue4, ['asada', 'suadero'], chalan2, mutex2, "Aczino")
    taquero4 = Taquero(queue5, queue6, ['tripa', 'cabeza'], chalan2, mutex2, "MarioTicky")
    quesadillero = Quesadillero(queuesadilla1,queuesadilla2)
    tacosElote = Taqueria(taquero1,taquero2,taquero3,taquero4,quesadillero)
    tacosElote.run()


