from enum import Enum


class Status(Enum):
    SUCCESS = 0
    FAILURE = 1
    RUNNING = 2


class Tree:
    def __init__(self, tasks, name=""):
        self.tasks = tasks
        self.__name__ = name

    def __call__(self):
        return self.run()

    def run(self):
        return Status.SUCCESS

    def run_task(self, task, *args, **kwargs):
        result = task(*args, **kwargs)
        return result, result


class Sequence(Tree):
    def run(self):
        results = []
        for task in self.tasks:
            result, status = self.run_task(task)
            results.append(result)

            print(f"sequence {self.__name__} at {task.__name__} with status {status}")

            if status != Status.SUCCESS:
                return results, status

        return results, Status.SUCCESS


class Selector(Tree):
    def run(self):
        results = []
        for task in self.tasks:
            result, status = self.run_task(task)
            results.append(result)

            print(f"selector {self.__name__} at {task.__name__} with status {status}")

            if status != Status.FAILURE:
                return results, status

        return results, Status.FAILURE

