import threading
import multiprocessing
import time
import random
import sys
from subprocess import os


MAX_LOOP = 5           # Numero de vezes que o protocolo csma-cd executara
MAX_STATION = 10       # Numero de estacoes na rede
MAX_PACKETS = 5        # Numero maximo de pacotes que cada estacao tenta transmitir
TIME_SLOT = 0.00514     # Tempo de cada slot de tempo
RATE_COLLISION = 25    # Taxa de colisoes na rede , medida em porcentagem
CABLE = [None] * 1     # Variavel global que representa o meio fisico (cabo)
COLLISION = [None] * 1 # Variavel global que representa se ouve uma colisao ou nao

SUCESS = [0] * MAX_STATION  # Vetor que contem o numero de transmissoes bem sucedidas de cada estacao
FAIL = [0] * MAX_STATION    # Vetor que contem o numero de transmissoes mal sucedidas de cada estacao


# Protocolo de acesso multiplo ao meio com deteccao de colisao
def csmaCd (station):
    cont = 0
    while cont <= MAX_LOOP:
        cont = cont + 1
        time.sleep (random.uniform(0.0,5.0)) # Tempo aleatorio simulando o preparo dos pacotes para envio

        print ['',"\nESTACAO %d - verificando cabo\n" % (station.id)][len(sys.argv) > 1 and (sys.argv[1] == '-d')],

        if freeCable(): # Verifica se cabo esta sendo usado

            print ['',"\nESTACAO %d - utilizando cabo \n" % (station.id)][len(sys.argv) > 1 and (sys.argv[1] == '-d')],

            transmit(station)   # Simula inicio de uma trasmissao, podendo ocorrer ou nao colisao
            if COLLISION[0]:    # Se existir colisao , entao e calculado o backoff
                COLLISION[0] = False
                CABLE[0] = True
                backOffTime(station)    # Calcula o tempo exponencial binario
        else:
            while  not freeCable(): # Aguarda cabo ser desocupado (espera ocupada, csma persistente)
                pass


def backOffTime (station):
    # Apos 10 tentativas o conjunto de tempos para espera nao cresce mais
    if station.transmissionAttempts <= 10:
        station.transmissionAttempts += 1
    timeMax = 2 ** station.transmissionAttempts

    print ['',"ESTACAO %d esperara de 0 a %d slots de tempo\n" % (station.id, timeMax)][len(sys.argv) > 1 and (sys.argv[1] == '-d')],
    timeWait = random.uniform(0.0,timeMax)

    print ['',"ESTACAO %d esperara %d slots na tentativa %d\n" % (station.id, timeWait, station.transmissionAttempts)][len(sys.argv) > 1 and (sys.argv[1] == '-d')],
    timeWait = timeWait * TIME_SLOT
    time.sleep(timeWait)

def transmit(station):

    CABLE[0] = False # Estacao "pega" cabo para ela
    print ['',"ESTACAO %d - iniciando transmissao \n" % (station.id)][len(sys.argv) > 1 and (sys.argv[1] == '-d')],

    causingCollision (station)  # Funcao que simula uma colisao

    randomNumPackets = random.randrange(1,MAX_PACKETS)  # Numero aleatorio de pacotes a serem enviados

    print ["","ESTACAO %d - enviara %d pacotes\n" % (station.id,randomNumPackets)][len(sys.argv) > 1 and (sys.argv[1] == '-d')],

    for i in range(randomNumPackets):
        print ["","\t- ESTACAO %d - enviando pacote %d \n" % (station.id, i+1)][len(sys.argv) > 1 and (sys.argv[1] == '-d')],
        time.sleep (TIME_SLOT)  # Delay do envio de cada quadro, ocupando tempo de um slot . Aqui e simulado o envio de um pacote de dados

        if collision(): # Simulacao da deteccao de colisoes, apos o envio de cada pacote
            print ["","\n< ;-( ESTACAO %d - detectou ### COLISAO ### \n" % (station.id)][len(sys.argv) > 1 and (sys.argv[1] == '-d')],
            station.fail += 1   # Se transmissao fallhou e contabilizado
            FAIL[station.id] = station.fail

            if len(sys.argv) != 1 and sys.argv[1] == '-r':
                printResul()

            return  # Se aconteceu colisao a transmissao e abortada

    CABLE[0] = True # Estacao terminou transferencia, entao libera o meio fisico

    print ["","\n< :-) ESTACAO %d - terminou transmissao com sucesso \n" % (station.id)][len(sys.argv) > 1 and (sys.argv[1] == '-d')],
    station.sucess += 1 # Se transmissao foi bem sucessedida e contabilizado
    SUCESS[station.id] = station.sucess

    if len(sys.argv) != 1 and sys.argv[1] == '-r':
        printResul()
    else:
        print "\nESTACAO %d transmitiu com SUCESSO " % (station.id)

    station.transmissionAttempts = 0

# Funcao para gerar ou nao uma colisao
def causingCollision (station):
    luck = random.randrange(1,99)
    if luck <= RATE_COLLISION:
        COLLISION[0] = True

# Detecta colisao
def collision():
    return COLLISION[0]

# Detecta se cabo esta livre
def freeCable():
    return CABLE[0]

# Impressao dos resultados
def printResul ():
    if len(sys.argv) != 1 and sys.argv[1] != '-d':
        os.system("clear")

    print "\n\n|      #  TRANSMISSOES  #     |"
    print "| ESTACAO | SUCESSOS | FALHAS |"
    print "+---------+----------+--------+"

    for i in range(MAX_STATION):
        print "|    %d    |    %d     |   %d    |" % (i, SUCESS[i], FAIL[i])
        print "+---------+----------+--------+"

# Impressao da ajuda
def help():
    print "Use a linha de comando :"
    print "    python csmaCd.py [-d] [-r] "
    print "Com parametros opcionais, que sao:"
    print "   -d , para modo debug"
    print "   -r , para modo de impressao dos resultados"
    print "   sem utilizar as ops, o programa seguira o enunciado"


# Classe que representa cada estacao
class Station(object):
    def __init__(self, id):
        self.id = id
        self.transmissionAttempts = 0
        self.sucess = 0
        self.fail = 0
        csmaCd(self)


def main():

    COLLISION[0] = False
    # Cabo e inicializado ocupado, seguindo o enunciado, simulando a transferencia de um quadro quando N estacoes estao prontas
    CABLE[0] = False
    stations = []

    if len(sys.argv) == 1 or (len(sys.argv) > 1 and (sys.argv[1] == '-d' or sys.argv[1] == '-r')):

        # Iniciolizando as Threads , onde cada thread e uma estacao concorrendo ao meio
        for i in range(MAX_STATION):
            station = threading.Thread(target = Station, args = (i,))
            stations.append(station)

        for station in stations:
            station.start()


        print ['' ,"Cabo inicia com transmissao de uma mensagem\n"][len(sys.argv) > 1 and (sys.argv[1] == '-d')],
        # Tempo da primeira mensagem no cabo
        time.sleep(3)

        print (['' ,"&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& CABO LIVRE &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\n"][len(sys.argv) > 1 and (sys.argv[1] == '-d')]),
        # Cabo agora esta livre, entao e setado para True
        CABLE[0] = True

        # Espera o termino das estacoes
        for station in stations:
            station.join()

        printResul()

    else:
        help()

if __name__ == '__main__':
    main()
