class Camera:
    def __init__(self):
        self.x = 10
        self.y = 10

    def get_coords(self):
        return self.x, self.y

    def x_move(self, coefficient):
        self.x += 3 * coefficient

    def y_move(self, coefficient):
        self.y += 3 * coefficient
