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
        print(f'Velocidade: {velocidade:.2f}km/h')
        tempo_inicio = 0

def botao_pedestre_callback(channel):
    print(f'Botão no pino {channel} pressionado.')

def enviar_estado_semaforo(pino_bits, codigo):
    for i in range(3):
        estado = (codigo >> i) & 1
        gpio.set_output(pino_bits[i], estado)
    
# Configuração de saídas dos Semáforos C1 e C2
for pin in config.SEMAFORO_C1 + config.SEMAFORO_C2:
    gpio.setup_output(pin)

# Configuração de entradas com interrupt para todos os botões
botoes_interrupt = [
    config.BOTOES['C1_P'],
    config.BOTOES['C1_T'],
    config.BOTOES['C2_P'],
    config.BOTOES['C2_T'],
]

for pin_botao in botoes_interrupt:
    gpio.setup_input_interrupt(pin_botao, botao_pedestre_callback)

gpio.setup_input_interrupt(config.SENSORES['S1']['A'], sensor_a_callback)
gpio.setup_input_interrupt(config.SENSORES['S1']['B'], sensor_b_callback)

gpio.setup_input_polling(config.BOTOES['C1_T'])
gpio.setup_input_polling(config.BOTOES['C1_P'])

try:
    print('Módulo GPIO ativo.')
    while True:
        for codigo_cor in range(8):
            enviar_estado_semaforo(config.SEMAFORO_C1, codigo_cor)
            enviar_estado_semaforo(config.SEMAFORO_C2, codigo_cor)
            time.sleep(3)
        # Exemplo de Polling
        if gpio.get_input(config.BOTOES['C1_T']):
            print('Polling: Botão de Travessia C1 pressionado.')
        if gpio.get_input(config.BOTOES['C1_P']):
            print('Polling: Botão de Pedestre Principal C1 pressionado.')
        if gpio.get_input(config.BOTOES['C2_T']):
            print('Polling: Botão de Travessia C2 pressionado.')
        if gpio.get_input(config.BOTOES['C2_P']):
            print('Polling: Botão de Pedestre Principal C1 pressionado.')

except KeyboardInterrupt:
    gpio.cleanup()