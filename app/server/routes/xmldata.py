from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import (
    delete_file,
    retrieve_file,
    retrieve_files,
    add_file
)
from server.models.xmldata import (
    ErrorResponseModel,
    ResponseModel,
    FileSchema,
)

router = APIRouter()


@router.get("/", response_description="Files retrieved")
async def get_files():
    files = await retrieve_files()
    if files:
        return ResponseModel(files, "Files data retrieved successfully")
    return ResponseModel(files, "Empty list returned")


@router.get("/{title}", response_description="File data retrieved")
async def get_file_data(title):
    file = await retrieve_file(title)
    if file:
        return ResponseModel(file, "File data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "File doesn't exist.")


@router.post("/", response_description="File data added into the database")
async def add_file_data(file: FileSchema = Body(...)):
    file = jsonable_encoder(file)
    new_file = await add_file(file)
    return ResponseModel(new_file, "File added successfully.")


@router.delete("/{id}", response_description="File data deleted from the database")
async def delete_file_data(id: str):
    deleted_file = await delete_file(id)
    if deleted_file:
        return ResponseModel(
            "File with ID: {} removed".format(id), "File deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "File with id {0} doesn't exist".format(id)
    )