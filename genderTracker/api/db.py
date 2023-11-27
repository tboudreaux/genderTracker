from genderTracker.models.models import User, Gender, Day
from genderTracker.utils.auth import auth_requested
from genderTracker.setup import db, app
from flask import request, jsonify


import re

DELIMPATTERN = r"[;,/|\s]+"
GUEST_UUID ="00000000-0000-0000-0000-000000000000"


@app.route('/api/gender/register', methods=['POST'])
@auth_requested
def gender_post(current_user):
    payload = request.get_json()
    genderName = payload['gender']
    pronouns = re.split(DELIMPATTERN, payload['pronouns'])
    if not Gender.query.filter_by(name=genderName).count() > 0:
        g = Gender(genderName, pronouns, payload['description'])
        db.session.add(g)
        db.session.commit()
    else:
        g = Gender.query.filter_by(name=genderName).first()

    if current_user != None:
        newDay = Day(current_user.uuid, g.uuid)
    else:
        newDay = Day(GUEST_UUID, g.uuid)
    db.session.add(newDay)

    db.session.commit()
    return jsonify({'success': True}), 201

@app.route('/api/gender/list', methods=['GET'])
def get_all_genders():
    genders = Gender.query.all()
    names = list()
    for gender in genders:
        names.append(gender.name)

    return jsonify(names), 200

    
