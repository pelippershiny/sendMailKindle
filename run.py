import os
import subprocess
import json
import shutil
import re
import sys

# Ruta al archivo de configuración
CONFIG_FILE = "config.json"
LOG_FILE = "log.txt"

def log_message(message):
    """Escribe un mensaje en el archivo de registro y en la consola."""
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(message + '\n')
    print(message)

# Verificar si el archivo de configuración existe
if not os.path.exists(CONFIG_FILE):
    log_message(f"ERROR: No se encontró el archivo de configuración '{CONFIG_FILE}'.")
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
    log_message("ERROR: No se ha proporcionado la ruta de Calibre en el archivo de configuración.")
    exit(1)

# Comprobar si se ha proporcionado un archivo EPUB como parámetro
if len(sys.argv) < 2:
    log_message("ERROR: No se ha proporcionado la ruta al archivo EPUB.")
    exit(1)

# Ruta del archivo EPUB proporcionado
ORIGINAL_EPUB = sys.argv[1]
log_message(f"Ruta del archivo EPUB proporcionado: '{ORIGINAL_EPUB}'")

# Verificar que la ruta de Calibre sea correcta
log_message(f"Verificando la ruta de Calibre: '{calibre_path}'")
if not os.path.exists(os.path.join(calibre_path, "ebook-meta.exe")):
    log_message(f"ERROR: No se encontró Calibre en la ruta especificada: '{calibre_path}'")
    exit(1)

# Comprobar si el archivo EPUB existe
if not os.path.exists(ORIGINAL_EPUB):
    log_message(f"ERROR: El archivo EPUB no existe en la ruta especificada: '{ORIGINAL_EPUB}'")
    exit(1)

# Extraer los metadatos del archivo EPUB
log_message("Extrayendo metadatos del archivo EPUB...")
meta_command = [os.path.join(calibre_path, "ebook-meta.exe"), ORIGINAL_EPUB]
result = subprocess.run(meta_command, capture_output=True, text=True, encoding='utf-8')

# Verificar si hubo un error en la ejecución del comando
if result.returncode != 0:
    log_message(f"ERROR: El comando 'ebook-meta.exe' falló con el código de retorno {result.returncode}.")
    log_message(f"Salida de error: {result.stderr}")
    exit(1)

metadata = result.stdout

# Imprimir todos los metadatos
print("Metadatos del archivo EPUB:")
print(metadata)

# Extraer título del archivo EPUB
title = None

if metadata:
    for line in metadata.splitlines():
        if line.startswith("Title               :"):
            title = line.split(":", 1)[1].strip()

# Verificar que se haya extraído el título
if not title:
    log_message("ERROR: No se pudo extraer el título del archivo EPUB.")
    exit(1)

# Eliminar caracteres no válidos en el nombre del archivo
new_name = f"{title}.epub"
new_name = re.sub(r'[\/\\\:\*\?\"\<\>\|]', '_', new_name)
log_message(f"Nuevo nombre del archivo: '{new_name}'")

# Obtener la ruta y el directorio del archivo original
original_epub_dir = os.path.dirname(ORIGINAL_EPUB)
new_epub_path = os.path.join(original_epub_dir, new_name)

# Renombrar el archivo EPUB
shutil.move(ORIGINAL_EPUB, new_epub_path)
log_message(f"Archivo EPUB renombrado a: '{new_epub_path}'")

# Enviar el archivo por correo
log_message("Enviando el archivo EPUB por correo...")
smtp_command = [
    os.path.join(calibre_path, "calibre-smtp.exe"),
    from_email, to_email, "Aquí tienes tu archivo en formato EPUB.",
    "--attachment", new_epub_path,
    "--relay", smtp_server,
    "--port", str(smtp_port),
    "--username", smtp_username,
    "--password", smtp_password
]

email_result = subprocess.run(smtp_command)
if email_result.returncode != 0:
    log_message("ERROR: No se pudo enviar el archivo por correo.")
    exit(1)

log_message("Operación completada con éxito.")
