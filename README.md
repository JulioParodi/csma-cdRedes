# csma-cdRedes

Autor : Julio Cesar Pepplow Parodi
GRR : 20166160


1 - Como usar o programa ?
Para executar o programa execute o seguinte comando:
		python csmaCd.py [ ops ]
	Podendo utilizar duas opções, que são:
    Sem opções, o programa imprime as estações que conseguiram transmitir com sucesso e uma tabela de resultados finais, ao final da execução
		-d, modo debug , onde todas as ações de cada estação serão impressas na saída padrão
		-r , modo resultado, onde uma tabela dinâmica com os resultados das transmissões será impresso na saída padrão


2 - Implementação
	Devido as impressões dos resultados, o código fonte esta poluido , mas retirando-as , da principal função csmaCd() , podemos analisar melhor o protocolo :

def csmaCd (station):
        		if freeCable():
            		transmit(station)
           			 if COLLISION:
                			backOffTime(station)  
        			else:
            			while  not freeCable():
					pass

	Assim, percebe-se que o protocolo é bem simples. Contudo, foram retiradas variáveis essenciais para a análise, mas que para a simulação são indispensáveis.
	Procurei documentar o código para melhor entendimento do mesmo
