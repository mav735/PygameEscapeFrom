class MapGenerator:
    def __init__(self, screen_info):
        """:parameter screen_info: surface where you draw"""
        self.map_profile = [[0] * 50 for _ in range(50)]
        self.preset = None
        self.screen_size = self.width, self.height = screen_info.current_w, screen_info.current_h
        self.left = 10
        self.top = 10
        self.cell_size = max(self.width / 50, self.height / 50) * 5

    def set_view(self, left, top):
        """:parameter left: movement of player relatively start position X_coord
           :parameter top: movement of player relatively start position Y_coord"""
        self.left = left
        self.top = top

    def get_coords(self):
        """:returns position of player relatively start"""
        return self.left, self.top

    def get_map(self):
        """:returns Map info"""
        return self.map_profile

    def get_cell(self, mouse_coords):
        """:returns click position or None"""
        if mouse_coords[0] < self.left or mouse_coords[1] < self.top:
            return None
        if mouse_coords[0] > self.left + self.cell_size * self.width:
            return None
        if mouse_coords[1] > self.top + self.cell_size * self.height:
            return None
        return ((mouse_coords[0] - self.left) // self.cell_size,
                (mouse_coords[1] - self.top) // self.cell_size)


