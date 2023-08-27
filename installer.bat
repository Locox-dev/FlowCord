@echo off

REM Creating virtual environment for python
python -m venv venv

REM Activating the environment
call venv\Scripts\activate.bat

REM Installing packages
pip install -r requirements.txt