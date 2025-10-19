import subprocess
import webbrowser
import os
import time
import sys

# Caminho do diretório onde está o exe/run_app.py
base_path = os.path.dirname(os.path.abspath(__file__))

# Caminho do app.py
app_path = os.path.join(base_path, "./app.py")

# Verifica se app.py existe
if not os.path.exists(app_path):
    print(f"ERRO: app.py não encontrado em: {app_path}")
    sys.exit(1)

# Comando para rodar o Streamlit
cmd = [sys.executable, "-m", "streamlit", "run", app_path]

# Inicia o Streamlit (terminal visível)
subprocess.Popen(cmd)

# Espera o servidor iniciar
time.sleep(3)

# Abre o navegador apenas uma vez
webbrowser.open("http://localhost:8501")
