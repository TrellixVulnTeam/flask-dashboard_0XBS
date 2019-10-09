from app         import db
from flask_login import UserMixin

from . common    import COMMON, STATUS, DATATYPE

class User(UserMixin, db.Model):

    id          = db.Column(db.Integer,     primary_key=True)
    username    = db.Column(db.String(64),  unique = True)
    email       = db.Column(db.String(120), unique = True)
    firstName   = db.Column(db.String(500))
    lastName    = db.Column(db.String(500))
    role        = db.Column(db.Integer)
    password    = db.Column(db.String(500))
    password_q  = db.Column(db.Integer)
    image_file  = db.Column(db.String(20), nullable=False, default='logo.png')

    def __init__(self, username, password, firstName, email, lastName):
        self.username   = username 
        self.password   = password
        self.password_q = DATATYPE.CRYPTED
        self.firstName  = firstName
        self.email      = email
        self.lastName   = lastName

        self.group_id = None
        self.role     = None

    def __repr__(self):
        return '<User %r>' % (self.id)

    def save(self):

        # inject self into db session    
        db.session.add ( self )

        # commit change and save the object
        db.session.commit( )

        return self 

