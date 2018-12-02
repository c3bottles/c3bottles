# c3bottles

[![Codacy](https://api.codacy.com/project/badge/Grade/ab7d4e458baf487b984e5f6baa16e57f)](https://www.codacy.com/app/michik-github/c3bottles)
[![Coverage](https://api.codacy.com/project/badge/Coverage/ab7d4e458baf487b984e5f6baa16e57f)](https://www.codacy.com/app/c3bottles/c3bottles)
[![Build Status](https://travis-ci.org/c3bottles/c3bottles.svg)](https://travis-ci.org/c3bottles/c3bottles)
[![MIT License](https://img.shields.io/github/license/c3bottles/c3bottles.svg?maxAge=2592000)](https://github.com/c3bottles/c3bottles/blob/master/LICENSE.md)

Please have a look in [INSTALL.md](doc/INSTALL.md) on how to install and build
c3bottles. All the scripts and configuration needed to run c3bottles in
Docker are available as well, please see [DOCKER.md](doc/DOCKER.md) for the details.
If you want to get involved and improve c3bottles or adapt it to your specific
needs, please have a look at [DEVELOPMENT.md](doc/DEVELOPMENT.md).

## What is this about?

c3bottles is a bottle drop and collection management system for chaos events.
Collecting all the empty bottles is a hard task at every event since they
appear in large numbers at places and times you cannot always plan beforehand.
Bottle collectors need to roam the area all the time and check it periodically
for any left empty bottles.

To make this job a lot easier, bottle drop points were invented: Empty crates
are placed at spots in the area where a high level of empty bottles is
expected, e.g. exits of lecture halls, lounges or the main exit/entrance of a
building. The visitors are advised to leave their bottles not at random but
rather only at the designated bottle drop points. The bottle collectors then
only need to visit these points to do their job.

However, there are some caveats: In a large building nobody is able to memorize
all the drop points and some of them may be forgotten and overflow without
anyone noticing. In addition, if the planning in advance was not perfect (as
always), some drop points in popular locations may overflow very quickly making
the job of the collectors a lot harder. At an overflowing drop point, they
can't simply exchange a full crate for an empty one but instead have to put all
the bottles laying on and around the more than full crate into their fresh one.
In the worst case they then have lots of full but no empty crates left in
locations with a high bottle drop rate. If that ever happens, the bottlecalypse
is inevitable.

c3bottles aims to solve this problem using modern web technology combined with
crowdsourcing: A database tracks the state of all the drop points and visitors
noticing full or overflowing drop points can report that fact. The bottle
collectors will be notified and can react promptly. They track their tour and
the system can notify them of drop points not visited in a long time or needing
immediate action. Statistical analysis allows for continuous optimization of
drop point placement by scaling drop points according to the demand or
abandoning drop points in remote locations which are not used much anyway.

## How does this work?

During placement of bottle drop points, every drop point is registered in the
database with an identifier and its position. A label to be printed directly
from the web interface tells the visitors to report full drop points using a
URL specific for every drop point. On the website, the visitor can report the
drop point as needing attention by simply clicking a button. Optionally, the
visitor may inform the bottle collectors about the filling level of the drop
point.

The other end of the web interface shows a list of drop points to visit ordered
by priority: Drop points reported a lot lately get a higher priority. The
priority of drop points not visited for a long time grows over time as well,
so the collectors will check their state eventually.

A map shows the location of all the drop points so new members of the bottle
collector team can find them easily and visitors can always find the nearest
drop point to their current location.

The bottle collectors track their actions when visiting drop points by clicking
a button whenever they empty a drop point. In addition, they can change the
location of drop points, remove unused ones or create new ones on the fly as
needed.

## Evolution of features

The system has been used for bottle collection on 32C3, 33C3 and for trashcans
on SHA2017. During 34C3, bottle drop points as well as trashcans needed to be
emptied, so trashcans were added ad-hoc. After 34C3, categories were added,
so the system is now suited to track different categories of targets, be it
bottle drop points, trashcans or other locations that need to be visited
more or less frequently based on user feedback.

The map started as custom tiles rendered from a large PNG file and over time
has been extended to be compatible with a number of different map sources that
can be used with Leaflet, e.g. OpenStreetMap or [c3nav](https://c3nav.de/).
The details regarding different map configurations can be found in
[MAP.md](doc/MAP.md).
