from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
import psycopg2
import os
from dotenv import load_dotenv

import text_gen #includes gptCall function
import img_gen #includes sdCall and uploadCare function
import prompt_gen #includes promptGen function
 
app = Flask(__name__)

textPrompt = "Empty String"
textAnswer = "Empty String"
imgPrompt = "Empty String"
imgAnswer = "Empty String"
imgLink = "Empty String"

def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv('DB_DBNAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
    )
    return conn

debug = False # Change this to true for testing, but make sure to run the flask in --no-debug mode

def runApp():
    global textPrompt
    global textAnswer
    global imgPrompt
    global imgAnswer
    global imgLink

    if debug == True:
        print("********debug mode active, platform will not generate new content********")

    else:
        print("Generating new output")

        ### Prompt Generation
        textPrompt = prompt_gen.promptGen()
        print(textPrompt)

        ### Text Generation
        textAnswer = text_gen.gptCall(textPrompt)
        print(textAnswer)

        ### Image Generation
        imgPrompt = textAnswer[0] # Extract Image Prompt from headline
        imgAnswer = img_gen.sdCall(imgPrompt) # Generate Image via Replicate API 
        print(imgAnswer)
        imgLink = img_gen.uploadCare(imgAnswer) # Upload the resulting image to uploadcare CDN
        print(imgLink)

        ### Database reading and Writing
        conn = get_db_connection()
        cur = conn.cursor()

        # Insert data into the table
        cur.execute('INSERT INTO ai_headlines_table (headline, paragraph, image_url)'
                    'VALUES (%s, %s, %s)',
                    (textAnswer[0],
                    textAnswer[1],
                    imgLink)
                    )

        conn.commit()
        cur.close()
        conn.close()

        print("Generation finished, data inserted to database")




##### Running
job_defaults = {'coalesce': False,'max_instances': 3}
scheduler = BackgroundScheduler()
scheduler.add_job(runApp, 'interval', hours=7)
#scheduler.add_job(runApp, 'interval', minutes=1)
scheduler.start()



##### Routing

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM ai_headlines_table ORDER BY id DESC;")
    news = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', news=news)

@app.route('/about')
def about():
    return render_template('about.html')