from queue_functions import *
from threading import Thread
from queue import Queue
# from Mesero import agregar_ordenes



class Taquero():
    def __init__(self, queue1, queue2, tipos):
        self.queue_1 = queue1
        self.queue_2 = queue2
        self.tipos = tipos
        self.fillings = {"salsa": 150, "guacamole": 100,"cilantro": 200,"cebolla": 200}
        self.tortillas = 50
        self.rest =100  # 3 s / 100
        self.fan =60  # 6 s / 60
        self.using_queue_1 = True


    def check_rest(self, rest_time):
        print(f"Tiempo restante al descanso = {self.rest}\n")
        if self.rest <= 5:
            print('----Descansando alv----')
            time.sleep(3)
            self.rest += 100
        self.rest -= rest_time

    def fan_time(self, fan_time):
        print(f"Tiempo del abanico = {self.fan}\n")
        if self.fan <= 5:
            print("\t > Prendimos abanico")
            time1 = time.time()
            while time.time() - time1 < 6:
                pass
            print(f"\t\t >>> Abanicamos {time.time() - time1} segundacos")
            self.fan += 60
        self.fan -= fan_time


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
            print("\n\nQueue de {0} que se esta usando: {1} ".format(self.tipos, num_queue))
            orden = queue.get()
            orden['Answer']['start-time']= str(datetime.now())
            for batch in orden['orden']:
                if batch['status'] == 'open' and (batch['meat'] == self.tipos[0] or batch['meat'] == self.tipos[1]):
                    print(f"Batch antes: {batch}")
                    part_id = batch['part_id']
                    # print(batch['ingredients'])
                    if batch['quantity'] <= 5:
                        sleepTime=0
                        self.check_rest(batch['quantity'])
                        fan_thread = Thread(target=self.fan_time, args=(batch['quantity'],))
                        fan_thread.start()
                        orden['Answer']['steps'].append({"state":"running","action":"Doing tacos","part-id":part_id})
                        spent_fillings = int(batch['quantity'])

                        if self.tortillas<=5:
                            print("Esperando tortillas")
                        else:
                            for ingredient in batch['ingredients']:
                                if self.fillings[ingredient]<=5:
                                    print("Esperando ingredientes")
                                sleepTime+=0.5*batch['quantity']
                                self.fillings[ingredient] -= spent_fillings
                            if batch["type"]!= "quesataco":
                                sleepTime += batch['quantity']
                            self.tortillas -= batch['quantity']
                            batch['quantity'] = 0
                            time.sleep(sleepTime)
                            batch['status'] = 'closed'
                            orden['Answer']['steps'].append({"state": "Done", "action": "Batch completed", "part-id": part_id})
                            if self.using_queue_1:
                                self.using_queue_1 = False

                            print("Fillings: ", self.fillings)
                            print(f"Batch despues: {batch}")
                            print('\t\t >>> Batch terminado')

                        # Se regresa al objeto, y la orden que se quiere enviar a otro cocinero. El objeto aqui se regresa porque se necesita
                        # referencia a el, ya que se va a excluir de la lista en la funcion de agregar_ordenes en dum.py. Esto solo se envia cuando
                        # se termino el batch. Aun falta la funcionalidad de que va a pasar cuando la orden este completamente terminada jajaja salu2
                        # agregar_ordenes(taqueros,quesadillero,orden)
                            return orden

                    elif batch['quantity'] > 5:
                        sleepTime=0
                        self.check_rest(5)
                        fan_thread = Thread(target=self.fan_time, args=(5,))
                        fan_thread.start()
                        for ingredient in batch['ingredients']:
                            self.fillings[ingredient] -= 5
                            sleepTime+=0.5*5
                        if batch["type"]!="quesataco":
                            sleepTime+=5
                        batch['quantity'] -= 5
                        self.tortillas -=5
                        time.sleep(sleepTime)

                        orden['Answer']['steps'].append({"state": "Running", "action": "Doing tacos", "part-id": part_id})
                        self.queue_2.put(orden)
                        orden['Answer']['steps'].append({"state": "Waiting", "action": "Waiting for taquero", "part-id": part_id})
                        self.using_queue_1 = not self.using_queue_1
                        print("Fillings: ", self.fillings)
                        print(f"Batch despues: {batch}")
                        return
        else:
            # Agregar descanso qui vacio
            print("Queue vacio")
            return
