@echo off

REM Check if Python is installed
where python > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed.
    exit /b
)

echo Python installation checked!

REM Check if Node.js (npm/node) is installed
where node > nul 2>&1
if %errorlevel% neq 0 (
    echo Node.js is not installed.
    exit /b
)

echo Node.js installation checked!

REM Creating virtual environment for python
echo Creating virtual environment for python.
python -m venv venv

REM Activating the environment
call venv\Scripts\activate.bat

REM Installing packages
echo Installing python packages from requirements.txt.
pip install -r requirements.txt

REM Installing node packages
echo Installing node packages from package.json.
call npm install

echo Installation done!
echo You can now run start.bat to use the FlowCord tool!