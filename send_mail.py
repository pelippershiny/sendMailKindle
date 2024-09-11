import os
import subprocess
import json
import sys

# Ruta al archivo de configuración
CONFIG_FILE = "config.json"

# Verificar si el archivo de configuración existe
if not os.path.exists(CONFIG_FILE):
    print(f"ERROR: No se encontró el archivo de configuración '{CONFIG_FILE}'.")
    exit(1)

# Cargar la configuración desde config.json
with open(CONFIG_FILE, 'r') as config_file:
    config = json.load(config_file)

smtp_server = config.get("smtp_server")
smtp_port = config.get("smtp_port")
smtp_username = config.get("smtp_username")
smtp_password = config.get("smtp_password")
from_email = config.get("from_email")
to_email = config.get("to_email")
calibre_path = config.get("calibre_path")

# Verificar que la ruta de Calibre esté presente en la configuración
if not calibre_path:
    print("ERROR: No se ha proporcionado la ruta de Calibre en el archivo de configuración.")
    exit(1)

# Comprobar si se ha proporcionado un archivo como parámetro
if len(sys.argv) < 2:
    print("ERROR: No se ha proporcionado la ruta al archivo.")
    exit(1)

# Ruta del archivo proporcionado
FILE_PATH = sys.argv[1]
print(f"Ruta del archivo proporcionado: '{FILE_PATH}'")

# Verificar que la ruta de Calibre sea correcta
print(f"Verificando la ruta de Calibre: '{calibre_path}'")
if not os.path.exists(os.path.join(calibre_path, "calibre-smtp.exe")):
    print(f"ERROR: No se encontró Calibre en la ruta especificada: '{calibre_path}'")
    exit(1)

# Comprobar si el archivo proporcionado existe
if not os.path.exists(FILE_PATH):
    print(f"ERROR: El archivo no existe en la ruta especificada: '{FILE_PATH}'")
    exit(1)

# Enviar el archivo por correo
print("Enviando el archivo por correo...")
smtp_command = [
    os.path.join(calibre_path, "calibre-smtp.exe"),
    from_email, to_email, "Aquí tienes tu archivo.",
    "--attachment", FILE_PATH,
    "--relay", smtp_server,
    "--port", str(smtp_port),
    "--username", smtp_username,
    "--password", smtp_password
]

email_result = subprocess.run(smtp_command)
if email_result.returncode != 0:
    print("ERROR: No se pudo enviar el archivo por correo.")
    exit(1)

print("Operación completada con éxito.")
