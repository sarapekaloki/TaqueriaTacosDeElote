import threading

from queue_functions import *
from queue import Queue
from taquero import Taquero
from quesadillero import Quesadillero
from threading import Thread
from chalan import Chalan
from multiprocessing import Process


class Taqueria():
    def __init__(self,taquero1,taquero2,taquero3,taquero4,quesadillero):
        self.taquero1 = taquero1
        self.taquero2 = taquero2
        self.taquero3 = taquero3
        self.taquero4 = taquero4
        self.quesadillero = quesadillero
        self.chalanes = None
        self.taqueros = [self.taquero1,self.taquero2,self.taquero3,self.taquero4]

    def elegir_orden_del_taquero(self, taquero):

        if taquero.using_queue_1:
            if taquero.queue_1.empty():
                return None
            return taquero.queue_1.get()
        else:
            if taquero.queue_2.empty():
                return None
            return taquero.queue_2.get()

    def run(self):
        lista = []
        for i in self.taqueros:
            lista.append(i)
        lista.append(self.quesadillero)


        while True:
            meseros_threads=[]
            for i in range(20):
                t1 = Thread(target=self.agregar_ordenes)
                meseros_threads.append(t1)
            for thread in meseros_threads:
                thread.start()
            for thread in meseros_threads:
                thread.join()

            print("Queue 1 de: ", taquero1,":",list(taquero1.queue_1.queue))
            print("Queue 2 de: ", taquero1,":",list(taquero1.queue_2.queue))
            print("Queue 1 de: ", taquero2,":",list(taquero2.queue_1.queue))
            print("Queue 2 de: ", taquero2,":",list(taquero2.queue_2.queue))
            print("Queue 1 de: ", taquero3,":",list(taquero3.queue_1.queue))
            print("Queue 2 de: ", taquero3,":",list(taquero3.queue_2.queue))
            print("Queue 1 de: ", taquero4,":",list(taquero4.queue_1.queue))
            print("Queue 2 de: ", taquero4,":",list(taquero4.queue_2.queue))
            print("Queue 1 de: ", quesadillero,":",list(quesadillero.queue_2.queue))
            print("Queue 2 de: ", quesadillero,":",list(taquero4.queue_2.queue))
            orden1 = self.elegir_orden_del_taquero(taquero1)
            orden2 = self.elegir_orden_del_taquero(taquero2)
            orden3 = self.elegir_orden_del_taquero(taquero3)
            orden4 = self.elegir_orden_del_taquero(taquero4)
            orden_quesadillas = self.elegir_orden_del_taquero(quesadillero)
            print('Orden 1: ',orden1)
            print('Orden 2: ', orden2)
            print('Orden 3: ',orden3)
            print('Orden 4: ', orden4)
            print('Orden Quesadillas: ', orden_quesadillas)

            # self.elegir_queue_del_taquero(taquero1)
            # self.elegir_queue_del_taquero(taquero2)
            # r1 = self.taquero1.atender_orden(orden1)
            # r2 = self.taquero2.atender_orden(orden2)
            r1 = Thread(target=taquero1.atender_orden, args=(orden1,))
            r2 = Thread(target=taquero2.atender_orden, args=(orden2,))
            r3 = Thread(target=taquero1.atender_orden, args=(orden3,))
            r4 = Thread(target=taquero2.atender_orden, args=(orden4,))
            r5 = Thread(target=taquero2.atender_orden, args=(orden_quesadillas,))

            r1.start()
            r2.start()
            r3.start()
            r4.start()
            r5.start()
            r1.join()
            r2.join()
            r3.join()
            r4.join()
            r5.join()

            if orden1 != None and 'status' in orden1:
                if orden1['status'] == 'open':
                    self.agregar_ordenes(orden1)
            if orden2 != None and 'status' in orden2:
                if orden2['status'] == 'open':
                    self.agregar_ordenes(orden2)
            if orden3 != None and 'status' in orden3:
                if orden3['status'] == 'open':
                    self.agregar_ordenes(orden3)
            if orden4 != None and 'status' in orden4:
                if orden4['status'] == 'open':
                    self.agregar_ordenes(orden4)
            if orden_quesadillas != None and 'status' in orden_quesadillas:
                if orden_quesadillas['status'] == 'open':
                    self.agregar_ordenes(orden_quesadillas)


    def agregar_ordenes(self,ogOrden=None):

        taqueros_aux = self.taqueros.copy()
        taqueros_aux2 = self.taqueros.copy()
        if ogOrden == None:
            m, orden = read_message()
            cantidad = 0
            # "Queue vacio"
            if m == "":
                return
            # Borrar mensaje del sqs
            delete_message(m[0]['ReceiptHandle'])
            # Si llegan 300 o mas tacos no se atendera orden
            for batch in orden['orden']:
                cantidad += batch['quantity']
                if cantidad >= 300:
                    print("Orden rechazada ")
                    return
            # Agregar seccion answer
            orden['Answer'] = {'start-time': "", "end_time": "", "steps": []}
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
            print('ORDEN TERMINADA')
            print(orden)
            return
        max_length = min(queue_lengths)
        winner = taqueros_aux2[queue_lengths.index(max_length)]
        # winner.queue_1.put(orden)
        if len(orden['Answer']['steps'])>0:
            winner.queue_2.put(orden)
        else:
            winner.queue_1.put(orden)

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
    taquero1 = Taquero(queue1, queue2, ['adobada',None],chalan1,mutex1,"Cristiano Ronaldo")
    taquero2 = Taquero(queue3, queue4, ['asada','suadero'],chalan1,mutex1, "Jeff Bezos")
    taquero3 = Taquero(queue3, queue4, ['asada','suadero'],chalan2,mutex2,"Jesucristo el Robot del futuro")
    taquero4 = Taquero(queue5, queue6, ['tripa','cabeza'],chalan2,mutex2, "Gabriel Tavorin")

    quesadillero = Quesadillero(queuesadilla1,queuesadilla2)

    tacosElote = Taqueria(taquero1,taquero2,taquero3,taquero4,quesadillero)
    tacosElote.run()
    # p = Process(target=tacosElote.run)
    # p.start()
