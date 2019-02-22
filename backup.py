import os
import azure.storage.blob
import re
import yaml

#Get ENV secret variables
account_name = os.environ['ACCOUNT_NAME']
account_key = os.environ['ACCOUNT_KEY']
container_name = os.environ['CONTAINER_NAME']

#Import ConfigMap
#with open('/config/config.yml') as f:
with open('config.yml') as f:
    config = yaml.load(f)

config_folder = config['k8s-backup-config']['Backup_Dir']
config_filter = config['k8s-backup-config']['Filter']
config_blob_folder = config['k8s-backup-config']['Blob_Folder']

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
    #Test if file is already there
    if blobpath in blobs.items:
        print(blobpath + " is already uploaded")
    else:
    #Upload File
        connection.create_blob_from_path(container, blobpath, source_file)

#init Blob Connection
block_blob_service = azure.storage.blob.BlockBlobService(account_name=account_name, account_key=account_key)
# Filter Files
filteredfiles = getfiles(config_folder, config_filter)
blobs = getblobs(block_blob_service, container_name)
for file in filteredfiles:
    uploadFiles(config_folder, file, block_blob_service, container_name, config_blob_folder, blobs)