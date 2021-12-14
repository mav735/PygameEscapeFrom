class MapGenerator:
    def __init__(self, screen_info):
        """:parameter screen_info: surface where you draw"""
        self.map_profile = [[0] * 50 for _ in range(50)]
        self.preset = None
        self.screen_size = self.width, self.height = screen_info.current_w, screen_info.current_h
        self.cell_size = max(self.width / 50, self.height / 50) * 5

    def get_map(self):
        """:returns Map info"""
        return self.map_profile
