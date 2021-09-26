class Taco():
    def __init__(self, carne,isQuesadilla, ingredientes=None):   
        self.carne = carne
        self.ingredientes=ingredientes
        self.finishTime=1
        self.isQuesadilla=isQuesadilla
        
    def setTime(self):
        for ingrediente in range(len(self.ingredientes)):
            self.finishTime=self.finishTime+.5
    
    
    
    
