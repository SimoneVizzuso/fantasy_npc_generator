@echo off
powershell -Command "(Get-Content -path data/model.env -Raw) -replace 'OLLAMA_MODEL=<path_to_model>', 'OLLAMA_MODEL=mixtral' | Set-Content -Path data/model.env"
powershell -Command "python -m venv .venv; .venv/Scripts/Activate.ps1; pip install -r requirements.txt; ollama pull mixtral; streamlit run webapp.py"