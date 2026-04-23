from modulo_gpio import GPIO_handler
import config
import time

gpio = GPIO_handler()

tempo_inicio = 0

def sensor_a_callback(channel):
    global tempo_inicio
    tempo_inicio = time.time()

def sensor_b_callback(channel):
    global tempo_inicio
    if tempo_inicio != 0:
        delta_t = time.time() - tempo_inicio
        # velocidade = (d/dt)*3.6
        velocidade = (2.0/delta_t) * 3.6
        print('Velocidade: {velocidade.2f}km/h')
        tempo_inicio = 0

def botao_pedestre_callback(channel):
    print('Botão no pino {channel} pressionado.')
    
# Configuração de saídas do Semáforo C1
for pin in config.SEMAFORO_C1:
    gpio.setup_output(pin)

# Configuração de entradas com interrupt (Ex: Sensor 1 e Botão 1)
gpio.setup_input_interrupt(config.SENSORES['S1']['A'], sensor_a_callback)
gpio.setup_input_interrupt(config.SENSORES['S1']['B'], sensor_b_callback)
gpio.setup_input_interrupt(config.BOTOES['C1_P'], botao_pedestre_callback)

try:
    print('Módulo GPIO ativo.')
    while True:
        # Exemplo de Polling
        if gpio.get_input(config.BOTOES['C1_T']):
            print('Polling: Botão de Travessia C1 pressionado.')
        # Exemplo de saída
        gpio.set_output(config.SEMAFORO_C1[0], True)
        time.sleep(1)
        gpio.set_output(config.SEMAFORO_C1[0], False)
        time.sleep(1)
        
except KeyboardInterrupt:
    gpio.cleanup()