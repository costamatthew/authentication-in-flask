from flask import Blueprint, current_app, render_template, request, jsonify

import secrets
from http import HTTPStatus
from flask_httpauth import HTTPTokenAuth
from app.models.user_model import UserModel
from app.services.end_session import end_session


api_token = secrets
auth = HTTPTokenAuth()
bp_api = Blueprint("bp_api", __name__, url_prefix='/api', template_folder='template')




@auth.verify_token
def verify_token(token):
    user = UserModel.query.filter_by(api_key=token).first()
    if user:
        return user.serialized




@bp_api.get("/signup")
def signup_page():
    return render_template("signup.html"), HTTPStatus.OK




@bp_api.post("/")
def signup():
    session = current_app.db.session
    data_form = request.form

    new_api_token = api_token.token_hex(16)
    password_to_hash = data_form["password"]

    new_user = UserModel(name=data_form["name"], 
                        last_name=data_form["last_name"], 
                        email=data_form["email"], 
                        api_key=new_api_token)

    new_user.password = password_to_hash
    end_session(session, new_user)
    return jsonify(new_user.serialized), HTTPStatus.OK




@bp_api.get("/")
@auth.login_required
def signup_get():
    return jsonify(auth.current_user()), HTTPStatus.OK




@bp_api.put("/")
@auth.login_required
def signup_update():
    session = current_app.db.session
    data = request.get_json()

    request_bearer_token = request.headers
    bearer_token = request_bearer_token.get("Authorization").replace("Bearer", "").strip()
    data_to_update: UserModel = UserModel.query.filter_by(api_key=bearer_token).first()

    for key, value in data.items():
        setattr(data_to_update, key, value)

    end_session(session, data_to_update)

    return jsonify(data_to_update.serialized), HTTPStatus.OK




@bp_api.delete("/")
@auth.login_required
def signup_delete():
    session = current_app.db.session

    request_bearer_token = request.headers
    bearer_token = request_bearer_token.get("Authorization").replace("Bearer", "").strip()
    data_to_delete: UserModel = UserModel.query.filter_by(api_key=bearer_token).first()

    session.delete(data_to_delete)
    session.commit()

    return "", HTTPStatus.NO_CONTENT
