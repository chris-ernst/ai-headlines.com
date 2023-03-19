import os
from dotenv import load_dotenv
import openai

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')


# Function gptCall takes a text promt as a String and returns headline and body paragraph as a list. 

def gptCall(textPrompt):
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": textPrompt}])
    
    gptAnswer = completion.choices[0].message.content
    gptAnswer = (gptAnswer.splitlines())
    #print(gptAnswer) 

    while('' in gptAnswer):
        gptAnswer.remove("")
    gptAnswer[0] = gptAnswer[0].strip('\"')
    #print(gptAnswer[0])

    gptAnswer[0].replace('Headline: ', '')
    #print(gptAnswer[0]) ###

    return(gptAnswer)

gptCall("Write an English news headline and intro paragraph of a event in Kongolese politics in a strange and unlikely fictional future timeline.")
