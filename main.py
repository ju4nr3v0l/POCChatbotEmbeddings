from flask import Flask,render_template, request
import functions

app = Flask(__name__)

convesations = []

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html')
    if request.form['question']:
        question ='Yo: ' + request.form['question']
        response = functions.most_similar(request.form['question'])
        answer = 'Bot: ' + response
        convesations.append(question)
        convesations.append(answer)
        return render_template('index.html', chat=convesations)
    else:
        return render_template('index.html', chat=convesations)
if __name__ == '__main__':
    app.run(debug=True, port=4000)

