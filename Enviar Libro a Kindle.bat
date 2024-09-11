@echo off
REM Abrir un cuadro de diálogo para seleccionar un archivo usando PowerShell
set "FILE_PATH="
for /f "delims=" %%i in ('powershell -command "& {Add-Type -AssemblyName System.Windows.Forms; $dialog = New-Object System.Windows.Forms.OpenFileDialog; $dialog.Filter = 'Todos los archivos (*.*)|*.*'; $dialog.ShowDialog() | Out-Null; $dialog.FileName}"') do set "FILE_PATH=%%i"

REM Verificar si se ha seleccionado un archivo
if "%FILE_PATH%"=="" (
    echo ERROR: No se ha seleccionado ningún archivo.
    exit /b 1
)

REM Obtener la extensión del archivo
set "FILE_EXT=%~x1"

REM Comprobar si la extensión es .epub
if /I not "%FILE_EXT%"==".epub" (
    REM Establecer la ruta al script de Python para archivos no EPUB
    set "SCRIPT_PATH=send_mail.py"
    
    REM Ejecutar el script de Python pasando el archivo como argumento
    python "%SCRIPT_PATH%" "%FILE_PATH%"
    
    REM Verificar si hubo algún error en la ejecución de Python
    if errorlevel 1 (
        echo ERROR: La ejecución del script de Python falló.
        exit /b 1
    )
    
    echo El script de Python se ejecutó correctamente.
    exit /b 0
)

REM Si la extensión es .epub, continuar con el script actual
REM Establecer la ruta al script de Python para archivos EPUB
set "SCRIPT_PATH=run.py"

REM Ejecutar el script de Python pasando el archivo EPUB como argumento
python "%SCRIPT_PATH%" "%FILE_PATH%"

REM Verificar si hubo algún error en la ejecución de Python
if errorlevel 1 (
    echo ERROR: La ejecución del script de Python falló.
    exit /b 1
)

echo El script de Python se ejecutó correctamente.
