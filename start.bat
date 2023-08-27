@echo off

REM Clear the terminal
cls

REM Activate the virtual environment (for Command Prompt)
call testvenv\Scripts\activate.bat

REM Run the Python script
python main.py