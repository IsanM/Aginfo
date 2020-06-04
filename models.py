from sqlalchemy.orm import backref
from app import db
from datetime import datetime


# DATABASE MODELING

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class District(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    districtName = db.Column(db.Text, nullable=False)
    area = db.relationship('Area', backref('district'))
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    # add relation ship with area(one to Many)
    # one to many relationship beetween district and user which mean one district live in many users


class Area(db.Model):
    areaid = db.Column(db.Integer, primary_key=True)
    areaName = db.Column(db.Text, nullable=False)
    district_id = db.Column(db.Integer(), db.ForeignKey('districts.id'))
    devisionoffices = db.relationship('Devisionoffice', backref('area'))
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    # add Relationship with offices(one to many)
    # add crop growing area


class Devisionoffice(db.Model):
    officeid = db.Column(db.Integer, primary_key=True)
    officeName = db.Column(db.Text, nullable=False)
    officeAddress = db.Column(db.Text, nullable=False)
    area_id = db.Column(db.Integer(), db.ForeignKey('areas.id'))
    users = db.relationship('User', backref='devisionoffice')
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fristname = db.Column(db.Text, nullable=False)
    lastname = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.Integer(10), nullable=False, unique=True)
    address = db.Column(db.Text, nullable=False)
    profile = db.Column(db.String(255), nullable=True)
    usertype = db.Column(db.String(20), nullable=False)
    active = db.Column(db.Boolean())
    farm = db.relationship('Farm', backref='user')
    fieldvisit = db.relationship('Fieldvisit', backref='user')
    devisionoffice_id = db.Column(db.Integer(), db.ForeignKey('devisionoffices.id'))
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    # one to many relationship between district and user which mean one district live in many users


farm_crops = db.Table('farm_crops',
                      db.Column('farm_id', db.Integer, db.ForeignKey('farms.id')),
                      db.Column('crop_id', db.Integer, db.ForeignKey('crops.id'))
                      )

farm_fieldvisits = db.Table('farm_fieldvisits',
                            db.Column('fieldvisit_id', db.Integer, db.ForeignKey('fieldvisits.id')),
                            db.Column('farm_id', db.Integer, db.ForeignKey('farms.id'))
                            )


class Fieldvisit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vistareaname = db.Column(db.Text, nullable=False)
    specialnotes = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class Farm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    farmname = db.Column(db.Text, nullable=False)
    latitude = db.Column(db.Float(10, 6), nullable=False)
    longitude = db.Column(db.Float(10, 6), nullable=False)
    phone = db.Column(db.Integer(10), nullable=False, unique=False)
    address = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(255), nullable=True, unique=False)
    crop = db.Column('Crop', backref='farm')
    farmtask = db.relationship('Farmtask', backref='farm')
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    farmtasks = db.relationship('Farmtask', backref='farm')
    fieldvisit = db.relationship('Fieldvisit', secondary=farm_fieldvisits, backref='farm')
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class Farmtask(db.Model):
    taskid = db.Column(db.Integer, primary_key=True)
    taskName = db.Column(db.Text, nullable=False)
    isDone = db.Column(db.Boolean())
    farm_id = db.Column(db.Integer(), db.ForeignKey('farms.id'))
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


crop_fertilizers = db.Table('crop_fertilizers',
                            db.Column('crop_id', db.Integer, db.ForeignKey('crops.id')),
                            db.Column('fertilizer_id', db.Integer, db.ForeignKey('fertilizers.id'))
                            )
crop_soils = db.Table('crop_soils',
                      db.Column('crop_id', db.Integer, db.ForeignKey('crops.id')),
                      db.Column('soil_id', db.Integer, db.ForeignKey('soils.id'))
                      )


class Crop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cropeName = db.Column(db.Text, nullable=False)
    cropImage = db.Column(db.String(255), nullable=False)
    farm_id = db.Column(db.Integer(), db.ForeignKey('farms.id'))
    farms = db.relationship('Farm', secondary=farm_crops, backref='crops')
    harvest = db.relationship('Harvest', backref='crop')
    pestdisease = db.relationship('Pestdisease', backref='crop')
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    # add relationships fertilizer,crop tasks,soils,user,harvesting,tasks


class Fertilizer(db.Model):
    fertilizerid = db.Column(db.Integer, primary_key=True)
    fertlizerName = db.Column(db.Text, nullable=False)
    gorowingLevel = db.Column(db.Text, nullable=False)
    fertilizertype = db.Column(db.Text, nullable=False)
    crops = db.relationship('Crop', secondary=crop_fertilizers, backref='fertilizer')
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    # Add relationship crops


class Soil(db.Model):
    soilid = db.Column(db.Integer, primary_key=True)
    soilidName = db.Column(db.Text, nullable=False)
    soilidType = db.Column(db.Text, nullable=False)
    growingLevel = db.Column(db.Text, nullable=False)
    crops = db.relationship('Crop', secondary=crop_soils, backref='soils')
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    # add relationship with crop


class Harvest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cropName = db.Column(db.Text, nullable=False)
    harvestAmount = db.Column(db.Float, nullable=False)
    sellingPrice = db.Column(db.Float, nullable=False)
    datetime = db.Column(db.Date, nullable=False)
    crop_id = db.Column(db.Integer(), db.ForeignKey('crops.id'))
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    # add relationship with crop


pestdisease_diseasethreatmants = db.Table('pestdisease_diseasethreatmants',
                                          db.Column('pestdisease_id', db.Integer, db.ForeignKey('pestdiseases.id')),
                                          db.Column('diseasethreatmant_id', db.Integer,  db.ForeignKey('diseasethreatmants.id'))

                                          )


class Pestdisease(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    diseaseName = db.Column(db.Text, nullable=False)
    diseaseCauses = db.Column(db.Text, nullable=False)
    diseaseSymptons = db.Column(db.Text, nullable=False)
    crops_id = db.Column(db.Integer(), db.ForeignKey('crops.id'))
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    # add relationship with crops threatments


class Diseasethreatmant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    threatmentName = db.Column(db.Text, nullable=False)
    threatments = db.Column(db.Text, nullable=False)
    threatmentChemicalLevel = db.Column(db.Text, nullable=False)
    preventionStatus = db.Column(db.Text, nullable=False)
    pestdisease = db.relationship('Pestdisease', secondary=pestdisease_diseasethreatmants, backref='diseasethreatmant')
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    # add relationship with crops

# class Tasks(db.Model):
# taskid = db.Column(db.Integer, primary_key=True)
# taskName = db.Column(db.String(200), nullable=False)
# taskIsDone = db.Column(db.Boolean, nullable=False)
# taskStartDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
# taskEndDate = db.Column(db.DateTime, nullable=False)
# add relationships
