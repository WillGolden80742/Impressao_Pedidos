@echo off

echo Iniciando o ambiente de pedidos...

REM Verifica se o Python está instalado
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python nao encontrado. Por favor, instale o Python e adicione ao PATH.
    pause
    exit /b
)

REM Instala as dependências necessárias
echo Instalando dependencias...
pip install gspread google-auth pywin32 >nul

REM Executa o script Python
echo Iniciando o monitoramento de pedidos...
python service.py

pause
