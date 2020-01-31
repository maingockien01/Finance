import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    
    SQLACHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \ 
        'sqlite:///' + os.path.join(basedir, 'finance.db')
    SQLAlCHEMT_TRACK_MODIFICATION = False
