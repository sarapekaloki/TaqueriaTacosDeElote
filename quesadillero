from queue_functions import *
from threading import Thread
from queue import Queue


# from Mesero import agregar_ordenes
class Quesadillero():
    def __init__(self, queue1, queue2):
        self.queue_1 = queue1
        self.queue_2 = queue2
        self.using_queue_1 = True

    def atender_orden(self):
        if self.using_queue_1:
            queue = self.queue_1
            num_queue = '1'
        elif not self.using_queue_1 and not self.queue_2.empty():
            queue = self.queue_2
            num_queue = '2'

        print("\n\nQueue de quesadillero que se esta usando: {0} ".format(num_queue))

        if not queue.empty():
            orden = queue.get()
            orden['Answer']['start-time']= str(datetime.now())
            for batch in orden['orden']:
                if batch['status'] == 'open' and batch['type']=='quesadilla':
                    print(f"Batch antes: {batch}")
                    part_id = batch['part_id']
                    # print(batch['ingredients'])
                    if batch['quantity'] <= 5:
                        sleepTime=0
                        orden['Answer']['steps'].append({"state":"running","action":"Doing quesadillas","part-id":part_id})
                        sleepTime= batch['quantity']*2
                        #Checar si tiene carne pues la orden no esta terminada
                        if batch['meat']!="" or len(batch['ingredients'])!=0:
                            batch['type']="quesataco"
                            print("AHORA ES QUESATACO")

                        batch['quantity2']+=batch['quantity']
                        batch['quantity'] = 0
                        # batch.pop('quantity2')
                        time.sleep(sleepTime)
                        batch['status'] = 'closed'
                        orden['Answer']['steps'].append({"state": "Done", "action": "Batch completed", "part-id": part_id})
                        if self.using_queue_1:
                            self.using_queue_1 = False
                        print(f"Batch despues: {batch}")
                        print('\t\t >>> Batch de quesadillas terminado')
                        return orden

                    elif batch['quantity'] > 5:
                        sleepTime= 10
                        batch['quantity'] -= 5
                        batch['quantity2']+= 5
                        time.sleep(sleepTime)

                        orden['Answer']['steps'].append({"state": "Running", "action": "Doing quesadillas", "part-id": part_id})
                        self.queue_2.put(orden)
                        orden['Answer']['steps'].append({"state": "Waiting", "action": "Waiting for quesadillero", "part-id": part_id})
                        self.using_queue_1 = not self.using_queue_1
                        print(f"Batch despues: {batch}")
                        return
        else:
            print("El queue esta vacio alaverga")

            # Agregar descanso qui vacio
            return
