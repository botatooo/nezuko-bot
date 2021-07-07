@echo off
taskkill /f /im py* /t
start cmd /c "py .\restart.py"
