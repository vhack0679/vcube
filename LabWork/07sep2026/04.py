def ascendingorder(fun):
    def wrapper(lst):
        alst = fun(lst)
        alst.sort()
        return alst
    return wrapper


def descendingorder(fun):
    def wrapper(lst):
        dlst = fun(lst)
        dlst.sort(reverse=True)
        return dlst
    return wrapper

@ascendingorder
@descendingorder
def lstreturn(lst):
    return lst


lst1 = [2, 3, 4, 1, 5,6]
res = lstreturn(lst1)
print(res)
