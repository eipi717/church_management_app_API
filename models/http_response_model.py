# Use this to transform the dict to serialized JSON
from fastapi.encoders import jsonable_encoder


class HttpResponse:
    message: str
    data: list[dict]

    def __init__(self, message: str, data: list[dict]):
        self.message = message
        self.data = data

    def convert_to_json(self):
        result_in_dict = {
            'message': self.message,
            'data': self.data
        }

        return jsonable_encoder(result_in_dict)

