from database import db

from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
def create_super_user():
    hashed_password = generate_password_hash('22251425Vyny*', method='sha256')
    super_user = User(username='vynoroidtechnologies@gmail.com', password=hashed_password)
    db.session.add(super_user)
    db.session.commit()