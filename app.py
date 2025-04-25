from flask import Flask, jsonify
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)

# Initialize Firebase Admin SDK
cred = credentials.Certificate("sweepeasily-credentials.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sweepeasily-default-rtdb.firebaseio.com/'
})

@app.route("/")
def home():
    return jsonify({"message": "Backend is working!"})

@app.route("/instructions")
def get_instructions():
    ref = db.reference("/")  # Root of the database
    data = ref.get()
    keys = list(data.keys()) if data else []
    return jsonify({"keys": keys})

if __name__ == "__main__":
    app.run()
