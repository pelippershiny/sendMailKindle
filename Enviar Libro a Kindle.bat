@echo off
REM Abrir un cuadro de diálogo para seleccionar un archivo usando PowerShell
set "FILE_PATH="
for /f "delims=" %%i in ('powershell -command "& {Add-Type -AssemblyName System.Windows.Forms; $dialog = New-Object System.Windows.Forms.OpenFileDialog; $dialog.Filter = 'Todos los archivos (*.*)|*.*'; $dialog.ShowDialog() | Out-Null; $dialog.FileName}"') do set "FILE_PATH=%%i"

REM Verificar si se ha seleccionado un archivo
if "%FILE_PATH%"=="" (
    echo ERROR: No se ha seleccionado ningún archivo.
    exit /b 1
)

REM Mostrar la ruta del archivo seleccionado
echo Ruta del archivo seleccionado: %FILE_PATH%

REM Obtener la extensión del archivo
for %%x in ("%FILE_PATH%") do set "FILE_EXT=%%~xx"

REM Comprobar si la extensión es .epub
if /I "%FILE_EXT%"==".epub" (
    REM Si el archivo es EPUB, redirigir al script run.py
    echo Redirigiendo al script run.py
    set "SCRIPT_PATH=run.py"
) else (
    REM Si el archivo no es EPUB, redirigir al script send_mail.py
    echo Redirigiendo al script send_mail.py
    set "SCRIPT_PATH=send_mail.py"
)

REM Ejecutar el script de Python pasando el archivo como argumento
python "%SCRIPT_PATH%" "%FILE_PATH%"

REM Verificar si hubo algún error en la ejecución de Python
if errorlevel 1 (
    echo ERROR: La ejecución del script de Python falló.
    exit /b 1
)

echo El script de Python se ejecutó correctamente.
