import time
from concurrent import futures
from os import cpu_count, getpid
from random import getrandbits, choice


def rando(x):
    print(f"work = {x}, pid = {getpid()}")
    return sum(getrandbits(1) for _ in range(x))


def main():
    chunks = cpu_count()
    total_work = 1000000000
    work = (int(total_work / chunks),) * chunks

    with futures.ProcessPoolExecutor() as executor:
        totes = sum(executor.map(rando, work))

    print(totes / total_work)


if __name__ == "__main__":
    print(f"cpu_count = {cpu_count()}")

    t = time.perf_counter()
    main()
    a = time.perf_counter()

    print(a - t)
