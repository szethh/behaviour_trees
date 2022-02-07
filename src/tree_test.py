from tree import Selector, Sequence, Status

doSuccess = lambda: Status.SUCCESS
doFailure = lambda: Status.FAILURE
doRunning = lambda: Status.RUNNING

def a(): return Status.SUCCESS
def b(): return Status.FAILURE
def c(): return Status.RUNNING


tree = Selector([
    b,
    Sequence([a, b, a], "choice"),
    c,
    a
], "head")

result = tree()

print(f'The result was {result}')

