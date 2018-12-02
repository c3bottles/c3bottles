class _MapSourceType(type):
    def __getattr__(cls, attr):
        return None


class MapSource(metaclass=_MapSourceType):

    @classmethod
    def get(cls, attr, default=None):
        return getattr(cls, attr) if attr in dir(cls) else default

    @classmethod
    def override(cls, attr, value):
        setattr(cls, attr, value)


class C3Nav35C3(MapSource):
    attribution = "Powered by <a href='https://c3nav.de/'>c3nav</a>"
    tileserver = "https://35c3.c3nav.de/map/"
    min_zoom = 0
    max_zoom = 5
    bounds = [[0.0, 0.0], [800.0, 550.0]]
    level_config = [[6, -1], [7, 0], [8, 1], [9, 2]]
    simple_crs = True
    hack_257px = True


class OpenStreetMapCamp2019(MapSource):
    attribution = \
        "<a href='https://www.openstreetmap.org/copyright'>© OpenStreepMap contributers</a>"
    tileserver = "https://{s}.tile.openstreetmap.org/"
    tileserver_subdomains = ["a", "b", "c"]
    min_zoom = 16
    max_zoom = 19
    initial_view = {
        "lat": 53.03124,
        "lng": 13.30734,
        "zoom": 17
    }
