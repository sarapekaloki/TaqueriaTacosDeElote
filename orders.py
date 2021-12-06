
from queue_functions import *
from datetime import datetime
def orden(id,id1,id2):
    orders = {"datetime":str(datetime.now()),"request_id":id,"status":"open","orden":[
      {
        'part_id': id1,
        'type': 'taco',
        'meat': 'adobada',
        'status': 'open',
        'quantity': 10,
        'ingredients': ["salsa", "cebolla", "cilantro"]
      },
        {
            'part_id': id2,
            'type': 'taco',
            'meat': 'asada',
            'status': 'open',
            'quantity': 10,
            'ingredients': ["salsa", "cebolla", "cilantro"]
        }
    ]}
    return orders
# purge()
for i in range (20):
    order = orden(i,(str(i)+'-0'),(str(i)+'-1'))
    write_message(order)
