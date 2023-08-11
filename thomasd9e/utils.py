from google.cloud import storage


def download_service_account_key():
    # Initialize the storage client
    client = storage.Client()

    # Define the bucket and blob (file) name
    bucket_name = "thomasde-secrets"
    blob_name = "DO-NOT-DELETE-static-file-service-key.json"
    destination_file_name = "/tmp/DO-NOT-DELETE-static-file-service-key.json"  # Temporary path on App Engine

    # Download the file
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.download_to_filename(destination_file_name)

    ## print(f"Downloaded {blob_name} from {bucket_name} to {destination_file_name}.") # For debugging

    return destination_file_name
