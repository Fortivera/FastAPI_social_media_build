from app.calcs import add


def test_add():
    print('testing add')
    sum = add(5, 4)
    assert sum == 8
