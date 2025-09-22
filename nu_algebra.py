class NU:
    def __init__(self, n, u):
        self.n = n
        self.u = u
    def __repr__(self):
        return f"({self.n}, {self.u})"
    def add(self, other):
        return NU(self.n + other.n, self.u + other.u)
    def mul(self, other):
        return NU(self.n * other.n, self.n * other.u + other.n * self.u)
    def scalar(self, a):
        return NU(a * self.n, abs(a) * self.u)
# Example usage:
x = NU(10, 1)
y = NU(5, 0.5)
print("x + y =", x.add(y))
print("x * y =", x.mul(y))
print("2 * x =", x.scalar(2))
