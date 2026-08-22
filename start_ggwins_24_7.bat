@echo off
title GG Wins 24/7 Server & Tunnel Guardian
cd /d "%~dp0"
echo ======================================================
echo   GG WINS - 24/7 CRASH-PROOF SERVER & CLOUDFLARE TUNNEL
echo ======================================================
echo Starting 24/7 Supervisor Guardian...
python supervisor.py
pause
