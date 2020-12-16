# Evridge
Simple Web Application which everyone can inform and advertise their event or something

Used only flask, python framework for webapp, html.

### How to use

```
pip install -r requirements.txt
```
install the required packages.

This repository includes '.db' file. 
but, if you delete it or want to create empty database file, delete '.db' file and write this script.
```
python
>> from database import init_db
>> init_db()
```
the function create SQLite database 'evridge.db' at your current directroy

to start server and evridge, enter the following command,
```
python run.py
```
and access http://localhost:5000 .
