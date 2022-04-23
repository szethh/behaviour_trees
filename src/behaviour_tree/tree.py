from abc import ABC
from enum import Enum
import random


class Status(Enum):
    SUCCESS = 0
    FAILURE = 1
    RUNNING = 2


class Tree(ABC):
    END_STATUS = None

    def __init__(self, tasks, name=""):
        self.tasks = tasks
        self.__name__ = name

    def __call__(self):
        return self.run()

    def run(self):
        results = []
        for task in self.tasks:
            result, status = self.run_task(task)
            results.append(result)

            if status != self.END_STATUS:
                return results, status

        return results, self.END_STATUS

    @staticmethod
    def run_task(task):
        result = task()
        if isinstance(result, tuple):
            return result[0], result[1]
        return result, result


class Sequence(Tree):
    """
    Runs all tasks until one succeeds.
    """
    END_STATUS = Status.SUCCESS


class Selector(Tree):
    """
    Runs all tasks that succeed.
    """
    END_STATUS = Status.FAILURE


class Repeat(Tree):
    def __init__(self, tasks, n, name=""):
        super().__init__(tasks, name)
        self.n = n

    def run(self):
        results = []
        for _ in range(self.n):
            result, status = self.run_task(self.tasks[0])
            results.append(result)
            if status == Status.FAILURE:
                return results, Status.FAILURE
        return results, Status.SUCCESS


class While(Tree):
    def __init__(self, tasks, condition, name=""):
        super().__init__(tasks, name)
        self.condition = condition

    def run(self):
        results = []
        while self.condition():
            result, status = self.run_task(self.tasks[0])
            results.append(result)
            if status == Status.FAILURE:
                return results, Status.FAILURE
        return results, Status.SUCCESS


class Not(Tree):
    def run(self):
        result, status = self.tasks[0]()
        return result, Status(not bool(status.value))


class Random(Tree):
    def __init__(self, tasks, name="", weights=None):
        super().__init__(tasks, name)
        self.weights = weights

    def run(self):
        t = random.choices(self.tasks, weights=self.weights)[0]
        return t()
