@echo off
echo Installing modules for Kinoflix !
echo  - Flask
echo  - Pystyle
echo  - PyYAML
echo  - Werkzeug Utils
timeout 3 > NUL
cls
python -m pip install flask pystyle pyyaml werkzeug
cls
echo Everything should have installed successfuly. You can now run the app.py through CMD.
echo If you need any further help ; refer to readme : https://github.com/nildontsleep/kinoflix
echo.
echo Press any key to exit the modules installer
pause > NUL
