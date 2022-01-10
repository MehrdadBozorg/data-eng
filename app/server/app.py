from fastapi import FastAPI

from logic.logic import read_files

app = FastAPI()


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}


@app.get("/files/", response_description="File names")
async def read_blob(url: str):
    # Add your code in multiprocessing and...
    # Use Pymongo and Bul insert
    # Better to call function in a logic module. So create this folder.

    result = read_files(url)
    return result