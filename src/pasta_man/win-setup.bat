@REM turn printing of commands off
@echo off

@REM print status
echo Operating System: Windows
echo setting up pasta-man
echo This might take a while.

@REM install using pyinstaller.
pyinstaller --onefile --noconsole pasta-man.py > NUL

@REM After this delete .spec file and build folder tree.
del build /s /q
del pasta-man.spec

@REM copy dist/pasta-man.exe to %USERPROFILE%\.pastaman\pasta-man.exe
copy dist\pasta-man.exe %USERPROFILE%\.pastaman\pasta-man.exe

@REM delete dist
del dist /s /q

@REM create vbs script
cd %USERPROFILE%\.pastaman
echo Set pastaShell = WScript.CreateObject("WScript.Shell") > pasta-man.vbs
echo pastaShell.Run "%USERPROFILE%\.pastaman\pasta-man.exe", 0, False >> pasta-man.vbs

@REM status
echo Complete.