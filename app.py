import os
from flask import Flask, jsonify, request, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import requests
import psycopg2
from google.cloud import storage

from dotenv import load_dotenv

# Load env variable
load_dotenv()
env_name = os.getenv('FLASK_ENV')
print(f"{env_name}")

client = storage.Client()
# Define your bucket name
bucket_name = 'project_bucket_for_test'


app = Flask(__name__)

db = SQLAlchemy()
if env_name == 'production':
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = f"postgresql+pg8000://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@/{os.getenv('DB_NAME')}?unix_sock={os.getenv('CONNECTION_NAME')}"
else:
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@34.76.42.189:5432/{os.getenv('DB_NAME')}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/')
def hello():
    proxy = os.environ.get('PROXY')
    proxyDict = {
        "http": proxy,
        "https": proxy
    }
    r = requests.get('http://ifconfig.me/ip', proxies=proxyDict)
    return 'You connected from IP address: ' + r.text + ' ' + str(env_name)  # + '|' + proxy


@app.route('/download/blob/<filename>')
def download_blob(filename):
    # Retrieve the file from Cloud Storage
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(filename)

    # Download the file to a temporary location
    temp_file_path = f'/tmp/{filename}'
    blob.download_to_filename(temp_file_path)

    # Serve the file for download
    return send_file(temp_file_path, as_attachment=True)


@app.route('/info')
def info():
    objects = []
    for o in client.list_blobs(bucket_name):
        objects.append(o.name)

    object_json = []
    for o in objects:
        object_json.append({'name': o})

    return jsonify(object_json), 200


@app.route('/books', methods=['GET'])
def get_books():
    query = 'SELECT * FROM books'
    books = db.session.execute(text(query)).fetchall()


    books_data = []
    for book in books:
        book_dict = {
            'id': book[0],
            'title': book[1]
        }
        books_data.append(book_dict)

    return jsonify(status=200, books_list=books_data), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', '8080')), debug=True)

# DO NOT USE IT FOR CLOUD RUN!!!! - it provides port 5000
# if __name__ == "__main__":
#    app.run()
