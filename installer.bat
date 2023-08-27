@echo off

REM Creating virtual environment for python
echo Creating virtual environment for python
python -m venv venv

REM Activating the environment
call venv\Scripts\activate.bat

REM Installing packages
echo Installing python packages from requirements.txt
pip install -r requirements.txt

REM Installing node packages
echo Installing node packages from package.json
call npm install

echo Installation DONE!
echo You can now run start.bat to use the FlowCord tool!