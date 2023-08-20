@echo off

REM Creating virtual environment for python
python3.11 -m venv venv

REM Activating the environment
call venv\Scripts\activate.bat

REM Installing packages
pip install windows-curses