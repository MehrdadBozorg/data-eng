from bson.objectid import ObjectId
import motor.motor_asyncio

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.file_manager

file_collection = database.get_collection("file_collection")


def xmldata_helper(xmldata) -> dict:
    return {
        "id": str(xmldata["_id"]),
        "patent_title": xmldata["patent_title"],
        "description": xmldata["description"],
        "abstract": xmldata["abstract"],
        "publication_year": xmldata["publication_year"],
        "application": xmldata["application"],
        "file_name": xmldata["file_name"],
    }


# Add a new file into to the database
async def insert_one_file(file_data: dict) -> dict:
    file = await file_collection.insert_one(file_data)
    new_file = await file_collection.find_one({"_id": file.inserted_id})
    return xmldata_helper(new_file)


# Retrieve all files present in the database
async def retrieve_files():
    files_data = []
    async for file in file_collection.find():
        files_data.append(xmldata_helper(file))
    return files_data


# Retrieve a file with a matching title
async def retrieve_file(title: str) -> dict:
    file = await file_collection.find_one({"title": title})
    if file:
        return xmldata_helper(file)


# Delete a file record from the database
async def delete_file(id: str):
    file = await file_collection.find_one({"_id": ObjectId(id)})
    if file:
        await file_collection.delete_one({"_id": ObjectId(id)})
        return True