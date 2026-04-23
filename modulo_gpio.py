# Módulo genérico pra ser usado no Sistema Central e nos Sistemas Distribuídos

import RPi.GPIO as GPIO
import time

class GPIO_handler():
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.instancias_pwm = {}

    def setup_output(self, pin):
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

    def setup_input_polling(self, pin):
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def setup_input_interrupt(self, pin, callback, bouncetime=300):
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        # Detecção da RISING_EDGE
        GPIO.add_event_detect(pin, GPIO.RISING, callback=callback, bouncetime=bouncetime)

    def set_output(self, pin, state):
        GPIO.output(pin, state)

    def get_input(self, pin):
        return GPIO.input(pin)
    
    def setup_pwm(self, pin, frequency=1000):
        GPIO.setup(pin, GPIO.OUT)
        pwm = GPIO.PWM(pin, frequency)
        pwm.start(0)
        self.instancias_pwm[pin] = pwm
        return pwm
    
    def set_pwm_duty_cycle(self, pin, duty_cycle):
        if pin in self.instancias_pwm:
            self.instancias_pwm[pin].ChangeDutyCycle(duty_cycle)

    def cleanup(self):
        GPIO.cleanup()
