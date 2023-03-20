from flask import Flask, render_template
import threading #important for timer
from apscheduler.schedulers.background import BackgroundScheduler

import text_gen #includes gptCall function
import img_gen #includes sdCall and uploadCare function
import prompt_gen #includes promptGen function

import psycopg2
import os
from dotenv import load_dotenv
 
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

debug = True # Change this to true for testing, but make sure to run the flask in --no-debug mode

def runApp():
    global textPrompt
    global textAnswer
    global imgPrompt
    global imgAnswer
    global imgLink

    if debug == True:
        print("********debug mode active********")
        # Dummy Data
        textAnswer = ['Kongolese President Appoints Robot as Prime Minister in Unprecedented Move', "In a surprising turn of events, the President of the Republic of Kongolo has assigned a highly sophisticated robot as the country's new Prime Minister. The move, which has never been seen before in the history of Kongolese politics, is part of the President's plan to modernize the government and increase efficiency. The robot, equipped with state-of-the-art artificial intelligence and advanced decision-making algorithms, is expected to play a key role in shaping the future of the nation. The decision has sparked a heated debate among citizens, with some praising the innovation while others expressing concerns about the ethical implications of appointing a non-human leader."]
        imgLink = "https://ucarecdn.com/6002e4af-da7b-452f-916a-1af113762651/"


    else:

        ### Prompt Generation
        textPrompt = prompt_gen.promptGen()

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




##### Running

# scheduler = BackgroundScheduler()
# scheduler.add_job(runApp, 'interval', hours=7)
# scheduler.start()

# runApp()



##### Routing

@app.route('/')
def index():
    # conn = get_db_connection()
    # cur = conn.cursor()
    # cur.execute("SELECT * FROM ai_headlines_table ORDER BY id DESC;")
    # news = cur.fetchall()
    # cur.close()
    # conn.close()
    # return render_template('index.html', news=news)
    return render_template('about.html')

@app.route('/about')
def about():
    return render_template('about.html')