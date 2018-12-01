class MapSource:
    attribution_name = None
    attribution_link = None
    tile_server = None
    bounds = None
    min_zoom = 0
    max_zoom = 7
    initial_zoom = 0
    level_config = None

    @classmethod
    def get_attribution(cls):
        if cls.attribution_name is None:
            return ""
        if cls.attribution_link is not None:
            return "Powered by <a href='{}'>{}</a>".format(
                cls.attribution_link, cls.attribution_name
            )
        else:
            return "Powered by {}".format(cls.attribution_name)


class C3Nav35C3(MapSource):
    attribution_name = "c3nav"
    attribution_link = "https://c3nav.de/"
    tile_server = "https://35c3.c3nav.de/map/"
    min_zoom = 0
    max_zoom = 5
    initial_zoom = 0
    bounds = [[0.0, 0.0], [800.0, 550.0]]
    level_config = [[6, -1], [7, 0], [8, 1], [9, 2]]
