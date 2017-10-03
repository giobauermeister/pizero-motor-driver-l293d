from time import sleep
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import sys

#variaveis globais
Broker = "iot.eclipse.org"
PortaBroker = 1883
KeepAliveBroker = 60
TopicoSubscribe = "RaspZeroWRobo"  #No formato: "mcs/deviceId/deviceKey/dataChnId", onde dataChnId e referente ao data channel Controller

# definicao dos pinos
M1A = 31
M1B = 15
M1EN = 11
M2A = 18 
M2B = 13
M2EN = 29 

#Callback - conexao ao broker realizada
def on_connect(client, userdata, flags, rc):
    print("[STATUS] Conectado ao Broker.")
 
    #faz subscribe automatico no topico
    client.subscribe(TopicoSubscribe,0)
 
#Callback - mensagem recebida do broker
def on_message(client, userdata, msg):
 MensagemRecebida = str(msg.payload)
 print("[MSG RECEBIDA] Topico: "+msg.topic+" / Mensagem: "+MensagemRecebida)
 
 #verifica qual a movimentacao desejada
 #Frente (os dois motores no sentido horario):
 if (MensagemRecebida == "F"):
	GPIO.output(M1EN, GPIO.HIGH)
	GPIO.output(M2EN, GPIO.HIGH)
	GPIO.output(M1A, GPIO.HIGH)
	GPIO.output(M1B, GPIO.LOW)
	GPIO.output(M2A, GPIO.HIGH)
	GPIO.output(M2B, GPIO.LOW)
	return
 
 #Esquerda (Motor 1 no sentido horario e Motor 2 no sentido anti-horario):
 if (MensagemRecebida == "E"):
	GPIO.output(M1EN, GPIO.HIGH)
	GPIO.output(M2EN, GPIO.HIGH)
	GPIO.output(M1A, GPIO.HIGH)
	GPIO.output(M1B, GPIO.LOW)
	GPIO.output(M2A, GPIO.LOW)
	GPIO.output(M2B, GPIO.HIGH)
	return
 
 #Direita (Motor 2 no sentido horario e Motor 1 no sentido anti-horario):
 if (MensagemRecebida == "D"):
	GPIO.output(M1EN, GPIO.HIGH)
	GPIO.output(M2EN, GPIO.HIGH)
	GPIO.output(M1A, GPIO.LOW)
	GPIO.output(M1B, GPIO.HIGH)
	GPIO.output(M2A, GPIO.HIGH)
	GPIO.output(M2B, GPIO.LOW)
	return

 #Re (Motor 1 e 2 no sentido anti-horario):
 if (MensagemRecebida == "R"):
	GPIO.output(M1EN, GPIO.HIGH)
	GPIO.output(M2EN, GPIO.HIGH)
	GPIO.output(M1A, GPIO.LOW)
	GPIO.output(M1B, GPIO.HIGH)
	GPIO.output(M2A, GPIO.LOW)
	GPIO.output(M2B, GPIO.HIGH)
	return

 #Parado (Motor 1 e 2 parados):
 if (MensagemRecebida == "P"):
	GPIO.output(M1EN, GPIO.LOW)
	GPIO.output(M2EN, GPIO.LOW)
	return

	

#----------------------
#  Programa principal
#----------------------

# inicia a biblioteca RPi.GPIO usando numeracao do Header
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# configura os pinos do driver como saida
GPIO.setup(M1A, GPIO.OUT)
GPIO.setup(M2A, GPIO.OUT)

GPIO.setup(M1B, GPIO.OUT)
GPIO.setup(M2B, GPIO.OUT)

GPIO.setup(M1EN, GPIO.OUT)
GPIO.setup(M2EN, GPIO.OUT)

#inicializa motores como desligados
GPIO.output(M1EN, GPIO.HIGH)
GPIO.output(M2EN, GPIO.HIGH)
GPIO.output(M1A, GPIO.HIGH)
GPIO.output(M1B, GPIO.LOW)
GPIO.output(M1EN, GPIO.LOW)
GPIO.output(M2EN, GPIO.LOW)

try:
	print("[STATUS] Inicializando MQTT...")
 
        #inicializa MQTT:
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
 
        client.connect(Broker, PortaBroker, KeepAliveBroker)
        client.loop_forever()
except KeyboardInterrupt:
        print "\nCtrl+C pressionado, encerrando aplicacao e saindo..."
        sys.exit(0)

