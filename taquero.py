import threading

from queue_functions import *
from threading import Thread
from queue import Queue
# from Mesero import agregar_ordenes
from chalan import Chalan



class Taquero():
    def __init__(self, queue1, queue2, tipos, chalan:Chalan,mutex=threading.Lock() ,name="Taquero X"):
        self.queue_1 = queue1
        self.queue_2 = queue2
        self.tipos = tipos
        self.chalan = chalan
        self.name = name
        self.mutex = mutex
        self.fillings = {"salsa": 150, "guacamole": 100,"cilantro": 200,"cebolla": 200, "tortillas":50}
        self.idle = 0
        self.rest =100  # 3 s / 100
        self.fan =60  # 6 s / 60
        self.using_queue_1 = True

    def __repr__(self):
        return self.name

    def call_chalan(self,filling, quantity_to_fill):
        if self.fillings[filling] <= quantity_to_fill:
            self.mutex.acquire()
            self.chalan.fill(self,filling)
            self.mutex.release()

    def check_rest(self, rest_time):
        if self.rest <= 5:
            time.sleep(3)
            self.rest += 100
        self.rest -= rest_time

    def fan_time(self, fan_time):
        if self.fan <= 5:
            time1 = time.time()
            while time.time() - time1 < 6:
                pass
            self.fan += 60
        self.fan -= fan_time

    def wait(self, waittime):
        time1 = time.time()
        while time.time() - time1 < waittime:
            pass

    def atender_orden(self):
        spent_fillings = 0

        if self.using_queue_1:
            queue = self.queue_1
            num_queue = '1'
        elif not self.using_queue_1 and not self.queue_2.empty():
            queue = self.queue_2
            num_queue = '2'
        else:
            queue = self.queue_1
            num_queue = '1'

        if not queue.empty():
            # se calcula el tiempo desde la ultima vez que hizo algo
            # time2 = time.time()

            orden = queue.get()
            for batch in orden['orden']:
                if batch['status'] == 'open' and (batch['meat'] == self.tipos[0] or batch['meat'] == self.tipos[1]):
                    part_id = batch['part_id']
                    # print(batch['ingredients'])

                    # El batch es MENOS O IGUAL a 5 tacos
                    if batch['quantity'] <= 5:
                        # Empezamos un contador de sleep time que es lo que r=tardara en ppreparar el batch de tacos
                        sleepTime=0
                        # revisamos el timepo que falta al taquero para descansar, y si llega a cero, se descansa
                        self.check_rest(batch['quantity'])
                        # Hacemos lo mismo con el abanico
                        fan_thread = Thread(target=self.fan_time, args=(batch['quantity'],))
                        fan_thread.start()

                        # Se agrega la operacion a la respuesta del JSON de salida
                        orden['Answer']['steps'].append({"state":"running","action":"Doing tacos","part-id":part_id})
                        # Se calculan cuantos fillings de cada uno se van a usar para esta iteracion
                        spent_fillings = int(batch['quantity'])

                        # Le quito x tortillas, de los x tacos que vamos a preparar // NEEDS CHECK
                        # Primero se llama al chalan para que rellen si es que no hay suficientes
                        self.call_chalan("tortillas",spent_fillings)
                        self.fillings["tortillas"] -= spent_fillings

                        # por cada filling del batch, le quito 5 a ese filling // NEEDS CHECK
                        for ingredient in batch['ingredients']:
                            self.call_chalan(ingredient,spent_fillings)
                            self.fillings[ingredient] -= spent_fillings
                            sleepTime += 0.5 * batch['quantity']
                        if batch["type"]!= "quesataco":
                            sleepTime += batch['quantity']

                        # Como quedan menos de 5 ingredientes, el batch se termina
                        batch['quantity'] = 0
                        # time.sleep(sleepTime)

                        # se le da el estatus de closed al batch
                        batch['status'] = 'closed'
                        orden['Answer']['steps'].append({"state": "Done", "action": "Batch completed", "part-id": part_id})
                        # Usamos el queue 2, ya que acabamos un batch
                        if self.using_queue_1:
                            self.using_queue_1 = False

    
                        # Se regresa al objeto, y la orden que se quiere enviar a otro cocinero. El objeto aqui se regresa porque se necesita
                        # referencia a el, ya que se va a excluir de la lista en la funcion de agregar_ordenes en dum.py. Esto solo se envia cuando
                        # se termino el batch. Aun falta la funcionalidad de que va a pasar cuando la orden este completamente terminada jajaja salu2
                        # agregar_ordenes(taqueros,quesadillero,orden)
                        return orden

                    # El batch es MAYOR A 5 TACOS
                    elif batch['quantity'] > 5:
                        # Empezamos un contador de sleep time que es lo que r=tardara en ppreparar el batch de tacos
                        sleepTime=0

                        # revisamos el timepo que falta al taquero para descansar, y si llega a cero, se descansa
                        self.check_rest(5)
                        # Lo mismo con el abanico
                        fan_thread = Thread(target=self.fan_time, args=(5,))
                        fan_thread.start()

                        # Le quito 5 tortillas, de los 5 tacos que vamos a preparar // NEEDS CHECK
                        self.call_chalan("tortillas",5)
                        self.fillings["tortillas"] -= 5

                        # por cada filling del batch, le quito 5 a ese filling // NEEDS CHECK
                        for ingredient in batch['ingredients']:
                            self.call_chalan(ingredient,5)
                            self.fillings[ingredient] -= 5
                            sleepTime+=0.5*5
                        if batch["type"]!="quesataco":
                            sleepTime+=5

                        # Se descuentan los tacos que ya se hicieron a la cantidad total
                        batch['quantity'] -= 5
                        #  El timepo que toma hacer los tacos
                        # time.sleep(sleepTime)

                        orden['Answer']['steps'].append({"state": "Running", "action": "Doing tacos", "part-id": part_id})
                        self.queue_2.put(orden)
                        orden['Answer']['steps'].append({"state": "Waiting", "action": "Waiting for taquero", "part-id": part_id})
                        self.using_queue_1 = not self.using_queue_1
                        
                        return
        else:
            # tiempo = 0
            # time1 = time.time()
            # Agregar descanso qui vacio
            return
