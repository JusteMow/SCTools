@echo off
REM Pull automatique SCTools + submodule tkshared

echo.
echo ======================================
echo   GIT PULL - SCTools + tkshared
echo ======================================
echo.

echo [1/3] Pull SCTools...
git pull origin main

echo.
echo [2/3] Update du submodule tkshared...
git submodule update --remote --merge _shared/tkshared

echo.
echo [3/3] Reinstallation du package tkshared...
pip install -e _shared/tkshared --quiet

echo.
echo ======================================
echo   TERMINE !
echo   Package tkshared mis a jour
echo ======================================
pause

