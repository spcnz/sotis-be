from flask import Blueprint, request, jsonify, Response
from testingapp import db
from testingapp.models.testmodels import Test, Subject
from testingapp.utils.authutils import get_identity_if_logged_in

test_bp = Blueprint('test', __name__)

@test_bp.route('/test', methods=['GET'])
def get_all():
    return jsonify([test.to_dict() for test in Test.query.all()])

@test_bp.route('/test', methods=['POST'])
def create_test():
    try:
        user = get_identity_if_logged_in()
        print(user)

        return
        data = request.json
        title = data.get('title', 'NO TITLE')
        time_dependency = bool(data.get('time_dependency', False))
        subject_id = data.get('subject_id')
        new_test = Test(title=title, time_dependency=time_dependency, subject_id=subject_id)
        db.session.add(new_test)
        db.session.commit()

        return jsonify(new_test.to_dict())
    except Exception as error:
        print(error)
        return Response(status=400)
