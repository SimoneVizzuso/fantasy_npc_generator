#!/bin/bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
ollama pull mixtral
streamlit run webapp.py