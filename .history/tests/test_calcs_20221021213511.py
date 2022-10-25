import pytest
from app.calcs import add


@pytest.mark.parametrize("num1, num2, result", [(5, 4, 9)])
def test_add():
    print('testing add')
    sum = add(5, 4)
    assert sum == 9
