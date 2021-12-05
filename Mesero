from queue_functions import read_message
from Taquero import *
from Quesadillero import Quesadillero
from queue import Queue




# queue1 = Queue()
# queue2 = Queue()
# queue3 = Queue()
# queue4 = Queue()
# queue5 = Queue()
# queue6 = Queue()
# queuesadilla1 = Queue()
# queuesadilla2 = Queue()
#
#
# taquero1 = Cocinero(queue1, queue2, ['asada',None])
# taquero2 = Cocinero(queue3, queue4, ['asada','suadero'])
# taquero3 = Cocinero(queue3, queue4, ['asada','suadero'])
# taquero4 = Cocinero(queue5, queue6, ['tripa','cabeza'])
# quesadillero1 = Cocinero(queuesadilla1, queuesadilla2, ['quesadilla',None])

#
# orden = [
#     {
#         "part_id":"2-0",
#         "type":"taco",
#         "meat":"adobada",
#         "quantity":10,
#         "ingredientes":[]
#     },
#     {
#         "part_id":"2-1",
#         "type":"taco",
#         "meat":"asada",
#         "quantity":5,
#         "ingredientes":[]
#     },
#     {
#         "part_id": "2-1",
#         "type": "quesadilla",
#         "meat": "suadero",
#         "quantity": 5,
#         "ingredientes": []
#     },
#     {
#         "part_id": "2-1",
#         "type": "taco",
#         "meat": "tripa",
#         "quantity": 5,
#         "ingredientes": []
#     },
#     {
#         "part_id": "2-1",
#         "type": "taco",
#         "meat": "cabeza",
#         "quantity": 5,
#         "ingredientes": []
#     }
# ]

# m, orden = read_message()

def agregar_ordenes(taqueros, ogOrden=None):
    taqueros_aux = taqueros.copy()
    if ogOrden == None:
        m,orden = read_message()
        cantidad=0
        # Borrar mensaje del sqs
        delete_message(m[0]['ReceiptHandle'])
        #Si llegan 300 o mas tacos no se atendera orden
        for batch in orden['orden']:
            cantidad+=batch['quantity']
            if cantidad >= 300:
                print("Orden rechazada ")
                return
        # Agregar seccion answer
        orden['Answer']={'start-time':"","end_time":"","steps":[]}
    else:
        orden = ogOrden

    carnes = set()
    queue_lengths=[]
    for batch in orden['orden']:
        if batch['status']=='open':
            if batch['type']=='quesadilla':
                carnes.add(batch['type'])
                batch["quantity2"]=0
            else:
                carnes.add(batch['meat'])

    for taquero in taqueros_aux:
        if isinstance(taquero, Quesadillero) and 'quesadilla' not in carnes:
            taqueros.remove(taquero)
        if not isinstance(taquero,Quesadillero):
            if taquero.tipos[0] not in carnes and taquero.tipos[1] not in carnes:
                taqueros.remove(taquero)
    for taquero in taqueros:
        queue_lengths.append(taquero.queue_1.qsize()+taquero.queue_2.qsize())

    #Aqui, si queue_lengths es 0 es porque ya se termino la orden, porque ningun cocinero tuvo un tipo de carne que existiera en la orden. Ahi a ver que
    #se les ocurre hacer con esto. Y chequen que la funcionalidad de pasar entre queues si funcione
    if len(queue_lengths) <= 0:
        orden['Answer']['end_time']= str(datetime.now())
        print('ORDEN TERMINADA')
        print(orden)
        return

    max_length = min(queue_lengths)
    winner = taqueros[queue_lengths.index(max_length)]
    winner.queue_1.put(orden)
    # print(orden)

# agregar_ordenes([taquero1,taquero2,taquero3,quesadillero1],orden)
