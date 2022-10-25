import pytest
from app.calcs import add


@pytest.mark.parametrize("num1, num2, result", [(5, 4, 9)])
def test_add(num1, num2, result):
    print('testing add')

    assert add(num1, num2) == result
