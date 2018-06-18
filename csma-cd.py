import threading
import time
import random

MAX_STATION = 50
MAX_PACKETS = 5
TIME_SLOT = 0
transmissions = [None] * MAX_STATION
CABLE = [None] * 1 # Cable full = false ,empty = true
COLLISION = [None] * 1

def csmaCd (station):
    while True:
        time.sleep (random.uniform(0.0,2.0))
        print "ESTACAO %d VERIFICANDO CABO \n" % (station.id)
        if freeCable():
            print CABLE[0]
            print "cabo livre para estacao %d" % (station.id)
            transmit(station)
            if COLLISION[0]:
                COLLISION[0] = False
                CABLE[0] = True
                for i in range(MAX_STATION):
                    transmissions[i] = False
                #backOffTime()
        else:
            while  not freeCable():
                pass
                #print "estacao %d - esperando liberar cabo " % (station.id)
                #time.sleep(2)

def transmit(station):
    print "inicio tranmissao da estacao %d" % (station.id)
    CABLE[0] = False
    transmissions[station.id] = True
    #transmissions[(station.id + 1) % MAX_STATION] = True

    print transmissions, CABLE[0]
    randomNumPackets = random.randrange(MAX_PACKETS)
    print "estacao %d - enviara %d pacotes" % (station.id,randomNumPackets)
    for i in range(randomNumPackets):
        print "estacao %d - enviando pacote %d " % (station.id, i+1)
        time.sleep (TIME_SLOT)
        if collision():
            print "##################### COLLISION ############################"
            return
    CABLE[0] = True
    print "estacao %d terminou transmissao com sucesso" % (station.id)
    transmissions[station.id] = False

def collision():
    i = 0
    for t in transmissions:
        if t:
            i = i + 1
    print "num transmissores %d" % (i)
    if i > 1:
        COLLISION[0] = True
    return COLLISION[0]

def freeCable():
    return CABLE[0]

class Station(object):
    def __init__(self, id):
        self.id = id
        print self.id
        csmaCd(self)

def main():
    for i in range(MAX_STATION):
        transmissions[i] = False
    print transmissions
    COLLISION[0] = False
    CABLE[0] = False
    for i in range(MAX_STATION):
        station = threading.Thread(target = Station, args = (i,))
        station.start()

    time.sleep(10)
    CABLE[0] = True

if __name__ == '__main__':
    main()
