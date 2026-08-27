#!/usr/bin/env bash
# Startup script for Intelligent Customer Signal Detector (Firstsource POC)

export PATH="$HOME/.local/bin:$PATH"

echo "⚡ Launching Intelligent Customer Signal Detector Dashboard..."
python3 -m streamlit run app.py
