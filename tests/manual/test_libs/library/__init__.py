class ComplicatedObject:
    var = 0

    def set(self, v):
        self.var = v

    def get(self):
        return self.var


def create_complicated_object():
    return ComplicatedObject()


def set_co(co, v):
    co.set(v)


def get_co(co):
    return co.get()


def do_something(action):
    print("Do ", action)


def get_double(number):
    return number * 2
