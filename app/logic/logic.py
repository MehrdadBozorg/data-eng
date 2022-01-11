from azure.storage.blob import BlobServiceClient
from io import BytesIO
from zipfile import ZipFile
from xml.etree.ElementTree import fromstring, ElementTree
import multiprocessing as mp
from server.database import do_insert_many, add_file
from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient

mongo_client = MongoClient('localhost', 27017)
db = mongo_client.file_manager
col = db.file_coll1

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

    file_list = [(name, myzip.read(name)) for name in myzip.namelist()]
    file_number = len(file_list)

    result_message = {'Rendered Files': file_number, 'Message': 'Ok' if file_number > 0 else 'Error' }

    render_files(file_list)


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


def render_files(files_list):
    # for file in files_dict:
    #     print(file)
    
    with mp.Pool() as pool:
        res = pool.map(render_file_data, files_list[4:7])
        col.insert_many(res)
    
    # print('res: ', res[0])
    # json_data = json.dumps(res)
    # json_data)


def render_file_data(xml_tuple):
    tree=tree=ElementTree(fromstring(xml_tuple[1]))
    root=tree.getroot()
    data = {}

    # extract title
    title = root.find('.//invention-title')
    if title:
        data['file_title'] = title.text
    else:
        data['file_title'] = None

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

    data['file_name'] = xml_tuple[0]

    return data


def parseXmlToJson(xml):
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