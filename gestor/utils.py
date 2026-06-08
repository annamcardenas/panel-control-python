import os

def limpiar_pantalla():
    os.system('clear')

def formatear_nombre(nombre, max_chars=16):
    if len(nombre) > max_chars:
        return nombre[:max_chars-3] + '...'
    return nombre

def leer_log():
    if not os.path.exists('logs/historial.log'):
        return []
    with open('logs/historial.log', 'r') as f:
        return f.readlines()

def imprimir_log():
    lineas = leer_log()
    if not lineas:
        print("No hay registros todavia")
        return
    print("\n--- Historial de ejecuciones ---")
    for linea in lineas[-10:]:
        print(linea.strip())
    print("--------------------------------\n")
