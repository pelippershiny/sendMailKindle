# sendMailKindle
 
# Guía de Instalación y Uso

## Dependencias

1. **Calibre**
   - Es necesario tener Calibre instalado para la gestión de metadatos y el envío de archivos.
   - Descarga Calibre desde [este enlace](https://calibre-ebook.com/es/download_windows).
   - La ruta predeterminada de instalación es `C:\\Program Files\\Calibre2`. 
     - **Nota:** Si Calibre se instala en una ruta diferente, asegúrate de modificar el archivo `config.json` con la ruta correcta después de ejecutar `instalador.bat`.

2. **Cuenta de Correo Electrónico**
   - Necesitarás una cuenta de correo electrónico que permita el envío de archivos. 
   - Se recomienda utilizar [GMX](https://www.gmx.es).

3. **Python**
   - Python es necesario para ejecutar los scripts de Python. 
   - El archivo `instalador.bat` se encargará de instalar Python automáticamente, si no está ya instalado en tu sistema.

## Pasos

1. **Ejecutar `instalador.bat`**
   - Ejecuta `instalador.bat` para instalar Python y configurar el archivo `config.json`.
   - Aporta la información solicitada durante la ejecución del script.

2. **Arrastrar el Archivo**
   - Arrastra un archivo con extensión `.epub` o `.mobi` al archivo `run.bat` para procesarlo.
   - El archivo será renombrado (si es necesario) y enviado por correo.

3. **Esperar la Recepción en el Kindle**
   - Espera a que el archivo se muestre en tu dispositivo Kindle.

## Notas Adicionales

- Asegúrate de que el archivo `config.json` esté correctamente configurado con la información de tu cuenta de correo y la ruta de instalación de Calibre.
- Si encuentras problemas con el envío de correos, verifica la configuración de tu cuenta de correo y la ruta de Calibre en `config.json`.

Si tienes alguna pregunta o problema, no dudes en buscar ayuda en los foros de soporte de Calibre o en el servicio de soporte de tu proveedor de correo electrónico.

