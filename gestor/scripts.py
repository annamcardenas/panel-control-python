import json
import os
import subprocess
import datetime

ARCHIVO = 'scripts.json'

def cargar_scripts():
    if not os.path.exists(ARCHIVO):
        return []
    with open(ARCHIVO, 'r') as f:
        return json.load(f)

def guardar_scripts(scripts):
    with open(ARCHIVO, 'w') as f:
        json.dump(scripts, f, indent=4)

def agregar_script(nombre, comando):
    scripts = cargar_scripts()
    scripts.append({'nombre': nombre, 'comando': comando})
    guardar_scripts(scripts)

def eliminar_script(indice):
    scripts = cargar_scripts()
    if 0 <= indice < len(scripts):
        scripts.pop(indice)
        guardar_scripts(scripts)

def ejecutar_script(indice):
    scripts = cargar_scripts()
    if not scripts or indice >= len(scripts):
        return False, 'Sin scripts', ''
    script = scripts[indice]
    try:
        inicio = datetime.datetime.now()
        resultado = subprocess.run(
            script['comando'],
            shell=True,
            timeout=30,
            capture_output=True,
            text=True
        )
        fin = datetime.datetime.now()
        duracion = (fin - inicio).seconds
        exito = resultado.returncode == 0
        salida = resultado.stdout.strip()
        guardar_log(script['nombre'], exito, duracion)
        return exito, script['nombre'], salida
    except subprocess.TimeoutExpired:
        guardar_log(script['nombre'], False, 30)
        return False, 'Timeout', ''

def guardar_log(nombre, exito, duracion):
    os.makedirs('logs', exist_ok=True)
    with open('logs/historial.log', 'a') as f:
        fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        estado = 'OK' if exito else 'ERROR'
        f.write(f'{fecha} | {estado} | {nombre} | {duracion}s\n')
