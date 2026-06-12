# Panel Control — Interfaz física para automatización de scripts

> Panel de control físico construido con Raspberry Pi 4 que permite ejecutar scripts de mantenimiento y administración del sistema mediante hardware físico, eliminando la necesidad de recordar comandos o abrir terminales.

---

## Descripción general

**Panel Control** es una aplicación Python que convierte una Raspberry Pi 4 en un panel de control autónomo. A través de un joystick, un pulsador y una pantalla LCD, el usuario puede navegar por una lista de scripts configurables y ejecutarlos con un solo botón.

El sistema responde visualmente mediante un módulo semáforo (LEDs rojo, amarillo y verde) y sonoramente mediante un zumbador pasivo, indicando en todo momento el estado de cada ejecución. Todos los eventos quedan registrados en un historial con fecha y hora.

**Caso de uso real:** Un programador o administrador de sistemas dispone de varios scripts de mantenimiento (backups, limpieza de logs, comprobación de red, monitorización del sistema). En lugar de abrir una terminal y recordar comandos, utiliza el panel físico para seleccionar y ejecutar cada tarea en segundos.

**Además, el panel cuenta con:**
- **Interfaz web** accesible desde cualquier navegador
- **Notificaciones por Telegram** al ejecutar scripts
- **API REST** para integración con otros sistemas

---

## Objetivos del proyecto

- Aplicar el uso de **librerías externas** instaladas con `pip`
- Organizar el código en **módulos y paquetes** Python
- Implementar **operaciones CRUD** sobre ficheros JSON
- Gestionar **errores y excepciones** de forma robusta
- Desarrollar una aplicación **funcional e interactiva**
- Integrar **hardware físico** con software Python

---

## Hardware utilizado

| Componente | Función | Pines GPIO |
|------------|---------|------------|
| Raspberry Pi 4 Model B 4GB | Unidad central de procesamiento | — |
| Pantalla LCD I2C 1602 | Muestra el menú y resultados | SDA (Pin 3), SCL (Pin 5) |
| Módulo semáforo (R/Y/G) | Indica el estado de ejecución | GPIO 5, 6, 13 |
| Pulsador digital | Ejecuta el script seleccionado | GPIO 17 (Pin 11) |
| Módulo joystick (SW) | Navega entre scripts | GPIO 19 (Pin 35) |
| Zumbador pasivo | Confirmación sonora | GPIO 12 (Pin 32) |

### Diagrama de conexiones

```
Raspberry Pi 4 — Pines utilizados
─────────────────────────────────
Pin 1  (3.3V)  → Joystick VCC
Pin 2  (5V)    → Zumbador VCC
Pin 3  (SDA)   → LCD SDA
Pin 4  (5V)    → LCD VCC
Pin 5  (SCL)   → LCD SCL
Pin 6  (GND)   → LCD GND
Pin 11 (GPIO17)→ Pulsador Signal
Pin 14 (GND)   → Pulsador GND
Pin 17 (3.3V)  → Pulsador VCC
Pin 20 (GND)   → Semáforo GND
Pin 25 (GND)   → Joystick GND
Pin 29 (GPIO5) → Semáforo Rojo
Pin 30 (GND)   → Zumbador GND
Pin 31 (GPIO6) → Semáforo Amarillo
Pin 32 (GPIO12)→ Zumbador Signal
Pin 33 (GPIO13)→ Semáforo Verde
Pin 35 (GPIO19)→ Joystick SW
```

---

## Librerías externas utilizadas

| Librería | Versión | Instalación | Uso |
|----------|---------|-------------|-----|
| `gpiozero` | 2.0.1 | `pip install gpiozero` | Control de LEDs, botones y zumbador |
| `lgpio` | 0.2.2 | `pip install lgpio` | Backend GPIO para Raspberry Pi 4 |
| `RPLCD` | 1.4.0 | `pip install RPLCD` | Control de pantalla LCD I2C |
| `smbus2` | 0.6.1 | `pip install smbus2` | Comunicación I2C |
| `flask` | 3.1.3 | `pip install flask` | API REST e interfaz web |
| `requests` | 2.34.2 | `pip install requests` | Notificaciones Telegram |
| `python-dotenv` | 1.2.2 | `pip install python-dotenv` | Cargar variables de entorno |

---

## Estructura del proyecto

```
panel_control/
│── main.py               # Punto de entrada — bucle principal del panel
│── admin.py              # Interfaz de administración CRUD por terminal
│── scripts.json          # Base de datos de scripts configurables
│── .gitignore            # Exclusiones de Git
│── README.md             # Documentación del proyecto
│── gestor/               # Paquete principal
│   │── __init__.py       # Centraliza importaciones del paquete
│   │── hardware.py       # Control de LEDs, botones y zumbador
│   │── display.py        # Control de la pantalla LCD I2C
│   │── scripts.py        # Lógica CRUD y ejecución de scripts
│   │── utils.py          # Funciones auxiliares y gestión de logs
│── logs/
│   └── historial.log     # Registro de ejecuciones con fecha y hora
```

---

## Módulos estándar de Python utilizados

| Módulo | Uso en el proyecto |
|--------|-------------------|
| `os` | Comprobación de existencia de ficheros y creación de directorios |
| `json` | Lectura y escritura del fichero `scripts.json` |
| `subprocess` | Ejecución de scripts del sistema operativo |
| `datetime` | Registro de fecha y hora en el historial de logs |
| `threading` | Gestión del zumbador en hilos separados para evitar bloqueos |
| `time` | Pausas y control de tiempos de ejecución |

---

## Instalación

### Requisitos previos
- Raspberry Pi 4 con Raspberry Pi OS 64-bit (Bookworm)
- I2C activado (`sudo raspi-config` → Interface Options → I2C)
- Dependencias del sistema:

```bash
sudo apt install swig liblgpio-dev -y
```

### Instalación del proyecto

```bash
# Clonar el repositorio
git clone https://github.com/annamcardenas/panel-control-python.git
cd panel-control-python

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install gpiozero lgpio RPLCD smbus2
```

---

## Ejecución

### Panel físico (manual)
```bash
cd panel_control
source venv/bin/activate
python3 main.py
```

### Panel físico (arranque automático al encender la Pi)
El servicio systemd se activa automáticamente. Para gestionarlo:

```bash
# Ver estado
sudo systemctl status panel_control.service

# Iniciar
sudo systemctl start panel_control.service

# Detener
sudo systemctl stop panel_control.service
```

### Administrador de scripts (CRUD)
```bash
python3 admin.py
```

---

## Uso del panel

| Acción | Hardware |
|--------|----------|
| Navegar al siguiente script | Joystick (presionar) |
| Ejecutar script seleccionado | Pulsador digital |
| Script en ejecución | LED amarillo encendido |
| Ejecución exitosa | LED verde + pitido corto |
| Error en ejecución | LED rojo + pitido largo |

---

## Scripts incluidos

| Script | Descripción | Resultado en LCD |
|--------|-------------|-----------------|
| Temperatura CPU | Temperatura del procesador | `45.3'C` |
| Estado WiFi | Comprueba conexión a internet | `WiFi: OK` / `WiFi: KO` |
| Uso disco | Espacio utilizado en disco | `23% de 29G` |
| Memoria RAM | Uso de memoria RAM | `512M/4.0G` |
| Backup logs | Copia de seguridad de logs | `Backup OK` |
| Limpiar logs | Vacía el historial | `Logs: Borrados` |
| Push GitHub | Sube el historial a GitHub | `Push: OK` |
| Test error | Script que falla intencionadamente | LED rojo |
| Mostrar IP | Muestra la IP de la Raspberry | `192.168.1.136` |

---

## CRUD de scripts

El archivo `scripts.json` almacena la configuración de todos los scripts. Se puede gestionar mediante el administrador interactivo:

```bash
python3 admin.py
```

```
=== Panel Control — Administrador ===
1. Ver scripts
2. Añadir script
3. Editar script
4. Eliminar script
5. Salir
```

Ejemplo de `scripts.json`:
```json
[
    {
        "nombre": "Temperatura CPU",
        "comando": "vcgencmd measure_temp | cut -d'=' -f2"
    }
]
```

---

## 📊 Historial de ejecuciones

Cada ejecución queda registrada en `logs/historial.log`:

```
2026-06-08 14:30:15 | OK    | Temperatura CPU | 0s
2026-06-08 14:30:22 | OK    | Estado WiFi     | 1s
2026-06-08 14:30:35 | ERROR | Test error      | 0s
```

---

## 🔄 Integración con GitHub

El script **Push GitHub** realiza automáticamente un commit y push del historial de ejecuciones al repositorio, permitiendo llevar un registro remoto de todas las tareas ejecutadas desde el panel.

```bash
git add logs/historial.log
git commit -m "Update logs 2026-06-08_14:37"
git push
```
---

## API REST y control remoto

El panel incluye una **API REST** que permite controlar todos los scripts desde cualquier dispositivo en la misma red.

### Endpoints disponibles

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Interfaz web interactiva |
| `/api/status` | GET | Lista todos los scripts disponibles |
| `/api/ejecutar/<id>` | GET | Ejecuta un script por su ID |
| `/api/logs` | GET | Últimas 20 ejecuciones |

### Ejemplo de uso

```bash
# Ver estado del panel
curl http://192.168.1.136:5000/api/status

# Ejecutar script (Temperatura CPU)
curl http://192.168.1.136:5000/api/ejecutar/0

# Ver logs
curl http://192.168.1.136:5000/api/logs
```

---

## Arranque automático

El proyecto se configura como servicio systemd para arrancar automáticamente al encender la Raspberry Pi, sin necesidad de teclado, ratón ni monitor.

```ini
[Unit]
Description=Panel Control
After=network.target

[Service]
ExecStart=/home/pi/panel_control/venv/bin/python3 /home/pi/panel_control/main.py
WorkingDirectory=/home/pi/panel_control
Restart=on-failure
User=pi

[Install]
WantedBy=multi-user.target
```

---

## Notificaciones Telegram

Cada vez que se ejecuta un script (desde el panel físico, la web o la API), el sistema envía una notificación a Telegram con el resultado.

### Configuración

1. Crea un bot en Telegram con [@BotFather](https://t.me/BotFather)
2. Obtén tu `CHAT_ID` con [@userinfobot](https://t.me/userinfobot)
3. Crea un archivo `.env` en la raíz del proyecto:

```bash
TELEGRAM_TOKEN=tu_token_aqui
TELEGRAM_CHAT_ID=tu_chat_id_aqui
```

---

## Autora

**Ana María Cárdenas Nevado**
Proyecto desarrollado como actividad evaluable de la asignatura de Python.
Repositorio: [github.com/annamcardenas/panel-control-python](https://github.com/annamcardenas/panel-control-python)
