# c3bottles

[![Build Status](https://travis-ci.org/c3bottles/c3bottles.svg)](https://travis-ci.org/c3bottles/c3bottles)

Please have a look in [INSTALL.md](INSTALL.md) on how to install and build
c3bottles.

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

However, there are some caveats: In a large building like the CCH nobody is
able to memorize all the drop points and some of them may be forgotten and
overflow without anyone noticing. In addition, if the planning in advance was
not perfect (as always), some drop points in popular locations may overflow
very quickly making the job of the collectors a lot harder. At an overflowing
drop point, they can't simply exchange a full crate for an empty one but
instead have to put all the bottles laying on and around the more than full
crate into their fresh one. In the worst case they then have lots of full but
no empty crates left in locations with a high bottle drop rate. If that ever
happens, the bottlecalypse is inevitable.

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
database with its number, position and capacity (i.e. number of empty crates).
It gets a label telling the visitors to report full drop points using a URL
specific for every drop point. On the website, the visitor can report the drop
point as needing attention by simply clicking a button. Optionally, the visitor
may inform the bottle collectors about the filling level of the drop point.

The other end of the web interface shows a list of drop points to visit ordered
by priority: Drop points reported a lot lately get a high priority which is
even higher if the respective drop point has a high capacity and/or was just
emptied and is filling up again quickly. Drop points not visited for a long
time get a high priority too, so the collectors can check their current state.

A map shows the location of all the drop points so new members of the bottle
collector team can find them easily and visitors can always find the nearest
drop point to their current location.

The bottle collectors track their actions when visiting drop points by clicking
a button whenever they empty a drop point. In addition, they can change the
location or capacity of drop points if needed.
