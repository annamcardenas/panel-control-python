import gestor
import time
import threading
from api import iniciar_api
from gestor.notificaciones import enviar_mensaje

indice_actual = 0
ejecutando = False

def mostrar_ip_en_lcd():
    import subprocess
    import re
    # Intentar obtener IP de la interfaz eth0 (cable) o wlan0 (WiFi)
    ip = None
    for interfaz in ['eth0', 'wlan0']:
        result = subprocess.run(['ip', '-4', 'addr', 'show', interfaz], capture_output=True, text=True)
        match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', result.stdout)
        if match:
            ip = match.group(1)
            break
    if not ip:
        ip = "Sin IP"
    # Mostrar en LCD
    gestor.mostrar("Mi IP es:", ip)
    time.sleep(5)  # 5 segundos para leerla

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

def _notificar(nombre, exito, salida):
    if exito:
        if 'GitHub' in nombre:
            enviar_mensaje(f'Push a GitHub\n*{nombre}*: {salida}')
        else:
            enviar_mensaje(f'OK *{nombre}*: {salida}')
    else:
        enviar_mensaje(f'ERROR *{nombre}*')

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
    threading.Thread(target=_notificar, args=(nombre, exito, salida), daemon=True).start()
    time.sleep(3)
    gestor.mostrar_script(indice_actual, nombre)
    gestor.leds_apagar()
    ejecutando = False

def ejecutar_desde_api(indice):
    global ejecutando
    if ejecutando:
        return {'error': 'Panel ocupado'}
    ejecutando = True
    scripts = gestor.cargar_scripts()
    if not scripts or indice >= len(scripts):
        ejecutando = False
        return {'error': 'Script no encontrado'}
    nombre = gestor.formatear_nombre(scripts[indice]['nombre'])
    gestor.mostrar_ejecutando(nombre)
    gestor.led_ejecutando()
    exito, resultado, salida = gestor.ejecutar_script(indice)
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
    threading.Thread(target=_notificar, args=(nombre, exito, salida), daemon=True).start()
    time.sleep(2)
    gestor.mostrar_script(indice, nombre)
    gestor.leds_apagar()
    ejecutando = False
    return {'exito': exito, 'resultado': salida, 'script': nombre}

def iniciar():
    global indice_actual
    gestor.mostrar_bienvenida()
    time.sleep(2)
    mostrar_ip_en_lcd()
    time.sleep(10)
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
    hilo_api = threading.Thread(target=iniciar_api, daemon=True)
    hilo_api.start()
    print("API REST iniciada en puerto 5000")
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
