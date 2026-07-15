@echo off
cd /d "%~dp0"

echo Enviando alteracoes para o GitHub...
git -c safe.directory="%CD%" add .
git -c safe.directory="%CD%" commit -m "fix: corrige deploy no Render" 2>nul
git -c safe.directory="%CD%" push origin main
if errorlevel 1 (
    echo.
    echo ERRO no push. Verifique login do GitHub e tente de novo.
    pause
    exit /b 1
)

echo.
echo Push OK! Abrindo o Render...
start https://dashboard.render.com
echo.
echo No Render:
echo 1. New ^> Blueprint (ou Web Service)
echo 2. Conecte o repositorio "vendas-de-projetos-arquitetura"
start https://github.com/leleostonks/vendas-de-projetos-arquitetura
echo 3. Start Command = streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
echo 4. Manual Deploy ^> Deploy latest commit
echo.
pause
