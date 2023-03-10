import os
import key
import time

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = key.OPENAI_API_KEY

history_lines = []

def add_history(line):
    history_lines.append(line)

def create_prompt():
    open_line = 'Pretend your talking to a friend so answer his question or suggest a new topic:\n'

    for line in history_lines:
        open_line + str(line) + '\n'
    print(open_line)
    return open_line

def start_chat(number_of_prompts):
    for x in range(number_of_prompts):     
        time.sleep(5)
        response = openai.Completion.create(
                model="text-davinci-003",
                prompt=create_prompt(),
                temperature=0.6,
            )
        result = response.choices[0].text
        add_history(result)

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        animal = request.form["animal"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=create_prompt(),
            temperature=0.5,
        )
        print(response)

        result = response.choices[0].text
        add_history(result)
        # return redirect(url_for("index", result=response.choices[0].text))

        start_chat(4)
    
        print(f'history: {history_lines}')
    return render_template("index.html", result=history_lines)

if __name__ == '__main__':
    app.run(debug=True)