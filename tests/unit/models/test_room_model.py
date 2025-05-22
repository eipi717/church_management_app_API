from models.room_model import Room
import datetime


def test_transform_to_dict_returns_correct_keys_and_values():
    now = datetime.date.today()
    room = Room(
        room_id=101,
        room_name="Main Hall",
        room_description="Large event space",
        room_capacity=200,
        room_is_booked=True
    )
    room.room_created_at = now
    room.room_last_updated_at = now

    result = room.transform_to_dict()

    assert isinstance(result, dict)
    assert result["room_id"] == 101
    assert result["room_name"] == "Main Hall"
    assert result["room_description"] == "Large event space"
    assert result["room_capacity"] == 200
    assert result["room_is_booked"] is True
    assert result["room_created_at"] == now
    assert result["room_last_updated_at"] == now