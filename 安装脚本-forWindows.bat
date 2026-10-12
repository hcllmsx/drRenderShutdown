@echo off
setlocal
set "SOURCE=%~dp0RenderShutdown-hcllmsx.py"
set "TARGET=%APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Deliver"

if not exist "%SOURCE%" goto missing
if not exist "%TARGET%" mkdir "%TARGET%"
if errorlevel 1 goto failed
copy /Y "%SOURCE%" "%TARGET%\RenderShutdown-hcllmsx.py" >nul
if errorlevel 1 goto failed

echo Installation complete.
echo Script: "%TARGET%\RenderShutdown-hcllmsx.py"
echo Restart DaVinci Resolve, then select End and RenderShutdown-hcllmsx in Deliver page Advanced Settings.
pause
exit /b 0

:missing
echo ERROR: RenderShutdown-hcllmsx.py was not found next to this BAT file.
pause
exit /b 1

:failed
echo ERROR: Could not create the destination folder or copy the script.
echo Destination: "%TARGET%"
pause
exit /b 1
