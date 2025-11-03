@echo off
REM Push automatique SCTools + submodule tkshared

echo.
echo ======================================
echo   GIT PUSH - SCTools + tkshared
echo ======================================
echo.

REM Vérifier si des changements dans le submodule
cd _shared\tkshared
git status
echo.

set /p push_submodule="Push le submodule tkshared ? (o/n) : "
if /i "%push_submodule%"=="o" (
    echo.
    echo [1/4] Push du submodule tkshared...
    git add .
    git commit -m "Update tkshared"
    git push origin main
    echo [OK] Submodule tkshared pushe
) else (
    echo [SKIP] Submodule non pushe
)

REM Retour à la racine SCTools
cd ..\..

echo.
echo [2/4] Ajout des changements SCTools...
git add .

echo.
set /p commit_msg="Message de commit : "
if "%commit_msg%"=="" set commit_msg=Update

echo.
echo [3/4] Commit SCTools...
git commit -m "%commit_msg%"

echo.
echo [4/4] Push SCTools...
git push origin main

echo.
echo ======================================
echo   TERMINE !
echo ======================================
pause

