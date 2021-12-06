import time
import random


def timer(func):
    def timed(*args, **kwargs):

        if 'n' in kwargs:
            times = []
            for i in range(kwargs.get('n')):
                start = time.time()
                result = func(*args, **kwargs)
                stop = time.time()
                times.append(stop-start)
            mean = sum(times) / len(times)
            print(f"Mean time of {kwargs.get('n')} executions: {mean} s")
        else:
            start = time.time()
            result = func(*args, **kwargs)
            stop = time.time()
            duration = stop - start
            print(f"Time of execution: {duration} s")

        return result
    return timed


@timer
def function(**kwargs):
    lap = random.random()
    time.sleep(lap)
    print("Boop")


function(n=20)
# function()
