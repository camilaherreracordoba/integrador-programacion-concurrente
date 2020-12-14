import random
import threading
import time
import logging

semaforoSucios = threading.Semaphore()
semaforoLibres = threading.Semaphore()
semaforoBacheros = threading.Semaphore()

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

class Bachero(threading.Thread):
    def __init__(self):    
        super().__init__()

    def lavar(self):
        global platosLimpios
        global platosSucios
#        while(platosSucios > 0):
        with semaforoBacheros:
            if(platosSucios > 0):
                logging.info('lavando plato')
                semaforoSucios.acquire()
                platosLimpios += 1
                platosSucios -= 1
            
                time.sleep(2)     
                semaforoSucios.release()
                estadoActual()
    def run(self):
        logging.info('lavando')
        while(True):
            self.lavar()

class Ayudante(threading.Thread):
    def __init__(self):
        super().__init__()
    def run(self):
        logging.info('recibiendo')
        while (True):
            self.traerPlatos()

    def traerPlatos(self):
        global platosEnUso
        global platosSucios
        semaforoLibres.acquire()
        if(platosEnUso > 0):
            logging.info('llevando plato')
            platosEnUso -= 1
            semaforoSucios.acquire()
            platosSucios += 1
            estadoActual()
            semaforoSucios.release()
        semaforoLibres.release()

def cocina():
    global platosLimpios
    global platosEnUso
    logging.info('la cocina está funcionando')
    estadoActual()
    for i in range(10): # para simular el fin de la jornada.
        time.sleep(random.randint(0, 10))
        cantidadRandom = random.randint(1, 5)
        if (platosLimpios > 0):
            if(cantidadRandom > platosLimpios):
                aux = cantidadRandom - platosLimpios
                cantidadRandom -= aux 
            platosLimpios -= cantidadRandom
            logging.info('---- platos usados: %i ----' %cantidadRandom)
            semaforoLibres.acquire()
            platosEnUso +=  cantidadRandom
            semaforoLibres.release()
            estadoActual()

def estadoActual():
    logging.info('limpios %i' %platosLimpios)
    logging.info('sucios %i' % platosSucios)
    logging.info('en uso %i' % platosEnUso)

platosEnUso = 0
platosSucios = 0
platosLimpios = 10


for i in range(10):
    a = Ayudante()
    a.name = 'ayudante'+str(i)
    a.start()

for i in range(1):
    b = Bachero()
    b.name = 'bachero'+str(i)
    b.start()

cocina = threading.Thread(target= cocina, name = 'Cocina')

cocina.start()