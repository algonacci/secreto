import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import dotenv_values


app = Flask(__name__)

config = dotenv_values(".env")
client = MongoClient(config["MONGODB_URI"])
app.db = client.secreto

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message = request.form['message']
        formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
        app.db.messages.insert_one({"message": message, "date": formatted_date})
        messages = [
            (message["message"],
             message["date"],
             datetime.datetime.today().strftime("%Y-%m-%d") == message["date"])
            for message in app.db.messages.find({})
        ]
        return render_template('index.html', messages=messages, title="Recent Messages")
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)