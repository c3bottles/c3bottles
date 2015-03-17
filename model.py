from datetime import datetime

from c3bottles import db

# A drop point is a location somewhere in the supervised area where one or
# several crates are placed for visitors to drop their empty bottles into.
#
# A drop point consists of a sign "bottle drop point <number>" at the wall
# which tells visitors that a drop point should be present there and a number
# of empty crates to drop bottles into. The sign is resembled by the location
# class whereas the crates are resembled by the capacity class. Drop points
# may exist with capacity zero (i.e. only a sign on the wall, no crates) or
# a location with valid time but no description or coordinates (i.e. the
# drop point is present somewhere but the location is unknown).
#
# If a drop point exists but has no location and capacity, the number has been
# registered in the system but sign & crate(s) have not been placed in the
# venue yet. If the `removed` column is not null, the drop point has been
# removed from the venue completely (numbers are not reassigned).
# 
# Each drop point is referenced by a unique number, which is consequently
# the primary key to identify a specific drop point. Since capacity and
# location of drop points may change over time, they are not simply saved in
# the table of drop points but rather classes themselves.

class DropPoint(db.Model):
	number = db.Column(db.Integer, primary_key=True, autoincrement=False)
	removed = db.Column(db.DateTime)

	def __init__(self, number, placed=False, loc_desc=None, loc_coords=None, crates=None, start_time=None):
		self.number = number
		db.session.add(self)
		if placed:
			Location(dp=self, start_time=start_time, description=loc_desc, coords=loc_coords)
			Capacity(dp=self, start_time=start_time, crates=crates)

	def remove(self, time=None):
		if not self.removed:
			if not time:
				time = datetime.today()
			self.removed = time
	
	def report(self, state=None, time=None):
		Report(dp=self, time=time, state=state)

	def visit(self, action=None, time=None):
		Visit(dp=self, time=time, action=action)
	
	def __repr__(self):
		return "<Drop point no. %s>" % self.number


# Drop points may be relocated at any time for whatever reason. For analysis
# after an event and optimization of the drop point locations for the next
# event at the same venue, drop point locations are tracked over time.
#
# Each location has a start time indicating the placement of the drop point
# at that location. If a drop point is relocated, a new location with the
# respective start time is added. If the start time is null, the drop point
# has been there since the creation of the universe.
#
# If the human-readable description as well as the coordinates both are null,
# the location of that drop point is unknwon.

class Location(db.Model):
	loc_id = db.Column(db.Integer, primary_key=True)
	dp_id = db.Column(db.Integer, db.ForeignKey("drop_point.number"), nullable=False)
	dp = db.relationship("DropPoint", backref=db.backref("locations", lazy="dynamic"))
	start_time = db.Column(db.DateTime)
	description = db.Column(db.String(140))
	coordinate_x = db.Column(db.Integer)
	coordinate_y = db.Column(db.Integer)
	coordinate_z = db.Column(db.Integer)

	def coords(self):
		return (coordinate_x, coordinate_y, coordinate_z)

	def __init__(self, dp, start_time=None, description=None, coords=None):
		self.dp = dp
		if not start_time:
			start_time = datetime.today()
		self.start_time = start_time
		self.description = description
		if coords and len(coords) is 3:
			self.coordinate_x = coords[0]
			self.coordinate_y = coords[1]
			self.coordinate_z = coordi[2]
		db.session.add(self)
	
	def __repr__(self):
		return "<Location %s of %s>" % (self.loc_id, self.dp)


# The capacity of drop points may change over time as empty crates can and
# will be added or removed on demand. Like the location, the capacity is
# tracked over time to allow for analysis and optimization after an event.
#
# Each capacity has a start time indicating the presence of a particular
# number of empty crates at the drop point at that time. If crates are added
# or removed, a new capacity with the respective start time is added. If the
# start time is null, the crates have been there forever.
#
# If the number of crates is null, the drop point only consists of a sign on
# the wall but no crates at all.

class Capacity(db.Model):
	cap_id = db.Column(db.Integer, primary_key=True)
	dp_id = db.Column(db.Integer, db.ForeignKey("drop_point.number"), nullable=False)
	dp = db.relationship("DropPoint", backref=db.backref("capacities", lazy="dynamic"))
	start_time = db.Column(db.DateTime)
	crates = db.Column(db.Integer, default=1)

	def __init__(self, dp, start_time=None, crates=None):
		self.dp = dp
		if not start_time:
			start_time = datetime.today()
		self.start_time = start_time
		if crates >= 0:
			self.crates = crates
		db.session.add(self)
	
	def __repr__(self):
		return "<Capacity %s of %s>" % (self.cap_id, self.dp)


# When visitors find a drop point needing maintenance, they may report the
# drop point to the bottle collectors. A report is issued for a given drop
# point which has a time and optionally some information about the state of
# the drop point in question.

report_states = ("DEFAULT", "NO_CRATES", "SOME_BOTTLES", "RESONABLY_FULL", "FULL", "OVERFLOW")

class Report(db.Model):
	rep_id = db.Column(db.Integer, primary_key=True)
	dp_id = db.Column(db.Integer, db.ForeignKey("drop_point.number"), nullable=False)
	dp = db.relationship("DropPoint", backref=db.backref("reports", lazy="dynamic"))
	time = db.Column(db.DateTime, nullable=False)
	state = db.Column(db.Enum(*report_states, name="report_states"), default=report_states[0])

	def __init__(self, dp, time=None, state=None):
		self.dp = dp
		if not time:
			time = datetime.today()
		self.time = time
		if state in report_states:
			self.state = state
		else:
			self.state = report_states[0]
		db.session.add(self)
	
	def __repr__(self):
		return "<Report %s of %s>" % (self.rep_id, self.dp)


# After a report of a problem with a certain drop point has been generated or
# a drop point has not been visited for a long time, the bottle collectors are
# advised to visit that drop point. After doing so, they log their visit and
# the action taken.

visit_actions = ("EMPTIED", "ADDED_CRATE", "REMOVED_CRATE", "RELOCATED", "REMOVED", "NO_ACTION")

class Visit(db.Model):
	vis_id = db.Column(db.Integer, primary_key=True)
	dp_id = db.Column(db.Integer, db.ForeignKey("drop_point.number"), nullable=False)
	dp = db.relationship("DropPoint", backref=db.backref("visits", lazy="dynamic"))
	time = db.Column(db.DateTime, nullable=False)
	action = db.Column(db.Enum(*visit_actions, name="visit_actions"), default=visit_actions[0])

	def __init__(self, dp, time=None, action=None):
		self.dp = dp
		if not time:
			time = datetime.today()
		self.time = time
		if action in visit_actions:
			self.action = action
		else:
			self.action = visit_actions[0]
		db.session.add(self)

	def __repr__(self):
		return "<Visit %s of %s>" % (self.vis_id, self.dp)
