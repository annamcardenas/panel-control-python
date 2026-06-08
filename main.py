import gestor
import time

indice_actual = 0
ejecutando = False

def siguiente_script():
    global indice_actual
    if ejecutando:
        return
    scripts = gestor.cargar_scripts()
    if not scripts:
        gestor.mostrar('Sin scripts', 'Añade scripts')
        return
    indice_actual = (indice_actual + 1) % len(scripts)
    nombre = gestor.formatear_nombre(scripts[indice_actual]['nombre'])
    gestor.mostrar_script(indice_actual, nombre)

def ejecutar_actual():
    global ejecutando
    if ejecutando:
        return
    ejecutando = True
    scripts = gestor.cargar_scripts()
    if not scripts:
        ejecutando = False
        return
    nombre = gestor.formatear_nombre(scripts[indice_actual]['nombre'])
    gestor.mostrar_ejecutando(nombre)
    gestor.led_ejecutando()
    gestor.apagar_zumbador()
    exito, resultado, salida = gestor.ejecutar_script(indice_actual)
    if exito:
        gestor.led_exito()
        if salida:
            gestor.mostrar(nombre, salida[:16])
        else:
            gestor.mostrar_exito(nombre)
        gestor.pitido_corto()
    else:
        gestor.led_error()
        gestor.mostrar_error(nombre)
        gestor.pitido_error()
    time.sleep(3)
    gestor.mostrar_script(indice_actual, nombre)
    gestor.leds_apagar()
    ejecutando = False

def iniciar():
    global indice_actual
    gestor.mostrar_bienvenida()
    time.sleep(2)
    scripts = gestor.cargar_scripts()
    if not scripts:
        gestor.mostrar('Sin scripts', 'Añade scripts')
        return
    nombre = gestor.formatear_nombre(scripts[indice_actual]['nombre'])
    gestor.mostrar_script(indice_actual, nombre)
    gestor.pulsador.when_pressed = ejecutar_actual
    gestor.joystick_sw.when_released = siguiente_script
    print("Panel Control iniciado")
    print("Pulsador = ejecutar script")
    print("Joystick = siguiente script")
    print("Ctrl+C para salir")
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        gestor.leds_apagar()
        gestor.apagar_zumbador()
        gestor.mostrar('Hasta luego', '')
        print("\nSaliendo...")

if __name__ == '__main__':
    iniciar()
