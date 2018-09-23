from flask_login import login_user, logout_user, login_required, LoginManager, current_user, UserMixin
from database_manager.setup import mgInstance
from authentication.User import User

# set flask_login
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'

# flask_login will use this method to get User class
# by given username
@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        newusername = user_id.encode('utf-8')
        findres = mgInstance.mongo.db.users.find_one({"username":newusername})
        if findres is not None:
            return User(mgInstance.mongo, newusername)
    return None