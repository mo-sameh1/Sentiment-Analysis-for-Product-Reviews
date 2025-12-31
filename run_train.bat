@echo off
echo Starting Model Training...
call .venv\Scripts\activate
python scripts\train_model.py
pause
