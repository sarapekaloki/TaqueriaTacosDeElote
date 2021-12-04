from os import system as sys
import random
import time

class visualizador():
    def __init__(self):
        self.ordenesPendientes = 10
        self.ordenesTerminadas = 0
        self.chalan1 = "ON"
        self.chalan2 = "OFF"
        # num orden, descanso, ventilador, tacos q ha hecho, ingredientes (agua, cebolla,cilantro,salsa)
        self.taquero1 = [2,"ON","OFF",10,[200,12,32,140]]
        self.taquero2 = [2,"ON","OFF",10,[200,12,32,140]]
        self.taquero3 = [2,"ON","OFF",10,[200,12,32,140]]
        self.taquero4 = [2,"ON","OFF",10,[200,12,32,140]]
        self.quesadillero = [2,10]

        #start end steps requestid subordenes
        self.output=[10.0,20.0,4,1234,4]

    def print(self):
        #windows sys("cls")
        #linux ubuntu mac 
        sys("clear")
        print("••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••• TAQUERIA: “TACOS DE ELOTE” ••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••")
        print("	•••••••••••••••••••••••••••••                          •••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••                ••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••")
        print("	           ORDENES:                                                      		   TAQUERO ADOBADA:                                                                               TAQUERO TRIPA Y CABEZA:                               ")
        print("	                             			         	TRABAJANDO EN ORDEN:{0}                                                                            TRABAJANDO EN ORDEN:{1}                                                            ".format(self.taquero1[0], self.taquero2[0]))
        print("	     #PENDIENTES:{0}          			         	INGREDIENTES:                                                                                    INGREDIENTES:                                                                    ".format(self.ordenesPendientes))
        print("	•••••••••••••••••••••••••••••         			   		AGUACATE: {0}                                                                                    AGUACATE: {1}                                                                        ".format(self.taquero1[4][0],self.taquero2[4][0]))
        print("	                                    			   		CEBOLLA: {0}                                                                                       CEBOLLA: {1}                                                                           ".format(self.taquero1[4][1],self.taquero2[4][1]))
        print("	                                    			   		CILANTRO: {0}                                                                                      CILANTRO: {1}                                                                           ".format(self.taquero1[4][2],self.taquero2[4][2]))
        print("	                                    			   		SALSA: {0}                                                                                         SALSA: {1}                                                                           ".format(self.taquero1[4][3],self.taquero2[4][3]))
        print("	                             			         	 DESCANSO:{0}                                                                                     DESCANSO:{1}                                                            ".format(self.taquero1[1], self.taquero2[1]))
        print("	                             			         	 VENTILADOR:{0}                                                                                  VENTILADOR:{1}                                                            ".format(self.taquero1[2], self.taquero2[2]))
        print("	                             			         	 TACOS REALIZADOS:{0}                                                                             TACOS REALIZADOS:{1}                                                            ".format(self.taquero1[3], self.taquero2[3]))
        print("	                                                       •••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••                ••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••")
        print("	•••••••••••••••••••••••••••••                          •••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••                ••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••")
        print("	           ORDENES:                                                      	TAQUERO ASADA Y SUADERO:                                                                       TAQUERO ASADA Y SUADERO:                               ")
        print("	                             			         	TRABAJANDO EN ORDEN:{0}                                                                            TRABAJANDO EN ORDEN:{1}                                                            ".format(self.taquero3[0], self.taquero4[0]))
        print("	     #TERMINADAS:{0}          			         	INGREDIENTES:                                                                                    INGREDIENTES:                                                                    ".format(self.ordenesTerminadas))
        print("	•••••••••••••••••••••••••••••         			   		AGUACATE: {0}                                                                                    AGUACATE: {1}                                                                        ".format(self.taquero3[4][0],self.taquero4[4][0]))
        print("	                                    			   		CEBOLLA: {0}                                                                                       CEBOLLA: {1}                                                                           ".format(self.taquero3[4][1],self.taquero4[4][1]))
        print("	                                    			   		CILANTRO: {0}                                                                                      CILANTRO: {1}                                                                           ".format(self.taquero3[4][2],self.taquero4[4][2]))
        print("	                                    			   		SALSA: {0}                                                                                         SALSA: {1}                                                                           ".format(self.taquero3[4][3],self.taquero4[4][3]))
        print("	                             			         	 DESCANSO:{0}                                                                                     DESCANSO:{1}                                                            ".format(self.taquero3[1], self.taquero4[1]))
        print("	                             			         	 VENTILADOR:{0}                                                                                  VENTILADOR:{1}                                                            ".format(self.taquero3[2], self.taquero4[2]))
        print("	                             			         	 TACOS REALIZADOS:{0}                                                                             TACOS REALIZADOS:{1}                                                            ".format(self.taquero3[3], self.taquero4[3]))
        print("	                                                       •••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••                ••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••")
        print("	••••••••••••••••••••••••••••••                         •••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••")
        print("	           CHALANES:                                                                      QUESADILLERO:")
        print("	        #1:  {0}                               			     	TRABAJANDO EN ORDEN:{1}    ".format(self.chalan1,self.quesadillero[0]))
        print("	        #2:  {0}           			     	                QUESADILLAS REALIZADAS:{1}   ".format(self.chalan2,self.quesadillero[1]))
        print("	••••••••••••••••••••••••••••••                         •••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••")
        print("\n")
        print(" ••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••")
        print("                                                            OUTPUT JSON:                                                                      ")
        print("                  START TIME:                    STEPS:                   REQUEST_ID:                      SUBORDENES:                   ")
        print("                  {0}                            {1}                      {2}                              {3}  ".format(self.output[0],self.output[2],self.output[3],self.output[4]))
        print("                  END TIME:  ")
        print("		  {0}".format(self.output[1]))
        print(" ••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••")




        time.sleep(1)
        # for i in range(10):
        #     sys.stdout.write("\r{0}, {1}".format("Hola buenas tardes",i))
        #     # sys.stdout.flush()
        #     time.sleep(0.5)

taqueria = visualizador()
while True:
    taqueria.taquero1[0]= random.randint(1,10)
    taqueria.print()