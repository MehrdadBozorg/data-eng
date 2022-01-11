from fastapi import FastAPI
from server.routes.xmldata import router as FileRouter
from logic.logic import read_files

app = FastAPI()

# Add the route to file GRUD to the main app.
app.include_router(FileRouter, tags=["Files"], prefix="/file")


@app.get("/", response_description="File names")
async def read_blob(url: str) -> tuple:
    """
    Get the url string (addressing the azure blob), render file data and return a message which indicates the status of response 
    and the number of rendered files.
    """

    return read_files(url)