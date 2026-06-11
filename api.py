from flask import Flask, jsonify
from gestor.scripts import cargar_scripts, ejecutar_script
from gestor.utils import leer_log

app = Flask(__name__)

@app.route('/')
def index():
    scripts = cargar_scripts()
    botones = ''
    for i, s in enumerate(scripts):
        botones += f'''
        <div class="script">
            <span>{s["nombre"]}</span>
            <button onclick="ejecutar({i})">▶ Ejecutar</button>
        </div>'''

    return f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Panel Control</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: monospace; background: #0d1117; color: #c9d1d9; padding: 20px; }}
        h1 {{ color: #58a6ff; margin-bottom: 5px; }}
        p {{ color: #8b949e; margin-bottom: 20px; font-size: 13px; }}
        .script {{ display: flex; justify-content: space-between; align-items: center;
                   background: #161b22; border: 1px solid #30363d; border-radius: 8px;
                   padding: 12px 16px; margin-bottom: 10px; }}
        button {{ background: #238636; color: white; border: none; padding: 8px 16px;
                  border-radius: 6px; cursor: pointer; font-family: monospace; font-size: 14px; }}
        button:hover {{ background: #2ea043; }}
        button:disabled {{ background: #3a3a3a; cursor: not-allowed; }}
        #resultado {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px;
                      padding: 16px; margin-top: 20px; min-height: 60px; }}
        .ok {{ color: #3fb950; }}
        .error {{ color: #f85149; }}
        h2 {{ color: #58a6ff; margin: 20px 0 10px; }}
        #logs {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px;
                 padding: 16px; font-size: 12px; max-height: 200px; overflow-y: auto; }}
        .log-ok {{ color: #3fb950; }}
        .log-error {{ color: #f85149; }}
    </style>
</head>
<body>
    <h1> Panel Control</h1>
    <p>Raspberry Pi 4 — Control remoto de scripts</p>
    {botones}
    <div id="resultado">Selecciona un script para ejecutar...</div>
    <h2> Últimas ejecuciones</h2>
    <div id="logs">Cargando...</div>

    <script>
        function ejecutar(id) {{
            const div = document.getElementById('resultado');
            div.innerHTML = 'Ejecutando...';
            div.className = '';
            document.querySelectorAll('button').forEach(b => b.disabled = true);
            fetch('/api/ejecutar/' + id)
                .then(r => r.json())
                .then(data => {{
                    if (data.exito) {{
                        div.innerHTML = '✅ <b>' + data.script + '</b>: ' + (data.resultado || 'OK');
                        div.className = 'ok';
                    }} else {{
                        div.innerHTML = '❌ <b>' + data.script + '</b>: Error';
                        div.className = 'error';
                    }}
                    cargarLogs();
                }})
                .catch(() => {{ div.innerHTML = '❌ Error de conexión'; }})
                .finally(() => {{ document.querySelectorAll('button').forEach(b => b.disabled = false); }});
        }}

        function cargarLogs() {{
            fetch('/api/logs')
                .then(r => r.json())
                .then(data => {{
                    const div = document.getElementById('logs');
                    div.innerHTML = data.logs.reverse().map(l =>
                        '<div class="' + (l.includes('ERROR') ? 'log-error' : 'log-ok') + '">' + l + '</div>'
                    ).join('');
                }});
        }}

        cargarLogs();
        setInterval(cargarLogs, 10000);
    </script>
</body>
</html>'''


@app.route('/api/status', methods=['GET'])
def status():
    scripts = cargar_scripts()
    lista = [{'id': i, 'nombre': s['nombre']} for i, s in enumerate(scripts)]
    return jsonify({'status': 'online', 'scripts': lista})

@app.route('/api/ejecutar/<int:indice>', methods=['GET'])
def ejecutar(indice):
    from main import ejecutar_desde_api
    resultado = ejecutar_desde_api(indice)
    if 'error' in resultado:
        return jsonify(resultado), 400
    return jsonify(resultado)

@app.route('/api/logs', methods=['GET'])
def logs():
    lineas = leer_log()
    return jsonify({'logs': [l.strip() for l in lineas[-20:]]})

def iniciar_api():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
