from flask import Flask, request, jsonify
from google.cloud import storage
import json
import os

app = Flask(__name__)

# Load service account from environment variable
service_account_info = json.loads(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON'))
storage_client = storage.Client.from_service_account_info(service_account_info)

bucket_name = 'YOUR_BUCKET_NAME'  # Replace this

@app.route('/generate_signed_url', methods=['GET'])
def generate_signed_url():
    file_name = request.args.get('file_name')
    if not file_name:
        return jsonify({'error': 'Missing file_name parameter'}), 400

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    url = blob.generate_signed_url(
        version="v4",
        expiration=300,  # URL valid for 5 minutes
        method='PUT',
        content_type='application/octet-stream'
    )

    return jsonify({'url': url})

# ✅ Keep-Alive Route
@app.route('/keep_alive', methods=['GET'])
def keep_alive():
    return jsonify({'status': 'Server is live 🚀'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
