from functools import reduce
from typing import Generator, Sequence, Callable, T, Any


class Pipeline:
    def __init__(self, tasks: Sequence[Callable[[T], Any]]):
        self.__tasks: Sequence[Callable[[T], Any]] = tasks

    def apply_to(self, values: Sequence[Any]) -> Generator[Any, None, None]:
        """
            Apply a pipeline of functions to some sequence of data
        """
        def run(data: T, func: Callable[[T], Any]): return func(data)

        return (
            reduce(run, self.__tasks, value)
            for value in values
        )


def example():
    tasks = (hex, str)
    data = [1, 2, 3, 4]
    pipe = Pipeline(tasks).apply_to(data)

    for result in pipe:
        print(result)


if __name__ == "__main__":
    example()
