class Taco():
    def __init__(self, carne, ingredientes=None):   
        self.carne = carne
        self.ingredientes=ingredientes
        self.finishTime=1
        
    def setTime(self):
        for ingrediente in range(len(self.ingredientes)):
            self.finishTime+=.5
    
    
    
    
