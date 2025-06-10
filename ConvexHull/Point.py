
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
    def __mul__(self, other):
        return self.x * other.y - self.y * other.x



n = int(input())
points = []
for i in range(n):
    coord = list(map(int, input().split()))
    points.append(Point(coord[0], coord[1]))


