class Taquero():
    def __init__(self,name , carne1, queue1, queue2, carne2=None):
        self.name = name
        self.carne1 = carne1
        self.carne2 = carne2
        self.tacosCount = 0
        self.tortillaCount = 0
        self.salsaCount = 0
        self.cebollaCount = 0
        self.cilantroCount = 0
        self.aguacateCount = 0
        self.queue1 = queue1
        self.queue2 = queue2
        self.breakTime = 0
        self.resting=False
    
    
    def setBreak(self,rest):
        self.resting=rest
    
        





