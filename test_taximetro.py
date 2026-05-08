from taximetro import calculate_fare


def test_only_stopped_time():
    result = calculate_fare(10, 0)

    assert result == 0.20


def test_only_moving_time():
    result = calculate_fare(0, 10)

    assert result == 0.50