@echo off
powershell -Command "(Get-Content -path .env -Raw) -replace 'OLLAMA_MODEL=<path_to_model>', 'OLLAMA_MODEL=qwen3:8b' | Set-Content -Path data/model.env"
powershell -Command "python -m venv .venv; .venv/scripts/activate.bat; pip install -r requirements.txt; ollama pull qwen3:8b; streamlit run webapp.py"