from models.http_response_model import HttpResponse


def empty_response(message: str):
    return HttpResponse(message=message, data=[]).convert_to_json()


def response_with_data(data):
    return HttpResponse(message='', data=data).convert_to_json()