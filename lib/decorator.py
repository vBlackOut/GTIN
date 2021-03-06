def decorator_except_stringdigital(function):
    def new_function(*args, **kwargs):
        if type(args[1]) == str:
            if not args[1].isdigit():
                return False
            function_return = function(*args, **kwargs)
            return function_return
        else:
            return False
    return new_function
