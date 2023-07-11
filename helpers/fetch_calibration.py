import os
import google.auth
current_dir = os.getcwd()
creds_path = current_dir +"/secrets/moten-consulting-dev-a53884c8e28c.json"
credentials, project = google.auth.load_credentials_from_file(creds_path)


from google.cloud import storage 
from helpers.logging import logger
gcs_client = storage.Client(project=project,
                           credentials=credentials)

def download_blob(bucket_name, source_blob_name, destination_file_name):
    """ 
    download an object from bucket to a file
    """
    try :
        blob_size = gcs_client.bucket(bucket_name)\
                                 .get_blob(source_blob_name)\
                                     .size/(1024*1024)
        logger.info(f"downloading file {source_blob_name},  size : {round(blob_size)} Mb")
        bucket = gcs_client.bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)
        logger.info(f"file {source_blob_name} successfully downloaded to tmp folder")
    except Exception as e:
        logger.error(traceback.format_exc())

bucket_name = 'moten-protocols'
destination_folder = "calibration/"
launcher_project_id = "Tests gyro" #MATTER

bucket=gcs_client.get_bucket(bucket_name)
blobs=bucket.list_blobs() 
for blob in blobs:
    source_blob_name = blob.name
    if launcher_project_id in source_blob_name :
        try:
            os.makedirs(destination_folder + source_blob_name.split("/")[0] + "/")
        except :
            pass
        # first folder is the name of the webapp session and could be different from the launcher mesure id person
        destination_file_name = destination_folder + source_blob_name.split("/")[0] + "/" + source_blob_name.split("/")[-1]
        download_blob(bucket_name, source_blob_name, destination_file_name)