class MapSource:
    @classmethod
    def __getattr__(cls, _):
        return None


class C3Nav35C3(MapSource):
    attribution = "Powered by <a href='https://c3nav.de/'>c3nav</a>"
    tile_server = "https://35c3.c3nav.de/map/"
    min_zoom = 0
    max_zoom = 5
    initial_zoom = 0
    bounds = [[0.0, 0.0], [800.0, 550.0]]
    level_config = [[6, -1], [7, 0], [8, 1], [9, 2]]
    simple_crs = True
    hack_257px = True


class OpenStreeMapCamp2019(MapSource):
    attribution = \
        "<a href='https://www.openstreetmap.org/copyright'>© OpenStreepMap Contributers</a>"
    tile_server = "https://{s}.tile.openstreetmap.org/"
    tile_server_subdomains = ["a", "b", "c"]
    min_zoom = 17
    max_zoom = 19
    initial_zoom = 17
    initial_view = {
        "lat": 53.03124,
        "lng": 13.30734,
        "zoom": 17
    }
