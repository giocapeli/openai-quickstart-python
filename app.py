import os
import key
import time
import openai
from flask import Flask, redirect, render_template, request, url_for

open_line = f'Pretend your talking to a friend so answer his question or make a new question following the context. '

app = Flask(__name__)
openai.api_key = key.OPENAI_API_KEY

history_lines = ['\nWhat you think is the meaning of life?\n']

# def test_prompt(question):
#         response = openai.Completion.create(
#                 model="text-davinci-003",
#                 prompt=question,
#                 temperature=0.6,
#                 max_tokens=1000
#             )
#         print(f'Response: {response}')
#         result = response.choices[0].text
#         print(result)

def add_history(line):
    # print(f'Line: {line}')
    history_lines.append(line)

def create_prompt():
    # print(f'current history:{history_lines}')
    for line in history_lines:
        # print(line)
        # print(history_lines)
        open_line += str(line)
    print(f'Open Line:{open_line}')
    
    return open_line

def start_chat(number_of_prompts):
    for x in range(number_of_prompts):     
        prompt = create_prompt()
        print(f'Prompt: {prompt}')
        response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                temperature=0.6,
                max_tokens=1000
            )
        # print(f'Response: {response}')
        result = response.choices[0].text
        time.sleep(5)
        add_history(result)
        
def chat_01():
    person = "chat01"
    prompt = open_line + f'You are {person}:'
    for line in history_lines:
        prompt += str(line)
    prompt += f'{person}: '
    response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                temperature=0.6,
                max_tokens=1000
            )
    result = response.choices[0].text
    time.sleep(5)
    add_history(f'{person}: {result}')
    print(f'\nHistory 01: {history_lines} \nPrompt 01: {prompt} \nResult 01: {result}')


def chat_02():
    person = "chat02"
    prompt2 = open_line + f'You are {person}'
    for line in history_lines:
        prompt2 += str(line)
    prompt2 += f'{person}: '
    response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt2,
                temperature=0.6,
                max_tokens=1000
            )
    result = response.choices[0].text
    time.sleep(5)
    add_history(f'{person}: {result}')
    print(f'\nHistory 02: {history_lines} \nPrompt 02: {prompt2} \nResult 02: {result}')

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        chat_01()
        chat_02()
        chat_01()
        chat_02()
    result = ''
    for line in history_lines:
        result += f'<h2>{line}</h2>\n'
    return render_template("index.html", result=result)

if __name__ == '__main__':
    app.run(debug=True)
    
