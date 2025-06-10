import matplotlib.pyplot as plt

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

    def __str__(self):
        return f'({self.x}, {self.y})'

def orientation(a, b, c):
    val = (b - a) * (c - a)

    if val < 0:
        return -1
    elif val > 0:
        return 1
    return 0
def Andrew(points_raw):
    n = len(points_raw)

    if n < 3:
        print("Для построения выпуклой оболочки требуется не менее 3 точек.")
        return [[-1]]

    points = [Point(p[0], p[1]) for p in points_raw]


    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_title("Алгоритм Эндрю: Построение Выпуклой Оболочки")
    ax.set_xlabel("X-координата")
    ax.set_ylabel("Y-координата")
    ax.grid(True)
    ax.set_aspect('equal', adjustable='box')

    all_x = [p.x for p in points]
    all_y = [p.y for p in points]
    ax.scatter(all_x, all_y, color='blue', zorder=2, label="Исходные точки")
    for i, p in enumerate(points):
        ax.text(p.x + 0.1, p.y + 0.1, f'P{i}', fontsize=9, color='blue')

    plt.pause(3)
    print("Шаг 1: Исходные точки на графике.")

    points_sorted_lex = sorted(points, key=lambda p: (p.x, p.y))
    print("Шаг 2: Точки отсортированы лексикографически (по X, затем по Y).")

    for text in list(ax.texts):
        text.remove()
    for collection in ax.collections:
        collection.remove()

    ax.scatter(all_x, all_y, color='blue', zorder=2)

    sorted_x = [p.x for p in points_sorted_lex]
    sorted_y = [p.y for p in points_sorted_lex]
    ax.plot(sorted_x, sorted_y, 'k--', alpha=0.5, label="Лексикографический порядок")
    for i, p in enumerate(points_sorted_lex):
        ax.text(p.x + 0.1, p.y + 0.1, f'Sorted {i}: {p}', fontsize=9, color='purple')
        ax.scatter(p.x, p.y, color='purple', s=30, zorder=3)
    plt.pause(3)
    print("Шаг 2 (продолжение): Визуализация отсортированных точек.")

    p_first = points_sorted_lex[0]
    p_last = points_sorted_lex[-1]
    for line in ax.lines[:]: line.remove()
    for collection in ax.collections[:]: collection.remove()
    for text in list(ax.texts): text.remove()
    ax.scatter(all_x, all_y, color='blue', zorder=2)

    ax.plot([p_first.x, p_last.x], [p_first.y, p_last.y], 'r--', alpha=0.7, linewidth=2, label="Разделительная линия (P_first - P_last)")
    ax.scatter(p_first.x, p_first.y, color='red', s=100, marker='*', zorder=3, label="P_first")
    ax.scatter(p_last.x, p_last.y, color='red', s=100, marker='X', zorder=3, label="P_last")
    plt.pause(3)
    print("Шаг 3: Начинаем построение верхней и нижней цепей.")
    print(f"P_first = {p_first}, P_last = {p_last}. Точки будут классифицироваться относительно этой линии.")

    hull1 = [points_sorted_lex[0]]
    hull2 = [points_sorted_lex[0]]


    hull1_line, = ax.plot([], [], 'g-', linewidth=2, zorder=4, label="Верхняя цепь")
    hull2_line, = ax.plot([], [], 'm-', linewidth=2, zorder=4, label="Нижняя цепь")


    ax.scatter(hull1[0].x, hull1[0].y, color='lightgreen', s=50, zorder=5)
    ax.scatter(hull2[0].x, hull2[0].y, color='violet', s=50, zorder=5)
    plt.pause(3)

    for i in range(n):
        current_point = points_sorted_lex[i]
        print(f"\n--- Обрабатываем точку {current_point} (индекс {i} в отсортированном списке) ---")

        if orientation(p_first, p_last, current_point) == 1 or current_point == p_first or current_point == p_last:
            print(f"   Точка {current_point} рассматривается для ВЕРХНЕЙ оболочки.")
            ax.scatter(current_point.x, current_point.y, color='green', s=100, marker='D', zorder=5)
            plt.pause(0.5)
            while len(hull1) > 1 and orientation(hull1[-2], hull1[-1], current_point) >= 0:
                p_to_pop = hull1[-1]
                orient_val = orientation(hull1[-2], p_to_pop, current_point)
                orient_desc = "по часовой стрелке" if orient_val == 1 else "коллинеарно"
                print(f"     Поворот {hull1[-2]} -> {p_to_pop} -> {current_point} {orient_desc}. Удаляем {p_to_pop} из hull1.")
                ax.scatter(p_to_pop.x, p_to_pop.y, color='red', s=150, marker='X', zorder=6)
                plt.pause(0.5)
                hull1.pop()
                hull1_line.set_xdata([p.x for p in hull1])
                hull1_line.set_ydata([p.y for p in hull1])
                plt.pause(0.5)

            print(f"     Добавляем {current_point} в hull1. Текущая hull1: {hull1 + [current_point]}.")
            hull1.append(current_point)
            hull1_line.set_xdata([p.x for p in hull1])
            hull1_line.set_ydata([p.y for p in hull1])
            ax.scatter([p.x for p in hull1[:-1]], [p.y for p in hull1[:-1]], color='lightgreen', s=50, zorder=5)
            ax.scatter(hull1[-1].x, hull1[-1].y, color='lightgreen', s=50, zorder=5)
            plt.pause(1)


        if orientation(p_first, p_last, current_point) == -1 or current_point == p_first or current_point == p_last:
            print(f"   Точка {current_point} рассматривается для НИЖНЕЙ оболочки.")
            ax.scatter(current_point.x, current_point.y, color='darkviolet', s=100, marker='D', zorder=5)
            plt.pause(0.5)

            while len(hull2) > 1 and orientation(hull2[-2], hull2[-1], current_point) <= 0:
                p_to_pop = hull2[-1]
                orient_val = orientation(hull2[-2], p_to_pop, current_point)
                orient_desc = "против часовой стрелки" if orient_val == -1 else "коллинеарно"
                print(f"     Поворот {hull2[-2]} -> {p_to_pop} -> {current_point} {orient_desc}. Удаляем {p_to_pop} из hull2.")
                ax.scatter(p_to_pop.x, p_to_pop.y, color='red', s=150, marker='X', zorder=6)
                plt.pause(0.5)
                hull2.pop()
                hull2_line.set_xdata([p.x for p in hull2])
                hull2_line.set_ydata([p.y for p in hull2])
                plt.pause(0.5)

            print(f"     Добавляем {current_point} в hull2. Текущая hull2: {hull2 + [current_point]}.")
            hull2.append(current_point)
            hull2_line.set_xdata([p.x for p in hull2])
            hull2_line.set_ydata([p.y for p in hull2])
            ax.scatter([p.x for p in hull2[:-1]], [p.y for p in hull2[:-1]], color='violet', s=50, zorder=5)
            ax.scatter(hull2[-1].x, hull2[-1].y, color='violet', s=50, zorder=5)
            plt.pause(1)

    print("\nШаг 4: Построение верхней и нижней оболочек завершено.")
    print(f"Финальная верхняя оболочка (hull1): {hull1}")
    print(f"Финальная нижняя оболочка (hull2): {hull2}")
    convex_hull = hull1 + hull2[1:-1][::-1]

    if len(convex_hull) < 3:
        print("Невозможно построить выпуклую оболочку (менее 3 уникальных вершин).")
        plt.show()
        return [[-1]]

    print(f"\nШаг 5: Оболочки объединены. Финальная выпуклая оболочка: {convex_hull}")

    for line in ax.lines[:]: line.remove()
    for collection in ax.collections[:]: collection.remove()
    for patch in ax.patches[:]: patch.remove()
    for text in list(ax.texts): text.remove()

    ax.scatter(all_x, all_y, color='blue', zorder=2, label="Исходные точки")
    ax.scatter(p_first.x, p_first.y, color='red', s=100, marker='*', zorder=3, label="P_first")
    ax.scatter(p_last.x, p_last.y, color='red', s=100, marker='X', zorder=3, label="P_last")

    final_hull_points_for_plot = convex_hull + [convex_hull[0]]
    final_hull_x = [p.x for p in final_hull_points_for_plot]
    final_hull_y = [p.y for p in final_hull_points_for_plot]
    ax.plot(final_hull_x, final_hull_y, 'r-', linewidth=3, zorder=5, label="Выпуклая оболочка")
    ax.scatter([p.x for p in convex_hull], [p.y for p in convex_hull], color='red', s=100, zorder=6)

    plt.legend()
    plt.show()

    return [[int(p.x), int(p.y)] for p in convex_hull]


print("Введите количество точек:")
n_input = int(input())

print(f"Введите {n_input} точек, каждую на новой строке в формате 'x y':")
points_data_raw = []
for _ in range(n_input):
    coord = list(map(int, input().split()))
    points_data_raw.append(coord)


convex_hull_result = Andrew(points_data_raw)

print("\n--- Результат (вершины выпуклой оболочки) ---")
if len(convex_hull_result) == 1 and convex_hull_result[0][0] == -1:
    print("Невозможно построить выпуклую оболочку.")
else:
    for point in convex_hull_result:
        print(f"{point[0]}, {point[1]}")
