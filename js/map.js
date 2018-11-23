/* eslint no-shadow: 0, no-param-reassign: 0 */
const $ = require('jquery');
const L = require('leaflet');
const gettext = require('./gettext.js');

const bounds = [[0.0, 0.0], [800.0, 550.0]];
const levels = [[6, '-1'], [7, '0'], [8, '1'], [9, '2']];
const tile_server = 'https://35c3.c3nav.de/map/';

global.map = undefined;
global.current_level = undefined;
global.level_control = undefined;

function redraw_marker() {
  for (const dp in drop_points) {
    if (!drop_points[dp].removed) {
      draw_marker(dp);
    }
  }
}

// use 257x257 px tiles from c3nav correctly
const originalInitTile = L.GridLayer.prototype._initTile;

L.GridLayer.include({
  _initTile(tile) {
    originalInitTile.call(this, tile);
    const tileSize = this.getTileSize();

    tile.style.width = `${tileSize.x + 1}px`;
    tile.style.height = `${tileSize.y + 1}px`;
  },
});

// from c3nav: site/static/site/js/c3nav.js
const LevelControl = L.Control.extend({
  options: {
    position: 'bottomright',
    addClasses: '',
  },

  onAdd() {
    this._container = L.DomUtil.create('div', `leaflet-control-levels leaflet-bar ${this.options.addClasses}`);
    this._tileLayers = {};
    this._overlayLayers = {};
    this._levelButtons = {};
    this.currentLevel = null;

    return this._container;
  },

  addLevel(id, title) {
    this._tileLayers[id] = L.tileLayer(`${tile_server + String(id)}/{z}/{x}/{y}.png`, {
      minZoom: -2,
      maxZoom: 5,
      bounds: L.GeoJSON.coordsToLatLngs(bounds),
      attribution: 'Powered by <a href="https://c3nav.de/">c3nav</a>',
    });
    const overlay = L.layerGroup();

    this._overlayLayers[id] = overlay;

    const link = L.DomUtil.create('a', '', this._container);

    link.innerHTML = title;
    link.level = id;
    link.href = '#';

    L.DomEvent.on(link, 'mousedown dblclick', L.DomEvent.stopPropagation).on(link, 'click', this._levelClick, this);

    this._levelButtons[id] = link;

    return overlay;
  },

  setLevel(id) {
    if (id === this.currentLevel) {
      return true;
    }
    if (this._tileLayers[id] === undefined) {
      return false;
    }

    if (this.currentLevel) {
      this._tileLayers[this.currentLevel].remove();
      this._overlayLayers[this.currentLevel].remove();
      L.DomUtil.removeClass(this._levelButtons[this.currentLevel], 'current');
    }
    this._tileLayers[id].addTo(map);
    this._overlayLayers[id].addTo(map);
    L.DomUtil.addClass(this._levelButtons[id], 'current');
    this.currentLevel = id;

    return true;
  },

  _levelClick(e) {
    e.preventDefault();
    e.stopPropagation();
    this.setLevel(e.target.level);
    if (typeof update_hash === 'function') {
      current_level = e.target.level - 7;
      update_hash();
    }
    redraw_marker();
  },

  finalize() {
    const buttons = $(this._container).find('a');

    buttons.addClass('current');
    buttons.width(buttons.width());
    buttons.removeClass('current');
  },
});

global.set_map_level = function(lvl) {
  if (typeof levels[lvl++] === 'undefined') {
    lvl = 0;
  }
  current_level = lvl - 1;
  level_control.setLevel(levels[lvl][0]);
};

global.init_map = function() {
  map = L.map('map', {
    attributionControl: true,
    zoom: 0,
    minZoom: 0,
    maxZoom: 5,
    crs: L.CRS.Simple,
    maxBounds: L.GeoJSON.coordsToLatLngs(bounds),
  });

  level_control = new LevelControl().addTo(map);
  const locationLayers = {};

  for (let l = levels.length - 1; l >= 0; l--) {
    const level = levels[l];
    const layerGroup = level_control.addLevel(level[0], level[1]);

    locationLayers[level[0]] = L.layerGroup().addTo(layerGroup);
  }
  level_control.finalize();

  set_map_level(0);

  global.default_map_view = function() {
    map.fitBounds(bounds);
  };

  redraw_marker();
};

global.get_icon = function(type) {
  const size = 12;
  let zoom = 6 - (map.getMaxZoom() - map.getZoom());

  if (zoom < 1) {
    zoom = 1;
  }

  return L.icon({
    iconSize: [size * zoom, size * zoom],
    iconAnchor: [size * zoom / 2, size * zoom],
    iconUrl: `${imgdir}/markers/${type}.svg`,
    popupAnchor: [0, -size * zoom],
  });
};

global.allow_dp_creation_from_map = function() {
  map.on('click', e => {
    const latlng = e.latlng;

    function get_marker(latlng) {
      const marker = L.marker(latlng, {
        icon: get_icon('CREATED'),
        draggable: true,
      });

      $(map).one('zoomend', () => {
        if (map.hasLayer(marker)) {
          map.removeLayer(marker);
          get_marker(marker._latlng);
        }
      });
      $(map).one('click', () => {
        map.removeLayer(marker);
      });
      const lat = marker._latlng.lat.toFixed(2);
      const lng = marker._latlng.lng.toFixed(2);

      marker.bindPopup(
        L.popup({ closeButton: false }).setContent(
          `<a class='btn btn-primary white' href='${create_dp_url}/${current_level}/${lat}/${lng}'>${gettext(
            'Create a new drop point'
          )}</a>`
        )
      );
      marker.on('dragend', function() {
        const lat = this._latlng.lat.toFixed(2);
        const lng = this._latlng.lng.toFixed(2);

        this._popup.setContent(
          `<a class='btn btn-primary white' href='${create_dp_url}/${current_level}/${lat}/${lng}'>${gettext(
            'Create a new drop point'
          )}</a>`
        );
      });
      map.addLayer(marker);

      return marker;
    }
    const marker = get_marker(latlng);

    marker.openPopup();
  });
};

global.draw_marker = function(num) {
  if (map.hasLayer(drop_points[num].layer)) {
    map.removeLayer(drop_points[num].layer);
  }
  if (drop_points[num].level !== current_level) {
    return;
  }
  drop_points[num].layer = L.geoJson(
    {
      type: 'Feature',
      geometry: {
        type: 'Point',
        coordinates: [drop_points[num].lng, drop_points[num].lat],
      },
      properties: {
        last_state: drop_points[num].last_state,
        number: Number.parseInt(num, 10),
      },
    },
    {
      filter(feature) {
        return feature.geometry.coordinates[0] !== null && feature.geometry.coordinates[1] !== null;
      },
      pointToLayer(feature, latlng) {
        const marker = L.marker(latlng, {
          icon: get_icon(feature.properties.last_state),
        });

        marker.on('click', e => {
          const dp = e.target.feature;

          show_dp_modal(dp.properties.number, pane_on_click);
        });
        if (map.getZoom() > map.getMaxZoom() - 2) {
          marker.bindTooltip(num, {
            permanent: true,
            direction: 'bottom',
          });
        }

        return marker;
      },
    }
  );
  $(map).one('zoomend', () => {
    draw_marker(num);
  });
  map.addLayer(drop_points[num].layer);
};
