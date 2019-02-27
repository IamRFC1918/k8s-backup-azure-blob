import os
import azure.storage.blob
import re
import yaml
from datetime import datetime, timedelta

#Get ENV secret variables
account_name = os.environ['ACCOUNT_NAME']
account_key = os.environ['ACCOUNT_KEY']
container_name = os.environ['CONTAINER_NAME']

account_name = account_name[:-2]
account_key = account_key[:-2]
container_name = container_name[:-2]


#Import ConfigMap
with open('/config/blob-config.yml') as f:
    config = yaml.load(f)

config_folder = config['k8s-backup-config']['Backup_Dir']
config_filter = config['k8s-backup-config']['Filter']
config_blob_folder = config['k8s-backup-config']['Blob_Folder']
retention_days = config['k8s-backup-config']['retention_days']

#Get File list by Filter
def getfiles(folder, filter):
    files = list()
    pattern = re.compile(filter)
    for file in os.listdir(folder):
        if pattern.match(file):
            files.append(file)
    return files
#Get blobs on container
def getblobs(connection, container):
    blobs = connection.list_blobs(container)
    return blobs

#Upload Files
def uploadFiles(folder, file, connection, container, prefix, blobs):
    blobpath = prefix + '/' + file
    source_file = os.path.join(folder, file)
    # Test if there is no File in blobs
    if len(blobs.items) == 0:
        #Upload File
        connection.create_blob_from_path(container, blobpath, source_file)
        print("Will now upload blob " + blobpath)
    else:
        #Test if file is already there
        if blobpath in blobs.items:
            print(blobpath + " is already uploaded")
        else:
        #Upload File
            connection.create_blob_from_path(container, blobpath, source_file)
            print("Will now upload blob " + blobpath)

#Erase Files older than specified in config
def deleteFiles(connection, blobs, container, retention):
    for blob in blobs:
        time_diff = datetime.now() - blob.properties.last_modified
        if time_diff>retention:
            connection.delete_blob(container, blob.name)
            print("Deleted Blob " + blob.name + " because of retention time")    


#init Blob Connection
block_blob_service = azure.storage.blob.BlockBlobService(account_name=account_name, account_key=account_key)
# Filter Files
filteredfiles = getfiles(config_folder, config_filter)
blobs = getblobs(block_blob_service, container_name)
for file in filteredfiles:
    uploadFiles(config_folder, file, block_blob_service, container_name, config_blob_folder, blobs)
#deleteFiles(block_blob_service, blobs, container_name, retention_days)