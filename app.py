from flask import Flask, render_template, request, jsonify
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

### Database reading and Writing
conn = get_db_connection()
cur = conn.cursor()

def runApp():
    global textPrompt
    global textAnswer
    global imgPrompt
    global imgAnswer
    global imgLink

    print("Generating new output")

    ### Prompt Generation
    textPrompt = prompt_gen.promptGen()
    print(textPrompt)

    ### Text Generation
    textAnswer = text_gen.gptCall(textPrompt)
    print(textAnswer)

    ### Image Generation
    imgPrompt = textAnswer["headline"] # Extract Image Prompt from headline
    imgAnswer = img_gen.sdCall(imgPrompt) # Generate Image via Replicate API
    print(imgAnswer)
    imgLink = img_gen.uploadCare(imgAnswer) # Upload the resulting image to uploadcare CDN
    print(imgLink)

    ### Model information
    image_model = "sdxl"
    text_model = "gpt-4-turbo"

    # Insert data into the table
    cur.execute('INSERT INTO ai_headlines_table (headline, paragraph, image_url, image_model, text_model)'
                'VALUES (%s, %s, %s, %s, %s)',
                (textAnswer["headline"],
                textAnswer["paragraph"],
                str(imgLink),
                image_model,
                text_model)
                )

    conn.commit()
    cur.close()
    conn.close()

    print("Generation finished, data inserted to database")


##### Debugging
debug = False # Change this to true for testing, but make sure to run the flask in --no-debug mode

if debug == True:
    print("********debug mode active, run Python3 app.py in terminal to test********")
    runApp()
else:
    print("********debug mode inactive********")
    from apscheduler.schedulers.background import BackgroundScheduler
    scheduler = BackgroundScheduler()
    #### Running
    job_defaults = {'coalesce': False,'max_instances': 3}
    scheduler.add_job(runApp, 'interval', hours=7)
    # scheduler.add_job(runApp, 'interval', minutes=3)
    scheduler.start()



##### Routing

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/news')
def news():
    items_per_page = 10
    page = request.args.get('page', 1, type=int)

    # Ensure page is not below 1
    page = max(page, 1)

    conn = get_db_connection()
    cur = conn.cursor()

    # Get total news count to calculate total pages
    cur.execute("SELECT COUNT(*) FROM ai_headlines_table;")
    total_news_count = cur.fetchone()[0]
    total_pages = (total_news_count + items_per_page - 1) // items_per_page

    # Ensure page does not exceed total pages
    page = min(page, total_pages)

    offset = (page - 1) * items_per_page
    cur.execute("SELECT * FROM ai_headlines_table ORDER BY id DESC LIMIT %s OFFSET %s;", (items_per_page, offset))
    news = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('news.html', news=news, page=page, total_pages=total_pages)


@app.route('/about')
def about():
    return render_template('about.html')



# Flagging content
@app.route('/flag-content', methods=['POST'])
def flag_content():
    content_id = request.json.get('contentId')
    user_response = request.json.get('captchaResponse')  # Captcha response from the frontend

    # Insert data into the table
    cur.execute('INSERT INTO ai_headlines_flagged_content (content_id)'
                'VALUES (%s)',
                (content_id,)
                )

    conn.commit()
    cur.close()
    conn.close()

    print(f"Content ID {content_id} has been flagged")

    return jsonify({"message": "Content flagged successfully"}), 200
