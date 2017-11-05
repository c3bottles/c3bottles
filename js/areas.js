/**
 * A GeoJSON object containing all the building levels as polygons.
 *
 */
var levels = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {"level": 4},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-36.74, 80.47], [-1.23, 83.97], [22.68, 84.03],
                    [74.88, 80.72], [78.75, 76.46], [65.30, 69.72],
                    [26.63, 72.66], [26.19, 74.24], [15.21, 75.61],
                    [2.02, 73.63]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {"level": 3},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-35.86, 62.79], [2.02, 73.53], [13.18, 74.07],
                    [23.29, 72.82], [27.51, 72.21], [74.88, 63.70],
                    [84.55, 59.67], [86.13, 49.27], [65.30, 34.74],
                    [26.54, 41.97], [1.85, 44.90]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {"level": 2},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-90.70, 50.96], [-66.18, 66.72], [-42.80, 61.98],
                    [-26.37, 56.46], [1.40, 42.49], [26.54, 39.30],
                    [74.79, 17.64], [84.99, -7.44], [67.24, -26.12],
                    [1.58, -15.11]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {"level": 1},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-91.14, -2.55], [-65.92, 27.29], [-42.54, 16.72],
                    [0.88, -17.14], [11.69, -22.19], [77.52, -43.71],
                    [86.13, -57.61], [65.21, -66.72], [1.23, -62.27],
                    [-25.66, -50.40]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {"level": 0},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-78.40, -61.61], [-69.52, -56.75], [-23.64, -52.27],
                    [7.73, -65.18], [21.80, -64.21], [85.43, -73.05],
                    [92.46, -77.60], [70.31, -82.33], [21.45, -83.28],
                    [-27.60, -84.75], [-52.56, -82.59]
                ]]
            }
        }
    ]
};

/**
 * A GeoJSON object containing all the rooms within the building.
 *
 */
var rooms = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "name": "Elevators 4. OG",
                "level": 4
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [16.52, 76.16], [24.61, 77.37], [30.06, 76.74],
                    [27.77, 74.75]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "name": "Rangfoyer 1",
                "level": 4
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-35.68, 80.40], [-5.27, 83.65], [-1.41, 83.14],
                    [-18.81, 81.26], [-12.30, 79.70], [-1.49, 78.00],
                    [10.37, 76.90], [30.67, 79.46], [33.31, 78.82],
                    [2.02, 73.75]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "name": "Rangfoyer 2",
                "level": 4
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [26.89, 72.97], [31.03, 76.96], [35.95, 76.80],
                    [35.07, 75.80], [42.80, 74.80], [55.72, 74.02],
                    [65.13, 74.02], [70.22, 76.04], [75.15, 75.56],
                    [64.95, 70.11]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "name": "Elevators 3. OG",
                "level": 3
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [14.94, 50.79], [24.87, 54.62], [30.32, 53.07],
                    [27.77, 47.40]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "name": "Zwischenfoyer 1",
                "level": 3
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-34.72, 62.59], [-0.88, 72.40], [3.25, 70.85],
                    [-9.14, 68.37], [-10.28, 66.48], [-17.05, 64.21],
                    [-11.43, 60.24], [-2.46, 56.51], [7.21, 54.01],
                    [16.26, 57.28], [29.97, 59.89], [32.96, 58.36],
                    [1.84, 45.64]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "name": "Zwischenfoyer 2",
                "level": 3
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [26.89, 43.71], [32.43, 57.56], [35.68, 59.22],
                    [37.88, 58.63], [36.39, 54.83], [38.76, 54.57],
                    [37.00, 50.06], [42.98, 48.17], [55.20, 46.07],
                    [62.67, 46.01], [65.21, 48.22], [67.41, 48.05],
                    [73.21, 54.37], [77.61, 53.70], [64.69, 36.81]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "name": "Elevators 2. OG",
                "level": 2
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [15.25, -6.27], [25.14, 0.13], [29.36, -2.02],
                    [26.89, -11.44]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "name": "Hauptfoyer 1",
                "level": 2
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-35.24, 15.71], [-6.15, 36.03], [0.88, 31.43],
                    [-15.21, 19.89], [9.76, 0.70], [27.51, 12.13],
                    [32.96, 6.49], [1.76, -14.01]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "name": "Hauptfoyer 2",
                "level": 2
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [26.89, -16.38], [33.05, 8.75], [40.34, 7.80],
                    [37.44, -4.57], [64.16, -10.14], [70.40, 1.054],
                    [77.87, -1.05], [65.13, -24.61]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "name": "Foyer G",
                "level": 2
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-76.82, 44.65], [-50.45, 63.31], [-43.95, 61.23],
                    [-52.56, 52.27], [-45.62, 50.12], [-50.98, 47.34],
                    [-24.96, 31.06], [-41.84, 20.63]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "name": "Elevators 1. OG",
                "level": 1
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [10.28, -55.23], [27.51, -47.64], [33.31, -50.37],
                    [29.36, -57.16], [24.43, -58.40], [18.19, -58.33]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "name": "Garderobe 1",
                "level": 1
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-15.38, -39.71], [-9.58, -33.80], [6.15, -25.24],
                    [33.93, -43.33], [11.34, -53.75]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "name": "Garderobe 2",
                "level": 1
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [31.20, -54.62], [33.57, -50.35], [38.41, -51.07],
                    [40.87, -47.40], [47.55, -46.38], [66.62, -49.27],
                    [70.58, -52.48], [64.69, -59.36]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "name": "Heaven",
                "level": 1
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [2.29, -53.96], [5.54, -52.80], [18.11, -58.36],
                    [32.78, -59.53], [30.41, -63.59], [7.38, -62.59]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "name": "Foyer ABC",
                "level": 1
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-75.76, -13.24], [-49.22, 18.65], [-43.42, 15.28],
                    [-44.56, -5.27], [-59.06, -17.81], [-23.64, -41.84],
                    [-29.62, -45.09]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "name": "Elevators EG",
                "level": 0
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [2.72, -78.66], [18.11, -76.17], [33.49, -77.14],
                    [28.56, -80.00]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "name": "Lobby",
                "level": 0
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [27.86, -80.65], [36.65, -75.45], [86.66, -78.19],
                    [72.86, -82.20]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "name": "Saal 3",
                "level": 0
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-58.18, -63.59], [-26.98, -51.62], [8.525, -65.95],
                    [1.32, -67.71], [-6.94, -68.85], [-25.66, -73.15]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "name": "Foyer 3",
                "level": 0
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-75.41, -61.86], [-69.61, -58.86], [-24.87, -73.20],
                    [-5.89, -68.78], [14.33, -74.04], [22.94, -73.60],
                    [26.02, -74.73], [-8.09, -79.46]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "name": "Saal 4",
                "level": 0
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [1.76, -68.11], [8.44, -65.95], [21.53, -64.81],
                    [33.57, -67.00], [39.73, -70.32], [35.68, -72.69],
                    [23.20, -73.70]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "name": "Foyer 4",
                "level": 0
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [23.20, -73.82], [35.42, -72.84], [37.00, -72.05],
                    [48.43, -72.66], [56.60, -73.85], [52.91, -75.72],
                    [38.06, -75.34], [26.81, -74.68]
                ]]
            }
        }
    ]
};

/*
 * Checks whether a point lies within a polygon.
 *
 */
function point_in_polygon(poly, point) {
    for (var c = false, i = -1, l = poly.length, j = l - 1; ++i < l; j = i) {
        if (((poly[i][0] <= point[0] && point[0] < poly[j][0]) || (poly[j][0] <= point[0] && point[0] < poly[i][0])) &&
            (point[1] < (poly[j][1] - poly[i][1]) * (point[0] - poly[i][0]) / (poly[j][0] - poly[i][0]) + poly[i][1])) {
            (c = !c);
        }
    }
    return c;
}

/*
 * Gets the building level for a point by checking all possible level polygons.
 * Returns the level number if the point is within a level or null if it is
 * in none.
 *
 */
exports.get_level = function(point) {
    for (var i in levels.features) {
        if (point_in_polygon(levels.features[i].geometry.coordinates[0], point)) {
            return levels.features[i].properties.level;
        }
    }
    return null;
};

/*
 * Gets the room for a point by checking all possible room polygons.
 * Returns the room properties if the point is within a room or null if it is
 * in none.
 *
 */
exports.get_room = function(point) {
    for (var i in rooms.features) {
        if (point_in_polygon(rooms.features[i].geometry.coordinates[0], point)) {
            return rooms.features[i].properties;
        }
    }
    return null;
};
