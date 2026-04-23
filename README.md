# Controle-Transito

Projeto de controle de trânsito com Raspberry Pi usando GPIO para:
- leitura de sensores de passagem;
- leitura de botões (principal e travessia);
- acionamento de saídas de semáforo;
- cálculo de velocidade por tempo entre sensores.

## Visão Geral

Até o momento, o projeto está dividido em três arquivos principais:
- `main.py`: ponto de entrada da aplicação, cadastro de callbacks e loop principal.
- `modulo_gpio.py`: abstração das operações de GPIO (entrada, saída, interrupção e PWM).
- `config.py`: mapeamento dos pinos BCM para semáforos, botões e sensores.

## Requisitos

- Raspberry Pi com GPIO disponível.
- Python 3.9+.
- Dependência Python:
	- `RPi.GPIO>=0.7.1`

## Instalação

1. Clone o repositório.
2. (Opcional) Crie e ative um ambiente virtual.
3. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Execução

Execute o programa principal:

```bash
python main.py
```

Em alguns ambientes Raspberry Pi, pode ser necessário executar com privilégios elevados:

```bash
sudo python main.py
```

Para interromper a execução, use `Ctrl + C`. O método `cleanup()` será chamado para liberar os pinos GPIO.

## Mapeamento de Pinos (BCM)

Definidos em `config.py`:

- Semáforos:
	- `SEMAFORO_C1 = [17, 18, 23]`
	- `SEMAFORO_C2 = [24, 8, 7]`
- Botões:
	- `C1_P = 1`
	- `C1_T = 12`
	- `C2_P = 25`
	- `C2_T = 22`
- Sensores:
	- `S1 = {A: 16, B: 20}`
	- `S2 = {A: 21, B: 27}`
	- `S3 = {A: 11, B: 0}`
	- `S4 = {A: 5, B: 6}`

## Funcionamento Atual

- Configura saídas do semáforo C1.
- Registra interrupções para:
	- sensor A (`S1.A`), marcando o tempo inicial;
	- sensor B (`S1.B`), calculando velocidade;
	- botão de pedestre principal (`C1_P`).
- No loop principal:
	- faz polling do botão de travessia (`C1_T`);
	- alterna o primeiro pino do semáforo C1 em intervalos de 1 segundo.