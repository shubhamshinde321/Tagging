


def new_decorators(func):
    def inbound_func():
        print('Processing Started')
        func()
        print('Processing Stopped')

    return inbound_func

@new_decorators
def deocrator_needed():
    print('Decorator Needed')

# deocrator_needed = new_decorators(deocrator_needed)
deocrator_needed()
