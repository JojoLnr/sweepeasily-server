import firebase_admin
from firebase_admin import credentials
from flask import Flask, jsonify

app = Flask(__name__)

cred = credentials.Certificate("sweepeasily-credentials.json")
firebase_admin.initialize_app(cred)

@app.route("/")
def home():
    return jsonify({"message": "Backend is working!"})

if __name__ == "__main__":
    app.run()
