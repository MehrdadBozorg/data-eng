from bson.objectid import ObjectId
import motor.motor_asyncio

"""
Manage REST application transactions. 
"""

# DB Connection info
MONGO_DETAILS = "mongodb://localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.file_manager
file_collection = database.get_collection("file_collection")


def xmldata_helper(xmldata: dict) -> dict:
    """
    Helper function to render file data in well-defined json schema.

    :rturn, the the data as a json (dictionary) with wel-defined schema.
    """
    return {
        "id": str(xmldata["_id"]),
        "patent_title": xmldata["patent_title"],
        "description": xmldata["description"],
        "abstract": xmldata["abstract"],
        "publication_year": xmldata["publication_year"],
        "application": xmldata["application"],
        "file_name": xmldata["file_name"],
    }


async def retrieve_files() -> list:
    """
    Retrieve list of all files' records present in the database.

    :return, the list of retrieved files; data as a lis of jsons(dictionaries).
    """
    files_data = []
    async for file in file_collection.find():
        files_data.append(xmldata_helper(file))
    return files_data


async def retrieve_file(title: str) -> dict:
    """
    Retrieve record of file with a matching title.

    :return, the retrieved file data as json(dictionary).
    """
    file = await file_collection.find_one({"file_title": title})
    if file:
        return xmldata_helper(file)


async def delete_file(id: str) -> bool:
    """
    Delete a file record from the database by getting its id.

    :return, True if it's deleted successfully and no return value (None) otherwise.
    """
    file = await file_collection.find_one({"_id": ObjectId(id)})
    if file:
        await file_collection.delete_one({"_id": ObjectId(id)})
        return True