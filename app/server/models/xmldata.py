from typing import Optional


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