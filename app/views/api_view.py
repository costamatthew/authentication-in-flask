from flask import Blueprint, current_app, render_template, request, jsonify

from http import HTTPStatus
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app.models.user_model import UserModel
from app.services.end_session import end_session


bp_api = Blueprint("bp_api", __name__, url_prefix='/api', template_folder='template')




@bp_api.route("/auth", methods=["POST"])
def auth():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    user = UserModel.query.filter_by(email=username).first()
    if UserModel.verify_password(user, password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)

    return jsonify({"msg": "Bad username or password"}), 401




@bp_api.get("/signup")
def signup_page():
    return render_template("signup.html"), HTTPStatus.OK




@bp_api.post("/")
def signup():
    session = current_app.db.session
    data_form = request.form

    password_to_hash = data_form["password"]

    new_user = UserModel(name=data_form["name"], 
                        last_name=data_form["last_name"],
                        password=data_form["password"],
                        email=data_form["email"]) 

    new_user.password = password_to_hash
    end_session(session, new_user)
    return jsonify(new_user.serialized), HTTPStatus.OK




@bp_api.get("/")
@jwt_required()
def signup_get():
    user_email = get_jwt_identity()
    data: UserModel = UserModel.query.filter_by(email=user_email).first()
    data_serialized = data.serialized
    
    return jsonify(data_serialized), HTTPStatus.OK




@bp_api.put("/")
@jwt_required()
def signup_update():
    session = current_app.db.session
    data = request.get_json()

    user_email = get_jwt_identity()
    data_to_update: UserModel = UserModel.query.filter_by(email=user_email).first()

    for key, value in data.items():
        setattr(data_to_update, key, value)

    end_session(session, data_to_update)

    return jsonify(data_to_update.serialized), HTTPStatus.OK




@bp_api.delete("/")
@jwt_required()
def signup_delete():
    session = current_app.db.session

    user_email = get_jwt_identity()
    data_to_delete: UserModel = UserModel.query.filter_by(email=user_email).first()

    session.delete(data_to_delete)
    session.commit()

    return "", HTTPStatus.NO_CONTENT
