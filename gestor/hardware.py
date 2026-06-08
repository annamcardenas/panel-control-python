from gpiozero import LED, TonalBuzzer, Button
import time
import threading

led_rojo = LED(5)
led_amarillo = LED(6)
led_verde = LED(13)

zumbador = TonalBuzzer(12)

pulsador = Button(17, pull_up=False, bounce_time=0.05)
joystick_sw = Button(19, pull_up=True, bounce_time=0.05)

def leds_apagar():
    led_rojo.off()
    led_amarillo.off()
    led_verde.off()

def led_exito():
    leds_apagar()
    led_verde.on()

def led_error():
    leds_apagar()
    led_rojo.on()

def led_ejecutando():
    leds_apagar()
    led_amarillo.on()

def _pitido(frecuencia, duracion):
    try:
        zumbador.stop()
        time.sleep(0.02)
        zumbador.play(frecuencia)
        time.sleep(duracion)
        zumbador.stop()
    except:
        try:
            zumbador.stop()
        except:
            pass

def pitido_corto():
    threading.Thread(target=_pitido, args=(440, 0.15), daemon=True).start()

def pitido_error():
    threading.Thread(target=_pitido, args=(220, 0.3), daemon=True).start()

def pitido_timeout():
    def _t():
        for _ in range(3):
            _pitido(880, 0.2)
            time.sleep(0.1)
    threading.Thread(target=_t, daemon=True).start()

def apagar_zumbador():
    try:
        zumbador.stop()
    except:
        pass
    try:
        from gpiozero import DigitalOutputDevice
        silencio = DigitalOutputDevice(12)
        silencio.off()
        silencio.close()
    except:
        pass
