from flask import Flask, jsonify
import firebase_admin
from firebase_admin import credentials, db
import os

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

@app.route("/batch/<batch_name>", methods=["GET"])
def get_batch(batch_name):
    try:
        ref = db.reference(batch_name)
        data = ref.get()

        if not data:
            return jsonify({'success': False, 'error': f'No data found for batch: {batch_name}'}), 404

        # Split the comma-separated string into a clean list of URLs
        urls = [url.strip() for url in data.split(",") if url.strip()]
        return jsonify({'success': True, 'urls': urls})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == "__main__":
    app.run()
