# c3bottles example configuration file
#
# Copy this file to config.py and edit it as needed. In any case, you have
# to set a proper SQLALCHEMY_DATABASE_URI and a SECRET_KEY. The other settings
# are optional.

# Example SQLAlchemy database URI for PostgreSQL.
# SQLALCHEMY_DATABASE_URI = "postgresql://username:password@host/database"

# Example SQLAlchemy database URI for SQLite (relative path).
# SQLALCHEMY_DATABASE_URI = "sqlite:///c3bottles.db"

# The secret key used for signing the session cookie.
# SECRET_KEY = "changeme"

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

# The factor at which the crate count of a drop point impacts the visit
# priority. A factor of 0.1 means that the priority is increased by 10% for
# every additional crate. (default: 0.1)
# SIZE_IMPACT_FACTOR = 0.1

# vim: set expandtab ts=4 sw=4:
