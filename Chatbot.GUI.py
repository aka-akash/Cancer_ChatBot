from flask import Flask, render_template, request
from Chatbot_Resp import chatbot_response

app = Flask(__name__)
app.config['SECRET_KEY'] = "you-will-never-guess"

Bot = []
Human = []


def addBot(add):
    res = chatbot_response(add)
    Bot.append(res)


def addHuman(add):
    Human.append(add)
    addBot(add)


@app.route('/Chatbot_Page')
def login():
    return render_template('Chatbot_Page.html')


@app.route('/Chatbot_bot')
def Chatbot_Bot():
    return render_template('Chatbot_Bot.html')


@app.route('/Chatbot', methods=['GET', 'POST'])
def ask():
    if request.method == 'POST':
        if(len(Human) == 0):
            addHuman(request.form['ques'])
        else:
            if(request.form['ques'] == Human[-1]):
                pass
            else:
                addHuman(request.form['ques'])
        return render_template('Chatbot_Bot.html', Length=len(Bot), Bot=Bot, Human=Human)


if __name__ == '__main__':
    app.run(debug=True)
