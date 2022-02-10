# Flask Processing Images Demo

This project is supposed to learn Flask.

# Run locally

1) Create venv: `python -m venv venv`
2) Activate venv: `source venv/bin/activate`
3) Install Python dependencies: `pip install -r requirements.txt`
4) Export port: `export PORT=8000`
5) Run: `python app.py`
6) Visit: [http://localhost:8000/](http://localhost:8000/)

## Actual bug

You need to change `https` to `http` in `templates/processing.html` line `var socket = io.connect('https://' + document.domain + ':' + location.port);` to run locally.

# Herokuapp

Project is deployed to [Heroku](https://heroku.com/): [Link to app](https://flask-demo-rosalux.herokuapp.com/)

# Contributions

Feel free to message me, open issues, provide helpful informations with best practises and so on. This will help me learning.

# Ideas

* Replace the random number with a session ID as unique key for identifying background task
* Checking max size limit and correct file type, secure upload form
* Replace Flask Executor with a Message Queue
