from models.http_response_model import HttpResponse


def test_http_response_conversion_to_json():
    data = [{"id": 1, "title": "Test Item"}, {"id": 2, "title": "Another"}]
    message = "Success"
    response = HttpResponse(message=message, data=data)

    json_output = response.convert_to_json()

    assert isinstance(json_output, dict)
    assert json_output["message"] == message
    assert json_output["data"] == data