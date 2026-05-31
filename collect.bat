@echo off
pushd "%~dp0%"

REM inicia sem console
start "" "%~dp0\venv\Scripts\pythonw.exe" -m src.main

exit
