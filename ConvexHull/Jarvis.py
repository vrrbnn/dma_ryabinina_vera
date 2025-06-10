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


def start_point(points):
    mn = 0
    for i in range(1, len(points)):
        if points[i].x < points[mn].x:
            mn = i
        elif points[i].x == points[mn].x:
            if points[i].y > points[mn].y:
                mn = i
    return mn

def orientation(p, q, r):
    vector_product = (q-p)*(r-p)
    if vector_product == 0:
        return 0
    elif vector_product > 0:
        return 1 #значение для принятия точки в оболочку
    else:
        return 2

def Jarvis(points, n):
    if n < 3:
        return
    l = start_point(points)

    hull = []

    p = l
    q = 0
    while True:
        hull.append(p)
        q = (p + 1) % n
        for i in range(n):
            if orientation(points[p], points[i], points[q]) == 1:
                q = i
        p = q
        if p == l:
            break

    for point in hull:
        print(points[point].x, points[point].y)


convexHull = Jarvis(points, n)

