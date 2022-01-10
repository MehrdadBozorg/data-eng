from typing import Optional

from pydantic import BaseModel, Field


class FileSchema(BaseModel):
    title: str = Field
    description: str = Field
    abstract: str = Field
    publication_year: int = Field
    application: list = []

    class Config:
        schema_extra = {
            "example": {
                "title": "title",
                "description": "description",
                "abstract": "abstract",
                "publication_year": 2022,
                "application": [
                    {'document-id': [
                        {'country': ['US'
                                     ], 'doc-number': ['08631885'
                                                       ], 'kind': ['A'
                                                                   ], 'date': ['19960416'
                                                                               ]
                         },
                        {'doc-number': ['1996US-08631885'
                                        ]
                         },
                        {'doc-number': ['68290266'
                                        ]
                         }
                    ]
                    }
                ]
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