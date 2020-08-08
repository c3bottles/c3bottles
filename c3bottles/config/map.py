import json


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

    @classmethod
    def json(cls):
        return json.dumps(
            {
                "attribution": cls.get("attribution", ""),
                "tileserver": cls.get("tileserver", ""),
                "tileserver_subdomains": cls.get("tileserver_subdomains", []),
                "bounds": cls.get("bounds", None),
                "initial_view": cls.get("initial_view", None),
                "level_config": cls.get("level_config", None),
                "min_zoom": cls.get("min_zoom", 0),
                "max_zoom": cls.get("max_zoom", 0),
                "simple_crs": cls.get("simple_crs", False),
                "hack_257px": cls.get("hack_257px", False),
                "tms": cls.get("tms", False),
                "no_wrap": cls.get("no_wrap", False),
            }
        )


class C3Nav35C3(MapSource):
    attribution = "Powered by <a href='https://c3nav.de/'>c3nav</a>"
    tileserver = "https://35c3.c3nav.de/map/"
    min_zoom = 0
    max_zoom = 5
    bounds = [[0.0, 0.0], [800.0, 550.0]]
    level_config = [[6, -1], [7, 0], [8, 1], [9, 2]]
    simple_crs = True
    hack_257px = True


class EH19(MapSource):
    attribution = "Powered by <a href='https://c3nav.de/'>c3nav</a>"
    tileserver = "https://eh19.c3nav.de/map/"
    min_zoom = 3
    max_zoom = 6
    bounds = [[-33.9, -66.9], [155.07, 122.07]]
    level_config = [
        [1, 0],
        [200, 0.5],
        [4, 1],
        [8, 2],
        [9, 3],
        [10, 4],
        [11, 5],
        [12, 6],
    ]
    simple_crs = True
    hack_257px = True
    initial_view = {"lat": 27.93750, "lng": 60.62500, "zoom": 3}


class OpenStreetMapCamp2019(MapSource):
    attribution = (
        "<a href='https://www.openstreetmap.org/copyright'>© OpenStreepMap contributers</a>"
    )
    tileserver = "https://{s}.tile.openstreetmap.org/"
    tileserver_subdomains = ["a", "b", "c"]
    min_zoom = 16
    max_zoom = 19
    initial_view = {"lat": 53.03124, "lng": 13.30734, "zoom": 17}
