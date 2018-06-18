import threading
import multiprocessing
import time
import random
import sys
from subprocess import os

MAX_LOOP = 1
MAX_STATION = 10
MAX_PACKETS = 5
TIME_SLOT = 0.0053
RATE_COLLISION = 25 # rate of collision on cable
CABLE = [None] * 1 # Cable full = false ,empty = true
COLLISION = [None] * 1

SUCESS = [0] * MAX_STATION
FAIL = [0] * MAX_STATION

def csmaCd (station):
    cont = 0
    while cont <= MAX_LOOP:
        cont = cont + 1
        time.sleep (random.uniform(0.0,5.0))

        print ['',"\nESTACAO %d - verificando cabo\n" % (station.id)][len(sys.argv) > 1 and (sys.argv[1] == '-d')],

        if freeCable():

            print ['',"\nESTACAO %d - utilizando cabo \n" % (station.id)][len(sys.argv) > 1 and (sys.argv[1] == '-d')],

            transmit(station)
            if COLLISION[0]:
                COLLISION[0] = False
                CABLE[0] = True
                backOffTime(station)
        else:
            while  not freeCable():
                pass


def backOffTime (station):
    if station.transmissionAttempts <= 10:
        station.transmissionAttempts += 1
    timeMax = 2 ** station.transmissionAttempts

    print ['',"ESTACAO %d esperara de 0 a %d slots de tempo\n" % (station.id, timeMax)][len(sys.argv) > 1 and (sys.argv[1] == '-d')],
    timeWait = random.uniform(0.0,timeMax)

    print ['',"ESTACAO %d esperara %d slots na tentativa %d\n" % (station.id, timeWait, station.transmissionAttempts)][len(sys.argv) > 1 and (sys.argv[1] == '-d')],
    timeWait = timeWait * TIME_SLOT
    time.sleep(timeWait)

def transmit(station):

    CABLE[0] = False
    print ['',"ESTACAO %d - iniciando transmissao \n" % (station.id)][len(sys.argv) > 1 and (sys.argv[1] == '-d')],

    causingCollision (station)

    randomNumPackets = random.randrange(1,MAX_PACKETS)

    print ["","ESTACAO %d - enviara %d pacotes\n" % (station.id,randomNumPackets)][len(sys.argv) > 1 and (sys.argv[1] == '-d')],

    for i in range(randomNumPackets):
        print ["","\t- ESTACAO %d - enviando pacote %d \n" % (station.id, i+1)][len(sys.argv) > 1 and (sys.argv[1] == '-d')],
        time.sleep (TIME_SLOT)

        if collision():
            print ["","\n< ;-( ESTACAO %d - detectou ### COLISAO ### \n" % (station.id)][len(sys.argv) > 1 and (sys.argv[1] == '-d')],
            station.fail += 1
            FAIL[station.id] = station.fail

            if len(sys.argv) != 1 and sys.argv[1] == '-r':
                printResul()

            return

    CABLE[0] = True # Estacao terminou transferencia, entao libera o meio fisico

    print ["","\n< :-) ESTACAO %d - terminou transmissao com sucesso \n" % (station.id)][len(sys.argv) > 1 and (sys.argv[1] == '-d')],
    station.sucess += 1
    SUCESS[station.id] = station.sucess
    if len(sys.argv) != 1 and sys.argv[1] == '-r':
        printResul()
    else:
        print "\nESTACAO %d transmitiu com SUCESSO " % (station.id)

    station.transmissionAttempts = 0


def causingCollision (station):
    luck = random.randrange(1,99)
    if luck <= RATE_COLLISION:
        COLLISION[0] = True


def collision():
    return COLLISION[0]

def freeCable():
    return CABLE[0]

def printResul ():
    if len(sys.argv) != 1 and sys.argv[1] != '-d':
        os.system("clear")

    print "\n\n|      #  TRANSMISSOES  #     |"
    print "| ESTACAO | SUCESSOS | FALHAS |"
    print "+---------+----------+--------+"

    for i in range(MAX_STATION):
        print "|    %d    |    %d     |   %d    |" % (i, SUCESS[i], FAIL[i])
        print "+---------+----------+--------+"

def help():
    print "Use a linha de comando :"
    print "python csmaCd.py [ops] "
    print "Com parametros opcionais, que sao:"
    print " -d , para modo debug"
    print " -r , para modo de impressao dos resultados"
    print " sem utilizar as ops, o programa seguira o enunciado"


class Station(object):
    def __init__(self, id):
        self.id = id
        self.transmissionAttempts = 0
        self.sucess = 0
        self.fail = 0
        csmaCd(self)


def main():

    COLLISION[0] = False
    CABLE[0] = False
    stations = []

    if len(sys.argv) == 1 or (len(sys.argv) > 1 and (sys.argv[1] == '-d' or sys.argv[1] == '-r')):

        for i in range(MAX_STATION):
            station = threading.Thread(target = Station, args = (i,))
            stations.append(station)

        for station in stations:
            station.start()


        print ['' ,"Cabo inicia com transmissao de uma mensagem\n"][len(sys.argv) > 1 and (sys.argv[1] == '-d')],
        time.sleep(3)

        print (['' ,"&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& CABO LIVRE &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\n"][len(sys.argv) > 1 and (sys.argv[1] == '-d')]),
        CABLE[0] = True


        for station in stations:
            station.join()

        printResul()

    else:
        help()

if __name__ == '__main__':
    main()
