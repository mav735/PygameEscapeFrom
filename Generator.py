from preset import *


class MapGenerator:
    def __init__(self):
        """Generates 50x50 map with walls"""
        self.map_profile = [['0'] * 50 for _ in range(50)]

        w, h = 5, 5
        x, y = 0, 0
        self.start_point = 22, 13
        random_roads = 10

        rooms = map_generator(w, h)
        print(*rooms, sep='\n')
        for line in rooms:
            for room in line:
                room = square_room(room)
                for i in range(len(room)):
                    for j in range(len(room[i])):
                        self.map_profile[j + y][i + x] = room[i][j]
                y += len(room)
            x += max(line)
            y = 0

        x = 0
        for j in range(len(rooms)):
            y = 0
            for i in range(len(rooms[j]) - 1):
                y += rooms[j][i]
                path = randint(1, min(rooms[j][i + 1], rooms[j][i]) - 2)
                self.map_profile[y - 1][path + x] = '1'
                self.map_profile[y][path + x] = '1'
            x += max(rooms[j])

        sides_st = []
        sides_en = []
        for i in range(50):
            if self.map_profile[1][i] == '3':
                sides_st.append(i)
            if self.map_profile[1][i] == '5':
                sides_en.append(i)

        sides_en.pop()
        del sides_st[0]

        for i in range(len(rooms) - 1):
            path = randint(1, min(rooms[i][0], rooms[i + 1][0]) - 2)
            for j in range(sides_en[i], sides_st[i] + 1):
                self.map_profile[path][j] = '1'

        road = 0
        while road < random_roads:
            dot = randint(0, 49), randint(0, 49)
            flags = [False, False]
            points = [None, None]
            for j in range(dot[1], 48):
                point = self.map_profile[dot[0]][j]

                try:
                    point_left = self.map_profile[dot[0] - 1][j]
                except IndexError:
                    point_left = '0'
                try:
                    point_right = self.map_profile[dot[0] + 1][j]
                except IndexError:
                    point_right = '0'

                if point == '5':
                    flags[0] = True
                    points[0] = dot[0], j
                if point == '3':
                    flags[1] = True
                    points[1] = dot[0], j

                if flags[0]:
                    try:
                        assert point in ['0', '1', '3', '5']
                        assert (point_right == '1' and point_left == '1') or \
                               (point_right != '1' and point_left != '1')
                    except AssertionError:
                        flags = [False, False]
                        break
                if all(flags):
                    break

            if all(flags):
                road += 1 if points[0][1] < points[1][1] + 1 else 0
                for j in range(points[0][1], points[1][1] + 1):
                    self.map_profile[points[0][0]][j] = '1'

    def get_map(self):
        """:returns Map info"""
        return self.map_profile
