# c3bottles example configuration file
#
# Copy this file to config.py and edit it as needed. In any case, you have
# to set a proper SQLALCHEMY_DATABASE_URI and a SECRET_KEY. The other settings
# are optional.

# Example SQLAlchemy database URI for PostgreSQL.
# SQLALCHEMY_DATABASE_URI = "postgresql://username:password@host/database"

# Example SQLAlchemy database URI for SQLite (relative path).
# SQLALCHEMY_DATABASE_URI = "sqlite:///c3bottles.db"

# Database URL for the Docker service as in docker-compose.yml.
# SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@db/postgres

# The secret key used for signing the session cookie.
# SECRET_KEY = "changeme"

# The map to use. The different maps are defined in c3bottles/config/map.py
# and the setting here selects one of the different maps that are available.
# Any setting can be overridden by calling the override() method of any map
# configuration. This can be useful if settings need to be changed at runtime
# without redeployment which could mean rebuilding containers etc.
# from c3bottles.config.map import *
# MAP_SOURCE = C3Nav35C3
# C3Nav35C3.override("tileserver", "https://tiles.example.tld/")

# The name of the drop point label template. This must be a SVG file placed in
# the templates/label directory. The setting is the base name of this file,
# i.e. without extension.
# LABEL_STYLE = "default"

# Enable and configure the integrated Prometheus endpoint. To use Prometheus in
# Docker, please set PROMETHEUS_ADDRESS to 0.0.0.0 instead of 127.0.0.1 to make
# it accessible from outside the container.
# PROMETHEUS_ENABLED = True  # (default: False)
# PROMETHEUS_ADDRESS = "0.0.0.0"  # (default: 127.0.0.1)
# PROMETHEUS_PORT = 9567

# Mark the session and remember cookies as secure. You should enable this if
# you run c3bottles on a HTTPS server.
# SESSION_COOKIE_SECURE = True
# REMEMBER_COOKIE_SECURE = True

# Show error messages in the web server log file instead of just "500".
# (default: False)
# PROPAGATE_EXCEPTIONS = True

# Disable anonymous reporting (useful during the setup phase in the beginning
# of an event. (default: False)
# NO_ANONYMOUS_REPORTING = False

# Base interval at which drop points should be visited by the bottle collection
# team. (default: 2 hours)
# BASE_VISIT_INTERVAL = 120  # in minutes

# Default visit priority of a drop point if no reports were submitted since the
# last visit or since creation of the drop point if it has not been visited yet.
# The setting should be handled with care. A higher setting decreases the
# dependence of visit priority from reports by increasing the base level.
# A setting of 0 completely disables the growth of visit priority over time if
# no reports have been submitted. (default: 1)
# DEFAULT_VISIT_PRIORITY = 1

##############################################
#    PLEASE KEEP THE LINES BELOW UNCHANGED   #
# EXCEPT YOU REALLY KNOW WHAT YOU ARE DOING! #
##############################################
SQLALCHEMY_TRACK_MODIFICATIONS = False
BABEL_TRANSLATION_DIRECTORIES = "../translations"
SESSION_COOKIE_HTTPONLY = True
REMEMBER_COOKIE_HTTPONLY = True
