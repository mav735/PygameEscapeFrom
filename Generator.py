from preset import *


class MapGenerator:
    def __init__(self):
        """Generates 50x50 map with walls"""
        self.map_profile = [['0'] * 50 for _ in range(50)]

        '''
        self.map_profile[0] = ['2'] * 50
        self.map_profile[-1] = ['7'] * 50
        for i in range(len(self.map_profile)):
            self.map_profile[i][0] = '3'
            self.map_profile[i][-1] = '5'
        self.map_profile[0][0] = '4'
        self.map_profile[-1][0] = '6'

        row = randint(0, 49)
        column = randint(0, 49)
        while self.map_profile[row][column] != 1:
            row = randint(0, 49)
            column = randint(0, 49)
        '''

        w, h = 5, 5
        x, y = 0, 0
        rooms = map_generator(w, h)
        print(*rooms, sep='\n')
        for line in rooms:
            for room in line:
                room = square_room(room)
                for i in range(len(room)):
                    for j in range(len(room[i])):
                        self.map_profile[i + x][j + y] = room[i][j]
                y += len(room)
            x += max(line)
            y = 0
        self.start_point = 1, 1

    def get_map(self):
        """:returns Map info"""
        return self.map_profile
