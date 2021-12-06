import threading

from queue_functions import *
from queue import Queue
from taquero_Hugo import Taquero
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
        print('Eligiendo...')

        if taquero.using_queue_1:
            if taquero.queue_1.empty():
                return None
            # print(taquero1.queue_1.get())
            return taquero.queue_1.get()
        else:
            if taquero.queue_2.empty():
                return None
            return taquero.queue_2.get()


    def start_taquero(self,taquero):
        print("hola")
        while True:
            print(f"{taquero}, Queue 1: {list(taquero.queue_1.queue)}\n{taquero}, Queue 1.2 {list(taquero.queue_2.queue)}")
            orden = self.elegir_orden_del_taquero(taquero)
            print(f'{taquero}, Orden 1: {orden}')
            taquero.atender_orden(orden)
            if orden != None:
                if orden['status'] == 'open':
                    self.agregar_ordenes(orden)

    def mesero(self):
        while True:
            self.agregar_ordenes()


    def run(self):
        # lista = []
        # for i in self.taqueros:
        #     lista.append(i)
        # lista.append(self.quesadillero)

        m = Thread(target=self.mesero, args=())
        # t1 = Thread(target=self.start_taquero, args=(self.taquero1,))
        # t2 = Thread(target=self.start_taquero, args=(self.taquero2,))
        # t3 = Thread(target=self.start_taquero, args=(self.taquero3,))
        # t4 = Thread(target=self.start_taquero, args=(self.taquero4,))
        m.start()
        # t1.start()
        # t2.start()
        # t3.start()
        # t4.start()
        m.join()
        # t1.join()
        # t2.join()
        # t3.join()
        # t4.join()



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
    taquero1 = Taquero(queue1, queue2, ['adobada',None],chalan1,mutex1,"Fermin")
    taquero2 = Taquero(queue3, queue4, ['asada','suadero'],chalan1,mutex1, "Hector Osuna")
    taquero3 = Taquero(queue3, queue4, ['asada','suadero'],chalan2,mutex2,"David Espina")
    taquero4 = Taquero(queue5, queue6, ['tripa','cabeza'],chalan2,mutex2, "Marcos Moroyoqui")

    quesadillero = Quesadillero(queuesadilla1,queuesadilla2)

    tacosElote = Taqueria(taquero1,taquero2,taquero3,taquero4,quesadillero)
    tacosElote.run()
    # p = Process(target=tacosElote.run)
    # p.start()
