

class A:
    def __init__(self, x) -> None:
        super().__init__()
        self.x = x



class B:
    def __init__(self, x) -> None:
        super().__init__()
        self.x = x


class C:
    def __init__(self, x) -> None:
        super().__init__()
        self.x = x

    def print(self):
        return self.x.x

a = A(10)
b = B(11)
c = C(b)
c.print()
