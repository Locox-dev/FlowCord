@echo off

echo Make sure to have disabled your CSS theme before.

REM Prompt user for confirmation
SET /P AREYOUSURE=Are you sure you want to continue (Y/[N])?
IF /I "%AREYOUSURE%" NEQ "Y" GOTO END

REM Activate the virtual environment (for Command Prompt)
call venv\Scripts\activate.bat

REM Revert changes made to Discord (doesn't work all the time)
python customcss.py --revert

REM Get the directory path
set "folder=%~dp0"

REM Display directory path
echo "%folder%"

REM Prompt user for final confirmation
SET /P FINALCONFIRM=This will uninstall. Are you really sure (Y/[N])?
IF /I "%FINALCONFIRM%" NEQ "Y" GOTO END

REM Delete the directory
rmdir /s /q "%folder%"
echo Uninstallation done.

:END
