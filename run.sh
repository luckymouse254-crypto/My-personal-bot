#!/bin/bash
echo "Starting @Mouselucky_bot..."
if [ ! -d "venv" ]; then
  echo "Creating venv..."
  python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt
python3 bot.py
