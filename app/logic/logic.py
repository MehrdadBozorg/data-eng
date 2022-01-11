from azure.storage.blob import BlobServiceClient
from io import BytesIO
from zipfile import ZipFile
from xml.etree.ElementTree import fromstring, ElementTree
import multiprocessing as mp
from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient


def read_files(url: str) -> tuple:
    """
    Get the url for the respective blob. Connect and download it, then extract the files in memory (not disk), and call render_files
    function to extract data from files and save them in DB.

    :return, a tuble of metadata result and message to show in browser, indicating the number of rendered files and response status.
    """
    url_parts = url_splitter(url)
    account_url = url_parts['account_url']
    account_key = url_parts['account_key']
    container_name = url_parts['container_name']
    blob_name = url_parts['blob_name']

    blob_service_client_instance = BlobServiceClient(
        account_url=account_url, credential=account_key)

    blob_client_instance = blob_service_client_instance.get_blob_client(
        container_name, blob_name, snapshot=None)

    blob_data = blob_client_instance.download_blob()
    
    data = blob_data.readall()

    inmem = BytesIO(data)
    myzip = ZipFile(inmem)

    file_list = [(name, myzip.read(name)) for name in myzip.namelist()]
    render_files(file_list)
    
    file_number = len(file_list)
    result = {'Rendered Files': file_number, 'Message': 'Ok' if file_number > 0 else 'Error' }
    message = "Files are retrieved successfully" if file_number > 0 else "Error in rendering the files."

    return(result, message)


def url_splitter(url: str) -> dict:
    """
    Split the given url to extract required information to connect to the blob and download it.
    
    :return, the config information as a dictionary.
    """
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


def render_files(files_list: list):
    """
    Get the list of files, concerrently (by the multiprocessing approach) render demmanded fields (info) from each and then save the lis as a
    bulk in the mongodb.
    """

    # DB connection info
    mongo_client = MongoClient('localhost', 27017)
    db = mongo_client.file_manager
    col = db.file_collection
    
    with mp.Pool() as pool:
        res = pool.map(render_file_data, files_list)
        col.insert_many(res)


def render_file_data(xml_tuple: tuple) -> dict:
    """
    Get the tuple of xml file as a string and the name of the file, then extract the demmanded tags' values (info).
    
    :return, the dictionary of file data together with the file name.
    """
    tree=tree=ElementTree(fromstring(xml_tuple[1]))
    root=tree.getroot()
    data = {}

    # extract title
    title = root.find('.//invention-title')
    if title:
        data['patent_title'] = title.text
    else:
        data['patent_title'] = None

    # extract description
    description = root.find('description')
    if description:
        des_text = ""
        for txt in description:
            for c in txt.iter():
                des_text += str(c.text)

        data['description'] = des_text
    else:
        data['description'] = None

    # extract abstract
    abstract = root.findall('.//abstract')
    if abstract:
        text = ''
        for txt in abstract:
            for c in txt.iter():
                text += c.tail
        data['abstract'] = text
    else:
        data['abstract'] = None

    # extract publication year
    publication_date = root.findall('.//publication-of-grant-date//date')
    if publication_date:
        year = publication_date[0].text[0: 4]
        data['publication_year'] = year
    else:
        data['publication_year'] = None

    # extract application
    application = root.findall('.//application-reference')
    if application:
        app_parsed = parseXmlToJson(application)
        data['application'] = app_parsed['application-reference']
    else:
        data['application'] = None

    # add the name of the file as a field in the data document.
    data['file_name'] = xml_tuple[0]

    return data


def parseXmlToJson(xml: str) -> list:
    """
    Get the xml data as a string, and render it as a json. It's used to extract the nested tags info.

    :return, the list of all nested tags as the json records.
    """
    response = {}
    for child in list(xml):
        if len(list(child)) > 0:
            if child.tag in response:
                response[child.tag].append(parseXmlToJson(child))
            else: 
                response[child.tag] = [parseXmlToJson(child)]
        else:
            if child.tag in response:
                response[child.tag].append([child.text] or [''])
            else: 
                response[child.tag] = [child.text] or ['']

    return response