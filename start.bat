@echo off

REM Clear the terminal
cls

REM Activate the virtual environment (for Command Prompt)
call venv\Scripts\activate.bat

REM Display ASCII art using "type" command
type title.txt

REM Run the Python script
python main.py