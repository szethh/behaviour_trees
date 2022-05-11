from abc import ABC
from enum import Enum
import random


class Status(Enum):
    FAILURE = 0
    SUCCESS = 1
    RUNNING = 2

    def __bool__(self):
        return bool(self.value)


class Tree(ABC):
    END_STATUS = None

    def __init__(self, *args, name=""):
        self.tasks = list(args)
        self.__name__ = name
        self.results = []

    def __call__(self):
        return self.run()

    def __str__(self):
        return f'{self.__class__.__name__} {self.__name__}'

    def result_names(self):
        return [r.__name__ for r in self.results]

    def run(self):
        self.results = []
        for task in self.tasks:
            result, status = self.run_task(task)
            self.results.append(result)

            if status != self.END_STATUS:
                return self.results, status

        return self.results, self.END_STATUS

    def get_first_task(self, status=None, reverse=False):
        if status is None:
            status = self.END_STATUS or Status.SUCCESS
        rn = range(len(self.results)-1, -1, -1) if reverse else range(len(self.results))
        for i in rn:
            if isinstance(self.tasks[i], Tree):
                s = self.tasks[i].get_first_task(status, reverse)
                if s:
                    return s
            else:
                if self.results[i] == status:
                    return self.tasks[i]

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
    def __init__(self, *args, n=1, name=""):
        super().__init__(*args, name=name)
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
    def __init__(self, *args, condition, name=""):
        super().__init__(*args, name=name)
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
        result, status = self.run_task(self.tasks[0])
        return result, Status(not bool(status))


class Random(Tree):
    def __init__(self, *args, name="", weights=None):
        super().__init__(*args, name=name)
        self.weights = weights

    def run(self):
        t = random.choices(self.tasks, weights=self.weights)[0]
        return self.run_task(t)
