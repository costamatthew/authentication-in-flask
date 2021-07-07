from flask import (Blueprint, render_template, redirect)
from flask_httpauth import HTTPDigestAuth
from app.models.user_model import UserModel

bp_admin = Blueprint("bp_admin", __name__, url_prefix='/admin', template_folder='templates')

auth = HTTPDigestAuth()




@auth.get_password
def get_password(email):
    try:
        user = UserModel.query.filter_by(email=email).first()
        return user.password
    except:
        ...




@bp_admin.route('/')
@auth.login_required
def admin():
    user_email = auth.current_user()
    user_info = UserModel.query.filter_by(email=user_email).first()
    user_info_serialized = user_info.serialized
    return render_template("admin.html", data=user_info_serialized)




@bp_admin.route('/logout')
@auth.login_required
def logout():
    return redirect("/admin/"), 401
