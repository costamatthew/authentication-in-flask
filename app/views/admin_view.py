from flask import (Blueprint)
from flask_httpauth import HTTPBasicAuth
from app.models.user_model import UserModel

bp_admin = Blueprint("bp_admin", __name__, url_prefix='/admin')

auth = HTTPBasicAuth()




@auth.verify_password
def verify_password(username, password):
    try:
        user = UserModel.query.filter_by(email=username).first()
        if UserModel.verify_password(user, password):
            return user.serialized["API_Key"]
    except:
        pass



@bp_admin.route('/')
@auth.login_required
def admin():
    return "API Key: {}".format(auth.current_user())
