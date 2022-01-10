from bson.objectid import ObjectId
import motor.motor_asyncio

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.file_manager

file_collection = database.get_collection("file_collection")


def xmldata_helper(xmldata) -> dict:
    return {
        "id": str(xmldata["_id"]),
        "title": xmldata["title"],
        "description": xmldata["description"],
        "abstract": xmldata["abstract"],
        "publication_year": xmldata["publication_year"],
        "application": xmldata["application"],
    }


# Retrieve all files present in the database
async def retrieve_files():
    files_data = []
    async for file in file_collection.find():
        files_data.append(xmldata_helper(file))
    return files_data


# Delete a file record from the database
async def delete_file(id: str):
    file = await file_collection.find_one({"_id": ObjectId(id)})
    if file:
        await file_collection.delete_one({"_id": ObjectId(id)})
        return True