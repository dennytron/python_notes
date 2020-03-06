def add_param(argument):
    def _decor(func):
        def _wrapper(*args, **kwargs):
            return func(argument, *args, **kwargs)
        return _wrapper
    return _decor

@add_param("merci")
def main(p1, p2, p3):
    print(p1)
    print(p2)
    print(p3)

main("gagablagblag", "blagy")
