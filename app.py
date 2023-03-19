from flask import Flask, render_template
import threading #important for timer

import text_gen #includes gptCall function
import img_gen #includes sdCall and uploadCare function
import prompt_gen #includes promptGen function

app = Flask(__name__)

textPrompt = "Empty String"
textAnswer = "Empty String"
imgPrompt = "Empty String"
imgAnswer = "Empty String"
imgLink = "Empty String"


def runApp(debug, timeIntervals):

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
        #threading.Timer(timeIntervals, runApp).start() 

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
        # Goes here




##### Running

# debug = True # Change this to true for testing, but make sure to run the flask in --no-debug mode
# timeIntervals = 300 # Run intervals in seconds
runApp(False, 300)

##### Routing

@app.route('/')
def index():
    return render_template('index.html', textAnswer=textAnswer, imgLink=imgLink)

@app.route('/about')
def about():
    return render_template('about.html')