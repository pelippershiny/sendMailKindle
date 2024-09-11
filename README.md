# Enviar Libro a Kindle

## Dependencias

1. **Calibre**: Es necesario instalar Calibre desde [aquí](https://calibre-ebook.com/es/download_windows). Después de la instalación, revisa si la ruta de instalación es "C:\\Program Files\\Calibre2". Si es diferente, modifica el archivo `config.json` con la ruta correcta.
2. **Cuenta de Correo**: Necesitarás una cuenta de correo que permita enviar archivos. Se recomienda [gmx.es](https://www.gmx.es).
3. **Python**: Es necesario, pero será instalado automáticamente al ejecutar `instalador.bat`.

## Pasos

1. Ejecuta `instalador.bat` y proporciona la información solicitada para configurar el entorno.
2. Ejecuta `Enviar Libro a Kindle.bat`.
3. Selecciona el archivo `.epub` o `.mobi` que deseas enviar a tu Kindle.
4. Espera a que el archivo se envíe y se muestre en tu Kindle.

## Opcional: Hacer el Programa Más Accesible

Para hacer que el programa sea más accesible y ejecutable buscando su nombre en la búsqueda de Windows:

1. **Crear un Acceso Directo:**
   - Haz clic derecho sobre `Enviar Libro a Kindle.bat` y selecciona "Crear acceso directo".

2. **Mover el Acceso Directo al Menú de Inicio:**
   - Mueve o copia el acceso directo al siguiente directorio:
     ```plaintext
     %APPDATA%\Microsoft\Windows\Start Menu\Programs
     ```
   - Puedes acceder a este directorio abriendo el Explorador de archivos y pegando la ruta en la barra de direcciones o usando el comando `Run` (Win + R) y pegando la ruta.

## Notas

- Asegúrate de que todos los archivos necesarios (`send_mail.py`, `run.py`, `config.json`) estén en el mismo directorio que el archivo `.bat` para un funcionamiento correcto.
- Si encuentras problemas, verifica la configuración en `config.json` y asegúrate de que Calibre esté instalado en la ruta especificada.
