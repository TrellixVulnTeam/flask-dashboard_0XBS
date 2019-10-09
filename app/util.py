from flask   import json, url_for, jsonify, render_template
from jinja2  import TemplateNotFound
from app     import app

from . models import User
from app    import app, db, bc
from . common import *
from sqlalchemy import desc,or_
import hashlib
from flask_mail  import Message
import re
from flask       import render_template

import      os, datetime, time, random
from PIL import Image
basedir = os.path.abspath(os.path.dirname(__file__))
# build a Json response
def response( data ):
    return app.response_class( response=json.dumps(data),
                               status=200,
                               mimetype='application/json' )

def g_db_commit( ):

    db.session.commit( );    

def g_db_add( obj ):

    if obj:
        db.session.add ( obj )

def g_db_del( obj ):

    if obj:
        db.session.delete ( obj )

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

