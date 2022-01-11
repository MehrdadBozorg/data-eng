from typing import Optional
from pydantic import BaseModel, Field


class FileSchema(BaseModel):
    """
    Schema for file records, that contain all demanded fields. All fields are optional instead of file_name. 
    The not existent fields (tags), in each documents are field by None automatically. 
    """
    patent_title: Optional[str] 
    description: Optional[str] 
    abstract: Optional[str] 
    publication_year: Optional[int] 
    application: Optional[list]  
    file_name: str = Field(...)

    class Config:
        """
        Define the examplary format of one record.
        """
        schema_extra = {
            "example": {
                "patent_title": "Patent Name",
                "description": "Patent Description",
                "abstract": "Patent abstract",
                "publication_year": 2022,
                "application": ["tag1", "tag2"],
                "file_name": "example.xml"
            }
        }


def ResponseModel(data: dict, message: str) -> dict:
    """
    Indicating the response format.

    :return, a json in response to requests, that contains data, status code and the generated message. 
    """
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    """
    Indicating the error format.

    :return, a json showing error in response to requests, that contains error detail, status code and the generated message. 
    """

    return {"error": error, "code": code, "message": message}