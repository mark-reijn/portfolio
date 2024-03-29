import csv
import os
from dotenv import load_dotenv
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from pymongo import MongoClient
from flask import Flask, render_template, url_for, request, redirect
app = Flask(__name__)
load_dotenv()

keyVaultName = "PortfolioVaultMark2023V7"
KVUri = f"https://{keyVaultName}.vault.azure.net"

def connectToDatabase():
    if os.getenv("DB_CONNECTION") == None:
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=KVUri, credential=credential)
        dbString = client.get_secret("DbConnection").value
    else:
        dbString = os.getenv("DB_CONNECTION")

    mongoClient = MongoClient(f"mongodb+srv://{dbString}")
    db = mongoClient.spotify
    return db.song

def write_to_file(data):
    with open('database.txt', mode='a') as database:
        email = data['email']
        subject = data['subject']
        message = data['message']
        file = database.write(f'\n{email},{subject},{message}')

def write_to_csv(data):
    with open('database.csv', 'a', newline='') as csvfile:
        email = data['email']
        subject = data['subject']
        message = data['message']
        writer = csv.writer(csvfile)
        writer.writerow([email, subject, message])


@app.route('/submit_form', methods=['GET', 'POST'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        write_to_csv(data)
        return redirect('/thankyou.html')
    else:
        return 'Something went wrong!'

def songs_from_db():
    collection = connectToDatabase()
    songs = collection.find({}, {'_id': False})
    array = []

    for song in songs:
        array.append(song)

    return(array)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/index")
def index():
    return render_template("index.html")

@app.route('/songs')
def songs():
    return render_template(
        "songs.html",
        songs=songs_from_db()
    )

@app.route('/works')
def works():
    return render_template("works.html")

@app.route("/thankyou.html")
def thank():
    return render_template("thankyou.html")