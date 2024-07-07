# third-party imports
from flask import current_app
from flask_login import UserMixin
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# local imports
from . import db, login_manager


# set up user_loader
@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))


class User(UserMixin, db.Model):
  __tablename__ = "user"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(60), nullable=False)
  gender = db.Column(db.String(60), nullable=False)
  phone = db.Column(db.String(60), nullable=False, unique=True)
  email = db.Column(db.String(60), nullable=False, unique=True)
  role = db.Column(db.String(20), nullable=False, default="user")
  password = db.Column(db.String(128), nullable=False)
  joined_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
  usage_help = db.relationship("UsageHelp", backref="user", lazy=True)
  criteria = db.relationship("Criteria", backref="user", lazy=True)
  sub_criteria = db.relationship("SubCriteria", backref="user", lazy=True)
  location_point = db.relationship("LocationPoint", backref="user", lazy=True)
  tour_type = db.relationship("TourType", backref="user", lazy=True)
  tour_list = db.relationship("TourList", backref="user", lazy=True)

  def get_reset_token(self, expires_sec=1800):
    serial = Serializer(current_app.config["SECRET_KEY"], expires_sec)
    return serial.dumps({"user_id": self.id}).decode("utf-8")

  @staticmethod
  def verify_reset_token(token):
    serial = Serializer(current_app.config["SECRET_KEY"])
    try:
      user_id = serial.loads(token)["user_id"]
    except:
      return None
    return User.query.get(user_id)

  def __repr__(self):
    return f"{self.id}"

class UsageHelp(db.Model):
  __tablename__ = "usage_help"

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(128), nullable=False)
  description = db.Column(db.Text, nullable=True)
  image = db.Column(db.String(20), nullable=False, default="default.jpg")
  content = db.Column(db.Text, nullable=False,)
  posted_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
  updated_date = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now)
  user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

  def __repr__(self):
    return f"{self.id}"

class Criteria(db.Model):
  __tablename__ = "criteria"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=False)
  code = db.Column(db.String(128), nullable=False)
  attribute = db.Column(db.String(128), nullable=False)
  weight = db.Column(db.Float, nullable=False)
  posted_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
  updated_date = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now)
  user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
  sub_criteria = db.relationship("SubCriteria", back_populates="criteria")

  def __repr__(self):
    return f"{self.id}"

class SubCriteria(db.Model):
  __tablename__ = "sub_criteria"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=False)
  value = db.Column(db.Integer, nullable=False)
  posted_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
  updated_date = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now)
  user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
  criteria_id = db.Column(db.Integer, db.ForeignKey("criteria.id"), nullable=False)
  criteria = db.relationship("Criteria", back_populates="sub_criteria")

  def __repr__(self):
    return f"{self.value}"

class LocationPoint(db.Model):
  __tablename__ = "location_point"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=False)
  posted_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
  updated_date = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now)
  user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

  def __repr__(self):
    # return f"<Location Point: {self.name}>"
    return f"{self.id}"

class TourType(db.Model):
  __tablename__ = "tour_type"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=False)
  posted_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
  updated_date = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now)
  user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
  tour_list = db.relationship("TourList", back_populates="tour_type")

  def __repr__(self):
    return f"{self.id}"

class TourList(db.Model):
  __tablename__ = "tour_list"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=False)
  ticket = db.Column(db.Integer, nullable=False)
  facility = db.Column(db.Integer, nullable=False)
  infrastructure = db.Column(db.Integer, nullable=False)
  transportation_access = db.Column(db.Integer, nullable=False)
  description = db.Column(db.Text, nullable=True)
  image = db.Column(db.String(20), nullable=False, default="default.jpg")
  content = db.Column(db.Text, nullable=False,)
  posted_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
  updated_date = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now)
  user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
  tour_type_id = db.Column(db.Integer, db.ForeignKey("tour_type.id"), nullable=False)
  tour_type = db.relationship("TourType", back_populates="tour_list")
  distances = db.relationship("TourDistance", backref="tour_list", lazy=True) # relationship to distances

  def __repr__(self):
    return f"{self.id}"

class TourDistance(db.Model):
  __tablename__ = "tour_distance"

  id = db.Column(db.Integer, primary_key=True)
  tour_list_id = db.Column(db.Integer, db.ForeignKey("tour_list.id"), nullable=False)
  location_point_id = db.Column(db.Integer, db.ForeignKey("location_point.id"), nullable=False)
  distance = db.Column(db.Integer, nullable=False, default=0)
  location_point = db.relationship("LocationPoint")

  def __repr__(self):
    return f"{self.id}"