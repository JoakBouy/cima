from create_app import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150))
    phone_number = db.Column(db.String(150), nullable=False)
    insurance_id = db.Column(db.String(150), nullable=False, unique=True)
    appointments = db.relationship('Appointment', lazy=True)

    def __repr__(self):
        return f'{self.full_name} {self.email} {self.insurance_id}'


class Appointment(db.Model):
    __tablename__ = 'appointment'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User')
    full_name = db.Column(db.String(150), nullable=False)
    note = db.Column(db.String(150), nullable=False)
    phone_number = db.Column(db.String(150), nullable=False)
    dehydration = db.Column(db.String(150)) 
    vomiting = db.Column(db.String(150))
    diarrhea = db.Column(db.String(150))
    abdominal_pain = db.Column(db.String(150))
    symptom_count = db.Column(db.Integer)
    diagnosis = db.Column(db.String(150))

    def __repr__(self):
        return f'{self.full_name} {self.note} {self.phone_number} {self.dehydration} {self.vomiting} {self.diarrhea} {self.abdominal_pain} {self.symptom_count}'
