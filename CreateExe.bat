@echo OFF
"%py26%\python.exe" util\preprocessor.py
"%py26%\python.exe" util\py2exe_setup.py
rmdir /q /s build
move dist exe