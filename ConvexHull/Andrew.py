
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


def orientation(a, b, c):
    val = (b - a) * (c - a)
    if val < 0:
        return -1
    elif val > 0:
        return 1
    return 0


def Andrew(points):
    n = len(points)

    if n < 3:
        return -1

    points = sorted(points, key=lambda p: (p.x, p.y))
    hull1 = [points[0]]
    hull2 = [points[0]]
    for i in range(n):
        if orientation(points[0], points[-1], points[i]) == 1:
            while len(hull1) > 1 and orientation(hull1[-2], hull1[-1], points[i]) >= 0:
                hull1.pop()
            hull1.append(points[i])
        if orientation(points[0], points[-1], points[i]) == -1:
            while len(hull2) > 1 and orientation(hull2[-2], hull2[-1], points[i]) <= 0:
                hull2.pop()
            hull2.append(points[i])
    convex_hull = hull1 + [points[-1]] + hull2[1:][::-1]
    if len(convex_hull) < 3:
        return [[-1]]
    return convex_hull


convexHull = Andrew(points)
if len(convexHull) == 1 and convexHull[0][0] == -1:
    print(-1)
else:
    for point in convexHull:
        print(f"{point.x}, {point.y}")
