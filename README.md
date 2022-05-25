# Wordle Helper App

Super quick app to help give hints for Wordle puzzles.

## Requirements
- git
- python3.8
- python3.8-venv
- nginx
- supervisor 

## Installation

git clone ... /path
cd /path
python3.8 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
cp ./nginx.conf /etc/nginx/sites-available/wordlehelper.conf
cp ./supervisor.con /etc/supervisor.d/wordlehelper.conf
