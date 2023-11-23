from flask import Blueprint, request
from google.cloud import storage
from flask import jsonify

bp = Blueprint('cloud_storage', __name__, url_prefix='/cloud_storage')


@bp.route('/upload', methods=['POST'])
def authenticate_implicit_with_adc():
    # Instantiates a client
    storage_client = storage.Client()

    # The name for the root bucket
    bucket_name = "character-manager"
    file = request.files['file']

    destination_blob_name = f'/userid/{file.filename}'
    print("destination", destination_blob_name)
    bucket = storage_client.get_bucket(bucket_name, timeout=5)
    print(f"Bucket {bucket.name} get.")
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(file, timeout=10)
    return jsonify({"message": "success"}), 200


@bp.route('/get/{file_name}', methods=['GET'])
def get_uploaded_file(file_name):
    # Instantiates a client
    storage_client = storage.Client()

    # The name for the root bucket
    bucket_name = "character-manager"

    # destination_blob_name = f'{user_id}/{group_id}/{file.filename}'
    target_blob_name = file_name
    bucket = storage_client.get_bucket(bucket_name, timeout=5)
    print(f"Bucket {bucket.name} get.")
    blob = bucket.blob(target_blob_name)
    blob.exists()
    return
