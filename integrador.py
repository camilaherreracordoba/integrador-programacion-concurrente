import random
import threading
import time
import logging

semaforoSucios = threading.Semaphore()
#semaforoLimpios = threading.Semaphore()
semaforoLibres = threading.Semaphore()
monitorPlatosSucios = threading.Condition()

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

class Bachero(threading.Thread):
    def __init__(self):    
        super().__init__()

    def lavar(self):
        global platosLimpios
        global platosSucios
        with monitorPlatosSucios:
            monitorPlatosSucios.wait()
            logging.info('lavando plato')
            platosSucios -= 1
#            with semaforoLimpios:
            platosLimpios += 1
            time.sleep(2)
            estadoActual()     
    def run(self):
        logging.info('lavando')
        while(True):
            self.lavar()

class Mesero(threading.Thread):
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
            with monitorPlatosSucios:
                monitorPlatosSucios.notify()
                estadoActual()
            semaforoSucios.release()
        semaforoLibres.release()

def cocina():
    global platosLimpios
    global platosEnUso
    logging.info('la cocina está funcionando')
    estadoActual()
    while(True):
#        semaforoLimpios.acquire()
        time.sleep(random.randint(0, 10))
        if (platosLimpios > 0):
            platosLimpios -= 1
            logging.info('---- usando plato ----')
#            semaforoLimpios.release()
            semaforoLibres.acquire()
            platosEnUso += 1
            semaforoLibres.release()
            estadoActual()

def estadoActual():
#    logging.info()
    logging.info('limpios %i' %platosLimpios)
    logging.info('sucios %i' % platosSucios)
    logging.info('en uso %i' % platosEnUso)

platosEnUso = 0
platosSucios = 0
platosLimpios = 1


for i in range(100):
    m = Mesero()
    m.name = 'mesero'+str(i)
    m.start()

for i in range(50):
    b = Bachero()
    b.name = 'bachero'+str(i)
    b.start()

cocina = threading.Thread(target= cocina, name = 'Cocina')

cocina.start()



