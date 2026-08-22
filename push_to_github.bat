@echo off
title Push GG Wins to GitHub
cd /d "%~dp0"
echo ========================================================
echo   UPLOADING GG WINS CASINO TO GITHUB (measrarbasha-cyber)
echo ========================================================

git init
git branch -M main
git remote remove origin 2>nul
git remote add origin https://github.com/measrarbasha-cyber/ggwins-casino.git
git add .
git commit -m "Deploy full GG Wins production website & games"
echo Pushing files to GitHub...
git push -u origin main --force

echo ========================================================
echo   UPLOAD COMPLETE! All files are now on GitHub.
echo ========================================================
pause
