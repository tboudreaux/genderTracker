from genderTracker.models.models import User, Gender, Day
from genderTracker.utils.auth import auth_requested
from genderTracker.setup import db, app
from flask import request, jsonify


import re

DELIMPATTERN = r"[;,/|\s]+"
GUEST_UUID ="00000000-0000-0000-0000-000000000000"

def register_new_gender(name, pronouns, description):
    sameGender = Gender.query.filter_by(name=name, pronouns=pronouns).count()
    if not sameGender > 0:
        print("enrolling new gender " + name + " with pronouns " + str(pronouns))
        g = Gender(name, pronouns, description)
        db.session.add(g)
        db.session.commit()
        return True
    print("enrollment failed")
    return False



@app.route('/api/gender/register', methods=['POST'])
@auth_requested
def gender_post(current_user):
    payload = request.get_json()
    genderName = payload['gender']
    pronouns = re.split(DELIMPATTERN, payload['pronouns'])
    register_new_gender(genderName, pronouns, payload['description'])
    return jsonify({'success': True}), 201

@app.route('/api/gender/day', methods=['POST'])
@auth_requested
def day_post(current_user):
    payload = request.get_json()
    print(payload)
    genderName = payload['gender']
    pronouns = re.split(DELIMPATTERN, payload['pronouns'])
    register_new_gender(genderName, pronouns, payload['genderDescription'])
    g = Gender.query.filter_by(name=genderName).first()

    if current_user != None:
        newDay = Day(current_user.uuid, g.uuid, description=payload['dayDescription'])
    else:
        newDay = Day(GUEST_UUID, g.uuid, description=payload['dayDescription'])
    db.session.add(newDay)

    db.session.commit()
    return jsonify({'success': True}), 201

@app.route('/api/gender/list', methods=['GET'])
def get_all_genders():
    genders = Gender.query.all()
    names = list()
    for gender in genders:
        names.append((gender.name, gender.pronouns, gender.description))

    return jsonify(names), 200

def get_user_records(uuid):
    # Query the User table to get the UUID of the user with the given username
    user = User.query.filter_by(uuid=uuid).first()
    if not user:
        return "User not found", 404

    # Query to join User, Day, and Gender tables
    records = db.session.query(Day, Gender).join(User).join(Gender).filter(User.uuid == user.uuid).all()

    # Construct the JSON object
    result = []
    for day, gender in records:
        entry = {
            "gender": gender.name,
            "pronouns": gender.pronouns,
            "datetime": day.datetime.strftime("%Y-%m-%d %H:%M"),
            "description": day.description
        }
        result.append(entry)

    return result

def get_gender_dist(uuid):
    # Query the User table to get the UUID of the user with the given username
    user = User.query.filter_by(uuid=uuid).first()
    if not user:
        return "User not found", 404

    # Query to count each gender's occurrence for the user
    gender_counts = db.session.query(Gender.name, db.func.count(Gender.name))\
                              .join(Day)\
                              .filter(Day.user_uuid == user.uuid)\
                              .group_by(Gender.name)\
                              .all()

    # Construct the result as a dictionary
    result = {gender: count for gender, count in gender_counts}
    return result


@app.route('/api/gender/history', methods=['GET'])
@auth_requested
def get_gender_history(current_user):
    if current_user != None:
        return jsonify(get_user_records(current_user.uuid)), 200
    else:
        return jsonify(get_user_records(GUEST_UUID)), 200

@app.route('/api/gender/pie', methods=['GET'])
@auth_requested
def get_gender_distribution(current_user):
    if current_user != None:
        records = get_gender_dist(current_user.uuid)
    else:
        records = get_gender_dist(GUEST_UUID)
    return jsonify(records), 200
