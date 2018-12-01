/* eslint no-shadow: 0, no-param-reassign: 0 */
const $ = require('jquery');
const L = require('leaflet');
const gettext = require('./gettext.js');

global.map = undefined;
global.current_level = 0;
global.map_category = -1;

let layer_control = null;

function get_layer(level) {
  const level_config = global.map_source.level_config;

  for (const item in level_config) {
    if (level_config[item][1] === parseInt(level, 10)) {
      return level_config[item][0];
    }
  }
}

function get_level(layer) {
  const level_config = global.map_source.level_config;

  for (const item in level_config) {
    if (level_config[item][0] === parseInt(layer, 10)) {
      return level_config[item][1];
    }
  }
}

function redraw_markers() {
  for (const dp in drop_points) {
    if (!drop_points[dp].removed) {
      draw_marker(dp);
    }
  }
}

global.redraw_markers = redraw_markers;

function setCategory(num) {
  global.map_category = num;
  $('.map-category-select-button')
    .removeClass('btn-primary')
    .addClass('btn-default');
  $('.map-category-select-button')
    .filter(`[data-category_id='${num}']`)
    .removeClass('btn-default')
    .addClass('btn-primary');
  redraw_markers();
}

global.setMapCategory = setCategory;

// from c3nav: site/static/site/js/c3nav.js
const LayerControl = L.Control.extend({
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

  addLayer(id, title) {
    this._tileLayers[id] = L.tileLayer(`${global.map_source.tileserver + String(id)}/{z}/{x}/{y}.png`, {
      minZoom: global.map_source.min_zoom,
      maxZoom: global.map_source.max_zoom,
      bounds: global.map_source.bounds !== undefined ? L.GeoJSON.coordsToLatLngs(global.map_source.bounds) : undefined,
      attribution: global.map_source.attribution,
      subdomains: global.map_source.tileserver_subdomains,
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

  setLayer(id) {
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
    this.setLayer(e.target.level);
    current_level = get_level(e.target.level);
    if (typeof update_hash === 'function') {
      update_hash();
    }
    redraw_markers();
  },

  finalize() {
    const buttons = $(this._container).find('a');

    buttons.addClass('current');
    buttons.width(buttons.width());
    buttons.removeClass('current');
  },
});

global.set_map_level = function(level) {
  if (global.map_source.level_config !== undefined) {
    current_level = parseInt(level, 10);
    layer_control.setLayer(get_layer(current_level));
  } else {
    current_level = 0;
  }
};

global.init_map = function() {
  if (global.map_source.hack_257px) {
    const originalInitTile = L.GridLayer.prototype._initTile;

    L.GridLayer.include({
      _initTile(tile) {
        originalInitTile.call(this, tile);
        const tileSize = this.getTileSize();

        tile.style.width = `${tileSize.x + 1}px`;
        tile.style.height = `${tileSize.y + 1}px`;
      },
    });
  }

  const map_options = {
    attributionControl: true,
    zoom: global.map_source.initial_zoom,
    minZoom: global.map_source.min_zoom,
    maxZoom: global.map_source.max_zoom,
    maxBounds: global.map_source.bounds ? L.GeoJSON.coordsToLatLngs(global.map_source.bounds) : undefined,
  };

  if (global.map_source.simple_crs) {
    map_options.crs = L.CRS.Simple;
  }

  map = L.map('map', map_options);

  if (global.map_source.level_config !== undefined) {
    layer_control = new LayerControl().addTo(map);
    const locationLayers = {};

    const levels = global.map_source.level_config;

    for (let l = levels.length - 1; l >= 0; l--) {
      const level = levels[l];
      const layerGroup = layer_control.addLayer(level[0], String(level[1]));

      locationLayers[level[0]] = L.layerGroup().addTo(layerGroup);
    }
    layer_control.finalize();
    set_map_level(0);
  } else {
    L.tileLayer(`${global.map_source.tileserver}{z}/{x}/{y}.png`, {
      minZoom: global.map_source.min_zoom,
      maxZoom: global.map_source.max_zoom,
      bounds: global.map_source.bounds !== undefined ? L.GeoJSON.coordsToLatLngs(global.map_source.bounds) : undefined,
      attribution: global.map_source.attribution,
      subdomains: global.map_source.tileserver_subdomains,
    }).addTo(map);
  }

  global.default_map_view = function() {
    if (global.map_source.bounds !== undefined) {
      map.fitBounds(global.map_source.bounds);
    } else if (global.map_source.initial_view !== undefined) {
      const initial = global.map_source.initial_view;

      map.setView([initial.lat, initial.lng], initial.zoom);
    }
  };

  redraw_markers();
};

global.get_icon = function(category, state) {
  const size = 12;
  let zoom = 6 - (map.getMaxZoom() - map.getZoom());

  if (zoom < 1) {
    zoom = 1;
  }

  return L.icon({
    iconSize: [size * zoom, size * zoom],
    iconAnchor: [size * zoom / 2, size * zoom],
    iconUrl: `${imgdir}/markers/${category}/${state}.svg`,
    popupAnchor: [0, -size * zoom],
  });
};

global.allow_dp_creation_from_map = function() {
  map.on('click', e => {
    const latlng = e.latlng;

    function get_marker(latlng) {
      const marker = L.marker(latlng, {
        icon: get_icon('new', 'CREATED'),
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
  if (global.map_category > -1 && drop_points[num].category_id !== global.map_category) {
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
        category_id: drop_points[num].category_id,
      },
    },
    {
      filter(feature) {
        return feature.geometry.coordinates[0] !== null && feature.geometry.coordinates[1] !== null;
      },
      pointToLayer(feature, latlng) {
        const marker = L.marker(latlng, {
          icon: get_icon(feature.properties.category_id, feature.properties.last_state),
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

$('.map-category-select-button').on('click', ev => {
  const num = $(ev.currentTarget).data('category_id');

  setCategory(num);

  let hash = `#${current_level}/${map.getCenter().lat.toFixed(2)}/${map.getCenter().lng.toFixed(2)}/${map.getZoom()}`;

  if (global.map_category > -1) {
    hash += `/${global.map_category}`;
  }

  location.hash = hash;
});
