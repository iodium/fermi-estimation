# Fermi Estimation Quiz
The Fermi Estimation Quiz is a daily web based quiz in which users have to answer Fermi Estimation Questions using ranges.
## Installation
```bash
git clone https://github.com/iodium/fermi-estimation

pip install -r requirements.txt
```
## Usage
```bash
python3 app.py
```
Or
```bash
python app.py
```
Open the http://127.0.0.1:5000 link to start the quiz.
```bash
* Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 466-173-880
```
## Features
- Persistent Storage via SQLite
- Aggregate Statistics
- User Recognition via Cookies
- Daily Question Refresh
## Tech Stack
- Python 3
- Flask
- Pandas
- SQLite
