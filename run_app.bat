@echo off
echo Starting Sentiment Analysis Dashboard...
call .venv\Scripts\activate
streamlit run streamlit_app.py --server.headless true
pause
