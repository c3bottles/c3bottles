/* eslint no-shadow: 0, no-param-reassign: 0 */
const $ = require('jquery');
const L = require('leaflet');
const gettext = require('./gettext');
const modals = require('./modals');

const imgDir = $('meta[name=endpoint]').data('img');

let mapObj;
let mapSource;
let layerControl;
let currentLevel = 0;
let mapCategory = -1;

function getLayerNumber(level) {
  const level_config = mapSource.level_config;

  for (const item in level_config) {
    if (level_config[item][1] === parseInt(level, 10)) {
      return level_config[item][0];
    }
  }
}

function getLevelNumber(layer) {
  const level_config = mapSource.level_config;

  for (const item in level_config) {
    if (level_config[item][0] === parseInt(layer, 10)) {
      return level_config[item][1];
    }
  }
}

function getIcon(category, state) {
  const size = 12;
  let zoom = 6 - (mapObj.getMaxZoom() - mapObj.getZoom());

  if (zoom < 1) {
    zoom = 1;
  }

  return L.icon({
    iconSize: [size * zoom, size * zoom],
    iconAnchor: [size * zoom / 2, size * zoom],
    iconUrl: `${imgDir}/markers/${category}/${state}.svg`,
    popupAnchor: [0, -size * zoom],
  });
}

module.exports.getIcon = getIcon;

function drawMarker(num) {
  if (mapObj.hasLayer(drop_points[num].layer)) {
    mapObj.removeLayer(drop_points[num].layer);
  }
  if (drop_points[num].level !== currentLevel) {
    return;
  }
  if (mapCategory > -1 && drop_points[num].category_id !== mapCategory) {
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
          icon: getIcon(feature.properties.category_id, feature.properties.last_state),
        });

        marker.on('click', e => {
          const dp = e.target.feature;

          modals.show(dp.properties.number, pane_on_click);
        });
        if (mapObj.getZoom() > mapObj.getMaxZoom() - 2) {
          marker.bindTooltip(num, {
            permanent: true,
            direction: 'bottom',
          });
        }

        return marker;
      },
    }
  );
  $(mapObj).one('zoomend', () => {
    drawMarker(num);
  });
  mapObj.addLayer(drop_points[num].layer);
}

module.exports.drawMarker = drawMarker;

function redrawMarkers() {
  for (const dp in drop_points) {
    if (!drop_points[dp].removed) {
      drawMarker(dp);
    }
  }
}

module.exports.redrawMakers = redrawMarkers;

module.exports.getCategory = function() {
  return mapCategory;
};

function setCategory(num) {
  mapCategory = num;
  $('.map-category-select-button')
    .removeClass('btn-primary')
    .addClass('btn-light');
  $('.map-category-select-button')
    .filter(`[data-category_id='${num}']`)
    .removeClass('btn-light')
    .addClass('btn-primary');
  redrawMarkers();
}

module.exports.setCategory = setCategory;

module.exports.isInitialized = function() {
  return mapObj !== undefined;
};

module.exports.getLevel = function() {
  return currentLevel;
};

module.exports.setLevel = function(level) {
  if (mapSource.level_config !== undefined) {
    currentLevel = parseInt(level, 10);
    layerControl.setLayer(getLayerNumber(currentLevel));
  } else {
    currentLevel = 0;
  }
  redrawMarkers();
};

function initializeMap(mapSource_) {
  mapSource = mapSource_;
  if (mapSource.hack_257px) {
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
    minZoom: mapSource.min_zoom,
    maxZoom: mapSource.max_zoom,
    maxBounds: mapSource.bounds ? L.GeoJSON.coordsToLatLngs(mapSource.bounds) : undefined,
  };

  if (mapSource.simple_crs) {
    map_options.crs = L.CRS.Simple;
  }

  mapObj = L.map('map', map_options);

  if (mapSource.level_config !== undefined) {
    // from c3nav: site/static/site/js/c3nav.js
    const LayerControlWidget = L.Control.extend({
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
        this._tileLayers[id] = L.tileLayer(`${mapSource.tileserver + String(id)}/{z}/{x}/{y}.png`, {
          minZoom: mapSource.min_zoom,
          maxZoom: mapSource.max_zoom,
          bounds: mapSource.bounds !== undefined ? L.GeoJSON.coordsToLatLngs(mapSource.bounds) : undefined,
          attribution: mapSource.attribution,
          subdomains: mapSource.tileserver_subdomains,
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
        this._tileLayers[id].addTo(mapObj);
        this._overlayLayers[id].addTo(mapObj);
        L.DomUtil.addClass(this._levelButtons[id], 'current');
        this.currentLevel = id;

        return true;
      },

      _levelClick(e) {
        e.preventDefault();
        e.stopPropagation();
        this.setLayer(e.target.level);
        currentLevel = getLevelNumber(e.target.level);
        if (typeof update_hash === 'function') {
          update_hash();
        }
        redrawMarkers();
      },

      finalize() {
        const buttons = $(this._container).find('a');

        buttons.addClass('current');
        buttons.width(buttons.width());
        buttons.removeClass('current');
      },
    });

    layerControl = new LayerControlWidget().addTo(mapObj);

    const levels = mapSource.level_config;

    for (let l = levels.length - 1; l >= 0; l--) {
      layerControl.addLayer(levels[l][0], String(levels[l][1]));
    }
    layerControl.finalize();
  } else {
    L.tileLayer(`${mapSource.tileserver}{z}/{x}/{y}.png`, {
      minZoom: mapSource.min_zoom,
      maxZoom: mapSource.max_zoom,
      bounds: mapSource.bounds !== undefined ? L.GeoJSON.coordsToLatLngs(mapSource.bounds) : undefined,
      attribution: mapSource.attribution,
      subdomains: mapSource.tileserver_subdomains,
      tms: mapSource.tms,
      noWrap: mapSource.no_wrap,
    }).addTo(mapObj);
  }

  module.exports.setDefaultView = function() {
    if (mapSource.initial_view !== undefined) {
      const initial = mapSource.initial_view;

      mapObj.setView([initial.lat, initial.lng], initial.zoom);
    } else if (mapSource.bounds !== undefined) {
      mapObj.fitBounds(mapSource.bounds);
    } else {
      mapObj.fitWorld();
    }
  };

  return mapObj;
}

module.exports.initializeMap = initializeMap;

module.exports.allowDpCreation = function() {
  mapObj.on('click', e => {
    const latlng = e.latlng;

    function get_marker(latlng) {
      const marker = L.marker(latlng, {
        icon: getIcon('new', 'CREATED'),
        draggable: true,
      });

      $(mapObj).one('zoomend', () => {
        if (mapObj.hasLayer(marker)) {
          mapObj.removeLayer(marker);
          get_marker(marker._latlng);
        }
      });
      $(mapObj).one('click', () => {
        mapObj.removeLayer(marker);
      });
      const lat = marker._latlng.lat.toPrecision(7);
      const lng = marker._latlng.lng.toPrecision(7);

      marker.bindPopup(
        L.popup({ closeButton: false }).setContent(
          `<a class='btn btn-primary white' href='${create_dp_url}/${currentLevel}/${lat}/${lng}'>${gettext(
            'Create a new drop point'
          )}</a>`
        )
      );
      marker.on('dragend', function() {
        const lat = this._latlng.lat.toPrecision(7);
        const lng = this._latlng.lng.toPrecision(7);

        this._popup.setContent(
          `<a class='btn btn-primary white' href='${create_dp_url}/${currentLevel}/${lat}/${lng}'>${gettext(
            'Create a new drop point'
          )}</a>`
        );
      });
      mapObj.addLayer(marker);

      return marker;
    }
    const marker = get_marker(latlng);

    marker.openPopup();
  });
};

$('.map-category-select-button').on('click', ev => {
  const num = $(ev.currentTarget).data('category_id');

  setCategory(num);

  let hash =
    `#${currentLevel}/` +
    `${mapObj.getCenter().lat.toPrecision(7)}/` +
    `${mapObj.getCenter().lng.toPrecision(7)}/` +
    `${mapObj.getZoom()}`;

  if (mapCategory > -1) {
    hash += `/${mapCategory}`;
  }

  location.hash = hash;
});
