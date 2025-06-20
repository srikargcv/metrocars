from flask import Flask, request, jsonify
from google.cloud import storage
from datetime import timedelta
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # ✅ To allow Flutter web or any frontend to access this server

# ✅ Load Google Cloud Storage credentials
storage_client = storage.Client.from_service_account_json('service_account.json')

@app.route('/generate_signed_url', methods=['GET'])
def generate_signed_url():
    try:
        bucket_name = 'metrocars'  
        file_name = request.args.get('file_name')

        if not file_name:
            return jsonify({'error': 'Missing file_name parameter'}), 400

        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)

        url = blob.generate_signed_url(
            version="v4",
            expiration=timedelta(minutes=30), 
            method="PUT",
            content_type="application/octet-stream"
        )

        return jsonify({'url': url})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
