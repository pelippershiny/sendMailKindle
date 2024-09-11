import os
import subprocess
import json
import shutil
import re

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

# Comprobar si se ha proporcionado un archivo EPUB como parámetro
import sys
if len(sys.argv) < 2:
    print("ERROR: No se ha proporcionado la ruta al archivo EPUB.")
    exit(1)

# Ruta del archivo EPUB proporcionado
ORIGINAL_EPUB = sys.argv[1]
print(f"Ruta del archivo EPUB proporcionado: '{ORIGINAL_EPUB}'")

# Verificar que la ruta de Calibre sea correcta
print(f"Verificando la ruta de Calibre: '{calibre_path}'")
if not os.path.exists(os.path.join(calibre_path, "ebook-meta.exe")):
    print(f"ERROR: No se encontró Calibre en la ruta especificada: '{calibre_path}'")
    exit(1)

# Comprobar si el archivo EPUB existe
if not os.path.exists(ORIGINAL_EPUB):
    print(f"ERROR: El archivo EPUB no existe en la ruta especificada: '{ORIGINAL_EPUB}'")
    exit(1)

# Extraer los metadatos del archivo EPUB
print("Extrayendo metadatos del archivo EPUB...")
meta_command = [os.path.join(calibre_path, "ebook-meta.exe"), ORIGINAL_EPUB]
result = subprocess.run(meta_command, capture_output=True, text=True)
metadata = result.stdout

# Extraer título y autor del archivo EPUB (usando el campo 'Title', no 'Title sort')
title = None
author = None

for line in metadata.splitlines():
    if line.startswith("Title               :"):
        title = line.split(":", 1)[1].strip()
    elif line.startswith("Author(s)           :"):
        author = line.split(":", 1)[1].strip()

# Eliminar todo lo que está entre corchetes en el campo del autor
if author:
    author = re.sub(r'\[.*?\]', '', author).strip()

if not title or not author:
    print("ERROR: No se pudo extraer el título o el autor del archivo EPUB.")
    exit(1)

# Eliminar caracteres no válidos en el nombre del archivo
new_name = f"{author} - {title}.epub"
new_name = re.sub(r'[\/\\\:\*\?\"\<\>\|]', '_', new_name)
print(f"Nuevo nombre del archivo: '{new_name}'")

# Obtener la ruta y el directorio del archivo original
original_epub_dir = os.path.dirname(ORIGINAL_EPUB)
new_epub_path = os.path.join(original_epub_dir, new_name)

# Renombrar el archivo EPUB
shutil.move(ORIGINAL_EPUB, new_epub_path)
print(f"Archivo EPUB renombrado a: '{new_epub_path}'")

# Enviar el archivo por correo
print("Enviando el archivo EPUB por correo...")
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
    print("ERROR: No se pudo enviar el archivo por correo.")
    exit(1)

print("Operación completada con éxito.")
