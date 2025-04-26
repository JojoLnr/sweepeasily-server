from flask import Flask, jsonify, redirect
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db
import os

app = Flask(__name__)
CORS(app, origins=["https://sweepeasily.com"])

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
        # Update click count in the database
        count_ref = db.reference(f"batch_clicks/{batch_name}")
        current = count_ref.get() or 0
        count_ref.set(current + 1)
        
        ref = db.reference(batch_name)
        data = ref.get()

        if not data:
            return jsonify({'success': False, 'error': f'No data found for batch: {batch_name}'}), 404

        # Split the comma-separated string into a clean list of URLs
        urls = [url.strip() for url in data.split(",") if url.strip()]
        return jsonify({'success': True, 'urls': urls})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route("/casinos", methods=["GET"])
def get_all_casinos():
    try:
        ref = db.reference("_casinos")
        data = ref.get()

        if not data:
            return jsonify({'success': True, 'casinos': {}})

        return jsonify({'success': True, 'casinos': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route("/image/<path:image_name>")
def get_image(image_name):
    base_url = "https://raw.githubusercontent.com/JojoLnr/sweepeasily-server/main/GithubImages/"
    full_url = base_url + image_name
    return redirect(full_url)

if __name__ == "__main__":
    app.run()
