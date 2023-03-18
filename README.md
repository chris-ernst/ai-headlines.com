# ai-headlines.com

## Flask startup guide

### Create Local Environment

    Python -m venv venv
    source venv/bin/activate

### Set up Flask App

    pip install Flask

Create app.py

    touch app.py

Add following code to app.py:

    from flask import Flask, render_template

    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')

Create gitignore and add "*pyc" to it:

    touch .gitignore
    echo "*.pyc" >> .gitignore

### Add templating

    mkdir templates

    touch templates/index.html

Add following code to index.html:

    {% extends 'base.html' %}

    {% block content %}
        <h1>Hello World!</h1>
        <h2>Welcome to FlaskApp!</h2>
    {% endblock %}

Create a template:

    touch templates/base.html

Add following code to base.html:

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>FlaskApp</title>
    </head>
    <body>
        <nav>
            <a href="#">FlaskApp</a>
            <a href="#">About</a>
        </nav>
        <hr>
        <div class="content">
            {% block content %} {% endblock %}
        </div>
    </body>
    </html>

### Add Tailwind CSS to project

    pip install tailwindcss
    mkdir static
    cd static
    tailwindcss init
    touch input.css output.css

Add following code to input.css:

    @tailwind base;
    @tailwind components;
    @tailwind utilities;

Replace the code in tailwind.config.js with this:

    /** @type {import('tailwindcss').Config} */
    module.exports = {
    content: ["../templates/**/*.{html,js}"],
    theme: {
        extend: {},
    },
    plugins: [],
    }

Then start the watcher, while still in the 'static' directory:

    tailwindcss -i input.css -o output.css --watch


### Run the Flask app
Ready to run!

    export FLASK_APP=app
    export FLASK_ENV=development
    flask run

Change the port if 5000 is already occupied: 

    export FLASK_RUN_PORT=8000

### When finished, deploy via Gunicorn

Minify CSS:

    tailwindcss -i static/input.css -o static/output.css --minify

Install Gunicorn and freeze requirements:

    pip install gunicorn
    pip freeze > requirements.txt

Open a file named gunicorn_config.py:

    touch gunicorn_config.py

Add following code to file:

    bind = "0.0.0.0:8080"
    workers = 2

### Deploy to DigitalOcean App platform

Change the Build and Run commands of the app. Replace the existing command with the following:

    gunicorn --worker-tmp-dir /dev/shm app:app

### Add Database to app

Coming soon. 