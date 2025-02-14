import os
import tempfile
import pytest
import      datetime,time,os,re
from sqlalchemy  import desc,or_

from flask_frozen import Freezer

from app         import app, lm, db, bc
from . common    import COMMON, DATATYPE
from . models    import User

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('flask_test.cfg')
 
    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()
 
    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()
 
    yield testing_client  # this is where the testing happens!
 
    ctx.pop()
