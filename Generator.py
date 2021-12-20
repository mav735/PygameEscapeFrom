from random import randint


class MapGenerator:
    def __init__(self):
        """Generates 50x50 map with walls"""
        self.map_profile = [[1] * 50 for _ in range(50)]
        self.map_profile[0] = ['2'] * 50
        self.map_profile[-1] = ['7'] * 50
        for i in range(len(self.map_profile)):
            self.map_profile[i][0] = 3
            self.map_profile[i][-1] = 5
        self.map_profile[0][0] = '4'
        self.map_profile[-1][0] = '6'
        row = randint(0, 49)
        column = randint(0, 49)
        while self.map_profile[row][column] != 1:
            row = randint(0, 49)
            column = randint(0, 49)
        self.start_point = (1, 1)
        self.preset = None

    def get_map(self):
        """:returns Map info"""
        return self.map_profile
