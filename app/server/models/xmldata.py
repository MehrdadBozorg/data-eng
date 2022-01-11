from typing import Optional

from pydantic import BaseModel, Field


class FileSchema(BaseModel):
    file_title: Optional[str] 
    description: Optional[str] 
    abstract: Optional[str] 
    publication_year: Optional[int] 
    application: Optional[list]  
    file_name: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "file_title": "John Doe",
                "description": "jdoe@x.edu.ng",
                "abstract": "Water resources engineering",
                "publication_year": 2,
                "application": ["3.0"],
                "file_name": "example.xml"
            }
        }



def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}