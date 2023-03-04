import csv
import json
from pymongo import MongoClient
from flask import Flask, render_template, url_for, request, redirect
app = Flask(__name__)

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
    user = "markreijn"
    password = "Rn0TwmhnShIeDrWf"
    client = MongoClient(f"mongodb+srv://{user}:{password}@portfolio.7sw702i.mongodb.net/?retryWrites=true&w=majority")
    db = client.spotify
    return db.song

@app.route('/')
def homepage():
    return render_template('index.html')

# @app.route('/<string:page_name>')
# def html_page(page_name):
#     return render_template(page_name)


# def write_to_file(data):
#     with open('database.txt', mode='a') as database:
#         email = data['email']
#         subject = data['subject']
#         message = data['message']
#         file = database.write(f'\n{email},{subject},{message}')


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

    print(songs)
    return(songs)

@app.route('/songs')
def get_songs():
    collection = connectToDatabase()
    test = collection.find({}, {'_id': False})
    return render_template(
        "../templates/songs.html",
        songs="hallo man"
    )