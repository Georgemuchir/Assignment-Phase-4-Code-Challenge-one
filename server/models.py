from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

# Custom metadata for foreign key naming convention
db = SQLAlchemy(metadata={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"
})

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    super_name = db.Column(db.String, nullable=False)
    
    # Relationships and serialization rules
    hero_powers = relationship('HeroPower', backref='hero', cascade="all, delete-orphan")
    powers = association_proxy('hero_powers', 'power')
    serialize_rules = ('-hero_powers.hero',)

    def __repr__(self):
        return f'<Hero {self.id}>'

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    
    # Relationships and validation
    hero_powers = relationship('HeroPower', backref='power', cascade="all, delete-orphan")
    heroes = association_proxy('hero_powers', 'hero')
    serialize_rules = ('-hero_powers.power',)

    @validates('description')
    def validate_description(self, key, description):
        if len(description) < 20:
            raise ValueError("Description must be at least 20 characters long.")
        return description

    def __repr__(self):
        return f'<Power {self.id}>'

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)
    hero_id = db.Column(db.Integer, ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, ForeignKey('powers.id'), nullable=False)
    
    # Validation and serialization rules
    serialize_rules = ('-hero.hero_powers', '-power.hero_powers')

    @validates('strength')
    def validate_strength(self, key, strength):
        if strength not in ['Strong', 'Weak', 'Average']:
            raise ValueError("Strength must be 'Strong', 'Weak', or 'Average'.")
        return strength

    def __repr__(self):
        return f'<HeroPower {self.id}>'