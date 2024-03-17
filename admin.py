
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from database import app

app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
admin = Admin(app, name='Admin', template_mode='bootstrap3')