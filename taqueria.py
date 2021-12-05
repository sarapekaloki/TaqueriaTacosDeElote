from queue_functions import *
from queue import Queue
from Taquero import Taquero
from Quesadillero import Quesadillero
from threading import Thread
from multiprocessing import Process
from Mesero import *

class Taqueria():
    def __init__(self,taquero1,taquero2,taquero3,taquero4,quesadillero):
        self.taquero1 = taquero1
        self.taquero2 = taquero2
        self.taquero3 = taquero3
        self.taquero4 = taquero4
        self.quesadillero = quesadillero
        self.chalanes = None
        self.taqueros = [self.taquero1,self.taquero2,self.taquero3,self.taquero4]

    def run(self):
        # t1,t2 = self.threads()
        # t1.start()
        # t2.start()
        while True:
            self.agregar_ordenes()
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

        # print(orden)

if __name__ == "__main__":
    queue1 = Queue()
    queue2 = Queue()
    queue3 = Queue()
    queue4 = Queue()
    queue5 = Queue()
    queue6 = Queue()
    queuesadilla1 = Queue()
    queuesadilla2 = Queue()

    taquero1 = Taquero(queue1, queue2, ['adobada',None])
    taquero2 = Taquero(queue3, queue4, ['asada','suadero'])
    taquero3 = Taquero(queue3, queue4, ['asada','suadero'])
    taquero4 = Taquero(queue5, queue6, ['tripa','cabeza'])

    quesadillero = Quesadillero(queuesadilla1,queuesadilla2)

    tacosElote = Taqueria(taquero1,taquero2,taquero3,taquero4,quesadillero)
    tacosElote.run()
    # p = Process(target=tacosElote.run)
    # p.start()


