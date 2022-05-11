from behaviour_tree.tree import Selector, Sequence, Status, While, Repeat, Not, Random


def mock_status(status):
    def _mock_status(x=None):
        def __mock_status():
            return status, status

        __mock_status.__name__ = str(x)
        return __mock_status

    return _mock_status


doSuccess = mock_status(Status.SUCCESS)
doFailure = mock_status(Status.FAILURE)
doRunning = mock_status(Status.RUNNING)


def test_selector():
    s = Selector(doFailure(0), doFailure(1), doFailure(2))
    result, status = s()
    assert status == Status.FAILURE
    assert len(result) == 3

    s = Selector(doFailure(0), doSuccess(1), doFailure(2))
    result, status = s()
    assert status == Status.SUCCESS
    assert len(result) == 2

    s = Selector(doSuccess(0), doSuccess(1), doSuccess(2))
    result, status = s()
    assert status == Status.SUCCESS
    assert len(result) == 1

    s = Selector(doRunning(0), doFailure(1), doFailure(2))
    result, status = s()
    assert status == Status.RUNNING
    assert len(result) == 1


def test_sequence():
    s = Sequence(doFailure(0), doFailure(1), doFailure(2))
    result, status = s()
    assert status == Status.FAILURE
    assert len(result) == 1

    s = Sequence(doSuccess(0), doSuccess(1), doFailure(2))
    result, status = s()
    assert status == Status.FAILURE
    assert len(result) == 3

    s = Sequence(doSuccess(0), doSuccess(1), doSuccess(2))
    result, status = s()
    assert status == Status.SUCCESS
    assert len(result) == 3

    s = Sequence(doSuccess(0), doRunning(1), doRunning(2))
    result, status = s()
    assert status == Status.RUNNING
    assert len(result) == 2


def test_random():
    s = Random(doSuccess(0), doFailure(1), weights=[0, 1])
    result, status = s()
    assert status == Status.FAILURE
    assert result == Status.FAILURE

    s = Random(doSuccess(0), doSuccess(1), doFailure(1), weights=[0, 1, 0])
    result, status = s()
    assert status == Status.SUCCESS
    assert result == Status.SUCCESS


def test_repeat():
    s = Repeat(doSuccess(0), n=3)
    result, status = s()
    assert status == Status.SUCCESS
    assert len(result) == 3

    s = Repeat(doFailure(0), n=3)
    result, status = s()
    assert status == Status.FAILURE
    assert len(result) == 1


def test_while():
    x = 0

    def cond():
        nonlocal x
        b = x < 3
        x += 1
        return b

    s = While(doSuccess(0), condition=cond)
    result, status = s()
    assert status == Status.SUCCESS
    assert len(result) == 3


def test_not():
    s = Not(doSuccess(0))
    result, status = s()
    assert status == Status.FAILURE

    s = Not(doFailure(0))
    result, status = s()
    assert status == Status.SUCCESS


def test_get_first_task():
    s = Selector(doFailure(0), Selector(doFailure(2), doFailure(3), doSuccess(4)), doSuccess(5), doRunning(1))
    s()
    assert s.get_first_task(Status.FAILURE).__name__ == '0'
    assert s.get_first_task(Status.SUCCESS).__name__ == '4'
    assert s.get_first_task(Status.FAILURE, reverse=True).__name__ == '3'

    s = Sequence(doSuccess(0), Selector(doFailure(2), doRunning(3), doSuccess(4)), doFailure(5))
    s()
    assert s.get_first_task(Status.SUCCESS).__name__ == '0'
    assert s.get_first_task(Status.FAILURE).__name__ == '2'
    assert s.get_first_task(Status.RUNNING, reverse=True).__name__ == '3'
