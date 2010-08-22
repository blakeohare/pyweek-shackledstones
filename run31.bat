@echo OFF
IF "%py31%" == "" SET py31="C:\Python31"
"%py31%\python.exe" util\preprocessor.py
"%py31%\python.exe" game.py