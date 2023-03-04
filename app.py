import csv
import json
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from pymongo import MongoClient
from flask import Flask, render_template, url_for, request, redirect
app = Flask(__name__)

keyVaultName = "PortfolioVaultMark2023"
KVUri = f"https://{keyVaultName}.vault.azure.net"

def convertToJsonArray(data):
    array = [];
    for item in data['items']:
            array.append({
                "id":item['track']['id'],
                "href":item['track']['external_urls']['spotify'],
                "name":item['track']['name'],
                "artist":item['track']['artists'][0]['name'],
                "duration":item['track']['duration_ms'],
                "image":item['track']['album']['images'][0]['url']
            })
    return json.dumps(array)

def connectToDatabase():
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=KVUri, credential=credential)
    dbString = client.get_secret("DbConnection")

    mongoClient = MongoClient(f"mongodb+srv://{dbString.value}")
    db = mongoClient.spotify
    return db.song

def write_to_file(data):
    with open('database.txt', mode='a') as database:
        email = data['email']
        subject = data['subject']
        message = data['message']
        file = database.write(f'\n{email},{subject},{message}')

# @app.route('/submit_form', methods=['GET', 'POST'])
# def submit_form():
#     if request.method == 'POST':
#         data = request.form.to_dict()
#         write_to_csv(data)
#         return redirect('/thankyou.html')
#     else:
#         return 'Something went wrong!'

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

