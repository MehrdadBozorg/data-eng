from typing import Protocol
from azure.storage.blob import BlobServiceClient
from io import BytesIO
from zipfile import ZipFile
from xml.dom import minidom

def read_files(url):
    url_parts = url_splitter(url)
    account_url = url_parts['account_url']
    account_key = url_parts['account_key']
    container_name = url_parts['container_name']
    blob_name = url_parts['blob_name']

    # TODO Error handling message
    blob_service_client_instance = BlobServiceClient(
        account_url=account_url, credential=account_key)

    # TODO Error handling message
    blob_client_instance = blob_service_client_instance.get_blob_client(
        container_name, blob_name, snapshot=None)

    # TODO Error handling message 
    blob_data = blob_client_instance.download_blob()
    data = blob_data.readall()


    inmem = BytesIO(data)
    myzip = ZipFile(inmem)

    file_dict = {name: myzip.read(name) for name in myzip.namelist()}
    file_number = len(file_dict)

    result_message = {'Rendered Files': file_number, 'Message': 'Ok' if file_number > 0 else 'Error' }

    return(result_message, "Files are retrieved successfully")

def url_splitter(url):
    #TODO: add unit test
    protocol_part = url.split('://')
    url_parts = protocol_part[1].split('/')
    account_url = protocol_part[0]  + '://' + url_parts[0]
    containder_name = url_parts[1]
    name_query_split = url_parts[2].split('?')
    blob_name = name_query_split[0]
    account_key = name_query_split[1]


    return {
        'account_url': account_url,
        'container_name': containder_name,
        'blob_name': blob_name,
        'account_key': account_key
    }


 