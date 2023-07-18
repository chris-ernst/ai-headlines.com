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
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='output.css') }}">
        <title>FlaskApp</title>
    </head>
    <body>
        <nav></nav>
        <hr>
        <div class="content">
            {% block content %} {% endblock %} 
        </div>
    </body>
    </html>

### Add Tailwind CSS to project

    pip install pytailwindcss
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

Or:
    flask run --debug -p 8000

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

### Create .env file

    touch .env

Add the following to .gitignore: 

    .env

Add sensitive information in this format:

    DB_PASSWORD=YourPasswordHere

Then call the environment variables like so:

    import os
    from dotenv import load_dotenv

    password=os.getenv('DB_PASSWORD'),

### Add PostgreSQL Database to app

Install Psycopg2

    pip install psycopg2-binary

Add the following code to app.py: 

    import psycopg2

    def get_db_connection():
        conn = psycopg2.connect(
            dbname=os.getenv('DB_DBNAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
        )
        return conn

### Add table 

Use 'Beekeper Studio' to set up the table with the help of a UI or via Python like this example:

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('DROP TABLE IF EXISTS books;')
    cur.execute('CREATE TABLE books (id serial PRIMARY KEY,'
                                 'title varchar (150) NOT NULL,'
                                 'author varchar (50) NOT NULL,'
                                 'pages_num integer NOT NULL,'
                                 'review text,'
                                 'date_added date DEFAULT CURRENT_TIMESTAMP);'
                                 )

### Add Data to table

Insert data into the table

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute('INSERT INTO ai_headlines_table (headline, paragraph, image_url)'
                    'VALUES (%s, %s, %s)',
                    (textAnswer[0],
                    textAnswer[1],
                    imgLink)
                    )

        conn.commit()
        cur.close()
        conn.close()

### Read Data from table

    @app.route('/')
    def index():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM ai_headlines_table ORDER BY id DESC;")
        news = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('index.html', news=news)

### Display Data in HTML

Database Query returns a list. Loop through the list and grab the data points one by one. 

    {% for item in news %}

        <img src="{{ item[4] | default('No image available') }}">
        <p class="text-lg pb-6 md:pb-0">{{ item[3] | default('No text available') }}</p>

    {% endfor %}

### That's it!
