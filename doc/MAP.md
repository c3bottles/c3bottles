# Map configuration

c3bottles can use any map source that can be configured as a layer in
[Leaflet](https://leafletjs.com/). Map configuration happens in two stages:

1.  Map sources and their paramters (e.g. tile server URL, zoom levels, layers
    and building levels, coordinate bounds etc.) are configured as properties
    of Python objects in `c3bottles/config/map.py`. These are hard-coded but
    can of course be adapted to specific setups if needed.
 
2.  One of these sources is chosen in `config.py` by setting the `MAP_SOURCE`
    configuration parameter. In addition to selecting one of the map sources,
    the user can decide to override specific parameters (typically tile server
    URLs) by doing something like this in `config.py`:

        from c3bottles.config.map import ExampleMapSource
        MAP_SOURCE = ExampleMapSource
        ExampleMapSource.override("tileserver", "https://tiles.example.org/")

    The configuration file is Python code that is executed on server startup,
    so a lot of things are possible here, if needed.

## Preconfigured map sources

c3bottles ships with a number of map sources that can be used directly:

*   **OpenStreetMap**: This is the easiest way to use geographical tiles for
    an outdoor event. This source uses tiles directly from the tile servers
    behind [OpenStreetMap](https://www.openstreetmap.org/).

    The *OpenStreetMapCamp2019* configuration is an example for OpenStreetMap
    and pointing at the location of the Chaos Communication Camp 2019 in
    Mildenberg. The starting location and zoom levels can be easily adapted
    as needed. OpenStreepMap only has one layer.

*   **c3nav**: c3nav is a routing webservice for chaos events that is available
    for use at [https://c3nav.de/](https://c3nav.de/) and being developed at
    [https://github.com/c3nav/c3nav/](https://github.com/c3nav/c3nav/).

    Like c3bottles, c3nav is based on Leaflet and provides high-quality tiles
    of venues for events like the Chaos Communication Congress which we can
    use via this map source. The configuration named *C3Nav35C3* contains an
    event-specific tile server URL which probably changes with the next event.

    The c3nav configuration contains a `level_configuration` since it uses
    a number of map layers that correlate to building levels.

    In addition, it needs a number of specific hacks, which are needed to
    properly use the  tiles:

    *   The `hack_257px` option enables a code snippet in `js/map.js` to deal
        with the non-standard tile size of 257x257 pixels.
    *   The `simple_crs` option changes the coordinate reference system used
        from the default (geographical coordinates) to a simpler one that is
        better suited for hand-crafted custom tiles for a plane like a building
        instead of a globe.

    If you want to use tiles from c3nav, please contact the c3nav developers
    beforehand. It is their decision if they let you use their tiles (and the
    bandwidth on their tile servers).

## Adding map sources

You can easily add your own map source either to `c3bottles/config/map.py`,
define it directly in `config.py` or add it somewhere else and import it
from there.

Map sources are Python classes inheriting from `MapSource` which is defined
in `c3bottles/config/map.py`. Please make sure to use this base class as it
provides a few methods and special characteristics that are needed for it to
work properly.

Parameters of map sources are static, class level variables.

The following configuration parameters are currently used from map sources
(types shown are Python data types):

*   **tileserver** (*str*, mandatory): The base tile server URL. This should
    end with a `/` and is used to create the tile URLs. Currently, this is
    simply appended by `level/zoom/longitude/latitude.png` with the `level/`
    part being optional (depending on whether a `level_configuration` has been
    given). The string `{s}` in the URL is randomly replaced by one of the
    elements from `tileserver_subdomains` if that has been set.

*   **tileserver_subdomains** (*list* of *str*, optional): An optional list
    of subdomain strings that are chosen randomly to distribute load over
    a number of different tile servers.

*   **attribution** (*str*, optional): An attribution text, and possibly a
    link that is shown in the bottom right corner to properly attribute the
    tile provider. This has to be set in accordance with the tile provider
    and usually contains a link to the service whose tiles are used and
    possibly a copyright statement for the tile author(s). This is not
    mandatory from a technical point of view but should always be set.

*   **min_zoom** (*int*, mandatory): The minimum zoom level that the user
    may choose.

*   **max_zoom** (*int*, mandatory): The maximum zoom level that the user
    may choose.

*   **bounds** (*list* of *lists* of *floats*, optional): This setting
    can be used to restrict the user to a specific region on the map.
    This must be a list with two elements, which in turn are lists of two
    floats, like such:

        [[min_x, min_y], [max_x, max_y]]

    Make sure to use *lists* here instead of *tuples* as this value is
    directly embedded in JavaScript code.

*   **initial_view** (*dict* of *floats*, optional): The initial default view
    used on the map. This is a *dict* that needs three values: `lat` for the
    latitude, `lng` for the longitude and `zoom`. if this is not set, the
    map will call Leaflet's `fitBound()` method, if `bounds` have been
    set and `fitWorld()` otherwise.

*   **level_config** (*list* of *lists* of *ints*, optional): This setting
    defines a correlation between map layers (as they are used in tile URLs)
    and e.g. building levels. For this, a list of lists of two integers has
    to be given where the first corresponds to a map layer number and the
    second one to a level number that is used in the c3bottles database and
    shown in the level selector widget on the map, like such:

        [[23, -1], [30, 0], [42, 1]]

    If no `level_config` has been set, all drop points will default to a
    level of 0 and levels will be disabled completely in the frontend.

    Make sure to use *lists* here instead of *tuples* as this value is
    directly embedded in JavaScript code.

Specific map sources may have their own configuration parameters used as
special hacks to enable code only needed for these sources. For these
parameters see the list of preconfigured map sources above.

## Rendering your own tiles

Originally, c3bottles has been designed for a map that was a huge image and
from which tiles could rendered with a semi-automatic toolchain. Other maps
then can simply be used by exchanging the base image and rendering new tiles.

These tiles are built using Imagemagick, GDAL and gdal2tiles. If you use
Debian, you can install the dependencies like this:

    sudo apt install imagemagick gdal-bin libgdal-dev
    pip install gdal2tiles

The base image for the tiles needs to be a square with a size that is a power
of 2. Suppose your image is named `static/img/map.png`, then you first have
to convert it to a square with an edge length of the next power of 2. You can
find out the size of the image with `file` or `identify`:

    cd static/img
    identify map.png

The output looks like this:

    map.png PNG 5500x10500 5500x10500+0+0 8-bit sRGB 21.7418MiB 0.000u 0:00.000

In this case, the next power of 2 larger than 10500 pixels would be 16384, so
the image needs to be resized to 16384x16384 pixels:

    convert map.png -background white -compose Copy -gravity center \
                  -resize 16384x16384 -extent 16384x16384 map_sq.png

If this fails, you may have to increase your ImageMagick memory limit in
`/etc/ImageMagick-6/policy.xml`

After you have successfully create a square image, you can render the tiles
from `map_sq.png` using GDAL and gdal2tiles:

    gdal_translate -of vrt map_sq.png map_sq.vrt
    gdal2tiles.py -w none -p raster map_sq.vrt tiles

Your tiles will be in the `static/img/tiles` directory and can be used with a
map source like this in `c3bottles/config/map.py`:

    class CustomTiles(MapSource):
        attribution = "self-made"
        tileserver = "/static/img/tiles/"
        min_zoom = 0
        max_zoom = 6
        tms = True
        no_wrap = True
