from enum import Enum


class Status(Enum):
    SUCCESS = 0
    FAILURE = 1
    RUNNING = 2


class Action:
    def __init__(self, name="", task=None):
        self.task = task if task else self.run
        self.__name__ = task.__name__ if name is "" else name

    def __call__(self):
        return self.task()

    def run(self, *args, **kwargs):
        return Status.SUCCESS


class Tree(Action):
    def __init__(self, tasks, name=""):
        super().__init__(name=name)
        self.tasks = tasks

    def run_task(self, task, *args, **kwargs):
        result = task(*args, **kwargs)
        if isinstance(task, Action):  # for actions
            return result
        return result, Status.FAILURE  # for regular functions


class Sequence(Tree):
    def run(self, *args, **kwargs):
        results = []
        for task in self.tasks:
            # pass results[-1:] to *args
            result, status = self.run_task(task, *[*args, results[-1:]], **kwargs)
            results.append(result)

            print(f"sequence {self.__name__} at {task.__name__} with status {status} and result {result}")

            if status != Status.SUCCESS:
                return results, status

        return results, Status.SUCCESS


class Selector(Tree):
    def run(self, *args, **kwargs):
        results = []
        for task in self.tasks:
            result, status = self.run_task(task, *args, **kwargs)
            results.append(result)

            print(f"selector {self.__name__} at {task.__name__} with status {status} and result {result}")

            if status != Status.FAILURE:
                return results, status

        return results, Status.FAILURE

