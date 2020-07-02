from flasksystem import db, login_manager, app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# DATABASE MODELING
"""
class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
"""


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class District(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    districtName = db.Column(db.Text, nullable=False)
    area = db.relationship('Area', backref='district', lazy=True)
    created_timestamp = db.Column(db.DateTime, default=datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # add relation ship with area(one to Many)
    # one to many relationship beetween district and user which mean one district live in many users


class Area(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    areaName = db.Column(db.Text, nullable=False)
    devisionoffices = db.relationship('Devisionoffice', backref='area')
    district_id = db.Column(db.Integer, db.ForeignKey('district.id'), nullable=False)
    created_timestamp = db.Column(db.DateTime, default=datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # add Relationship with offices(one to many)
    # add crop growing area


class Devisionoffice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    officeName = db.Column(db.Text, nullable=False)
    officeAddress = db.Column(db.Text, nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'))
    users = db.relationship('User', backref='devisionoffice')
    created_timestamp = db.Column(db.DateTime, default=datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fristname = db.Column(db.Text, nullable=False)
    lastname = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.Integer, nullable=False, unique=True)
    address = db.Column(db.Text, nullable=False)
    profile = db.Column(db.String(255), nullable=True)
    usertype = db.Column(db.String(20), nullable=False)
    active = db.Column(db.Boolean)
    farm = db.relationship('Farm', backref='user')
    fieldvisit = db.relationship('Fieldvisit', backref='user')
    devisionoffice_id = db.Column(db.Integer, db.ForeignKey('devisionoffice.id'))
    created_timestamp = db.Column(db.DateTime, default=datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # one to many relationship between district and user which mean one district live in many
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


farm_crops = db.Table('farm_crops',
                      db.Column('farm_id', db.Integer, db.ForeignKey('farm.id')),
                      db.Column('crop_id', db.Integer, db.ForeignKey('crop.id'))
                      )

farm_fieldvisits = db.Table('farm_fieldvisits',
                            db.Column('fieldvisit_id', db.Integer, db.ForeignKey('fieldvisit.id')),
                            db.Column('farm_id', db.Integer, db.ForeignKey('farm.id'))
                            )


class Fieldvisit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vistareaname = db.Column(db.Text, nullable=False)
    specialnotes = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_timestamp = db.Column(db.DateTime, default=datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class Farm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    farmname = db.Column(db.Text, nullable=False)
    latitude = db.Column(db.Float(10, 6), nullable=False)
    longitude = db.Column(db.Float(10, 6), nullable=False)
    phone = db.Column(db.Integer, nullable=False, unique=False)
    address = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(255), nullable=True, unique=False)
    farmtask = db.relationship('Farmtask', backref='farm')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    fieldvisit = db.relationship('Fieldvisit', secondary=farm_fieldvisits, backref='farm')
    created_timestamp = db.Column(db.DateTime, default=datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class Farmtask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    taskName = db.Column(db.Text, nullable=False)
    isDone = db.Column(db.Boolean)
    farm_id = db.Column(db.Integer, db.ForeignKey('farm.id'))
    created_timestamp = db.Column(db.DateTime, default=datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


crop_fertilizers = db.Table('crop_fertilizers',
                            db.Column('crop_id', db.Integer, db.ForeignKey('crop.id')),
                            db.Column('fertilizer_id', db.Integer, db.ForeignKey('fertilizer.id'))
                            )
crop_soils = db.Table('crop_soils',
                      db.Column('crop_id', db.Integer, db.ForeignKey('crop.id')),
                      db.Column('soil_id', db.Integer, db.ForeignKey('soil.id'))
                      )


class Crop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cropeName = db.Column(db.Text, nullable=False)
    cropImage = db.Column(db.String(255), nullable=False)
    farm_id = db.Column(db.Integer, db.ForeignKey('farm.id'))
    farms = db.relationship('Farm', secondary=farm_crops, backref='crop')
    harvest = db.relationship('Harvest', backref='crop')
    pestdisease = db.relationship('Pestdisease', backref='crop')
    created_timestamp = db.Column(db.DateTime, default=datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # add relationships fertilizer,crop tasks,soils,user,harvesting,tasks


class Fertilizer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fertlizerName = db.Column(db.Text, nullable=False)
    gorowingLevel = db.Column(db.Text, nullable=False)
    fertilizertype = db.Column(db.Text, nullable=False)
    crops = db.relationship('Crop', secondary=crop_fertilizers, backref='fertilizer')
    created_timestamp = db.Column(db.DateTime, default=datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # Add relationship crops


class Soil(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    soilidName = db.Column(db.Text, nullable=False)
    soilidType = db.Column(db.Text, nullable=False)
    growingLevel = db.Column(db.Text, nullable=False)
    crops = db.relationship('Crop', secondary=crop_soils, backref='soil')
    created_timestamp = db.Column(db.DateTime, default=datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # add relationship with crop


class Harvest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cropName = db.Column(db.Text, nullable=False)
    harvestAmount = db.Column(db.Float, nullable=False)
    sellingPrice = db.Column(db.Float, nullable=False)
    datetime = db.Column(db.Date, nullable=False)
    crop_id = db.Column(db.Integer, db.ForeignKey('crop.id'))

    # add relationship with crop


pestdisease_diseasethreatmants = db.Table('pestdisease_diseasethreatmants',
                                          db.Column('pestdisease_id', db.Integer, db.ForeignKey('pestdisease.id')),
                                          db.Column('diseasethreatmant_id', db.Integer,
                                                    db.ForeignKey('diseasethreatmant.id'))

                                          )


class Pestdisease(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    diseaseName = db.Column(db.Text, nullable=False)
    diseaseCauses = db.Column(db.Text, nullable=False)
    diseaseSymptons = db.Column(db.Text, nullable=False)
    crops_id = db.Column(db.Integer, db.ForeignKey('crop.id'))
    created_timestamp = db.Column(db.DateTime, default=datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # add relationship with crops threatments


class Diseasethreatmant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    threatmentName = db.Column(db.Text, nullable=False)
    threatments = db.Column(db.Text, nullable=False)
    threatmentChemicalLevel = db.Column(db.Text, nullable=False)
    preventionStatus = db.Column(db.Text, nullable=False)
    pestdisease = db.relationship('Pestdisease', secondary=pestdisease_diseasethreatmants, backref='diseasethreatmant')
    created_timestamp = db.Column(db.DateTime, default=datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # add relationship with crops

# class Tasks(db.Model):
# taskid = db.Column(db.Integer, primary_key=True)
# taskName = db.Column(db.String(200), nullable=False)
# taskIsDone = db.Column(db.Boolean, nullable=False)
# taskStartDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
# taskEndDate = db.Column(db.DateTime, nullable=False)
# add relationships
