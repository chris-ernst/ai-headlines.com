import os
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()
client = OpenAI()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

GPT_MODEL="gpt-4-turbo-preview"

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_headlines",
            "description": "Invent a fictional future news headline",
            "parameters": {
                "type": "object",
                "properties": {
                    "headline": {
                        "type": "string",
                        "description": "The headline of the fictional news story",
                    },
                    "paragraph": {
                        "type": "string",
                        "description": "The intro paragraph of the fictional news story",
                    },
                },
                "required": ["headline", "paragraph"],
            },
        }
    },
]



def chat_completion_request(messages, tools=None, tool_choice=None, model=GPT_MODEL):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e



def gptCall(textPrompt):
    chat_response = chat_completion_request(
        messages=textPrompt,
        tools=tools,
        tool_choice={"type": "function", "function": {"name": "get_headlines"}}
    )

    # print(chat_response.choices[0].message)
    gptAnswer = json.loads(chat_response.choices[0].message.tool_calls[0].function.arguments)

    # headline = gptAnswer["headline"]
    # print("Headline: " + headline)
    # paragraph = gptAnswer["paragraph"]
    # print("Paragraph: " + paragraph)

    return(gptAnswer)
