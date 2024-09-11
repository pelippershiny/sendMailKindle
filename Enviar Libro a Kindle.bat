@echo off
REM Guardar la ruta del directorio actual
set "CURRENT_DIR=%~dp0"

REM Abrir un cuadro de diálogo para seleccionar varios archivos usando PowerShell
set "FILE_PATHS="
for /f "delims=" %%i in ('powershell -command "& {Add-Type -AssemblyName System.Windows.Forms; $dialog = New-Object System.Windows.Forms.OpenFileDialog; $dialog.Filter = 'Todos los archivos (*.*)|*.*'; $dialog.Multiselect = $true; $dialog.ShowDialog() | Out-Null; $dialog.FileNames -join ';'}"') do set "FILE_PATHS=%%i"

REM Verificar si se han seleccionado archivos
if "%FILE_PATHS%"=="" (
    echo ERROR: No se ha seleccionado ningún archivo.
    exit /b 1
)

REM Procesar cada archivo seleccionado
for %%F in ("%FILE_PATHS:;=" "%") do (
    REM Mostrar la ruta del archivo seleccionado
    echo Procesando archivo: %%~F

    REM Obtener la extensión del archivo sin comillas adicionales
    for %%x in (%%~F) do set "FILE_EXT=%%~xx"

    REM Mostrar la extensión del archivo
    echo La extensión del archivo es: %FILE_EXT%

    REM Comprobar si la extensión es .epub
    if /I "%FILE_EXT%"==".epub" (
        REM Si el archivo es EPUB, redirigir al script run.py
        echo Redirigiendo al script run.py
        set "SCRIPT_PATH=%CURRENT_DIR%run.py"
    ) else (
        REM Si el archivo no es EPUB, redirigir al script send_mail.py
        echo Redirigiendo al script send_mail.py
        set "SCRIPT_PATH=%CURRENT_DIR%send_mail.py"
    )

    REM Ejecutar el script de Python pasando el archivo como argumento
    python "%SCRIPT_PATH%" "%%~F"

    REM Verificar si hubo algún error en la ejecución de Python
    if errorlevel 1 (
        echo ERROR: La ejecución del script de Python falló para el archivo %%~F.
        exit /b 1
    )

    echo El script de Python se ejecutó correctamente para el archivo %%~F.
)

echo Todos los archivos han sido procesados.
