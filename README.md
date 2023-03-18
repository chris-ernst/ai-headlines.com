# ai-headlines.com

## Flask startup guide

### Local Environment

        Python -m venv venv
        source venv/bin/activate
    
### Flask App

        pip install Flask

Create app.py

        touch app.py

Add following code to file:

        from flask import Flask

        app = Flask(__name__)

        @app.route('/')
        def hello():
            return '<h1>Hello, World!</h1>'

Ready to run!

        export FLASK_APP=app
        export FLASK_ENV=development
        flask run

Change the port if 5000 is already occupied: 

        export FLASK_RUN_PORT=8000

### Deploy via Gunicorn
        pip install gunicorn
        pip freeze > requirements.txt

Open a file named gunicorn_config.py:

        touch gunicorn_config.py

Add following code to file:

        bind = "0.0.0.0:8080"
        workers = 2

Create gitignore:

        touch .gitignore

Add following code to file:

        *.pyc

### Deploy to DigitalOcean App platform

**Important**   

Change the Build and Run commands of the app. Replace the existing command with the following:

        gunicorn --worker-tmp-dir /dev/shm app:app