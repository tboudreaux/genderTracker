from genderTracker.setup import app, db
from genderTracker.models.models import User
from genderTracker.utils.auth import token_required

from flask import jsonify, request, make_response
from sqlalchemy import func
import jwt
import datetime as dt
import secrets

@app.route('/login', methods=['POST'])
def login():
    token_valid_time = 30 # minutes
    payload = request.get_json()
    username = payload.get('username', None)
    email = payload.get('email', None)

    if username:
        username = username.lower()
    if email:
        email = email.lower()

    if not username and not email:
        return make_response('Could not verify', 401)

    ID = username if username else email
    if not payload or not ID or not payload['password']:
        return make_response('Could not verify', 401)
    if username:
        userQuery = User.query.filter(func.lower(User.username)==ID)
        if userQuery.count() == 0:
            return make_response('Could not verify', 401)
        user = userQuery.first()
    else:
        user = User.query.filter_by(email=ID).first()
    if user.check_password(payload['password']):
        token = jwt.encode({'public_id': user.username, 'exp': dt.datetime.utcnow() + dt.timedelta(minutes=token_valid_time)}, app.config['SECRET_KEY'])
        return jsonify({'token': token, 'expires': dt.datetime.utcnow() + dt.timedelta(minutes=token_valid_time), 'vtime': token_valid_time, 'public_id': user.username})
    return make_response('Could not verify', 401)

@app.route('/login/test')
@token_required
def login_test(current_user):
    return jsonify({'message': 'Login successful', 'username': current_user.username, 'email': current_user.email, 'admin': current_user.admin, 'enabled': current_user.enabled, 'auth': True});

@app.route('/login/revoke/all', methods=['POST'])
def revoke_all_tokens():
    payload = request.get_json()
    username = payload.get('username', None)
    email = payload.get('email', None)

    if not username and not email:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    ID = username if username else email
    if not payload or not ID or not payload['password']:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    if username:
        user = User.query.filter_by(username=ID).first()
    else:
        user = User.query.filter_by(email=ID).first()
    if user.check_password(payload['password']):
        app.config['SECRET_KEY'] = secrets.token_hex(16)
        db.session.commit()
        return jsonify({'message': 'All tokens revoked'})
    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
