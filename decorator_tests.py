def give_me_burgers(func_in):
    arg1 = "yum"    
    def out_fun(*args, **kwargs):
        args = args + (f"I like burgers, {arg1}",)
        func_in(*args, **kwargs)
    return out_fun

       
@give_me_burgers
def x(a, b, c, burgers):
    print(burgers)


@give_me_burgers
def y(b, burgers):
    print(f"{b} - {burgers}")


x(1,2,3)
y("yes")
