import time


def time_measure_decorator(f):
    def wrapper(*args):
        s = time.time()
        r = f(*args)
        e = time.time()
        print(f"time : {e-s}")
        return r
    return wrapper


@time_measure_decorator
def one_to_n_loop(n):
    result = 0
    for i in range(1, n+1):
        result = result + i
    return result


def ont_to_n_math(n):
    r = n * (n + 1) // 2
    return r


number = int(input("Input number : "))
func = time_measure_decorator(ont_to_n_math)
print(func(number))
print(one_to_n_loop(number))