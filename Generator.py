from preset import *


class MapGenerator:
    def __init__(self):
        """Generates 50x50 map with walls"""
        flag = False
        while True:
            try:
                self.map_profile = [['0'] * 50 for _ in range(50)]

                w, h = 5, 5  # room amount
                x, y = 0, 0

                self.start_point = 22, 13
                random_roads = 10  # amount random roads

                # Generation rooms
                rooms = map_generator(w, h)
                for line in rooms:
                    for room in line:
                        room = square_room(room)
                        for i in range(len(room)):
                            for j in range(len(room[i])):
                                self.map_profile[j + y][i + x] = room[i][j]
                        y += len(room)
                    x += max(line)
                    y = 0

                # Generation Roads in rows of rooms
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

                # Random roads in random places
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

                # random start point
                while True:
                    self.start_point = [randint(0, 49), randint(0, 49)]
                    if self.map_profile[self.start_point[0]][self.start_point[1]] == '1':
                        break

                while True:
                    self.monolith = [randint(0, 49), randint(0, 49)]
                    if self.map_profile[self.monolith[0]][self.monolith[1]] == '1' \
                            and self.monolith != self.start_point and \
                            self.start_point not in self.neighbours(self.monolith):
                        break
                self.map_profile[self.monolith[0]][self.monolith[1]] = '8'
                flag = True
                if flag:
                    break
            except IndexError:
                pass

    def get_map(self):
        """:returns Map info"""
        return self.map_profile

    @staticmethod
    def neighbours(point):
        """Returns coordinates of neighbours of current point"""
        result = []
        for k in range(9):
            dot = [point[0] - 1 + k % 3, point[1] - 1 + k // 3]
            result.append(dot)
        result = [p for p in result if -1 < p[0] < 50 and -1 < p[1] < 50]
        return result

    def get_monolith(self):
        """:returns Monolith position"""
        return self.monolith


if __name__ == '__main__':
    while True:
        map1 = MapGenerator()
        map1.get_map()