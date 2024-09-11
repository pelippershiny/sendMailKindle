@echo off
setlocal

:: Verificar si Python está instalado
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Python no está instalado. Instalando Python...
    :: Descargar el instalador de Python
    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe -OutFile python_installer.exe"

    :: Instalar Python
    python_installer.exe /quiet InstallAllUsers=1 PrependPath=1

    :: Limpiar el instalador
    del python_installer.exe
) else (
    echo Python ya está instalado.
)

:: Instalar dependencias
echo Instalando dependencias...
pip install --upgrade pip
pip install os subprocess json shutil re

:: Crear config.json
set /p smtp_server="Introduce el servidor SMTP (por ejemplo, mail.gmx.com): "
set /p smtp_port="Introduce el puerto SMTP (por ejemplo, 587): "
set /p smtp_username="Introduce el nombre de usuario SMTP (por ejemplo, usuario@gmx.es): "
set /p smtp_password="Introduce la contraseña SMTP: "
set /p to_email="Introduce la dirección de correo electrónico de destino (por ejemplo, USUARIO_67ASJP@KINDLE.COM): "

echo Creando config.json...
(
echo {
echo    "smtp_server": "%smtp_server%",
echo    "smtp_port": %smtp_port%,
echo    "smtp_username": "%smtp_username%",
echo    "smtp_password": "%smtp_password%",
echo    "from_email": "%smtp_username%",
echo    "to_email": "%to_email%",
echo    "calibre_path": "C:\\Program Files\\Calibre2"
echo }
) > config.json

echo Instalación completa.
endlocal
pause
