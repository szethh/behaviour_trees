from tree import Selector, Sequence, Status, While, Repeat, Not, Random


def mock_status(status):
    def _mock_status(x):
        def __mock_status():
            return x, status

        return __mock_status

    return _mock_status


doSuccess = mock_status(Status.SUCCESS)
doFailure = mock_status(Status.FAILURE)
doRunning = mock_status(Status.RUNNING)


def test_selector():
    s = Selector([doFailure(0), doFailure(1), doFailure(2)])
    result, status = s()
    assert status == Status.FAILURE
    assert result == [0, 1, 2]

    s = Selector([doFailure(0), doSuccess(1), doFailure(2)])
    result, status = s()
    assert status == Status.SUCCESS
    assert result == [0, 1]

    s = Selector([doSuccess(0), doSuccess(1), doSuccess(2)])
    result, status = s()
    assert status == Status.SUCCESS
    assert result == [0]

    s = Selector([doRunning(0), doFailure(1), doFailure(2)])
    result, status = s()
    assert status == Status.RUNNING
    assert result == [0]


def test_sequence():
    s = Sequence([doFailure(0), doFailure(1), doFailure(2)])
    result, status = s()
    assert status == Status.FAILURE
    assert result == [0]

    s = Sequence([doSuccess(0), doSuccess(1), doFailure(2)])
    result, status = s()
    assert status == Status.FAILURE
    assert result == [0, 1, 2]

    s = Sequence([doSuccess(0), doSuccess(1), doSuccess(2)])
    result, status = s()
    assert status == Status.SUCCESS
    assert result == [0, 1, 2]

    s = Sequence([doSuccess(0), doRunning(1), doRunning(2)])
    result, status = s()
    assert status == Status.RUNNING
    assert result == [0, 1]


def test_random():
    s = Random([doSuccess(0), doFailure(1)], weights=[0, 1])
    result, status = s()
    assert status == Status.FAILURE
    assert result == 1

    s = Random([doSuccess(0), doSuccess(1), doFailure(1)], weights=[0, 1, 0])
    result, status = s()
    assert status == Status.SUCCESS
    assert result == 1


def test_repeat():
    s = Repeat([doSuccess(0)], n=3)
    result, status = s()
    assert status == Status.SUCCESS
    assert result == [0, 0, 0]

    s = Repeat([doFailure(0)], n=3)
    result, status = s()
    assert status == Status.FAILURE
    assert result == [0]


def test_while():
    x = 0

    def cond():
        nonlocal x
        b = x < 3
        x += 1
        return b

    s = While([doSuccess(0)], condition=cond)
    result, status = s()
    assert status == Status.SUCCESS
    assert result == [0, 0, 0]


def test_not():
    s = Not([doSuccess(0)])
    result, status = s()
    assert status == Status.FAILURE

    s = Not([doFailure(0)])
    result, status = s()
    assert status == Status.SUCCESS
