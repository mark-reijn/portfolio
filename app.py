import csv
import json
import requests
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

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


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

@app.route('songs/<string:token>')
def get_songs(token):
       
    response = requests.get(
        "https://api.spotify.com/v1/playlists/4RpIr7DUkNf99IRy9Wk74H/tracks?market=NL&limit=10&offset=0", 
        headers={'Authorization':'Bearer '+ token})

    if response.status_code == 200:
        data = convertToJsonArray(response.json())
        methods.insertData(data)
        
    else: 
        print(response)