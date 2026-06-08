import json
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gestor.scripts import (
    cargar_scripts, guardar_scripts,
    agregar_script, eliminar_script
)

def ver_scripts():
    scripts = cargar_scripts()
    if not scripts:
        print("\nNo hay scripts guardados.")
        return
    print("\n=== Scripts disponibles ===")
    for i, s in enumerate(scripts):
        print(f"{i+1}. {s['nombre']}")
        print(f"   Comando: {s['comando']}")
    print("===========================\n")

def anadir_script():
    print("\n=== Añadir script ===")
    nombre = input("Nombre del script: ").strip()
    if not nombre:
        print("El nombre no puede estar vacio.")
        return
    comando = input("Comando a ejecutar: ").strip()
    if not comando:
        print("El comando no puede estar vacio.")
        return
    agregar_script(nombre, comando)
    print(f"Script '{nombre}' añadido correctamente.")

def editar_script():
    scripts = cargar_scripts()
    if not scripts:
        print("\nNo hay scripts para editar.")
        return
    ver_scripts()
    try:
        indice = int(input("Numero de script a editar: ")) - 1
        if indice < 0 or indice >= len(scripts):
            print("Numero invalido.")
            return
    except ValueError:
        print("Introduce un numero valido.")
        return
    print(f"\nEditando: {scripts[indice]['nombre']}")
    nuevo_nombre = input(f"Nuevo nombre (Enter para mantener '{scripts[indice]['nombre']}'): ").strip()
    nuevo_comando = input(f"Nuevo comando (Enter para mantener '{scripts[indice]['comando']}'): ").strip()
    if nuevo_nombre:
        scripts[indice]['nombre'] = nuevo_nombre
    if nuevo_comando:
        scripts[indice]['comando'] = nuevo_comando
    guardar_scripts(scripts)
    print("Script actualizado correctamente.")

def eliminar_script_menu():
    scripts = cargar_scripts()
    if not scripts:
        print("\nNo hay scripts para eliminar.")
        return
    ver_scripts()
    try:
        indice = int(input("Numero de script a eliminar: ")) - 1
        if indice < 0 or indice >= len(scripts):
            print("Numero invalido.")
            return
    except ValueError:
        print("Introduce un numero valido.")
        return
    nombre = scripts[indice]['nombre']
    confirmar = input(f"Eliminar '{nombre}'? (s/n): ").strip().lower()
    if confirmar == 's':
        eliminar_script(indice)
        print(f"Script '{nombre}' eliminado correctamente.")
    else:
        print("Operacion cancelada.")

def menu():
    while True:
        print("\n=== Panel Control — Administrador ===")
        print("1. Ver scripts")
        print("2. Añadir script")
        print("3. Editar script")
        print("4. Eliminar script")
        print("5. Salir")
        opcion = input("Elige una opcion: ").strip()
        if opcion == '1':
            ver_scripts()
        elif opcion == '2':
            anadir_script()
        elif opcion == '3':
            editar_script()
        elif opcion == '4':
            eliminar_script_menu()
        elif opcion == '5':
            print("Saliendo del administrador.")
            break
        else:
            print("Opcion no valida.")

if __name__ == '__main__':
    menu()
