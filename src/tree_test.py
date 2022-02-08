from tree import Selector, Sequence, Status, Action

doSuccess = lambda: Status.SUCCESS
doFailure = lambda: Status.FAILURE
doRunning = lambda: Status.RUNNING


def a(): return Status.SUCCESS
def b(): return Status.FAILURE
def c(): return Status.RUNNING
def greater_than_5(x): return Status.SUCCESS if x > 5 else Status.FAILURE
def returns_10(): return 10, Status.SUCCESS
def returns_3(): return 3, Status.SUCCESS


tree = Selector([
    b,
    Sequence([
        a,
        b
    ], "choice"),
    Sequence([
        Action(task=returns_10),
        Action(task=greater_than_5)
    ], "hehhahe"),
    a
], "head")

result, status = tree()

print(f'\nThe final status was {status}, and the result was {result}')

