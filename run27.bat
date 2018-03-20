@echo OFF
IF "%py27%" == "" SET py27="C:\Python27"
"%py27%\python.exe" util\preprocessor.py
"%py27%\python.exe" game.py