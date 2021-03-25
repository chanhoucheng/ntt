from app import app,db
from app.models import User,UserRoles,Role
from werkzeug.security import generate_password_hash, check_password_hash

admin=User(username="admin",email="admin@admim.com",password_hash=generate_password_hash("admin"))
db.session.add(admin)
db.session.commit()


user=User(username="user",email="user@admim.com",password_hash=generate_password_hash("user"))
db.session.add(user)
db.session.commit()

admin_role=Role(name='Admin')
db.session.add(admin_role)
db.session.commit()


user_role=Role(name='User')
db.session.add(user_role)
db.session.commit()

admin_user_role=UserRoles(user_id=1,role_id=1)
db.session.add(admin_user_role)
db.session.commit()

user_user_role=UserRoles(user_id=2,role_id=2)
db.session.add(admin_user_role)
db.session.commit()
