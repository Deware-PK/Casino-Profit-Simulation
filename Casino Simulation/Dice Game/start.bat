@echo off
set /p num_players="Enter the number of players: "
set /p times="Enter the number of simulation rounds: "
python dice_game.py %num_players% %times%
pause
