from flask import Blueprint, request, jsonify, Response
from testingapp import db
from testingapp.models.testmodels import Test, Subject
from testingapp.models.usermodels import User
from testingapp.utils.authutils import get_user_if_logged_in
from flask_jwt_extended import jwt_required, get_jwt_identity

test_bp = Blueprint('test', __name__)


@test_bp.route('/test', methods=['GET'])
@jwt_required
def get_all():
    subject_id = request.args.get('subject_id')
    
    return jsonify([test.to_dict() for test in Test.query.filter_by(subject_id=subject_id)])


@test_bp.route('/test', methods=['POST'])
def create_test():
    try:
        user = get_user_if_logged_in()
        if not user or user.role != 'teacher':
            return Response(status=400)

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


@test_bp.route('/test/<id>', methods=['GET'])
@jwt_required
def get_by_id(id):
    test = Test.query.get(id)
    if not test:
        return Response(status=400)

    
    return jsonify(test.to_dict(only=('parts.title','parts.id', 'title','time_dependency', 'time_limit_seconds', 'id', 'parts.submission', 'parts.navigation')))
