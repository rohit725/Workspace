@echo OFF
SETLOCAL EnableDelayedExpansion

:: Take input from user to replace the value with in configuration.
set /p server="Enter the server ip: "
set /p port="Enter the server port: "
set /p apitoken="Enter the api token: "

:: Add multiple call for Replace function in order to replace all the section values.
call :Replace "RESPONDER" , %server% , %port% , %apitoken%
exit /b %errorlevel%


:: ##########################
:: Add your further code here
:: ##########################


:: Replace function which will replace one value at a time
:Replace
  SET "responder="
  (
   FOR /f "tokens=1*delims=" %%a IN (responder.ini) DO (
    FOR /f "tokens=1*delims== " %%b IN ("%%a") DO (
     SET repro=Y
     IF "%%c"=="" (
      SET "responder="
      IF /i "%%b"=="[%~1]" SET responder=y
     ) ELSE (
      IF DEFINED responder IF "%%b"=="server" (SET "repro="&ECHO(server=%~2)
      IF DEFINED responder IF "%%b"=="serverport" (SET "repro="&ECHO(serverport=%~3)
      IF DEFINED responder IF "%%b"=="api_token" (SET "repro="&ECHO(api_token=%~4)
     )
     IF DEFINED repro ECHO(%%a
    )
   )
  ) > responder.ini.1
  if exist "responder.ini.1" move /y "responder.ini.1" "responder.ini" >NUL
exit /b 0
