@echo off
echo Installing dependencies for Backend...
py -m pip install -r backend/requirements.txt

echo Installing dependencies for Scraper...
py -m pip install -r scraper/requirements.txt
py -m playwright install

echo.
echo Dependencies installed successfully!
pause
