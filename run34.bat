@echo OFF
IF "%py34%" == "" SET py34="C:\Python34"
"%py34%\python.exe" util\preprocessor.py
"%py34%\python.exe" game.py