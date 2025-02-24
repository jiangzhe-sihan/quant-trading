@echo off
if not "%minimized%"=="" goto :minimized
set minimized=true
start /min cmd /c %0
goto :eof
:minimized
cd .\src
python main.py