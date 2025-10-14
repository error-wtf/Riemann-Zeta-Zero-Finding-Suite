@echo off
setlocal
REM Launch PowerShell driver next to this .bat
set SCRIPT_DIR=%~dp0
powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%rieman-zeta-zero.ps1"
endlocal
