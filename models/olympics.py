from utils.db import db
from flask_login import UserMixin



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    active = db.Column(db.Boolean, default=True)

    @property
    def is_active(self):
        return self.active



class Medals(db.Model):
    countrycode = db.Column(db.String(150), primary_key=True)
    country = db.Column(db.String(150), nullable=False, unique=True)
    countrylong = db.Column(db.String(150), nullable=False)
    gold = db.Column(db.Integer, nullable=False)
    silver = db.Column(db.Integer, nullable=False)
    bronze = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "countrycode": self.countrycode,
            "country": self.country,
            "countrylong": self.countrylong,
            "gold": self.gold,
            "silver": self.silver,
            "bronze": self.bronze,
            "total": self.total,
        }

    # Relationships with unique backref names
    players = db.relationship("Players", backref="medals_countrycode", lazy=True, foreign_keys="Players.countrycode")
    medalists = db.relationship("Medalists", backref="medals_countrycode", lazy=True, foreign_keys="Medalists.countrycode")


class Players(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    gender = db.Column(db.String(150), nullable=False)
    countrycode = db.Column(db.String(150), db.ForeignKey('medals.countrycode'), nullable=False)  # Foreign key for country code
    country = db.Column(db.String(150), db.ForeignKey('medals.country'), nullable=False)  # Foreign key for country name
    events = db.Column(db.String(150), nullable=False)

    # Explicit relationships for clarity
    medal_countrycode = db.relationship("Medals", foreign_keys=[countrycode], backref="players_by_countrycode")
    medal_country = db.relationship("Medals", foreign_keys=[country], backref="players_by_country")


class Medalists(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    gender = db.Column(db.String(150), nullable=False)
    medal_type = db.Column(db.String(150), nullable=False)
    countrycode = db.Column(db.String(150), db.ForeignKey('medals.countrycode'), nullable=False)  # Foreign key for country code
    country = db.Column(db.String(150), db.ForeignKey('medals.country'), nullable=False)  # Foreign key for country name
    event = db.Column(db.String(150), nullable=False)
    event_url = db.Column(db.String(150), nullable=False)

    # Explicit relationships for clarity
    medal_countrycode = db.relationship("Medals", foreign_keys=[countrycode], backref="medalists_by_countrycode")
    medal_country = db.relationship("Medals", foreign_keys=[country], backref="medalists_by_country")



class Events(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(150), nullable=False)
    tag = db.Column(db.String(150), nullable=False)
    sport = db.Column(db.String(150), nullable=False,)
    sport_code = db.Column(db.String(150), nullable=False)
    sport_url = db.Column(db.String(150), nullable=False)