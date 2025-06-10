import math

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

    def get_angle(self):
        return math.atan2(self.y, self.x)

    def __mul__(self, other):
        return self.x * other.y - self.y * other.x

n = int(input())
points = []
for i in range(n):
    coord = list(map(int, input().split()))
    points.append(Point(coord[0], coord[1]))

def orientation(a, b, c):
    val = (b - a) * (c - a)
    if val < 0:
        return -1
    elif val > 0:
        return 1 #значение для принятия новой точки в оболочку
    return 0

def Graham(points):
    n = len(points)

    if n < 3:
        return -1

    p0 = min(points, key=lambda p: (p.y, p.x))
    points_sorted = sorted(points, key=lambda x: (x - p0).get_angle()) #сортируем по полярному углу относительно начальной точки

    m = 1
    for i in range(1, len(points_sorted)):
        while i < len(points_sorted) - 1 and orientation(p0, points_sorted[i], points_sorted[i+1]) == 0:
            i += 1
        points_sorted[m] = points_sorted[i]
        m += 1

    if m < 3:
        return -1

    stack = [points_sorted[0], points_sorted[1]]

    for i in range(2, m):
        while len(stack) > 1 and orientation(stack[-2], stack[-1], points_sorted[i]) <= 0:
            stack.pop()
        stack.append(points_sorted[i])

    if len(stack) < 3:
        return [[-1]]

    return [[int(p.x), int(p.y)] for p in stack]

convexHull = Graham(points)
if len(convexHull) == 1 and convexHull[0][0] == -1:
    print(-1)
else:
    for point in convexHull:
        print(f"{point[0]}, {point[1]}")
