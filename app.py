import os
import key

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
        open_line + line + '\n'
        
    return open_line

def start_chat(number_of_prompts):
    for x in range(number_of_prompts):     
        response = openai.Completion.create(
                model="text-davinci-003",
                prompt=create_prompt(),
                temperature=0.6,
            )
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
        print(f'Resposne: {response}')
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    history_lines.append(result)

    nextcall = open_line
    for n in history_lines:
        nextcall += n
    
    
    print(f'history: {history_lines}')
    return render_template("index.html", result=result)




def generate_next_conversation_line(history):
    return """{}
You:
""".format(
        history.capitalize()
    )

if __name__ == '__main__':
    app.run(debug=True)