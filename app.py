from flask import Flask, jsonify, redirect
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db
import os
import requests

app = Flask(__name__)
CORS(app, origins=["https://sweepeasily.com"])
base_url = "https://github.com/JojoLnr/sweepeasily-server/blob/main/GithubImages/"

# Initialize Firebase Admin SDK
cred = credentials.Certificate("sweepeasily-credentials.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sweepeasily-default-rtdb.firebaseio.com/'
})

@app.route("/")
def home():
    return jsonify({"message": "Backend is working!"})

@app.route("/batch/<batch_name>", methods=["GET"])
def get_batch(batch_name):
    try:
        # Update click count in the database
        count_ref = db.reference(f"batch_clicks/{batch_name}")
        current = count_ref.get() or 0
        count_ref.set(current + 1)

        # Adjust path if needed based on database structure
        ref = db.reference(batch_name)  # Assuming the batch is stored directly at root level
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

@app.route("/image/<path:image_path>", methods=["GET"])
def get_image(image_path):
    try:
        # Construct the full URL to the raw GitHub file
        image_url = base_url + image_path

        # You can choose to fetch the image and return the raw content if needed, or just the URL
        return jsonify({"success": True, "image_url": image_url})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/get_casinos', methods=['GET'])
def get_casinos():
    try:
        # Access the "_casinos" node
        ref = db.reference('_casinos')
        data = ref.get()

        if data is None:
            return jsonify({"success": False, "message": "No data found."}), 404

        # Get all keys inside _casinos
        casino_keys = list(data.keys())

        return jsonify({"success": True, "casinos": casino_keys})

    except Exception as e:
        print("❌ Error retrieving casinos:", e)
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/get_instructions/<casino_key>', methods=['GET'])
def get_instructions(casino_key):
    try:
        # Access the specific casino under _casinos
        ref = db.reference(f'_casinos/{casino_key}')
        instructions = ref.get()

        if instructions is None:
            return jsonify({"success": False, "message": "Casino not found."}), 404
        
        instructions = instructions.replace("--/n--", "\n")
        return jsonify({"success": True, "instructions": instructions})

    except Exception as e:
        print(f"❌ Error retrieving instructions for {casino_key}:", e)
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == "__main__":
    app.run()
