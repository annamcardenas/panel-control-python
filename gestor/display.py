from RPLCD.i2c import CharLCD

lcd = CharLCD('PCF8574', 0x27)

def limpiar():
    lcd.clear()

def mostrar(linea1, linea2=''):
    lcd.clear()
    lcd.write_string(linea1[:16])
    if linea2:
        lcd.crlf()
        lcd.write_string(linea2[:16])

def mostrar_bienvenida():
    mostrar('Panel Control', 'Iniciando...')

def mostrar_script(indice, nombre):
    mostrar(f'> {nombre}'[:16], f'Script {indice+1}')

def mostrar_ejecutando(nombre):
    mostrar('Ejecutando...', nombre[:16])

def mostrar_exito(nombre):
    mostrar('OK', nombre[:16])

def mostrar_error(nombre):
    mostrar('ERROR', nombre[:16])
