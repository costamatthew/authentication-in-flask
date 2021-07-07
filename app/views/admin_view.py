from flask import (Blueprint, render_template, redirect)
from flask_httpauth import HTTPBasicAuth
from app.models.user_model import UserModel

bp_admin = Blueprint("bp_admin", __name__, url_prefix='/admin', template_folder='templates')

auth = HTTPBasicAuth()




@auth.verify_password
def verify_password(username, password):
    try:
        user = UserModel.query.filter_by(email=username).first()
        if UserModel.verify_password(user, password):
            return user.serialized
    except:
        pass




@bp_admin.route('/')
@auth.login_required
def admin():
    user_info = auth.current_user()
    return render_template("admin.html", data=user_info)




@bp_admin.route('/logout')
@auth.login_required
def logout():
    return redirect("/admin/"), 401
