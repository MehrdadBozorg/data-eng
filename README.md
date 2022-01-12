# Rendering XML Files

This is a restful API, over Python and MongoDB to retrieve and save data from xml files which are store as zip file on a Microsoft Azure Blob.

## Tech stack

The rest application has been implemented over [FastAPI](https://fastapi.tiangolo.com/) framework. The reason is the lower load of this library and its support for concurrent I/O and processor's operation. 

The concurrency is happening in the time of extracting data by multiprocessing (applied by multiprocessing library). It makes the application fast and scalable by increasing the number of files in each blob.

To cover the scalability in the number of blobs, asyncio (kind of threading) approach can be used. However, in this task we have just one url and one blob.

Saving files in database is done with one insertion, which does not need any parallelization. However, to handle the user interactions with database (retrieving and deleting file records), I got benefited from motor library to support [asyncio](https://docs.python.org/3.8/library/asyncio.html).

I used MongoDB in this application, to support schema flexibility in expansion.

Unzipping the blob is done in memory (and not in disk) to prevent extra I/O operations.
 

## Installation

Find the requirements.txt, and use the package manager [pip](https://pip.pypa.io/en/stable/) to install application.

```bash
pip install -r requirements.txt 
```
#### prerequisite

Make sure that Mongodb has been already installed on your system. 

## Contributing
Because of the lack of time, I didn't prepared testing for application. Any contribution to add testing is appreciated.
